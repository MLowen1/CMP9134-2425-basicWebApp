from datetime import datetime, timezone
from backend.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# --- Contact Model ---
class Contact(db.Model):
    __tablename__ = 'contact'  # Explicitly set table name
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Allow table redefinition during testing
    __table_args__ = {'extend_existing': True}

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone or ""  # Return empty string if phone is None
        }
    
    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name}>"

# --- User Model ---
class User(db.Model):
    __tablename__ = 'user'  # Explicitly set table name
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    
    # Allow table redefinition during testing
    __table_args__ = {'extend_existing': True}
    
    def set_password(self, plaintext: str) -> None:
        self.password_hash = generate_password_hash(plaintext, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, plaintext: str) -> bool:
        return check_password_hash(self.password_hash, plaintext)

    def to_json(self):
        return {"id": self.id, "username": self.username}

    def __repr__(self):
        return f"<User {self.username}>"

# --- Token Blocklist Model ---
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'  # Explicitly set table name
    
    id = db.Column(db.Integer, primary_key=True)
    # Remove the index=True parameter to prevent the automatic index creation
    # SQLAlchemy will still enforce uniqueness at the database level
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    # Allow table redefinition during testing
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f"<TokenBlocklist {self.jti}>"