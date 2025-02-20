from src.database.neo4j_connector import Neo4jConnection

def test_connection():
    conn = Neo4jConnection()
    try:
        conn.connect()
        print("Connection successful!")
        
        # Try a simple query
        result = conn.query("RETURN 1 as test")
        print("Query result:", result)
        
    except Exception as e:
        print(f"Connection failed: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_connection() 