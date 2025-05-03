# File: backend/models.py
# -----------------------------------
# Models should ONLY define data structures and should not import routes or blueprints
# This file defines the database models for the application using SQLAlchemy.
# Each class represents a table in the database.
# -----------------------------------

# Import necessary modules
from datetime import datetime # Used for timestamping
from werkzeug.security import generate_password_hash, check_password_hash # Used for password hashing and verification
from passlib.hash import bcrypt # Used for password hashing and verification
from .extensions import db # Import the SQLAlchemy database instance from extensions.py

# Remove any import of routes/blueprints that might be here
# DO NOT import contacts_bp here - this creates circular imports
# The commented lines below are examples of imports that should NOT be in models.py
# from .routes.contact_routes import contacts_bp # Example of a problematic import

# Define Contact model
# This class represents the 'contacts' table in the database.
class Contact(db.Model):
    # Define the primary key column
    id = db.Column(db.Integer, primary_key=True)
    # Define a string column for the contact's name, cannot be null
    name = db.Column(db.String(100), nullable=False)
    # Define a string column for the contact's email, must be unique and cannot be null
    email = db.Column(db.String(120), nullable=False)
    # Define a text column for the contact's message, cannot be null
    message = db.Column(db.Text, nullable=False)
    # Define a datetime column for the creation timestamp, defaults to the current UTC time
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # String representation of the Contact object, useful for debugging
    def __repr__(self):
        return f'<Contact {self.name}>'

    # Method to convert the Contact object to a dictionary, useful for JSON responses
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            # Format the created_at timestamp to ISO format if it exists
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Define User model
# This class represents the 'users' table in the database.
class User(db.Model):
    __tablename__ = 'user'  # Explicitly set the table name to 'user'
    
    # Define the primary key column
    id = db.Column(db.Integer, primary_key=True)
    # Define a string column for the username, must be unique and cannot be null
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Define a string column to store the hashed password, cannot be null
    password_hash = db.Column(db.String(128), nullable=False)
    # Make email required (not nullable) for authentication
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Add created_at timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to hash the provided password and store it in password_hash
    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    # Method to check if the provided password matches the stored hash
    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    # String representation of the User object
    def __repr__(self):
        return f'<User {self.username}>'
    
    # Method to convert the User object to a dictionary for JSON responses
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Define TokenBlocklist model
# This class represents the 'token_blocklist' table, used to store revoked JWTs.
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'  # Explicitly set the table name
    
    # Define the primary key column
    id = db.Column(db.Integer, primary_key=True)
    # Define a string column for the JWT ID (jti), must be unique and cannot be null, indexed for faster lookups
    jti = db.Column(db.String(36), nullable=False, index=True)
    # Define a datetime column for when the token was blocklisted, cannot be null
    created_at = db.Column(db.DateTime, nullable=False)

    # String representation of the TokenBlocklist object
    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'