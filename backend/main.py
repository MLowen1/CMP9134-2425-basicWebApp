from flask import request, jsonify
from config import app, db
from models import Contact


@app.route("/contacts", methods=["GET"])
def get_contacts():
    # HTTP Method: GET
    # Purpose: Retrieve all contacts from the database.
    # Interaction with Contact model:
    # - Uses Contact.query.all() to fetch all records from the database.
    # - Converts each Contact object to JSON using the to_json() method.
    # Data flow:
    # - No data is received from the client.
    # - Sends a JSON response containing a list of all contacts.
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    # HTTP Method: POST
    # Purpose: Create a new contact in the database.
    # Interaction with Contact model:
    # - Creates a new Contact object using the data received from the client.
    # - Adds the new Contact object to the database using db.session.add() and commits the transaction.
    # Data flow:
    # - Receives data from the client via request.json (firstName, lastName, email).
    # - Sends a JSON response indicating success or failure.
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include the first name, last name and email"}),
            400,
        )

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    # HTTP Method: PATCH
    # Purpose: Update an existing contact in the database.
    # Interaction with Contact model:
    # - Fetches the Contact object by ID using Contact.query.get().
    # - Updates the attributes of the Contact object with data received from the client.
    # - Commits the changes to the database using db.session.commit().
    # Data flow:
    # - Receives data from the client via request.json (firstName, lastName, email).
    # - Sends a JSON response indicating success or failure.
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated"}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # HTTP Method: DELETE
    # Purpose: Delete an existing contact from the database.
    # Interaction with Contact model:
    # - Fetches the Contact object by ID using Contact.query.get().
    # - Deletes the Contact object from the database using db.session.delete() and commits the transaction.
    # Data flow:
    # - No data is received from the client (only the user_id in the URL).
    # - Sends a JSON response indicating success or failure.
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__":
    # Initializes the database tables if they don't already exist.
    with app.app_context():
        db.create_all()

    # Starts the Flask application in debug mode.
    app.run(debug=True)