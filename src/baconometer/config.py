import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "neo4jtest123"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
