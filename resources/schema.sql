# createdb -U postgres asml

create table model ( 
       timestamp bigint
     , id text 
     , data text
     , metric decimal
     , primary key (timestamp, id)
);