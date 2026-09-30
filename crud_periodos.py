from datetime import datetime
from mysql.connector.errors import Error
import conexion
from calculo_impuesto import calcular_impuesto, detalle_calculo

db = conexion.Conexion()


class crud_periodos:

    # ---------------------------------------------------------
    # CONSULTAS
    # ---------------------------------------------------------
    def consultar(self, cliente_id=None):
        if cliente_id:
            sql = """
                SELECT p.*, c.nombre AS cliente, pr.codigo AS producto_codigo,
                       pr.nombre AS producto_nombre
                FROM periodos p
                JOIN clientes c ON c.idCliente = p.cliente_id
                JOIN productos pr ON pr.id = p.producto_id
                WHERE p.cliente_id = %s
                ORDER BY p.desde DESC
            """
            return db.consultar(sql, (cliente_id,))
        else:
            sql = """
                SELECT p.*, c.nombre AS cliente, pr.codigo AS producto_codigo,
                       pr.nombre AS producto_nombre
                FROM periodos p
                JOIN clientes c ON c.idCliente = p.cliente_id
                JOIN productos pr ON pr.id = p.producto_id
                ORDER BY p.desde DESC
            """
            return db.consultar(sql)

    def buscar_tarifa(self, producto_id, balance, fecha):
        """Busca tarifas vigentes que contengan el balance en la fecha indicada."""
        sql = """
            SELECT * FROM tarifas
            WHERE producto_id = %s
              AND %s BETWEEN desde AND hasta
              AND vigencia_desde <= %s
              AND (vigencia_hasta IS NULL OR vigencia_hasta >= %s)
        """
        return db.consultar(sql, (producto_id, balance, fecha, fecha))

    def verificar_superposicion(self, cliente_id, producto_id, desde, hasta,
                                excluir_id=None):
        """Verifica si hay superposición de períodos."""
        sql = """
            SELECT id FROM periodos
            WHERE cliente_id = %s AND producto_id = %s
              AND desde < %s AND hasta > %s
        """
        params = [cliente_id, producto_id, hasta, desde]
        if excluir_id:
            sql += " AND id != %s"
            params.append(excluir_id)
        resultado = db.consultar(sql, tuple(params))
        return len(resultado) > 0

    # ---------------------------------------------------------
    # VALIDACIONES
    # ---------------------------------------------------------
    def _validar(self, datos):
        # Cliente existe y es empresa
        sql_cliente = "SELECT tipo FROM clientes WHERE idCliente = %s"
        cliente = db.consultar(sql_cliente, (datos['cliente_id'],))
        if not cliente:
            return "El cliente indicado no existe."
        if cliente[0]['tipo'] != 'empresa':
            return "El Impuesto a las Actividades Economicas requiere un cliente de tipo empresa."

        # Balance
        try:
            balance = float(datos['balance'])
        except (ValueError, TypeError):
            return "Ingrese un balance mayor que cero."
        if balance <= 0:
            return "Ingrese un balance mayor que cero."

        # Fechas
        try:
            desde = datetime.strptime(datos['desde'], "%Y-%m-%d").date()
            hasta = datetime.strptime(datos['hasta'], "%Y-%m-%d").date()
        except ValueError:
            return "Formato de fecha invalido."
        if desde >= hasta:
            return "La fecha Hasta debe ser posterior a la fecha Desde."

        # Superposición
        if self.verificar_superposicion(
            datos['cliente_id'], datos['producto_id'],
            desde.isoformat(), hasta.isoformat()
        ):
            return "El periodo indicado se superpone con un periodo existente."

        return None  # todo OK

    # ---------------------------------------------------------
    # CALCULAR (sin guardar) — para vista previa
    # ---------------------------------------------------------
    def calcular(self, datos):
        error = self._validar(datos)
        if error:
            return {'error': error}

        balance = float(datos['balance'])
        tarifas = self.buscar_tarifa(
            datos['producto_id'], balance, datos['desde']
        )

        if len(tarifas) == 0:
            return {'error': "No existe una tarifa configurada para el balance indicado."}
        if len(tarifas) > 1:
            return {'error': "Existe mas de una tarifa aplicable. Corrija la tabla tarifaria."}

        tarifa = tarifas[0]
        detalle = detalle_calculo(balance, tarifa)
        return {'ok': True, 'detalle': detalle, 'tarifa_id': tarifa['id']}

    # ---------------------------------------------------------
    # GUARDAR
    # ---------------------------------------------------------
    def administrar(self, datos):
        error = self._validar(datos)

        if error:
            return {
                'estado': 'error',
                'mensaje': error
            }

        balance = float(datos['balance'])

        tarifas = self.buscar_tarifa(
            datos['producto_id'],
            balance,
            datos['desde']
        )

        if len(tarifas) == 0:
            return {
                'estado': 'error',
                'mensaje': 'No existe una tarifa configurada para el balance indicado.'
            }

        if len(tarifas) > 1:
            return {
                'estado': 'error',
                'mensaje': 'Existe mas de una tarifa aplicable. Corrija la tabla tarifaria.'
            }

        tarifa = tarifas[0]

        precio = calcular_impuesto(balance, tarifa)

        try:
            sql = """
                INSERT INTO periodos
                (cliente_id, producto_id, desde, hasta, balance,
                 tarifa_id, precio_calculado, formula_version, fecha_calculo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """

            valores = (
                datos['cliente_id'],
                datos['producto_id'],
                datos['desde'],
                datos['hasta'],
                balance,
                tarifa['id'],
                precio,
                'bloques_v1'
            )

            resultado = db.ejecutar(sql, valores)

            if resultado == 'ok':
                detalle = detalle_calculo(balance, tarifa)

                return {
                    'estado': 'ok',
                    'precio': precio,
                    'detalle': detalle
                }

            return {
                'estado': 'error',
                'mensaje': resultado
            }

        except Error as e:
            return {
                'estado': 'error',
                'mensaje': f'Error al guardar el periodo: {e}'
            }