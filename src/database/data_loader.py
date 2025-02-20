import sys
import os
# Add this at the top of the file to fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.neo4j_connector import Neo4jConnection

def load_initial_data():
    conn = Neo4jConnection()
    conn.connect()
    
    # Clear existing data
    conn.query("MATCH (n) DETACH DELETE n")
    
    # Create visa types
    visa_types = [
        {
            "name": "Skilled Worker Visa",
            "minimum_salary": 26200,
            "duration": "5 years",
            "processing_time": "3 weeks",
            "cost": 1235
        },
        {
            "name": "Global Talent Visa",
            "minimum_salary": None,  # No minimum salary requirement
            "duration": "5 years",
            "processing_time": "8 weeks",
            "cost": 608
        },
        {
            "name": "Start-up Visa",
            "minimum_salary": None,
            "duration": "2 years",
            "processing_time": "3 weeks",
            "cost": 363
        },
        {
            "name": "Innovator Visa",
            "minimum_salary": None,
            "duration": "3 years",
            "processing_time": "3 weeks",
            "cost": 1036
        },
        {
            "name": "Health and Care Worker Visa",
            "minimum_salary": 20960,
            "duration": "5 years",
            "processing_time": "3 weeks",
            "cost": 247
        }
    ]
    
    for visa in visa_types:
        query = """
        CREATE (v:VisaType {
            name: $name,
            minimum_salary: $minimum_salary,
            duration: $duration,
            processing_time: $processing_time,
            cost: $cost
        })
        """
        conn.query(query, visa)
    
    print("Successfully loaded visa types into the database!")
    conn.close()

if __name__ == "__main__":
    load_initial_data() 