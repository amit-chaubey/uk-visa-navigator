from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

class Neo4jConnector:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.driver = None

    def __enter__(self):
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.close() 