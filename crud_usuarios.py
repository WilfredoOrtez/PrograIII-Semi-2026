from mysql.connector.errors import Error
import conexion

db = conexion.Conexion()

class crud_usuarios:
    def __init__(self):
        # Aquí usamos tu código de estudiante
        self.tabla = "usuarios_usss019225"

    def consultar(self, buscar=""):
        sql = f"SELECT * FROM {self.tabla} WHERE nombre LIKE %s"
        return db.consultar(sql, (f"%{buscar}%",))

    def login(self, usuario, clave):
        sql = f"SELECT * FROM {self.tabla} WHERE usuario = %s AND clave = %s"
        resultado = db.consultar(sql, (usuario, clave))
        return resultado[0] if resultado else None

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = f"INSERT INTO {self.tabla} (usuario, clave, nombre, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
                valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'])
                return db.ejecutar(sql, valores)
            
            elif datos['accion'] == 'modificar':
                sql = f"UPDATE {self.tabla} SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s WHERE idUsuario=%s"
                valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'], datos['idUsuario'])
                return db.ejecutar(sql, valores)
            
            elif datos['accion'] == 'eliminar':
                sql = f"DELETE FROM {self.tabla} WHERE idUsuario=%s"
                return db.ejecutar(sql, (datos['idUsuario'],))
        except Error as e:
            return f"Error: {e}"