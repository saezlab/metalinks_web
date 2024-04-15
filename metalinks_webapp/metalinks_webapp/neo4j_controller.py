from neo4j import GraphDatabase, unit_of_work
import pandas as pd

class Neo4jController:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(uri, auth=(user, pwd))
        except Exception as e:
            print('Failed to create the driver', e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def get_subgraph(
    self,
    cellular_locations,
    tissue_locations,
    biospecimen_locations,
    diseases,
    pathways,
    database_cutoff,
    experiment_cutoff, 
    prediction_cutoff,
    combined_cutoff,
    include_exo,
    output="table"
):
        with self.__driver.session() as session:
            result = session.read_transaction(
                self.__get_subgraph,
                cellular_locations,
                tissue_locations,
                biospecimen_locations,
                diseases,
                pathways,
                database_cutoff,
                experiment_cutoff, 
                prediction_cutoff,
                combined_cutoff,
                include_exo,
                output
            )
            return result

    @staticmethod
    @unit_of_work(timeout=1000)
    def __get_subgraph(
        tx,
        cellular_locations,
        tissue_locations,
        biospecimen_locations,
        diseases,
        pathways,
        database_cutoff,
        experiment_cutoff, 
        prediction_cutoff,
        combined_cutoff,
        include_exo,
        output
    ):
        
        cypher_conditions = [
            "MATCH (m)-[a]->(p:Protein)",
            "WHERE type(a) IN ['CellinkerMetaboliteReceptor', 'ScconnectMetaboliteReceptor', 'StitchMetaboliteReceptor', 'NeuronchatMetaboliteReceptor', 'CellphoneMetaboliteReceptor']",
            "AND (($database_cutoff >= 200 OR $experiment_cutoff >= 300 OR $prediction_cutoff >= 700 OR $combined_cutoff >= 900) OR (type(a) <> 'StitchMetaboliteReceptor'))",
            "AND ((p.receptor_type in ['catalytic_receptor', 'gpcr', 'nhr']) OR ((p.receptor_type in ['lgic',  'other_ic', 'transporter', 'vgic'] AND a.mode in ['activation', 'inhibition'])))",
            "AND NOT a.mode in ['reaction', 'catalysis', 'expression']"
        ]

        if include_exo:


            if len(cellular_locations) > 0:
                cypher_conditions.append("AND ANY(value IN m.cellular_locations WHERE value IN $cellular_locations)")

            if len(diseases) > 0:
                cypher_conditions.append("AND ANY(value IN m.diseases WHERE value IN $diseases)")

            if len(pathways) > 0:
                cypher_conditions.append("AND ANY(value IN m.pathways WHERE value IN $pathways)")

            if len(tissue_locations) > 0:   

                cypher_conditions.append("AND (ANY(value IN m.tissue_locations WHERE value IN $tissue_locations)")

            if len(biospecimen_locations) > 0 and len(tissue_locations) > 0:

                cypher_conditions.append("OR ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations))")

            elif len(biospecimen_locations) > 0 and len(tissue_locations) == 0:
                    
                cypher_conditions.append("AND ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations)")

            elif len(tissue_locations) > 0:

                cypher_conditions.append(")")

        else:

            cypher_conditions.append("AND m.tissue_locations IS NOT NULL")

            if len(cellular_locations) > 0:
                cypher_conditions.append("AND ANY(value IN m.cellular_locations WHERE value IN $cellular_locations)")

            if len(tissue_locations) > 0:   
                cypher_conditions.append("AND ANY(value IN m.tissue_locations WHERE value IN $tissue_locations)")

            if len(biospecimen_locations) > 0:
                cypher_conditions.append("AND ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations)")

            if len(diseases) > 0:
                cypher_conditions.append("AND ANY(value IN m.diseases WHERE value IN $diseases)")

            if len(pathways) > 0:
                cypher_conditions.append("AND ANY(value IN m.pathways WHERE value IN $pathways)")

        if output == "table": 

            cypher_conditions.extend([
                """RETURN m.id as HMDB,
                m.name as MetName,
                p.symbol as Symbol,
                m.cellular_locations as CellLoc,
                m.tissue_locations as TissueLoc,
                m.biospecimen_locations as BiospecLoc,
                m.diseases as Diseases,
                m.pathways as Pathways,
                a.mode as Mode,
                a.database as Database,
                a.experiment as Experiment,
                a.prediction as Prediction,
                a.combined_score as Combined,
                p.id as Uniprot,
                p.protein_names as ProtName"""
            ])

            cypher_query = "\n".join(cypher_conditions)

            print(cypher_query)

            result = tx.run(
                cypher_query,
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                prediction_cutoff=prediction_cutoff,
                combined_cutoff=combined_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations,
                diseases=diseases,
                pathways=pathways,
            )

            df = pd.DataFrame(result.data())

            assert df.shape[0] > 0, "No results found for the given parameters. Please try again."

            return df
        
        elif output == "graph":
            
            met_conditions = cypher_conditions.copy()

            met_conditions.extend([
                """RETURN m.id as id,
                      'foundDrug' as group,
                       m.name as label
                    LIMIT 300"""
            ])

            prot_conditions = cypher_conditions.copy()

            prot_conditions.extend([
                """RETURN p.id as id,
                      'gene' as group,
                       p.symbol as label
                    LIMIT 300"""
            ])

            edge_conditions = cypher_conditions.copy()

            edge_conditions.extend([
                """RETURN m.id as from,
                       p.id as to,
                       'default' as group
                    LIMIT 300"""
            ])


            met_query   = "\n".join(met_conditions)
            prot_query  = "\n".join(prot_conditions)
            edge_query  = "\n".join(edge_conditions)

            metabolites = tx.run(
                met_query,
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                prediction_cutoff=prediction_cutoff,
                combined_cutoff=combined_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations,
                diseases=diseases,
                pathways=pathways,
            )

            proteins = tx.run(
                prot_query,
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                prediction_cutoff=prediction_cutoff,
                combined_cutoff=combined_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations,
                diseases=diseases,
                pathways=pathways,
            )

            edges = tx.run(
                edge_query,
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                prediction_cutoff=prediction_cutoff,
                combined_cutoff=combined_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations,
                diseases=diseases,
                pathways=pathways,
            )

            return metabolites.data(), proteins.data(), edges.data()



 