from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from typing import Generator, Any, Self
from geojson import Point
import pymongo
import yaml
import json

def get_geojson_point(latitud: int, longitud: int):
    """
    Obtiene un GeoJSON de tipo punto con la latitud y longitud almacenados

    Parameters
    ----------
        latitud: int
        longitud: int
    Returns
    -------
        json formatted string
            Contiene la informacion del punto (longitud y latitud)
    """

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
    """ 
    Obtiene las coordenadas de una dirección en formato geojson.Point
    Utilizar la API de geopy para obtener las coordenadas de la direccion
    Cuidado, la API es publica tiene limite de peticiones, utilizar sleeps.

    Parameters
    ----------
        address : str
            direccion completa de la que obtener las coordenadas
    Returns
    -------
        geojson.Point
            coordenadas del punto de la direccion
    """
    location = None

    while location is None:

        try:
            #Se puede utilizar un nombre aleatorio para user_agent
            location = Nominatim(user_agent="Gravyy", timeout = 10).geocode(address)

            if location:

                return get_geojson_point(location.latitude, location.longitude)
            else:
                print(f"ERROR. No se encontro la direccion {address}")
                return None
        
        except GeocoderTimedOut as e:
            #Volvemos a intentarlo
            print(e)
            continue

print(getLocationPoint("11111 Euclid Ave"))
