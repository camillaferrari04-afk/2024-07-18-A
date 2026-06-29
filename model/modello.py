from database.DAO import DAO
import networkx as nx
import copy

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    def chromosome(self):
        return DAO.getchromosomes()

    def creategraph(self, minimo, massimo):
        self._graph.clear()
        self.addnodes(minimo, massimo)
        self.addedges(minimo, massimo)
        return len(self._graph.nodes), len(self._graph.edges)

    def addnodes(self, minimo, massimo):
        self._nodes = []
        self._idMap = {}
        for n in DAO.getnodes(minimo, massimo):
            self._graph.add_node(n)
            self._nodes.append(n)
            self._idMap[n.GeneID+n.Function] = n

    def addedges(self, minimo, massimo):
        # dizionario id1, id2, weight
        for n in DAO.getedges(minimo, massimo):
            if n["ch1"]<=n["ch2"]:
                self._graph.add_edge(self._idMap[n["id1"]+n["f1"]], self._idMap[n["id2"]+n["f2"]], weight=n["weight"])
            if n["ch1"]>=n["ch2"]:
                self._graph.add_edge(self._idMap[n["id2"]+n["f2"]], self._idMap[n["id1"]+n["f1"]], weight=n["weight"])


    def getnodimaggiori(self):
        nodi = list(self._graph.nodes)
        nodi.sort(key=lambda x: len(self._graph.out_edges(x)), reverse=True)
        nodi = nodi[0:min(5, len(nodi))]

        diznodi = []
        for n in nodi:
            outed= self._graph.out_edges(n, data=True)
            diznodi.append({"nodo": n, "outed": len(outed), "weight": sum(x[2]["weight"] for x in outed)})

        return diznodi

###############################################################RICORSIONE#############################################
    def percorsoottimo(self):
        self.bestperc = []
        self.bestcost = float('inf')
        parziale=[]

        def ricorsione(nodo, costoparziale, parziale):
            #uscita

            #aggiorno
            if len(parziale)>len(self.bestperc):
                self.bestcost = costoparziale
                self.bestperc = copy.deepcopy(parziale)
            if len(parziale) == len(self.bestperc):
                if costoparziale < self.bestcost:
                    self.bestcost = costoparziale
                    self.bestperc = copy.deepcopy(parziale)

            #ricorsione
            for n in self._graph.neighbors(nodo):
                if len(parziale)==1:
                    if n not in parziale and n.Essential != parziale[-1].Essential:
                        parziale.append(n)
                        ricorsione(n, costoparziale + self._graph.get_edge_data(parziale[-2], parziale[-1])["weight"],
                                   parziale)
                        parziale.pop()
                else:
                    if self._graph.get_edge_data(parziale[-1], n)["weight"]>self._graph.get_edge_data(parziale[-2], parziale[-1])["weight"] and n not in parziale and n.Essential != parziale[-1].Essential:
                        parziale.append(n)
                        ricorsione(n, costoparziale+self._graph.get_edge_data(parziale[-2],parziale[-1])["weight"], parziale)
                        parziale.pop()

        for n in self._graph.nodes():
            parziale.append(n)
            ricorsione(n, 0, parziale)
            parziale.pop()

        return self.bestcost, self.bestperc

    def geteta(self, nodo):
        annonascita = nodo.date_of_birth
        return 2026-annonascita.year