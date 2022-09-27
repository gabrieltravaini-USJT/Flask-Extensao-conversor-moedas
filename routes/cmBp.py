from queue import Empty
from flask import Blueprint, render_template, request, redirect, url_for
from..extensions import db
from..models.conv import Moeda
from datetime import date, datetime, timedelta
import datetime as dt
from sqlalchemy import desc
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
from pandas.io.json import json_normalize
import json
import os
import numpy as np

#instanciar blueprint
cmBp = Blueprint('cmBp',__name__)

#declarar rota para blueprint

@cmBp.route('/')
def update():
    last_update = Moeda.query.order_by(desc(Moeda.data_base)).first().data_base
    next_update = last_update + timedelta(days=1)
    next_update = datetime.strftime(next_update,"%m-%d-%Y")
    today = dt.datetime.now().isoformat()
    today = pd.to_datetime(today)
    today = today.strftime("%m-%d-%Y")

    df_update = consultaCotacao(next_update,today)

    if  len (df_update)>0:
        for index,row in df_update.iterrows():
            data = datetime.strptime(row.ExchangeDate[0:10], '%Y-%m-%d')
            dia = Moeda(preco_compra = row.BuyPrice, preco_venda = row.SellPrice, data_base = data)
            db.session.add(dia)
            db.session.commit()
    return redirect(url_for("cmBp.menu"))


@cmBp.route('/menu')
def menu():
    return render_template('menu.html')



@cmBp.route('/hist',methods = ['POST','GET'])
def conv_list():
    moeda_query= Moeda.query.order_by(desc(Moeda.data_base)).all()
    return render_template('lista.html', lista = moeda_query)

@cmBp.route('/conv',methods = ['POST'])
def conv():
    return render_template("conv.html")

@cmBp.route('/conv/res',methods=['POST'])
def res_conv():
    op = request.form['tipo']
    qtd = float(request.form['qtd'])
    cotacao_dia = Moeda.query.order_by(desc(Moeda.data_base)).first()
    
    if op == "Vender Dolares":
        valor = qtd*cotacao_dia.preco_venda
        valor = str(('R${:.2f}'.format(valor)))
        return render_template('res.html',op = 'vender essa quantidade de Dolares você receberá:',valor = valor)

    else:
        valor = qtd*cotacao_dia.preco_compra
        valor = str(('R${:.2f}'.format(valor)))
        return render_template('res.html',op = 'comprar essa quantidade de Dolares custará:',valor = valor)
    


@cmBp.route('/populate')#RODAR APENAS PARA INICIALIZAR O BANCO
def populate_db():
    
    db.create_all()
    dt_fim = dt.datetime.now().isoformat()
    dt_fim = pd.to_datetime(dt_fim)
    dt_fim = dt_fim.strftime("%m-%d-%Y")

    df_pop=consultaCotacao("01-01-2000",dt_fim)
    
    for index,row in df_pop.iterrows():
        data = datetime.strptime(row.ExchangeDate[0:10], '%Y-%m-%d')
        dia = Moeda(preco_compra = row.BuyPrice, preco_venda = row.SellPrice, data_base = data)
        db.session.add(dia)
    db.session.commit()
    return redirect(url_for('cmBp.conv_list'))

def consultaCotacao (dataIniCotacao,dataFimCotacao):
    url_api = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='" + dataIniCotacao + "',dataFinalCotacao='" + dataFimCotacao + "')?$format=json"

    resp = requests.get(url_api)
    df_dolar = pd.json_normalize(json.loads(resp.text)['value'])

    df_dolar.rename(columns = {'cotacaoCompra': 'BuyPrice', 'cotacaoVenda': 'SellPrice', 'dataHoraCotacao': 'ExchangeDate'}, inplace = True)

    if(df_dolar.empty==False):
        df_dolar.ExchangeDate = df_dolar.ExchangeDate.astype(str)
        return df_dolar

    else:
        return pd.DataFrame()
    