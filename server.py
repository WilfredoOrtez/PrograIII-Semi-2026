from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import crud_clientes
import crud_periodos
import crud_producto
import crud_usuarios
import json

port = 3000

crudClientes = crud_clientes.crud_clientes()
crudPeriodos = crud_periodos.crud_periodos()
crudProductos = crud_producto.crud_productos()
crudUsuarios = crud_usuarios.crud_usuarios()


class miServidor(SimpleHTTPRequestHandler):

    def _responder_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode("utf-8"))

    def do_POST(self):

        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud).decode("utf-8")

        datos = json.loads(datos)
        if self.path == "/login":
            usuario = datos.get('usuario')
            clave = datos.get('clave')
            
            user = crudUsuarios.login(usuario, clave)
            
            if user:
                respuesta = {'ok': True, 'msg': 'Bienvenido al sistema'}
            else:
                respuesta = {'ok': False, 'msg': 'Usuario o clave incorrectos'}
                
            return self._responder_json(respuesta)

        if self.path == "/cliente":

            if datos["modulo"] == "cliente":
                respuesta = {'msg': crudClientes.administrar(datos)}
            elif datos["modulo"] == "producto":
                respuesta = {'msg': crudProductos.administrar(datos)}

            return self._responder_json(respuesta)
        
        elif self.path == "/usuario":
            respuesta = {'msg': crudUsuarios.administrar(datos)}
            return self._responder_json(respuesta)

        elif self.path == "/periodo":
            respuesta = crudPeriodos.administrar(datos)
            return self._responder_json(respuesta)

        else:

            return self._responder_json(
                {'msg': 'Ruta no encontrada'},
                404
            )

    def do_GET(self):

        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/clientes":

            datos = crudClientes.consultar(
                qs.get('buscar', [''])[0]
            )

            return self._responder_json(datos)

        elif urlParse.path == "/periodos":

            datos = crudPeriodos.consultar(
                qs.get('cliente_id', [None])[0]
            )

            return self._responder_json(datos)
        
        elif urlParse.path == "/productos":
            buscar = qs.get('buscar', [''])[0]
            datos = crudProductos.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))
            
        elif urlParse.path == "/usuarios":
            buscar = qs.get('buscar', [''])[0]
            datos = crudUsuarios.consultar(buscar)
            return self._responder_json(datos)

        elif urlParse.path == "/" or urlParse.path == "/index.html":
            self.path = "/login.html"
            return SimpleHTTPRequestHandler.do_GET(self)
    
        elif urlParse.path == "/vistas":
            self.path = f"/modulos/{qs.get('form', [''])[0]}.html"
            return SimpleHTTPRequestHandler.do_GET(self)
            
        # Si piden otro archivo (ej. sistema.html, css, js), que lo sirva normal
        return SimpleHTTPRequestHandler.do_GET(self)
print(f"Servidor corriendo en el puerto {port}")

server = HTTPServer(
    ("localhost", port),
    miServidor
)

server.serve_forever()