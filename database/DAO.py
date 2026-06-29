from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                    FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getchromosomes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct g.Chromosome 
                        from genes g
                        order by g.Chromosome """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getnodes(minimo, massimo):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        res = []

        query = """select *
                    from genes g
                    where g.Chromosome between %s and %s """

        cursor.execute(query, (minimo, massimo))

        for row in cursor.fetchall():
            res.append(Gene(**row))

        cursor.close()
        cnx.close()

        return res

    @staticmethod
    def getedges(minimo, massimo):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        res = []

        query = """with nodes as(select g.GeneID, g.`Function`, c.Localization, g.Chromosome  
                    from genes g, classification c
                    where g.Chromosome between %s and %s and g.GeneID = c.GeneID ),
                    AllInteractions AS (
                        SELECT GeneID1, GeneID2, Expression_Corr FROM interactions
                        UNION
                        SELECT GeneID2 AS GeneID1, GeneID1 AS GeneID2, Expression_Corr FROM interactions
                    )
                    SELECT 
                        n1.GeneID AS id1, n1.`Function` as f1,
                        n2.GeneID AS id2, n2.`Function` as f2,
                        ai.Expression_Corr AS weight, 
                        n1.Chromosome AS ch1, 
                        n2.Chromosome AS ch2
                    FROM nodes n1, nodes n2, AllInteractions ai
                    where n1.Localization = n2.Localization AND n1.GeneID < n2.GeneID and (ai.GeneID1 = n1.GeneID AND ai.GeneID2 = n2.GeneID) """

        cursor.execute(query, (minimo, massimo))

        for row in cursor.fetchall():
            res.append({"id1": row["id1"], "f1": row["f1"], "id2": row["id2"], "f2": row["f2"], "weight": row["weight"], "ch1": row["ch1"], "ch2": row["ch2"]})

        cursor.close()
        cnx.close()

        return res