from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        print(f"Initializing connection to: {self.uri} with user: {self.user}")  # Debug line

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test the connection
            self.driver.verify_connectivity()
            print("Successfully connected to Neo4j database!")  # Debug line
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")  # Debug line
            raise e

    def close(self):
        if self.driver:
            self.driver.close()
            print("Connection closed")  # Debug line

    def query(self, query, parameters=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session()
            response = list(session.run(query, parameters))
            print(f"Query executed successfully: {query[:50]}...")  # Debug line
        except Exception as e:
            print(f"Query failed: {str(e)}")
            print(f"Query was: {query}")
            print(f"Parameters were: {parameters}")
        finally:
            if session:
                session.close()
        return response 