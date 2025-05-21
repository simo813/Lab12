from database.DAO import DAO
import networkx as nx

from model.volume import Volume


class Model:
    def __init__(self):
        self.optPathWeight = None
        self.optPath = None
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
        listVolume = sorted(listVolume, key = lambda v: v.volume, reverse=True)
        return listVolume

    def getOptPath(self, length):
        self.optPath = []
        self.optPathWeight = 0
        graph = self.graphMO

        for node in graph.nodes:
            self.recursion(
                node=node,
                partial=[node],
                partialWeight=0,
                level=0,
                length=length
            )

        return self.optPath, self.optPathWeight

    def recursion(self, node, partial, partialWeight, level, length):
        graph = self.graphMO

        if level == length:
            if partial[-1] == partial[0]:  # ciclo chiuso
                if partialWeight > self.optPathWeight:
                    self.optPathWeight = partialWeight
                    self.optPath = list(partial)  # copia della lista
            return

        for successor in graph.neighbors(node):
            # Permetti di tornare al nodo iniziale solo alla fine
            if successor == partial[0] and level == length - 1:
                weight = graph.get_edge_data(node, successor).get('weight', 1)
                partial.append(successor)
                self.recursion(successor, partial, partialWeight + weight, level + 1, length)
                partial.pop()
            elif successor not in partial:
                weight = graph.get_edge_data(node, successor).get('weight', 1)
                partial.append(successor)
                self.recursion(successor, partial, partialWeight + weight, level + 1, length)
                partial.pop()
"""
Qua ci sono gli errori che ho fatto, tienili a mente per una prossima volta
    def getOptPath(self, length):
        partial = []
        self.optPath = []
        self.optPathWeight = 0
        graph = self.graphMO
        for node in graph.nodes:
            partial.append(node)  #errore 1
            partialWeight = 0
            level = 0
            self.recursion(node, partial, partialWeight, level, length)
    return self.optPath, self.optPathWeight
    
    def recursion(self, node, partial, partialWeight, level, length):
        graph = self.graphMO
    if level == length and partial[-1] == partial[0]: # condizione per verifare se aggiornare la soluzione migliore
        if partialWeight > self.optPathWeight:
            self.optPathWeight = partialWeight
            self.optPath = partial  #errore 3
            return
    for successor in graph.neighbors(node):
        if successor not in partial[1:]: #controllo che non percorra più volte lo stesso nodo
            weight = graph.get_edge_data(node, successor).get('weight', 1)
            partialWeight += weight  #errore 2
            partial.append(successor)
            self.recursion(successor, partial, partialWeight, level + 1, length)
            partial.pop()
            
Problemi nel codice attuale:
1)partial.append(node) nel ciclo esterno: stai aggiungendo il nodo iniziale alla lista partial, 
ma non lo rimuovi mai, quindi ogni iterazione parte con una lista già "sporca".

2)partialWeight viene modificato senza backtracking: dopo la ricorsione, dovresti sottrarre 
il peso aggiunto.

3)self.optPath = partial salva un riferimento alla lista partial, 
che poi viene modificata. Dovresti usare list(partial) per fare una copia.
"""







