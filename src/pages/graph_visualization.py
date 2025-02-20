import streamlit as st
from src.utils.graph_visualizer import VisaGraphVisualizer
import streamlit.components.v1 as components
from src.utils.neo4j_connector import Neo4jConnector

def render_graph_page():
    st.title("UK Visa Requirements Graph Visualization")
    
    # Initialize Neo4j connection and visualizer
    neo4j_connector = Neo4jConnector()
    visualizer = VisaGraphVisualizer(neo4j_connector)
    
    # Visualization options
    viz_type = st.radio(
        "Select Visualization Type",
        ["Interactive", "Static", "Export JSON"]
    )
    
    if viz_type == "Interactive":
        st.subheader("Interactive Graph Visualization")
        html_string = visualizer.generate_interactive_html()
        components.html(html_string, height=800)
        
    elif viz_type == "Static":
        st.subheader("Static Graph Visualization")
        buf = visualizer.generate_static_plot()
        st.image(buf)
        
    else:  # Export JSON
        st.subheader("Graph Data (JSON)")
        json_data = visualizer.export_graph_json()
        st.download_button(
            label="Download Graph Data",
            data=json_data,
            file_name="visa_graph.json",
            mime="application/json"
        )
        st.json(json_data)

if __name__ == "__main__":
    render_graph_page()