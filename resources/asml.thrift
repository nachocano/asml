namespace py services

enum ComponentType {
  DATASTREAM = 1,
  FEATGEN = 2,
  LEARNER = 3,
  DEPLOYER = 4
}

service StreamService {

  void emit(1:list<string> data),

  void notify(1:list<string> addresses)

}

service RegistryService {
  
  list<string> reg(1:ComponentType type, 2:string address),

  list<string> unreg(1:ComponentType type, 2:string address)
}


