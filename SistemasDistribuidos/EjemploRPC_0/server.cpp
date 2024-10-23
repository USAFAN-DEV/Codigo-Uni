#include "utils.h"
#include <iostream>
#include <string>
#include <thread>
#include <list>
#include "clientManager.h"

int main(int argc, char** argv){

    //init server
    int serverSocketID = initServer(3001);
    std::vector<unsigned char> buffer;

    //esperar conexion

    while(1){

        while(!CheckClient()) usleep(100); //Hasta que el cliente no se conecta, espera
        //La función usleep() en C/C++ se utiliza para suspender la ejecución del programa por un período de tiempo específico

        std::cout << "Cliente conectado\n";

        int clientId = getLastClientID(); //Cojemos el id del cliente que se ha conectado

        std::thread *th = new std::thread(clientManager::atiendeCliente, clientId);

        //Creamos un hilo, que es una tarea que se ejecuta de forma concurrente (en paralelo) con otras tareas del programa. 
        //Esto es útil para tareas como el manejo de múltiples conexiones en un servidor, que podrían estar representadas por cada hilo.
        //Le pasamos al thread como argumentos la funcion que tiene que ejecutar, y los argumentos que les va a pasar.

    }

    //cerrar
    close(serverSocketID);
    return 0;

}