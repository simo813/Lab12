from database.DAO import DAO
import networkx as nx

from model.volume import Volume


class Model:
    def __init__(self):
        self.DAO = DAO()
        self.graphMO = None

    def passNations(self):
        listNations = self.DAO.getNations()
        return listNations

    def createGraph(self, nation, year):
        self.graphMO = None
        graph = nx.Graph()
        listOfRetailersOfSelectedNation = self.DAO.getRetailersOfSelectedNation(nation)
        graph.add_nodes_from(listOfRetailersOfSelectedNation)
        for retailer1 in list(graph.nodes):
            for retailer2 in list(graph.nodes):
                if retailer1.Retailer_code > retailer2.Retailer_code:
                    connection = self.DAO.getConnection(retailer1, year, nation, retailer2)
                    if connection.weight > 0:
                        graph.add_edge(retailer1, retailer2, weight = connection.weight)
        self.graphMO = graph

    def calculateVolume(self):
        listVolume = []
        for node in self.graphMO:
            volumeNode = Volume(node, 0)
            for source, successor, data in self.graphMO.edges(node, data=True):
                volumeNode.volume += data['weight']
            listVolume.append(volumeNode)
        return listVolume








