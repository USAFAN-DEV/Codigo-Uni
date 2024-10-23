#include "clientManager.h"

void clientManager::atiendeCliente(int clientId){

    personaFuncs tipoMsg;
    std::vector<unsigned char> buffer;

    do{

        //recibimos el mensaje
        recvMSG(clientId, buffer);

        //desempaquetamos el tipo de mensaje
        tipoMsg = unpack<personaFuncs>(buffer);

        //si tipo mensaje:
        switch(tipoMsg){

            case PersonaF:
                
                //Creamos la persona
                Persona p;

                //Almacenamos la nueva persona
                clients[clientId] = p;
                buffer.clear();
                pack(buffer, ackMSG); //ackMSG: para comprobar que te han llegado bien los datos, el cliente recibe el buffer con el ackMSG para comprobar que te ha llegado bien la informacion

                break;

            case PersonaParamsF:

                string nombre;
                int edad;

                //unpackv para arrays y strings
                nombre.resize(unpack<int>(buffer)); //resize = realloc
                unpackv<char>(buffer, (char*)nombre.data(), nombre.size()); //buffer, nombre donde se guarda, tamaño.
                //(char*)nombre.data(): Esto obtiene un puntero a la memoria subyacente de la cadena nombre. Al hacer un cast a char*, se permite que unpackv escriba directamente en la memoria de la cadena.   
                edad = unpack<int>(buffer);

                //creamos la persona
                Persona p(nombre, edad);

                //almacenamos la nueva persona
                clients[clientId] = p;
                buffer.clear();
                pack(buffer, ackMSG);

                break;

            case PersonaDF:

                clients.erase(clientId);
                buffer.clear();
                pack(buffer, ackMSG);

                break;

            case setNombreF:

                string nombre;
                
                nombre.resize(unpack<int>(buffer));
                unpackv<char>(buffer, (char*)nombre.data(), nombre.size())

                clients[clientId].setNombre(nombre);
                buffer.clear();
                pack(buffer, ackMSG);
                
                break;

            case setEdadF:

                clients[clientId].setEdad(unpack<int>(buffer));
                buffer.clear();
                pack(buffer, ackMSG);

                break;

            case getNombreF:

                string nombre = clients[clientId].getNombre();
                
                //empaquetamos el ack
                pack(buffer, (personaFuncs)ackMSG);

                //empaquetamos el tamanio del nombre
                pack(buffer, (int)nombre.size());

                //empaquetamos la data del nombre
                packv(buffer, (char*)nombre.data(), nombre.size());

                break;

            case getEdadF:

                pack(buffer, (personaFuncs)ackMSG);

                pack(buffer, (int)clients[clientId].getEdad());

                break;

            default:

                std::cout << "ERROR: tipo de mensaje no valido\n";
                
                break;         

        }

    }while(tipoMsg != PersonaDF);
    closeConnection(clientId);

}