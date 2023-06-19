import streamlit as st
from neo4j_controller import Neo4jController
import pandas as pd
import base64




st.sidebar.title("Metalinks")

n4j = Neo4jController(
    st.secrets["neo4j_uri"],
    st.secrets["neo4j_user"],
    st.secrets["neo4j_password"],
)


st.sidebar.write("Select your parameters for contextualization")
cellular_locations = st.sidebar.text_input("Enter cellular locations (separated by commas)", "Extracellular, Intracellular")
tissue_locations = st.sidebar.text_input("Enter tissue locations (separated by commas)", "Kidney, All Tissues")
biospecimen_locations = st.sidebar.text_input("Enter biospecimen locations (separated by commas)", "Urine, Blood")
database_range = st.sidebar.slider("Select a range for 'a.database'", min_value=0, max_value=1000, value=(500, 1000))
experiment_range = st.sidebar.slider("Select a range for 'a.experiment'", min_value=0, max_value=1000, value=(500, 1000))

if st.sidebar.button("Get Subgraph"):
    cellular_locations_list = [loc.strip() for loc in cellular_locations.split(",")]
    tissue_locations_list = [loc.strip() for loc in tissue_locations.split(",")]
    biospecimen_locations_list = [loc.strip() for loc in biospecimen_locations.split(",")]

    subgraph = n4j.get_subgraph(
        cellular_locations_list,
        tissue_locations_list,
        biospecimen_locations_list,
        database_range,
        experiment_range
    )

    # Prepare the data for the dataframe
    data = []
    for record in subgraph:
        data.append({
            'HMDB': record['HMDB'],
            'MetName': record['MetName'],
            'Protein': record['Symbol'],
            'CellLoc': record['CellLoc'],
            'TissueLoc': record['TissueLoc'],
            'BiospecLoc': record['BiospecLoc'],
            'Mode': record['Mode'],
            'Direction': record['Direction'],
            'Status': record['Status'],
            'Uniprot': record['Uniprot'],
            'ProtName': record['ProtName'],
            'Protein': record['Symbol'],  # Include the protein symbol
        })

    # Create the dataframe
    df = pd.DataFrame(data)

    # Download button
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to base64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="metalinks_data.csv">Download CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

    st.dataframe(df)





