import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
