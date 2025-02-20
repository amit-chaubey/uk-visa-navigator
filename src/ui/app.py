import streamlit as st
import pandas as pd
from src.utils.neo4j_connector import Neo4jConnector
from src.pages.graph_visualization import render_graph_page

def render_home_page():
    st.title("UK Visa Navigator")
    st.write("Explore different UK visa types and their requirements")
    
    # Initialize Neo4j connection using context manager
    with Neo4jConnector() as conn:
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
        
        try:
            results = conn.driver.session().run(query, min_salary=min_salary)
            records = list(results)
            
            if records:
                # Convert results to DataFrame
                df = pd.DataFrame([dict(record) for record in records])
                st.dataframe(df)
            else:
                st.write("No visa types found matching your criteria.")
                
        except Exception as e:
            st.error(f"Error querying database: {str(e)}")

def main():
    # Add navigation to sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page",
        ["Home", "Graph Visualization"]
    )
    
    # Page routing
    if page == "Home":
        render_home_page()
    elif page == "Graph Visualization":
        render_graph_page()

if __name__ == "__main__":
    main()