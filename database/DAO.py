from database.DB_connect import DBConnect
from model.connection import Connection
from model.retailer import Retailer
from model.volume import Volume


class DAO():

    @staticmethod
    def getNations():
        result = []
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                select distinct (gr.Country) as Country
                from go_sales.go_retailers gr 
                ORDER by gr.Country asc  
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Country"])

        except Exception as e:
            print(f"Error fetching colors: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result

    @staticmethod
    def getRetailersOfSelectedNation(nation):
        result = []
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                    select *
                    from go_sales.go_retailers gr 
                    where GR.Country = %s
                  
               """
            cursor.execute(query, (nation, ))

            for row in cursor:
                result.append(Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"]))

        except Exception as e:
            print(f"Error fetching colors: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result

    @staticmethod
    def getConnection(retailer1, year, nation, retailer2):
        result = None
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                    
                    select count(*) as weight
                    from (
                        select distinct (gds.Product_number ), year (gds.`Date`) as year, gr.Country
                        from go_sales.go_retailers gr,  go_sales.go_daily_sales gds
                        where gr.Retailer_code = %s and year (gds.`Date`) = %s
                        and gr.Retailer_code = gds.Retailer_code and gr.Country = %s
                        ) as t1, 
                        (select distinct (gds.Product_number ), year (gds.`Date`) as year, gr.Country
                        from go_sales.go_retailers gr,  go_sales.go_daily_sales gds
                        where gr.Retailer_code = %s and gr.Retailer_code = gds.Retailer_code 
                        ) as t2
                    where t1.Product_number = t2.Product_number and t1.Country = t2.Country and t1.year = t2.year  

                   """
            cursor.execute(query, (retailer1.Retailer_code, year, nation, retailer2.Retailer_code))
            row = cursor.fetchone()

            result = Connection(retailer1.Retailer_code, retailer2.Retailer_code, row["weight"]) if row else 0

        except Exception as e:
            print(f"Error fetching: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result

    @staticmethod
    def getVolume(retailer, year, nation):
        result = None
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 

                        
                       """
            cursor.execute(query, (retailer.Retailer_code, year, nation))
            row = cursor.fetchone()

            result = Volume(retailer, row["volume"]) if row else 0

        except Exception as e:
            print(f"Error fetching: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result
