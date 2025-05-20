from database.DB_connect import DBConnect
from model.arco import Arco
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct Country 
                    from go_retailers gr      
            """

        cursor.execute(query)
        for row in cursor:
            result.append(row["Country"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailerOfCountry(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select * 
                    from go_retailers gr 
                    where gr.Country = %s    
               """

        cursor.execute(query, (country,))
        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select gds2.Retailer_code as r1 , gds.Retailer_code as r2, count(distinct gds2.Product_number) as peso
                        from go_daily_sales gds, go_daily_sales gds2 
                        where year(gds2.`Date`) = %s and year(gds.`Date`) = %s and gds2.Product_number = gds.Product_number and gds.Retailer_code>gds2.Retailer_code 
                        group by gds.Retailer_code, gds2.Retailer_code    
                  """

        cursor.execute(query, (anno, anno,))
        for row in cursor:
            if row["r1"] in idMap and row["r2"]in idMap:
                result.append(Arco(idMap[row["r1"]], idMap[row["r2"]], row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def addEdgeBetweenNodes(v0,v1,idMap, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select gds2.Retailer_code as r1, gds.Retailer_code as r2,  count(distinct gds2.Product_number) as peso
                    from go_daily_sales gds, go_daily_sales gds2 
                    where gds2.Retailer_code =%s and gds.Retailer_code=%s and gds.Product_number=gds2.Product_number and year(gds2.`Date`) = %s and year(gds.`Date`) =%s  
                          """

        cursor.execute(query, (v0, v1,anno,anno,))
        for row in cursor:
            if row["r1"] in idMap and row["r2"] in idMap:
                result.append(Arco(idMap[row["r1"]], idMap[row["r2"]], row["peso"]))
        cursor.close()
        conn.close()
        return result
