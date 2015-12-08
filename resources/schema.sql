# createdb -U postgres asml

create table model ( 
       timestamp bigint
     , id text 
     , data text
     , metric real
     , primary key (timestamp, id)
);