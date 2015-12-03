# createdb -U postgres asml

create table model ( 
       timestamp int
     , name text 
     , data text
     , metric decimal
     , primary key (timestamp, name)
);