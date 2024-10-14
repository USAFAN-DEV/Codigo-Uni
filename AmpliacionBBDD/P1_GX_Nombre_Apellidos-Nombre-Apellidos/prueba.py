from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from typing import Generator, Any, Self
from geojson import Point
import pymongo
import yaml
import json

"""
def get_geojson_point(latitud: int, longitud: int):

    geojson_point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitud, latitud]
        },
        "properties":{}
    }

    return json.dumps(geojson_point, indent=2)

def getLocationPoint(address: str) -> Point:

    location = None
    while location is None:
        try:
            time.sleep(1)
            #TODO
            # Es necesario proporcionar un user_agent para utilizar la API
            # Utilizar un nombre aleatorio para el user_agent
            location = Nominatim(user_agent="Gravyy").geocode(address)
            return get_geojson_point(location.latitude, location.longitude)
        
        except GeocoderTimedOut:
            # Puede lanzar una excepcion si se supera el tiempo de espera
            # Volver a intentarlo
            continue


with open("./models.yml", "r") as file:
    config = yaml.safe_load(file)

model_names = list(config["Model"].keys())
print(model_names)
"""

def initApp(definitions_path: str = "./models.yml", mongodb_uri="mongodb://localhost:27017/", db_name="abd") -> None:
    """ 
    Declara las clases que heredan de Model para cada uno de los 
    modelos de las colecciones definidas en definitions_path.
    Inicializa las clases de los modelos proporcionando las variables 
    admitidas y requeridas para cada una de ellas y la conexión a la
    collecion de la base de datos.
    
    Parameters
    ----------
        definitions_path : str
            ruta al fichero de definiciones de modelos
        mongodb_uri : str
            uri de conexion a la base de datos
        db_name : str
            nombre de la base de datos
    """

    # Inicializar base de datos
    try:

        client = pymongo.MongoClient(mongodb_uri)

    except Exception:

        print("ERROR. " + Exception)

    database = client[db_name] #Todavia no se crea la base de datos. Solo accede a ella. Se crea cuando se realize una operacion en ella
                               #Si la base de datos ya ha sido creada, mongo la devuelve, y no crea otra nueva.

    if db_name not in client.list_database_names():

        raise ValueError(f"ERROR: La base de datos '{db_name}' no existe.")

    # Declarar tantas clases modelo colecciones existan en la base de datos
    # Leer el fichero de definiciones de modelos para obtener las colecciones
    # y las variables admitidas y requeridas para cada una de ellas.
    # Ejemplo de declaracion de modelo para colecion llamada MiModelo

    with open("./models.yml", "r") as file:

        config = yaml.safe_load(file)

    model_names = list(config["Model"].keys())

    for model_name in model_names:

        globals()[model_name] = type(model_name, (Model,), {})
        globals()[model_name].init_class(database[model_name], config["Model"][model_name]["required_vars"], config["Model"][model_name]["admissible_vars"])

initApp()