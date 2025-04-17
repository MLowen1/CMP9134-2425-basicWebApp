from backend.config import db  # Updated import to point to the correct db


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


# ----------------------------------------------------------------------------
# Authentication / User model
# ----------------------------------------------------------------------------

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Basic user model used for JWT authentication.

    NOTE:
    -----
    The model purposefully keeps the feature‑set minimal – only what is
    required for the current iteration (username & password authentication).
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String(255), nullable=False)

    # ---------------------------------------------------------------------
    # Helper / convenience methods
    # ---------------------------------------------------------------------

    def set_password(self, plaintext: str) -> None:
        """Hash *plaintext* using PBKDF2 and store the result."""

        self._password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext: str) -> bool:
        """Return *True* if *plaintext* matches the stored hash."""

        return check_password_hash(self._password_hash, plaintext)

    # ------------------------------------------------------------------
    # Serialisation helpers – *never* include password hash in responses
    # ------------------------------------------------------------------

    def to_json(self):
        return {"id": self.id, "username": self.username}
