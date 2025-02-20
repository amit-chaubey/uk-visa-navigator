import streamlit as st
import sys
import os
# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.neo4j_connector import Neo4jConnection
import pandas as pd

def main():
    st.title("UK Visa Navigator")
    st.write("Explore different UK visa types and their requirements")
    
    # Initialize Neo4j connection
    conn = Neo4jConnection()
    conn.connect()
    
    # Create sidebar for filtering
    st.sidebar.title("Filter Options")
    min_salary = st.sidebar.slider("Minimum Salary (£)", 0, 100000, 26200)
    
    # Query visa types
    query = """
    MATCH (v:VisaType)
    WHERE v.minimum_salary IS NULL OR v.minimum_salary <= $min_salary
    RETURN v.name as Visa_Type,
           v.minimum_salary as Minimum_Salary,
           v.duration as Duration,
           v.processing_time as Processing_Time,
           v.cost as Cost
    """
    
    results = conn.query(query, {"min_salary": min_salary})
    
    if results:
        # Convert results to DataFrame
        df = pd.DataFrame([dict(record) for record in results])
        st.dataframe(df)
    else:
        st.write("No visa types found matching your criteria.")
    
    conn.close()

if __name__ == "__main__":
    main() 