from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pamejuly@localhost:3306/apitareas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bdd = SQLAlchemy(app)
ma = Marshmallow(app)

class Tarea(bdd.Model):
    __tablename__ = 'tareas'

    id = bdd.Column(bdd.Integer, primary_key=True, autoincrement=True)
    descripcion = bdd.Column(bdd.Text, nullable=False)
    fecha_maxima = bdd.Column(bdd.Date, nullable=False)
    fecha_creacion = bdd.Column(bdd.DateTime, default=bdd.func.current_timestamp())

    def __init__(self, descripcion, fecha_maxima, fecha_creacion = None):
        self.descripcion = descripcion
        self.fecha_maxima = fecha_maxima
        self.fecha_creacion = fecha_creacion

class TareaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        load_instance = True

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)


# Definir el endpoint para crear una nueva tarea
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    descripcion = request.json['descripcion']
    fecha_maxima = request.json['fecha_maxima']
    nueva_tarea = Tarea(descripcion=descripcion, fecha_maxima=fecha_maxima)
    
    bdd.session.add(nueva_tarea)
    bdd.session.commit()
    
    return tarea_schema.jsonify(nueva_tarea)

# Definir el endpoint para obtener todas las tareas
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    todas_las_tareas = Tarea.query.all()
    resultado = tareas_schema.dump(todas_las_tareas)
    return jsonify(resultado)

# Definir el endpoint para obtener tarea por ID
@app.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea(id):
    tarea = Tarea.query.get(id)
    return tarea_schema.jsonify(tarea)


# Definir el endpoint para eliminar una tarea
@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    tarea = Tarea.query.get(id)
    if not tarea:
        return jsonify({'message': 'Tarea no encontrada'}), 404
    
    bdd.session.delete(tarea)
    bdd.session.commit()
    
    return jsonify({'message': 'Tarea eliminada correctamente'})



if __name__ == '__main__':
    app.run(debug=True)
