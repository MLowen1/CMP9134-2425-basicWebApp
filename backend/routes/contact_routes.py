from flask import Blueprint, jsonify, request
from backend.extensions import db
from backend.models import Contact

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('', methods=['GET'])
def get_contacts():
    """Get all contacts."""
    contacts = Contact.query.all()
    return jsonify([contact.to_json() for contact in contacts])

@contacts_bp.route('', methods=['POST'])
def create_contact():
    """Create a new contact."""
    try:
        data = request.get_json()
        
        # Print for debugging
        print(f"Received contact data: {data}")
        
        # Validate presence of required fields
        required_fields = ["firstName", "lastName", "email"]
        if not all(k in data for k in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        # Validate that required fields are not empty strings
        if not data.get('firstName') or not data.get('lastName') or not data.get('email'):
             return jsonify({"message": "First name, last name, and email cannot be empty"}), 400
        
        # Create new contact
        new_contact = Contact(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email']
        )
        
        # Add optional fields if present
        if 'phone' in data:
            new_contact.phone = data['phone']
        
        # Save to database
        db.session.add(new_contact)
        db.session.commit()
        
        # Return the created contact
        return jsonify(new_contact.to_json()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating contact: {str(e)}")
        return jsonify({"message": f"Error creating contact: {str(e)}"}), 500

@contacts_bp.route('/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Get a specific contact by ID."""
    contact = db.session.get(Contact, contact_id)
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    return jsonify(contact.to_json())

@contacts_bp.route('/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update an existing contact."""
    try:
        contact = db.session.get(Contact, contact_id)
        if not contact:
            return jsonify({"message": "Contact not found"}), 404
        data = request.get_json()
        
        # Validate non-empty values if fields are provided
        if 'firstName' in data and not data['firstName']:
            return jsonify({"message": "First name cannot be empty"}), 400
        if 'lastName' in data and not data['lastName']:
            return jsonify({"message": "Last name cannot be empty"}), 400
        if 'email' in data and not data['email']:
            return jsonify({"message": "Email cannot be empty"}), 400

        # Update fields if present and valid
        if 'firstName' in data:
            contact.first_name = data['firstName']
        if 'lastName' in data:
            contact.last_name = data['lastName']
        if 'email' in data:
            contact.email = data['email']
        if 'phone' in data:
            contact.phone = data['phone'] # Allow empty phone
        
        # Save to database
        db.session.commit()
        return jsonify(contact.to_json())
    except Exception as e:
        db.session.rollback()
        print(f"Error updating contact: {str(e)}")
        return jsonify({"message": f"Error updating contact: {str(e)}"}), 500

@contacts_bp.route('/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete a contact."""
    try:
        contact = db.session.get(Contact, contact_id)
        if not contact:
            return jsonify({"message": "Contact not found"}), 404
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting contact: {str(e)}")
        return jsonify({"message": f"Error deleting contact: {str(e)}"}), 500
