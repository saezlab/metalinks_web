from neo4j import GraphDatabase, unit_of_work
from graphviz import Digraph

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
    database_range,
    experiment_range
):
        with self.__driver.session() as session:
            result = session.read_transaction(
                self.__get_subgraph,
                cellular_locations,
                tissue_locations,
                biospecimen_locations,
                database_range,
                experiment_range
            )
            return result

    @staticmethod
    @unit_of_work(timeout=1000)
    def __get_subgraph(
        tx,
        cellular_locations,
        tissue_locations,
        biospecimen_locations,
        database_range,
        experiment_range
    ):
        result = tx.run(
            """MATCH (m)-[a]->(p:Protein)
            WHERE $database_range[0] <= a.database <= $database_range[1]
            AND $experiment_range[0] <= a.experiment <= $experiment_range[1]
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
                a.direction as Direction,
                a.status as Status,
                p.id as Uniprot,
                p.protein_names as ProtName""",
            database_range=database_range,
            experiment_range=experiment_range,
            cellular_locations=cellular_locations,
            tissue_locations=tissue_locations,
            biospecimen_locations=biospecimen_locations
        )

        return result.data()
    
    def get_metabolite_graph(self, metabolite_ids,
                             cellular_locations,
                             tissue_locations,
                             biospecimen_locations,
                             database_range,
                             experiment_range):
        with self.__driver.session() as session:
            result = session.read_transaction(
                self.__get_metabolite_graph,
                metabolite_ids,
                cellular_locations,
                tissue_locations,
                biospecimen_locations,
                database_range,
                experiment_range
            )
            return result

    @staticmethod
    @unit_of_work(timeout=1000)
    def __get_metabolite_graph(tx, metabolite_ids, 
                               cellular_locations, 
                               tissue_locations, 
                               biospecimen_locations, 
                               database_range, 
                               experiment_range):
        
        result = tx.run(
            """MATCH (m)-[a]->(p:Protein)
            WHERE m.id IN $metabolite_ids
            AND (400 <= a.database <= 1000)
            // AND (150 <= a.experiment <= 1000)
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
                a.direction as Direction,
                a.status as Status,
                p.id as Uniprot,
                p.protein_names as ProtName""",
            metabolite_ids=metabolite_ids, 
            cellular_locations=cellular_locations,
            tissue_locations=tissue_locations,
            biospecimen_locations=biospecimen_locations,
            database_range=database_range,
            experiment_range=experiment_range
        )

        #restric results to the first 50 nodes and 50 edges
        result = result.data()
        # result = result[:50]
        return result
    
    def get_protein_graph(self, protein_ids):
        with self.__driver.session() as session:
            result = session.read_transaction(
                self.__get_protein_graph,
                protein_ids
            )
            return result
        
    @staticmethod
    @unit_of_work(timeout=1000)
    def __get_protein_graph(tx, protein_ids):
        result = tx.run(
            """MATCH (m)-[a]->(p:Protein)
            WHERE p.id IN $protein_ids
            RETURN m.id as HMDB,
                m.name as MetName,
                p.symbol as Symbol,
                m.cellular_locations as CellLoc,
                m.tissue_locations as TissueLoc,
                m.biospecimen_locations as BiospecLoc,
                a.mode as Mode,
                a.direction as Direction,
                a.status as Status,
                p.id as Uniprot,
                p.protein_names as ProtName""",
            protein_ids=protein_ids
        )

        return result.data()