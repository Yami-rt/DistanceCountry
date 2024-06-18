import unittest
from tarea import Ciudad, ObtenerCoordenadasMock, ObtenerCoordenadasAPI, calcular_distancia

class TestCalculoDistancia(unittest.TestCase):
    def setUp(self):
        self.ciudad_existente1 = Ciudad("Lima", "Peru")
        self.ciudad_existente2 = Ciudad("Buenos Aires", "Argentina")
        self.ciudad_inexistente = Ciudad("CiudadNoExistente", "PaisNoExistente")
        self.ciudad_repetida = Ciudad("Lima", "Peru")
        
        self.obtenerCoordenadasMock = ObtenerCoordenadasMock()
        self.obtenerCoordenadasAPI = ObtenerCoordenadasAPI()

    # Pruebas haciendo uso de Mock

    def test_distancia_ciudades_existentes_MOCK(self):
        coord1 = self.obtenerCoordenadasMock.obtener(self.ciudad_existente1)
        coord2 = self.obtenerCoordenadasMock.obtener(self.ciudad_existente2)
        distancia = calcular_distancia(coord1, coord2)
        self.assertAlmostEqual(distancia, 0.0)

    def test_ciudad_repetida_MOCK(self):
        coord1 = self.obtenerCoordenadasMock.obtener(self.ciudad_existente1)
        coord2 = self.obtenerCoordenadasMock.obtener(self.ciudad_repetida)
        distancia = calcular_distancia(coord1, coord2)
        self.assertAlmostEqual(distancia, 0.0)

    # Pruebas haciendo uso de API

    def test_distancia_ciudades_existentes_API(self):
        coord1 = self.obtenerCoordenadasAPI.obtener(self.ciudad_existente1)
        coord2 = self.obtenerCoordenadasAPI.obtener(self.ciudad_existente2)
        distancia = calcular_distancia(coord1, coord2)
        # Distancia aprox entre Lima y Buenos Aires
        self.assertAlmostEqual(distancia, 3120.0, delta=100.0)

    def test_ciudad_repetida_API(self):
        coord1 = self.obtenerCoordenadasAPI.obtener(self.ciudad_existente1)
        coord2 = self.obtenerCoordenadasAPI.obtener(self.ciudad_repetida)
        distancia = calcular_distancia(coord1, coord2)
        self.assertAlmostEqual(distancia, 0.0)

    def test_ciudad_inexistente_API(self):
        coord = self.obtenerCoordenadasAPI.obtener(self.ciudad_inexistente)
        self.assertEqual(coord.latitud, 0.0)
        self.assertEqual(coord.longitud, 0.0)


if __name__ == '__main__':
    unittest.main()
