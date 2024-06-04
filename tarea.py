from flask import request
import csv
from math import sin, cos, sqrt, atan2, radians

class Coordenada:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud

class Ciudad:
    def __init__(self, nombreCiudad, nombrePais):
        self.nombreCiudad = nombreCiudad
        self.nombrePais = nombrePais

class ObtenerCoordenadas:
    def obtener(self, ciudad):
        pass

class ObtenerCoordenadasMock(ObtenerCoordenadas):
    def obtener(self, ciudad):
        # Devuelve coordenadas fijas, independientemente de la ciudad.
        return Coordenada(10.0, 20.0)

class ObtenerCoordenadasAPI(ObtenerCoordenadas):
    def obtener(self, ciudad):
        url = f"https://nominatim.openstreetmap.org/search?q={ciudad.nombreCiudad},{ciudad.nombrePais}&format=json"
        response = request.get(url)
        if response.ok:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return Coordenada(lat, lon)
        return Coordenada(0.0, 0.0)

class ObtenerCoordenadasCSV(ObtenerCoordenadas):
    def __init__(self, file):
        self.file = file

    def obtener(self, ciudad):
        with open(self.file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar la cabecera
            for row in reader:
                city, country, lat, lon = row
                lat = float(lat)
                lon = float(lon)
                if city == ciudad.nombreCiudad and country == ciudad.nombrePais:
                    return Coordenada(lat, lon)
        print("No se encontraron las coordenadas de una de las ciudades.")
        return Coordenada(0.0, 0.0)

def calcular_distancia(coord1, coord2):
    R = 6371.0  # Radio de la Tierra en kilómetros
    lat1 = radians(coord1.latitud)
    lon1 = radians(coord1.longitud)
    lat2 = radians(coord2.latitud)
    lon2 = radians(coord2.longitud)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) * sin(dlat / 2) + cos(lat1) * cos(lat2) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def main():
    ciudad1 = Ciudad("Tokyo", "Japan")
    ciudad2 = Ciudad("Delhi", "India")

    # Puedes cambiar entre diferentes implementaciones aquí
    obtenerCoordenadas = ObtenerCoordenadasCSV("worldcities.csv")
    # obtenerCoordenadas = ObtenerCoordenadasAPI()
    # obtenerCoordenadas = ObtenerCoordenadasMock()

    coord1 = obtenerCoordenadas.obtener(ciudad1)
    coord2 = obtenerCoordenadas.obtener(ciudad2)

    if coord1.latitud != 0.0 and coord1.longitud != 0.0 and coord2.latitud != 0.0 and coord2.longitud != 0.0:
        distancia = calcular_distancia(coord1, coord2)
        print(f"La distancia entre {ciudad1.nombreCiudad} y {ciudad2.nombreCiudad} es de {distancia} km.")
    else:
        print("No se encontraron las coordenadas de una de las ciudades.")

if __name__ == "__main__":
    main()
