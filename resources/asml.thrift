namespace py services

service StreamService {

  void emit(1:list<string> data)

}

service NotificationService {

  /**
  * Ugly stuff, it should inherit from the other service,
  * but I'm getting a python import problem.
  * Will leave it like this for now
  */
  void emit(1:list<string> data)

  void best_model(1:string id, 2:string timestamp)

}