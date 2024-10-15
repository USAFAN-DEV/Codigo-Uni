#include "utils.h"
#include <iostream>
#include <string>
#include <thread>
#include <list>


int main(int argc, char** argv)
{

    //init server
    int serverSocketID = initServer(3000); 

    //Creamos buffer para recibir mensajes
    std::vector<unsigned char> buffer;

    //wait for connection
    while(!checkClient()) usleep(100);
    std::cout<<"Cliente conectado\n";

    //Necesito un identificador del cliente
    int clientId = getLastClientID();

    //Recibimos el mensaje
    recvMSG(clientId, buffer);

    //Guardamos el mensaje y lo desempaqueto
    std::string msg;
    msg.resize(buffer.size());
    unpackv(buffer, (char*)msg.data(), msg.size());

    std::cout << "Mensaje recibido: " << msg << "\n";

    //Cerramos la conexion
    closeConnection(clientId);

    //end
    close(serverSocketID);

    return 0;

}
