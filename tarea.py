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
    while True:
        print("Que desea hacer?")
        print("1. Calcular la distancia entre dos ciudades")
        print("2. Hallar el par de ciudades más cercano en comparación a un tercero")
        print("3. Salir")
        opcion = int(input("Ingrese el número de la opción deseada: "))

        if opcion == 1:
            ciudad1 = Ciudad(input("Ingrese el nombre de la primera ciudad: "), input("Ingrese el nombre del país de la primera ciudad: "))
            ciudad2 = Ciudad(input("Ingrese el nombre de la segunda ciudad: "), input("Ingrese el nombre del país de la segunda ciudad: "))

            obtenerCoordenadas = ObtenerCoordenadasCSV("worldcities.csv")
            coord1 = obtenerCoordenadas.obtener(ciudad1)
            coord2 = obtenerCoordenadas.obtener(ciudad2)

            distancia = calcular_distancia(coord1, coord2)
            print(f"La distancia entre {ciudad1.nombreCiudad} en {ciudad1.nombrePais} y {ciudad2.nombreCiudad} en {ciudad2.nombrePais} es de {distancia} km.")
        elif opcion == 2:
            ciudad1 = Ciudad(input("Ingrese el nombre de la primera ciudad: "), input("Ingrese el nombre del país de la primera ciudad: "))
            ciudad2 = Ciudad(input("Ingrese el nombre de la segunda ciudad: "), input("Ingrese el nombre del país de la segunda ciudad: "))
            ciudad3 = Ciudad(input("Ingrese el nombre de la tercera ciudad: "), input("Ingrese el nombre del país de la tercera ciudad: "))

            obtenerCoordenadas = ObtenerCoordenadasCSV("worldcities.csv")
            coord1 = obtenerCoordenadas.obtener(ciudad1)
            coord2 = obtenerCoordenadas.obtener(ciudad2)
            coord3 = obtenerCoordenadas.obtener(ciudad3)

            distancia1 = calcular_distancia(coord1, coord3)
            distancia2 = calcular_distancia(coord2, coord3)
            distancia3 = calcular_distancia(coord1, coord2)

            if distancia1 < distancia2 and distancia1 < distancia3:
                print(f"La distancia más corta es entre {ciudad1.nombreCiudad} en {ciudad1.nombrePais} y {ciudad3.nombreCiudad} en {ciudad3.nombrePais} con {distancia1} km.")
            elif distancia2 < distancia1 and distancia2 < distancia3:
                print(f"La distancia más corta es entre {ciudad2.nombreCiudad} en {ciudad2.nombrePais} y {ciudad3.nombreCiudad} en {ciudad3.nombrePais} con {distancia2} km.")
            else:
                print(f"La distancia más corta es entre {ciudad1.nombreCiudad} en {ciudad1.nombrePais} y {ciudad2.nombreCiudad} en {ciudad2.nombrePais} con {distancia3} km.")
        elif opcion == 3:
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
