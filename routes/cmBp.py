from flask import Blueprint, render_template, request, redirect, url_for
from..extensions import db
from..models.conv import Moeda
from datetime import date, datetime

#instanciar blueprint
cmBp = Blueprint('cmBp',__name__)

#declarar rota para blueprint

@cmBp.route('/')
def menu():
    return render_template('menu.html')


@cmBp.route('/testedb')
def uc_list():
    db.create_all() #- descomentar para criar o DB
    #ucs_query= Moeda.query.all()
    return render_template('Banco Criado!')

