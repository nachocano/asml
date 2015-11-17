# createdb -U postgres stml

create table model ( 
       epoch int
     , name text 
     , data text
     , primary key (epoch, name)
);