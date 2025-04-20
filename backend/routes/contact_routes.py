from flask import Blueprint, jsonify, request
# Use relative import
from ..extensions import db 
# Use relative import
from ..models import Contact
# Import jwt_required and get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_identity

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('', methods=['GET'])
@jwt_required() # Add JWT requirement
def get_contacts():
    """Get contacts for the current user."""
    current_user_id = get_jwt_identity()
    # Filter contacts by user_id
    contacts = Contact.query.filter_by(user_id=current_user_id).all()
    return jsonify([contact.to_json() for contact in contacts])

@contacts_bp.route('', methods=['POST'])
@jwt_required() # Add JWT requirement
def create_contact():
    """Create a new contact for the current user."""
    current_user_id = get_jwt_identity()
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
        
        # Create new contact and associate with user
        new_contact = Contact(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email'],
            user_id=current_user_id # Assign the user ID
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
@jwt_required() # Add JWT requirement
def get_contact(contact_id):
    """Get a specific contact by ID."""
    current_user_id = get_jwt_identity()
    contact = db.session.get(Contact, contact_id)
    if not contact or contact.user_id != current_user_id:
        return jsonify({"message": "Contact not found"}), 404
    return jsonify(contact.to_json())

@contacts_bp.route('/<int:contact_id>', methods=['PUT'])
@jwt_required() # Add JWT requirement
def update_contact(contact_id):
    """Update an existing contact."""
    current_user_id = get_jwt_identity()
    try:
        contact = db.session.get(Contact, contact_id)
        if not contact or contact.user_id != current_user_id:
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

# Correct the methods definition
@contacts_bp.route('/<int:contact_id>', methods=['DELETE'])
@jwt_required() # Add JWT requirement
def delete_contact(contact_id):
    """Delete a contact."""
    current_user_id = get_jwt_identity()
    try:
        contact = db.session.get(Contact, contact_id)
        if not contact or contact.user_id != current_user_id:
            return jsonify({"message": "Contact not found"}), 404
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting contact: {str(e)}")
        return jsonify({"message": f"Error deleting contact: {str(e)}"}), 500
