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


    while(1){

        while(!checkClient()) usleep(100);

        std::cout << "Cliente conectado" << endl;

        int clientId = getLastClientID();

        std::thread *th = new std::thread(clientManager::atiendeCliente, clientId);

    }

    close(serverSocketID);
    return 0;

}
