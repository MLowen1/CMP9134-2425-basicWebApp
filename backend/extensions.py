"""
Central place to create the shared Flask extensions.

Import the objects (db, jwt, …) **only** from this file so circular‑import
headaches disappear.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate # Import Migrate
import sqlalchemy as sa
# Import OpenverseClient
from .openverse_client import OpenverseClient

# Create extension instances
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
migrate = Migrate() # Instantiate Migrate
# Initialize Openverse client here
ov_client = OpenverseClient()

# Function to reset SQLAlchemy engine cache for tests
def reset_extensions():
    """Reset extension state between tests to avoid stale contexts."""
    if hasattr(db, '_app_engines'):
        db._app_engines = {}
    if hasattr(db, '_app_sessions'):
        db._app_sessions = {}

# Function to safely create tables - ignoring errors if they already exist
def safe_create_all():
    """Create all tables, ignoring errors about existing tables/indices."""
    from flask import current_app
    import sqlite3
    
    # Import models to ensure they're registered with SQLAlchemy
    from backend.models import User, Contact, TokenBlocklist
    
    # Using lower-level SQLAlchemy APIs to create tables
    with db.engine.connect() as conn:
        tables = db.metadata.sorted_tables
        for table in tables:
            try:
                table.create(bind=conn, checkfirst=True)
                print(f"Created table {table.name}")
            except sa.exc.OperationalError as e:
                if "already exists" in str(e):
                    print(f"Table {table.name} already exists")
                else:
                    print(f"Error creating table {table.name}: {e}")
