#include "utils.h"
#include <iostream>
#include <string>
#include <thread>
#include <list>
#include "conexionManager.h"
using namespace std;

int main(int argc, char** argv){

    int serverSocketID = initServer(3001);
    vector<unsigned char> buffer;

    while(1){

        while(!checkClient()) usleep(100);

        cout << "Conexion establecida" << endl;

        int conexionId = getLastClientID();

        thread *th = new thread(conexionManager::atiendeConexion, conexionId);

    }

}
