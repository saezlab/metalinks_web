import streamlit as st
from neo4j_controller import Neo4jController
import pandas as pd
import base64
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('..')
from aux import create_graph

st.set_page_config(page_title='Metalinks Web App', layout='wide')

logo_image = Image.open("data/metalinks_logo.png")

import io

logo_bytes = io.BytesIO()
logo_image.save(logo_bytes, format="PNG")
logo_base64 = base64.b64encode(logo_bytes.getvalue()).decode()

# Set the favicon
favicon_html = f"""
    <link rel="icon" href="data:image/png;base64,{logo_base64}">
    """

# Render the favicon HTML
st.markdown(favicon_html, unsafe_allow_html=True)

st.sidebar.image(logo_image, use_column_width=True)

selected_purpose = st.sidebar.select_slider("Select purpose", ["Contextualize", "Investigate"])

n4j = Neo4jController(
    st.secrets["neo4j_uri"],
    st.secrets["neo4j_user"],
    st.secrets["neo4j_password"],
)

if selected_purpose == "Contextualize":


    st.sidebar.write("Select your parameters for contextualization")
    cellular_locations = st.sidebar.text_input("Enter cellular locations (separated by commas)", "Extracellular, Cytoplasm")
    tissue_locations = st.sidebar.text_input("Enter tissue locations (separated by commas)", "Kidney, All Tissues")
    biospecimen_locations = st.sidebar.text_input("Enter biospecimen locations (separated by commas)", "Urine, Blood")
    database_range = st.sidebar.slider("Select a range STITCH database score", min_value=0, max_value=1000, value=(150, 1000))
    experiment_range = st.sidebar.slider("Select a range STITCH experimental score", min_value=0, max_value=1000, value=(150, 1000))

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

        st.dataframe(df)
        
        # Download button
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to base64 encoding
        href = f'<a href="data:file/csv;base64,{b64}" download="metalinks_data.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)


        # Summary box
        num_rows = len(df.index)
        num_unique_metabolites = df['HMDB'].nunique()
        num_unique_proteins = df['Protein'].nunique()

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        # Define custom color palette
        colors = ["#932a61", "#512D55"]

        # Summary table
        with col1:
            summary_data = {
                'Metrics': ['Number of Interactions', 'Number of Unique Metabolite Ligands', 'Number of Unique Protein Receptors'],
                'Values': [num_rows, num_unique_metabolites, num_unique_proteins]
            }
            summary_df = pd.DataFrame(summary_data)

            style = summary_df.style.hide_index()
            style.hide_columns()
            st.write(style.to_html(), unsafe_allow_html=True)
            #st.table(summary_df)


        # Bar chart - CellLoc
        with col2:
            cellloc_counts = df['CellLoc'].explode().value_counts()
            cellloc_percentages = cellloc_counts / len(df) * 100

            fig_cellloc, ax_cellloc = plt.subplots(figsize=(6, 4), facecolor='white')
            sns.barplot(x=cellloc_percentages.index, y=cellloc_percentages.values, ax=ax_cellloc, palette=colors)
            ax_cellloc.set_ylabel("Percentage")
            #ax_cellloc.set_title("Cellular Location Distribution")
            ax_cellloc.set_xticklabels(ax_cellloc.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_cellloc)

        # Bar chart - TissueLoc
        with col3:
            tissueloc_counts = df['TissueLoc'].explode().value_counts()
            tissueloc_percentages = tissueloc_counts / len(df) * 100

            fig_tissueloc, ax_tissueloc = plt.subplots(figsize=(6, 4), facecolor='white')
            sns.barplot(x=tissueloc_percentages.index, y=tissueloc_percentages.values, ax=ax_tissueloc, palette=colors)
            ax_tissueloc.set_ylabel("Percentage")
            #ax_tissueloc.set_title("Tissue Location Distribution")
            ax_tissueloc.set_xticklabels(ax_tissueloc.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_tissueloc)

        # Bar chart - BiospecLoc
        with col4:
            biospecloc_counts = df['BiospecLoc'].explode().value_counts()
            biospecloc_percentages = biospecloc_counts / len(df) * 100

            fig_biospecloc, ax_biospecloc = plt.subplots(figsize=(6, 4), facecolor='white')
            sns.barplot(x=biospecloc_percentages.index, y=biospecloc_percentages.values, ax=ax_biospecloc, palette=colors)
            ax_biospecloc.set_ylabel("Percentage")
            #ax_biospecloc.set_title("Biospecimen Location Distribution")
            ax_biospecloc.set_xticklabels(ax_biospecloc.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_biospecloc)

elif selected_purpose == "Investigate":

    st.sidebar.write("Select proteins or metabolites to investigate")


    # add switch for metabolites or proteins
    selected_entity = st.sidebar.select_slider('Select entity', ['Metabolites', 'Proteins'])

    if selected_entity == 'Metabolites':

        # put two text input for metabolites and proteins
        metabolite_string = st.sidebar.text_input("Enter metabolite IDs (separated by commas)", "HMDB0000220, HMDB0000895")
        cellular_locations = st.sidebar.text_input("Enter cellular locations (separated by commas)", "Extracellular")
        tissue_locations = st.sidebar.text_input("Enter tissue locations (separated by commas)", "Kidney, All Tissues")
        biospecimen_locations = st.sidebar.text_input("Enter biospecimen locations (separated by commas)", "Urine, Blood")
        database_range = st.sidebar.slider("Select a range for STITCH database score", min_value=0, max_value=1000, value=(150, 1000))
        experiment_range = st.sidebar.slider("Select a range for STITCH experimetal score", min_value=0, max_value=1000, value=(150, 1000))

        if st.sidebar.button("Get Subgraph"):

            metabolite_ids = [met.strip() for met in metabolite_string.split(",")]
            cellular_locations_list = [loc.strip() for loc in cellular_locations.split(",")]
            tissue_locations_list = [loc.strip() for loc in tissue_locations.split(",")]
            biospecimen_locations_list = [loc.strip() for loc in biospecimen_locations.split(",")]

            met_graph = n4j.get_metabolite_graph(metabolite_ids, cellular_locations_list, tissue_locations_list, biospecimen_locations_list, database_range, experiment_range)

            graph = create_graph(met_graph)

            # Render the graph using Graphviz
            st.graphviz_chart(graph.source)
 
    if selected_entity == 'Proteins':

        protein_ids = st.sidebar.text_input("Enter protein IDs (separated by commas)", "P02768, P02769")

        prot_graph = n4j.get_protein_graph(protein_ids)






