from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
con = MySQL(app)


@app.route('/alumnos', methods=['GET'])
def list_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = 'select * from alumnos'
        cursor.execute(sql)
        datos = cursor.fetchall()
        listAlum = []
        for fila in datos:
            alum = {'matricula': fila[0], 'nombre': fila[1], 'apaterno': fila[2], 'amaterno': fila[3], 'correo': fila[4]}
            listAlum.append(alum)

        return jsonify({'Alumnos': listAlum, 'mensaje': 'lista de alumnos'})

    except Exception as ex:
        return jsonify({'mensaje': str(ex)})


@app.route('/alumnos/<mat>', methods=['GET'])
def leer_alumno(mat):
    try:
        with con.connection.cursor() as cursor:
            sql = "SELECT * FROM alumnos WHERE matricula = %s"
            cursor.execute(sql, (mat,))
            datos = cursor.fetchone()

            if datos is not None:
                alum = {
                    'matricula': datos[0],
                    'nombre': datos[1],
                    'apaterno': datos[2],
                    'amaterno': datos[3],
                    'correo': datos[4]
                }
                return jsonify(alum)
            else:
                return jsonify({'mensaje': 'No se encontró el alumno con matrícula {}'.format(mat)})
    except Exception as ex:
        return jsonify({'mensaje': 'Error: {}'.format(str(ex))})


@app.route('/alumnos', methods=['POST'])
def registrar_alumnos():
    try:
        alumno = leer_alumno(request.json["matricula"])
        if alumno is not None:
            return jsonify({'mensaje': 'alumno existe', 'exito': False})
        else:
            cursor = con.connection.cursor()
            sql = """INSERT INTO alumnos(matricula, nombre, apaterno, amaterno, correo)
                     VALUES ({0}, '{1}', '{2}', '{3}', '{4}')""".format(request.json['matricula'],
                                                                        request.json['nombre'],
                                                                        request.json['apaterno'],
                                                                        request.json['amaterno'],
                                                                        request.json['correo'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje': 'Alumno Registrado', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': str(ex)})


@app.route('/alumnos/update', methods=['POST'])
def actualizar_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno = '{2}', correo = '{3}' where matricula = '{4}'""".format(request.json['matricula'],
                                                                    request.json['nombre'],
                                                                    request.json['apaterno'],
                                                                    request.json['amaterno'],
                                                                    request.json['correo'])
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje': 'Alumno Actualizado', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': str(ex)})


@app.route('/alumnos/delete/<mat>', methods=['DELETE'])
def borrar_alumno(mat):
    try:
        cursor = con.connection.cursor()
        sql = "DELETE FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (mat,))
        con.connection.commit()
        return jsonify({'mensaje': 'Alumno Eliminado', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': 'Error: {}'.format(str(ex))})


def pagina_no_encontrada(error):
    return '<h1> Página no encontrada </h1>', 404


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)