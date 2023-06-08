from flask import Flask, render_template, request, session
import numpy as np
from database import gimnas
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# DATETIME TO STR ("%d-%m-%Y")


def datetimeToStrDMY(data):
    dataStr = data.strftime("%d-%m-%Y")
    return dataStr

# DATETIME TO STR ("%Y-%m-%d")


def datetimeToStrYMD(data):
    dataStr = data.strftime("%Y-%m-%d")
    return dataStr

# DATA STR A OBJECTE DATETIME ("%d-%m-%Y")


def strToDatetime(data):
    dataObj = datetime.datetime.strptime(data, '%d-%m-%Y')
    return dataObj

# CREAM ARRAY AMB RESERVES


def taulaPistes(llistaReserves):
    vector = []
    for registre in range(0, 5):
        registreTemp = []
        for camp in range(0, 6):
            campTemp = ""
            for reserva in llistaReserves:
                if reserva['data'].weekday() == registre and reserva['data'].hour == camp+15:
                    campTemp = campTemp + \
                        reserva['nom']+" "+reserva['llinatges']
                    campTemp = campTemp + " ["+reserva['tipo']+"] "
            registreTemp.append(campTemp)
        vector.append(registreTemp)
    return vector

# COMPROVA DADES FORMULARI I DISPONIBILITAT RESERVA


def comprova(reservaPotencial):
    resultat = 0
    if reservaPotencial['idusuari'] == "":
        resultat = "CAL INDICAR EL CLIENT QUE FA LA RESERVA"
    if not reservaPotencial['tipopista']:
        resultat = "CAL INDICAR EL TIPUS DE PISTA"
    if resultat == 0:
        ocupada = gimnas.comprovaDisponibilitat(reservaPotencial['dia'],
                                                reservaPotencial['hora'],
                                                reservaPotencial['tipopista'])
        if ocupada == 1:
            resultat = "LA PISTA NO ESTA DISPONIBLE"
    return resultat


@app.route('/')
def index():
    avui = datetime.date.today()
    dilluns = avui-datetime.timedelta(days=avui.weekday())
    divendres = dilluns+datetime.timedelta(days=4)
    session['avui'] = datetimeToStrDMY(avui)
    session['dilluns'] = datetimeToStrDMY(dilluns)
    session['divendres'] = datetimeToStrDMY(divendres)
    print(session['avui'])
    print(session['dilluns'])
    print(session['divendres'])
    llistaRes = gimnas.carregaReserves(session['dilluns'])
    print(llistaRes)
    arrayReserves = taulaPistes(llistaRes)
    print(arrayReserves)
    return render_template('UT3_tasca_reserves.html', valors=arrayReserves)


@app.route('/reserves')
def reserves():
    llistaRes = gimnas.carregaReserves(session['dilluns'])
    arrayReserves = taulaPistes(llistaRes)
    return render_template('UT3_tasca_reserves.html', valors=arrayReserves)


@app.route('/setmanaMes')
def setmanaMes():
    dilluns = strToDatetime(session['dilluns'])+datetime.timedelta(days=7)
    divendres = dilluns + datetime.timedelta(days=4)
    session['dilluns'] = datetimeToStrDMY(dilluns)
    session['divendres'] = datetimeToStrDMY(divendres)
    llistaRes = gimnas.carregaReserves(session['dilluns'])
    arrayReserves = taulaPistes(llistaRes)
    return render_template('UT3_tasca_reserves.html', valors=arrayReserves)


@app.route('/setmanaMenys')
def setmanaMenys():
    dilluns = strToDatetime(session['dilluns'])-datetime.timedelta(days=7)
    divendres = dilluns + datetime.timedelta(days=4)
    session['dilluns'] = datetimeToStrDMY(dilluns)
    session['divendres'] = datetimeToStrDMY(divendres)
    llistaRes = gimnas.carregaReserves(session['dilluns'])
    arrayReserves = taulaPistes(llistaRes)
    return render_template('UT3_tasca_reserves.html', valors=arrayReserves)


@app.route('/formulariReserva')
def formulariReserva():
    llistaUsuaris = gimnas.carregaUsuaris()
    # print(llistaUsuaris)
    avui = datetime.date.today()
    avuiSTR = datetimeToStrYMD(avui)
    # print(avuiSTR)
    return render_template('UT3_tasca_formreserva.html',
                           usuaris=llistaUsuaris,
                           avui=avuiSTR)


@app.route('/reservar')
def reservar():
    idusuari = request.args.get('usuari')
    tipopista = request.args.get('tipopista')
    dia = request.args.get('dia')
    hora = request.args.get('hora')
    reservaPotencial = {
        'idusuari': idusuari,
        'tipopista': tipopista,
        'dia': dia,
        'hora': hora
    }
    # print(reservaPotencial)
    # COMPROVA DADES FORMULARI I DISPONIBILITAT RESERVA
    resultatComprovacio = comprova(reservaPotencial)

    if resultatComprovacio == 0:
        dataHora = dia+" "+str(hora)+":00:00"
        gimnas.reservaPista(dataHora, tipopista, idusuari)

        llistaRes = gimnas.carregaReserves(session['dilluns'])
        arrayReserves = taulaPistes(llistaRes)
        return render_template('UT3_tasca_reserves.html', valors=arrayReserves)

    else:
        llistaUsuaris = gimnas.carregaUsuaris()
        # print(llistaUsuaris)
        avui = datetime.date.today()
        avuiSTR = datetimeToStrYMD(avui)
        # print(avuiSTR)
        return render_template('UT3_tasca_formreserva.html',
                               usuaris=llistaUsuaris,
                               avui=avuiSTR,
                               alerta=resultatComprovacio)


if __name__ == '__main__':
    app.run(debug=True)
