using namespace std;

int main(int argc, char** argv){

    //init server
    int serverSocketID = initServer(3001);
    vector<unsigned char> buffer;

    while(1){

        //esperar hasta que se conecte un cliente

        while(!checkClient()) usleep(100);

        //cuando se conecte conseguir su id
        int clientId = getLastClientID();

        //crear un thread con la funcion que queramos invocar. Le pasamos el clientId como parametro
        thread th* = new thread()(clientManager::atiendeCliente, clientId);

    }

    //Cerramos el server
    close(serverSocketID);
    return 0;

}