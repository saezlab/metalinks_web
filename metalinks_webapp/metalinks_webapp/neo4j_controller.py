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
    database_cutoff,
    experiment_cutoff, 
    output="table"
):
        with self.__driver.session() as session:
            result = session.read_transaction(
                self.__get_subgraph,
                cellular_locations,
                tissue_locations,
                biospecimen_locations,
                database_cutoff,
                experiment_cutoff, 
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
        database_cutoff,
        experiment_cutoff, 
        output
    ):
        if output == "table":
            result = tx.run(
                """MATCH (m)-[a]->(p:Protein)
                WHERE (($database_cutoff <= a.database) OR ($experiment_cutoff <= a.experiment))
                AND type(a) = "StitchMetaboliteReceptor"
                AND NOT a.mode IN ["reaction", "catalysis", "expression", "pred_bind", "binding"]
                AND ANY(value IN m.cellular_locations WHERE value IN $cellular_locations)
                AND (ANY(value IN m.tissue_locations WHERE value IN $tissue_locations) 
                    OR ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations))
                RETURN m.id as HMDB,
                    m.name as MetName,
                    p.symbol as Symbol,
                    m.cellular_locations as CellLoc,
                    m.tissue_locations as TissueLoc,
                    m.biospecimen_locations as BiospecLoc,
                    a.mode as Mode,
                    a.database as Database,
                    a.experiment as Experiment,
                    p.id as Uniprot,
                    p.protein_names as ProtName""",
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations
            )

            # return result.data()

            df = pd.DataFrame(result.data())

            return df
        
        elif output == "graph":

            metabolites = tx.run(
                """MATCH (m)-[a]->(p:Protein)
                WHERE (($database_cutoff <= a.database) OR ($experiment_cutoff <= a.experiment))
                AND type(a) = "StitchMetaboliteReceptor"
                AND NOT a.mode IN ["reaction", "catalysis", "expression", "pred_bind", "binding"]
                AND ANY(value IN m.cellular_locations WHERE value IN $cellular_locations)
                AND (ANY(value IN m.tissue_locations WHERE value IN $tissue_locations) 
                    OR ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations))
                RETURN m.id as id,
                      'foundDrug' as group,
                       m.name as label""",
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations
            )

            proteins = tx.run(
                """MATCH (m)-[a]->(p:Protein)
                WHERE (($database_cutoff <= a.database) OR ($experiment_cutoff <= a.experiment))
                AND type(a) = "StitchMetaboliteReceptor"
                AND NOT a.mode IN ["reaction", "catalysis", "expression", "pred_bind", "binding"]
                AND ANY(value IN m.cellular_locations WHERE value IN $cellular_locations)
                AND (ANY(value IN m.tissue_locations WHERE value IN $tissue_locations) 
                    OR ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations))
                RETURN p.id as id,
                      'gene' as group,
                       p.symbol as label""",
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations
            )

            edges = tx.run(
                """MATCH (m)-[a]->(p:Protein)
                WHERE (($database_cutoff <= a.database) OR ($experiment_cutoff <= a.experiment))
                AND type(a) = "StitchMetaboliteReceptor"
                AND NOT a.mode IN ["reaction", "catalysis", "expression", "pred_bind", "binding"]
                AND ANY(value IN m.cellular_locations WHERE value IN $cellular_locations)
                AND (ANY(value IN m.tissue_locations WHERE value IN $tissue_locations) 
                    OR ANY(value IN m.biospecimen_locations WHERE value IN $biospecimen_locations))
                RETURN m.id as from,
                       p.id as to,
                       'default' as group""",
                database_cutoff=database_cutoff,
                experiment_cutoff=experiment_cutoff,
                cellular_locations=cellular_locations,
                tissue_locations=tissue_locations,
                biospecimen_locations=biospecimen_locations
            )

            return metabolites.data(), proteins.data(), edges.data()



 