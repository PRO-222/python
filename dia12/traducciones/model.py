import mysql.connector

class ModeloTraduccion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user= "root",
            password="root",
            database ="bd_traducciones_pro"
        )

    def agregar_palabra(self, espanol, ingles):
        cursor = self.conexion.cursor()
        sql= f"insert into traducciones values(default, '{espanol}', '{ingles}' )"
        cursor.execute(sql)
        self.conexion.commit()
        cursor.close()

    def buscar_palabra(self, espanol):
        cursor = self.conexion.cursor()
        sql = f"SELECT * FROM TRADUCCIONES WHERE palabra_espanol = '{espanol}'"
        cursor.execute(sql)
        resultado =cursor.fetchone()
        cursor.close()
        return resultado