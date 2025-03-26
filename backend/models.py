from config import db


class Contact(db.Model):
    # Attributes of the Contact class
    # These attributes represent the data that each Contact object will hold.
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each contact
    first_name = db.Column(db.String(80), unique=False, nullable=False)  # First name of the contact
    last_name = db.Column(db.String(80), unique=False, nullable=False)  # Last name of the contact
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email address of the contact (must be unique)

    # Explanation of OOP usage:
    # The Contact class is a blueprint for creating "contact" objects.
    # It inherits from db.Model, which is a class provided by Flask-SQLAlchemy.
    # This inheritance allows the Contact class to interact with the database,
    # enabling operations like creating, reading, updating, and deleting records.
    # This demonstrates the OOP principle of inheritance.

    def to_json(self):
        # Purpose of the to_json method:
        # This method converts a Contact object into a JSON-compatible dictionary.
        # JSON (JavaScript Object Notation) is commonly used for data exchange in web applications.
        # By defining this method, we can easily serialize Contact objects into JSON format
        # for use in APIs or other web-based interactions.
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }