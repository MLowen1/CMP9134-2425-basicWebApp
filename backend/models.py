from datetime import datetime, timezone
# Ensure db is imported from extensions, not main
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# --- Contact Model ---
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True) # Added phone field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Link to User

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }
    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name}>"

# --- User Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True) # Added email field

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
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TokenBlocklist {self.jti}>"