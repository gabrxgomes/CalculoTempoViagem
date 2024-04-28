from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)
bootstrap = Bootstrap(app)

def obter_coordenadas_por_cep(cep):
    geolocator = Nominatim(user_agent="testcomgeopy")
    location = geolocator.geocode(cep)
    return (location.latitude, location.longitude)

def calcular_tempo_viagem(cep_origem, cep_destino, velocidade_media):
    origem = obter_coordenadas_por_cep(cep_origem)
    destino = obter_coordenadas_por_cep(cep_destino)
    
    distancia = geodesic(origem, destino).kilometers
    tempo_horas = distancia / velocidade_media
    dias, horas = divmod(tempo_horas, 24)
    
    return int(dias), int(horas)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cep_origem = request.form['cep_origem']
        cep_destino = request.form['cep_destino']
        dias, horas = calcular_tempo_viagem(cep_origem, cep_destino, 60)
        return render_template('result.html', cep_origem=cep_origem, cep_destino=cep_destino, dias=dias, horas=horas)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
