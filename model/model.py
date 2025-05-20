import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.idMap = {}
        self.pesoMap = {}
        self._nodes=[]

    def getAllCountries(self):
        return DAO.getAllCountries()

    def build_Graph(self, country, anno):
        self._grafo.clear()
        self._nodes = DAO.getRetailerOfCountry(country)
        for node in self._nodes:
            self.idMap[node.Retailer_code] = node
        self._grafo.add_nodes_from(self._nodes)
        #archi = DAO.getAllEdges(anno, self.idMap)
        #for arco in archi:
        #    self._grafo.add_edge(arco.r1, arco.r2, weight=arco.peso)
        for node in self._grafo.nodes:
            for node2 in self._grafo.nodes:
                if (node !=node2 and not self._grafo.has_edge(node,node2)):
                    self.addEdge(node,node2,anno)


        return self._grafo

    def calcola_Volumi(self):
        nodi = self._nodes
        for n in nodi:
            somma_nodo = self.calcolaVolumeNodo(n)
            self.pesoMap[n] = somma_nodo
        self.pesoMap=sorted(self.pesoMap.items(), key=lambda x:x[1], reverse=True)
        return self.pesoMap


    def calcolaVolumeNodo(self, n):
        vicini = self._grafo.neighbors(n)
        somma = 0
        for vicino in vicini:
            somma += self._grafo[n][vicino]["weight"]
        return somma

    def addEdge(self,v0,v1, anno):
        result=DAO.addEdgeBetweenNodes(v0.Retailer_code, v1.Retailer_code, self.idMap,anno)
        for arco in result:
            self._grafo.add_edge(arco.r1, arco.r2, weight=arco.peso)


