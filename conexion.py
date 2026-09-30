import mysql.connector
from mysql.connector import Error

class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "db_sistema_impuestos"
        self.conectar()

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host, user=self.user,
                password=self.password, database=self.database
            )
            print("Conexión exitosa")
        except Error as e:
            print(f"Error al conectar: {e}")
            self.conexion = None

    def consultar(self, sql, params=None):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Error as e:
            print(f"Error al consultar: {e}")
            return []

    def ejecutar(self, sql, datos):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, datos)
            self.conexion.commit()
            cursor.close()
            return 'ok'
        except Error as e:
            print(f"Error al ejecutar: {e}")
            return f'Error: {e}'