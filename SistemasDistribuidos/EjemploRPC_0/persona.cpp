#include "persona.h"

Persona::Persona() : nombre(""), edad(0) {}
Persona::Persona(string nombre, int edad) : nombre(nombre), edad(edad) {}
Persona::~Persona(){}

//Los : despues del nombre de la funcion sirven para inicializar los miembros de datos de la clase antes de que se ejecute el cuerpo del constructor 

void Persona::setNombre(string nombre){this->nombre = nombre;}
void Persona::setEdad(int edad){this->edad = edad;}
string Persona::getNombre(){return this->nombre;}
int Persona::getEdad(){return this->edad;}