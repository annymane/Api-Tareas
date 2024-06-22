from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pamejuly@localhost:3306/apiflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bdd = SQLAlchemy(app)
ma = Marshmallow(app)

class Tarea(bdd.Model):
    __tablename__ = 'Tareas'

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


if __name__ == '__main__':
    app.run(debug=True)
