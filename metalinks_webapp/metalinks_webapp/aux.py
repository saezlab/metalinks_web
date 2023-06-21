import graphviz as gv

def create_graph(table_data):
    graph = gv.Graph(format='svg')

    # Extract HMDB IDs and Uniprot IDs
    hmdb_ids = set()
    uniprot_ids = set()
    for entry in table_data:
        hmdb_ids.add(entry['MetName'])
        uniprot_ids.add(entry['Symbol'])

    # Create nodes for metabolites as boxes
    with graph.subgraph() as metabolite_cluster:
        metabolite_cluster.attr('node', shape='box', style='filled', fillcolor='#932a61')
        for hmdb_id in hmdb_ids:
            metabolite_cluster.node(hmdb_id, label=hmdb_id)

    # Create nodes for proteins
    with graph.subgraph() as protein_cluster:
        protein_cluster.attr('node', shape='oval', style='filled', fillcolor='#512D55')
        for uniprot_id in uniprot_ids:
            protein_cluster.node(uniprot_id, label=uniprot_id)

    # Create edges between nodes if HMDB ID and Uniprot ID appear in the same column
    for entry in table_data:
        hmdb_id = entry['MetName']
        uniprot_id = entry['Symbol']
        if hmdb_id and uniprot_id:
            graph.edge(hmdb_id, uniprot_id)

    return graph
