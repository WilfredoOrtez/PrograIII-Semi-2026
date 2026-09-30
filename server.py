from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import crud_clientes
import crud_periodos
import json

port = 3000

crudClientes = crud_clientes.crud_clientes()
crudPeriodos = crud_periodos.crud_periodos()


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

        if self.path == "/cliente":

            respuesta = {
                'msg': crudClientes.administrar(datos)
            }

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

        elif urlParse.path == "/":

            self.path = "/index.html"

        return SimpleHTTPRequestHandler.do_GET(self)


print(f"Servidor corriendo en el puerto {port}")

server = HTTPServer(
    ("localhost", port),
    miServidor
)

server.serve_forever()