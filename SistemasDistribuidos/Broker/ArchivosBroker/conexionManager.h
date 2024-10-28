#pragma once
#include "utils.h"
using namespace std;
typedef enum{

	serverConn, //Se conecta un server
	clienteConn, //Se conecta un cliente
	
	ackMSG2
}brokerFuncs;

class conexionManager{

		public:
		
			static inline map<int, string> conexions;
			
			static inline bool salir=false;			
			static void atiendeConexion(int conexionId);
};