# createdb -U postgres stml

create table model ( 
       timestamp int
     , name text 
     , data text
     , metric decimal
     , primary key (timestamp, name)
);