namespace py services

service StreamService {

  void emit(1:list<string> data)

}

service NotificationService {

  void best_model(1:string id, 2:string timestamp)

}