#Python y POO

class Clase:

    nombre: str
    edad: int
    
    def __init__(self, **kwargs: dict[str, int]):

        self.__dict__.update(kwargs)


"""

--- self.__dict__ ---

self.__dict__ es un atributo que contiene un diccionario de todos los atributos de instancia del objeto en cuestión.
En este contexto:
    - self se refiere a la instancia actual de una clase
    - __dict__ es el diccionario que almacena los nombres y valores de los atributos asignados a esa instancia.

--- **kwargs ---

En Python, **kwargs es una forma de pasar un número arbitrario de argumentos con nombre a una función o método.

El término kwargs significa "keyword arguments" (argumentos con palabras clave), y cuando usas **kwargs
los argumentos se agrupan en un diccionario donde las claves son los nombres de los argumentos y los valores son los datos que se les asignan.

Es útil cuando necesitas manejar un número variable de argumentos con nombre en una función o método.

self.__dict__.update(kwargs) toma los valores de kwargs y actualiza el diccionario interno de atributos de la instancia (self.__dict__) con esos valores. 
Esto tiene el efecto de asignar dinámicamente los argumentos pasados como atributos de la instancia.

"""

#Se podria definir tambien:

class Clase2:

    nombre: str
    edad: int

    def __init__(self, nombre: str, edad: int):

        self.nombre = nombre
        self.edad = edad



#FUNCIONES
import json
json.dumps()

"""
json.dumps() es una función en Python que se utiliza para convertir un objeto de Python (como un diccionario o una lista) en una cadena JSON (JavaScript Object Notation). 

Parámetros Comunes
    obj: El objeto de Python que deseas convertir a JSON (por ejemplo, un diccionario o una lista).
    skipkeys: Si es True, se omiten las claves que no son cadenas. Por defecto es False.
    ensure_ascii: Si es True (por defecto), todos los caracteres no ASCII se escapan en la salida. Si se establece en False, se permiten caracteres no ASCII.
    indent: Si se proporciona un número entero, se utiliza para definir la cantidad de espacios para la indentación (lo que mejora la legibilidad).
    separators: Permite especificar cómo se separan los elementos, por ejemplo, puedes usar (',', ': ') para obtener un espacio después de los dos puntos.
    sort_keys: Si es True, las claves del diccionario se ordenan en la salida.


NO CONFUNDIR CON json.dump()

"""

#TODO 
    - YIELD
    - globals()[model_name] = type(model_name, (Model,), {})

