import streamlit as st
from neo4j_controller import Neo4jController
import pandas as pd
import base64
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import json
sys.path.append('..')
# from aux import create_graph
import streamlit.components.v1 as components

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


n4j = Neo4jController(
    st.secrets["neo4j_uri"],
    st.secrets["neo4j_user"],
    st.secrets["neo4j_password"],
)

st.sidebar.write("Select your parameters for contextualization")
cellular_locations = st.sidebar.text_input("Enter cellular locations (separated by commas)", "Extracellular, Cytoplasm")
tissue_locations = st.sidebar.text_input("Enter tissue locations (separated by commas)", "Kidney, All Tissues")
biospecimen_locations = st.sidebar.text_input("Enter biospecimen locations (separated by commas)", "Urine, Blood")
database_cutoff = st.sidebar.slider("Select cutoff for STITCH database score", 0, 1000, 993)
experiment_cutoff = st.sidebar.slider("Select cutoff for STITCH experimental score", 0, 1000, 993)

selected_purpose = st.sidebar.select_slider("Select visualization", ["Table", "Graph"])

if st.sidebar.button("Get Subgraph"):
    cellular_locations_list = [loc.strip() for loc in cellular_locations.split(",")]
    tissue_locations_list = [loc.strip() for loc in tissue_locations.split(",")]
    biospecimen_locations_list = [loc.strip() for loc in biospecimen_locations.split(",")]

    if selected_purpose == "Table":
         
        subgraph = n4j.get_subgraph(
            cellular_locations_list,
            tissue_locations_list,
            biospecimen_locations_list,
            database_cutoff,
            experiment_cutoff, 
            output="table"
        )
        # Prepare the data for the dataframe
        data = []
        for record in subgraph:
            data.append({
                'HMDB': record['HMDB'],
                'MetName': record['MetName'],
                'Protein': record['Symbol'],
                'ProtName': record['ProtName'],
                'CellLoc': record['CellLoc'],
                'TissueLoc': record['TissueLoc'],
                'BiospecLoc': record['BiospecLoc'],
                'Mode': record['Mode'],
                'Uniprot': record['Uniprot'],
                'DatabaseScore': record['Database'],
                'ExperimentalScore': record['Experiment']

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
                'Metrics': ['Number of Interactions', 'Number of unique metabolite ligands', 'Number of unique protein receptors'],
                'Values': [num_rows, num_unique_metabolites, num_unique_proteins]
            }
            summary_df = pd.DataFrame(summary_data)

            style = summary_df.style.hide(axis="index")
            style.hide(axis="columns")
            st.write(style.to_html(), unsafe_allow_html=True)


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

    elif selected_purpose == "Graph":

        subgraph = n4j.get_subgraph(            
            cellular_locations_list,
            tissue_locations_list,
            biospecimen_locations_list,
            database_cutoff,
            experiment_cutoff, 
            output="graph")
    

        # components.html(
        
        html_code = ''' 
        <head>
            <script src="https://cdn.drugst.one/latest/drugstone.js"></script>
            <link rel="stylesheet" href="https://cdn.drugst.one/latest/styles.css">
        </head>

        <drugst-one
            id='drugstone-component-id'
            groups='{
                "nodeGroups":{
                "gene":{"type":"gene","color":"#512D55","font":{"color":"#f0f0f0"},"groupName":"Gene","shape":"circle"},
                "foundDrug":{"type":"drug","color":"#932a61","font":{"color":"#000000"},"groupName":"Drug","shape":"diamond"}},
                "edgeGroups":{"default":{"color":"#000000","groupName":"default edge"},
                "metabolite":{"type":"drug","color":"#512D55","font":{"color":"#f0f0f0"},"groupName":"Drug","shape":"diamond"}
                }}'
            config='{
                "identifier":"symbol",
                "title":"MetalinksKG - metabolite-mediated cell-cell communication",
                "nodeShadow":true,
                "edgeShadow":false,
                showSidebar: "right",
                showOverview: true,
                showQuery: true,
                showItemSelector: true,
                showSimpleAnalysis: false,
                showAdvAnalysis: false,
                showConnectGenes: false,
                showSelection: false,
                showTasks: false,
                showNetworkMenu: false,
                "autofillEdges":false,
                "interactionDrugProtein":"ChEMBL",
                "activateNetworkMenuButtonAdjacentDrugs":false,
                "physicsOn":false,
                "activateNetworkMenuButtonAdjacentDisorderDrugs":false}'
            network='{}'>

            
        </drugst-one>

        <style>
        :root {
            --drgstn-primary: #932a61;
            --drgstn-secondary: #512D55;
            --drgstn-success: #48C774;
            --drgstn-warning: #ffdd00;
            --drgstn-danger: #ff2744;
            --drgstn-background: #f8f9fa;
            --drgstn-panel: #ffffff;
            --drgstn-info: #61c43d;
            --drgstn-text-primary: #151515;
            --drgstn-text-secondary: #eeeeee;
            --drgstn-border: rgba(0, 0, 0, 0.2);
            --drgstn-tooltip: rgba(74, 74, 74, 0.9);
            --drgstn-panel-secondary: #FFFFFF;
            --drgstn-height: 800px;
            --drgstn-font-family: Helvetica Neue, sans-serif;
        }
        </style>
        '''
   
        nodes = subgraph[0]
        nodes.extend(subgraph[1])
        network_data = {
            "nodes": nodes,
            "edges": subgraph[2]
        }
        html_code = html_code.replace("'{}'", json.dumps(network_data))
        html_code = html_code.replace("network={","network='{")
        html_code = html_code.replace("}]}>", "}]}'>")
        st.components.v1.html(html_code, height=1200, width=1200)

                # "showOverview": true,
                # "showQuery": False,
                # "showItemSelector": true,
                # "showSimpleAnalysis": false,
                # "showAdvAnalysis": true,
                # "showSelection": true,
                # "showTasks": off,
                # "showNetworkMenu": off,
                # "showLegend": true,
                # "showConnectGenes": false,