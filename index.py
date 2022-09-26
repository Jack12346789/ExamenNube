#from crypt import methods
import email
from email.policy import default
from unicodedata import category
from urllib import request
from flask import Flask, render_template, flash,redirect

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
 

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import app

app=Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:jerusalen@localhost/ExamenNube'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:Jerusalen_123@base-de-datos-nube.chyu7ziq5wad.us-east-1.rds.amazonaws.com/examennube'

app.config['SQLALCHEMY_TRACK_MODEFICATIONS']=False


# secret key
app.config['SECRET_KEY']='My super secret that no one is supposed to knaw'

#initialize the database
db=SQLAlchemy(app)


#============================================#
#== CREANDO TABLAS PARA LA BASE DE DATOS ====#
#============================================#
#=====Creando la tabla Escuela ====
class Escuela(db.Model):
    __tablename__ = 'escuela'
    codigo=db.Column(db.String(10),primary_key=True)
    nombre=db.Column(db.String(200),nullable=False)
    duracion=db.Column(db.Integer, nullable=False)
    
#=====Creando la tabla Estudiante ====    
class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id=db.Column(db.Integer, primary_key=True)
    DNI=db.Column(db.String(10),nullable=False)
    apellidos=db.Column(db.String(200),nullable=False)
    nombres=db.Column(db.String(200),nullable=False)
    feNacimiento=db.Column(db.String(30),nullable=False)
    sexo=db.Column(db.String(1),nullable=False)
    codEscuela = db.Column(db.String(10), db.ForeignKey('escuela.codigo'))#agregando esto al architeck
    category = db.relationship("Escuela")

#=====Creando la tabla Curso====== 
class Curso(db.Model):
    __tablename__ = 'curso'
    codigo=db.Column(db.String(10),primary_key=True)
    nombre=db.Column(db.String(200),nullable=False)
    credito=db.Column(db.Integer, nullable=False)
    
   
#=====Creando la tabla Matricula====== 
class Matricula(db.Model):
    __tablename__ = 'matricula'

    codigo=db.Column(db.String(10),primary_key=True)
    codEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    category = db.relationship("Estudiante")

    codCurso = db.Column(db.String(10), db.ForeignKey('curso.codigo'))
    category = db.relationship("Curso")

#creando.....
with app.app_context():#cada vez que inicio el server me crea las tablas
    db.create_all()

#===================================================================#
#===================================================================#

#creando formulario para el index
class NamerForm(FlaskForm):
    name=StringField("What's your name", validators=[DataRequired()])
    submit=SubmitField('Submit')
#==== ruta de la vista index===#
@app.route('/')
def index():
    first_name = '  Jack Huamani '
    flash("welcome to our website")

    return render_template('index.html',
    first_name=first_name)

#========================================================================#
#========================================================================#
#= AQUI SE CREAN LOS FORMULARIOS Y SUS RESPECTIVAS FUNCIONES DE UN CRUD ==#
#========================================================================#
#========================================================================#
#####

#======= Creando formulario Escuela ============
class EscuelaForm(FlaskForm):
    codigo = StringField("codigo", validators=[DataRequired()])
    nombre = StringField("nombre", validators=[DataRequired()])
    duracion = StringField("duracion", validators=[DataRequired()])
    submit = SubmitField('Submit')

#==== Guarda registro a escuela =====#
@app.route('/escuela/add', methods=['GET','POST'])
def add_escuela():
    nombre=None
    form=EscuelaForm()
    #validate form
    if form.validate_on_submit():
        escuela = Escuela(codigo=form.codigo.data, nombre = form.nombre.data, duracion = form.duracion.data)
        db.session.add(escuela)
        db.session.commit()
        nombre=form.nombre.data
        form.codigo.data=''
        form.nombre.data=''
        form.duracion.data=''
        flash("From Submitted Successfully")
    our_escuela = Escuela.query.order_by(Escuela.nombre)

    return render_template('add_escuela.html',
    nombre=nombre,
    form=form,
    our_escuela = our_escuela)

#==== Editar registro a escuela =====#
@app.route('/Escuela_edit/<codigo>',methods=['GET','POST'])
def update_escuela(codigo):
    esc=Escuela.query.get(codigo)
    form=EscuelaForm()
    if form.validate_on_submit():
        esc.codigo=form.codigo.data
        esc.nombre=form.nombre.data
        esc.duracion=form.duracion.data

        db.session.commit()

    nombre=form.nombre.data
    form.codigo.data=''
    form.nombre.data=''
    form.duracion.data=''
    flash("From Submitted Successfully")
    our_escuela=Escuela.query.order_by(Escuela.nombre)

    return render_template('edit_escuela.html',esc=esc,form=form,nombre=nombre,our_escuela=our_escuela)

#==== Eliminar Registro Escuela =====#
@app.route('/delete_Escuela/<codigo>')
def delete_escuela(codigo):
    deleteEscuela = Escuela.query.get(codigo)
    db.session.delete(deleteEscuela)
    db.session.commit()
    return redirect('/escuela/add')



#=======Creando fromulario para Curso============

class CursoForm(FlaskForm):
    codigo = StringField("codigo", validators=[DataRequired()])
    nombre = StringField("nombre", validators=[DataRequired()])
    credito = StringField("credito", validators=[DataRequired()])
    submit = SubmitField('Submit')



#==== Guarda registro a cuso =====#
@app.route('/curso/add', methods=['GET','POST'])
def add_curso():
    nombre=None
    form=CursoForm()
    #validate form
    if form.validate_on_submit():
        curso = Curso(codigo=form.codigo.data, nombre = form.nombre.data, credito = form.credito.data)
        db.session.add(curso)
        db.session.commit()
        nombre=form.nombre.data
        form.codigo.data=''
        form.nombre.data=''
        form.credito.data=''
        flash("From Submitted Successfully")
    our_curso = Curso.query.order_by(Curso.nombre)

    return render_template('add_curso.html',
    nombre=nombre,
    form=form,
    our_curso = our_curso)

#==== Editar registro a Curso =====#
@app.route('/curso_edit/<codigo>',methods=['GET','POST'])
def update_curso(codigo):
    cur=Curso.query.get(codigo)
    form=CursoForm()
    if form.validate_on_submit():
        cur.codigo=form.codigo.data
        cur.nombre=form.nombre.data
        cur.credito=form.credito.data

        db.session.commit()

    nombre=form.nombre.data
    form.codigo.data=''
    form.nombre.data=''
    form.credito.data=''
    flash("From Submitted Successfully")
    our_curso=Curso.query.order_by(Curso.nombre)
    return render_template('edit_curso.html',cur=cur,form=form,nombre=nombre,our_curso=our_curso)


#==== Eliminar Registro Curso =====#
@app.route('/delete_curso/<codigo>')
def delete_curso(codigo):
    deleteCurso = Curso.query.get(codigo)
    db.session.delete(deleteCurso)
    db.session.commit()
    return redirect('/curso/add')



#======= Creando fromulario para Estudiante============
class EstudianteForm(FlaskForm):
    DNI = StringField("DNI", validators=[DataRequired()])
    apellidos = StringField("apellidos", validators=[DataRequired()])
    nombres = StringField("nombres", validators=[DataRequired()])
    feNacimiento = StringField("feNacimiento", validators=[DataRequired()])
    sexo = StringField("sexo", validators=[DataRequired()])
    codEscuela = StringField("codEscuela", validators=[DataRequired()])
    submit = SubmitField('Submit')

#==== Guarda registro a Estudiante =====#

@app.route('/estudiante/add', methods=['GET','POST'])
def add_estudiante():
    nombres=None
    form=EstudianteForm()
    #validate form
    if form.validate_on_submit():
        escuela = Estudiante(DNI=form.DNI.data, apellidos = form.apellidos.data, nombres = form.nombres.data, feNacimiento = form.feNacimiento.data, sexo = form.sexo.data, codEscuela = form.codEscuela.data )
        db.session.add(escuela)
        db.session.commit()
        nombres=form.nombres.data
        form.DNI.data=''
        form.apellidos.data=''
        form.nombres.data=''
        form.feNacimiento.data=''
        form.sexo.data=''
        form.codEscuela.data=''
        flash("From Submitted Successfully")
    our_estudiante = Estudiante.query.order_by(Estudiante.nombres)
    escu=Escuela.query.order_by(Escuela.codigo)

    return render_template('add_estudiante.html',
    nombres=nombres,
    form=form,
    our_estudiante = our_estudiante, escu=escu)


#==== Editar registro a Estudiante =====#
@app.route('/estudiante_edit/<id>',methods=['GET','POST'])
def update_estudiante(id):
    est=Estudiante.query.get(id)
    form=EstudianteForm()
    if form.validate_on_submit():
        est.DNI=form.DNI.data
        est.apellidos=form.apellidos.data
        est.nombres=form.nombres.data
        est.feNacimiento=form.feNacimiento.data
        est.sexo=form.sexo.data
        est.codEscuela=form.codEscuela.data
    
        db.session.commit()

    nombres=form.nombres.data
    form.DNI.data=''
    form.apellidos.data=''
    form.nombres.data=''
    form.feNacimiento.data=''
    form.sexo.data=''
    form.codEscuela.data=''
    flash("From Submitted Successfully")
    our_estudiante=Estudiante.query.order_by(Estudiante.nombres)
    escu=Escuela.query.order_by(Escuela.codigo)
    escuel=Escuela.query.get(est.codEscuela)

    return render_template('edit_estudiante.html',est=est,form=form,nombres=nombres,our_estudiante=our_estudiante,escu=escu,escuel=escuel)

#==== Eliminar Registro Estudiante =====#
@app.route('/delete_estudiante/<id>')
def delete_estudiante(id):
    deleteEstudiante = Estudiante.query.get(id)
    db.session.delete(deleteEstudiante)
    db.session.commit()
    return redirect('/estudiante/add')


#==========Creando formulario para Matricula===============

class MatriculaForm(FlaskForm):
    codigo = StringField("codigo", validators=[DataRequired()])
    codEstudiante = StringField("codEstudiante", validators=[DataRequired()])
    codCurso = StringField("codCurso", validators=[DataRequired()])
    submit = SubmitField('Submit')

#==== Guarda registro a Matricula =====#
@app.route('/matricula/add', methods=['GET','POST'])
def add_matricula():
    codEstudiante=None
    form=MatriculaForm()
    #validate form
    if form.validate_on_submit():
        matricula = Matricula(codigo=form.codigo.data, codEstudiante = form.codEstudiante.data, codCurso = form.codCurso.data)
        db.session.add(matricula)
        db.session.commit()
        codEstudiante=form.codEstudiante.data
        form.codigo.data=''
        form.codEstudiante.data=''
        form.codCurso.data=''
        flash("From Submitted Successfully")
    our_matricula = Matricula.query.order_by(Matricula.codEstudiante)
    cur=Curso.query.order_by(Curso.codigo)

    return render_template('add_matricula.html',
    codEstudiante=codEstudiante,
    form=form,
    our_matricula= our_matricula,cur=cur)


#==== Editar registro a Matricula =====#
@app.route('/matricula_edit/<codigo>',methods=['GET','POST'])
def update_matricula(codigo):
    mat=Matricula.query.get(codigo)
    form=MatriculaForm()
    if form.validate_on_submit():
        mat.codigo=form.codigo.data
        mat.codEstudiante=form.codEstudiante.data
        mat.codCurso=form.codCurso.data

        db.session.commit()

    codEstudiante=form.codEstudiante.data
    form.codigo.data=''
    form.codEstudiante.data=''
    form.codCurso.data=''
    flash("From Submitted Successfully")
    our_matricula=Matricula.query.order_by(Matricula.codEstudiante)
    cur=Curso.query.order_by(Curso.codigo)
    curs=Curso.query.get(mat.codCurso)
    return render_template('edit_matricula.html',mat=mat,form=form,codEstudiante=codEstudiante,our_matricula=our_matricula,cur=cur,curs=curs)

#==== Eliminar Registro Matricula =====#
@app.route('/delete_matricula/<codigo>')
def delete_matricula(codigo):
    deleteMatricula = Matricula.query.get(codigo)
    db.session.delete(deleteMatricula)
    db.session.commit()
    return redirect('/matricula/add')

#=================================================================================#
#=================================================================================#
#================================ FIN DEL CODIGO =================================#
#=================================================================================#
#=================================================================================#
if __name__=='__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")
