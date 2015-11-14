# createdb -U postgres stml

create table model ( 
       epoch int
     , name text 
     , data bytea
     , primary key (epoch, name)
);