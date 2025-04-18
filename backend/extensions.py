"""
Central place to create the shared Flask extensions.

Import the objects (db, jwt, …) **only** from this file so circular‑import
headaches disappear.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db  = SQLAlchemy()
jwt = JWTManager()
