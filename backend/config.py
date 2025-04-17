from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# ----------------------------------------------------------------------------
# Flask application and extension initialisation
# ----------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

# NOTE: In production, the secret key *must* be provided via environment
# variables or a secure configuration service. It is hard‑coded here only to
# keep the demo self‑contained and to simplify automated testing.
app.config["SECRET_KEY"] = "change-me-in-production"  # Used by Flask

# SQLAlchemy configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///appdatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # <-- Fixed typo

# JWT configuration – again, this should be set from env variables in real
# deployments.
app.config["JWT_SECRET_KEY"] = "another-change-me-secret"  # Used by JWTs

# Create extensions instances
db = SQLAlchemy(app)
jwt = JWTManager(app)

# In‑memory token block‑list. For real applications, a persistent store should
# be used instead (e.g. Redis).
token_blocklist: set[str] = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload) -> bool:  # pragma: no cover
    """Callback used by flask-jwt-extended to check if a JWT has been revoked.

    The implementation below keeps the identifiers of revoked JWTs in an
    in‑memory *set*. This is more than enough for automated tests and local
    development, but **must** be replaced by a shared datastore (e.g. Redis)
    when the application is scaled to multiple instances.
    """
    jti: str = jwt_payload["jti"]
    return jti in token_blocklist

# Register blueprints after app is created and configured
from main import bp as main_bp
app.register_blueprint(main_bp)