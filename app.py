##===========================
#==========================
# AQUI CREO LAS RUTAS PARA MI CRUD
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/user_edit')
def edit_user():
    return render_template('edit_user.html')