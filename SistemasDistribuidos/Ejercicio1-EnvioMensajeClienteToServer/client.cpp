#include "utils.h"
#include <string>
#include <iostream>
#include <string>


int main(int argc,char** argv)
{

    //init connection
    auto connection = initClient("127.0.0.1", 3000); //auto es un comodin por si no me se el tipo
    std::cout<<"Cliente conectado\n";

    //enviamos un mensaje
    std::string msg = "Hola mundo"; //Complicado que funcione enviar una clase del cliente al servidor (string es una clase)
    //Cada caracter ocupa un byte y usamos formatos tipo char (esto lo tiene que saber el servidor)

    //Crear un buffer de envio (usamos los vectores de C++) y al otro lado tendremos un buffer de datos 
    std::vector<unsigned char> buffer; //Aqui meteremos los datos del string
    packv(buffer, msg.data(), msg.size()); //Permite introducir datos en el buffer

    //Enviamos el buffer
    sendMSG(connection.serverId, buffer);

    //end connection
    closeConnection(connection.serverId);

    return 0;
    
}
