# createdb -U postgres asml

create table model ( 
       id text
     , timestamp bigint
     , data text
     , primary key (id)
);

create table example (
      timestamp bigint
    , data text
    , primary key (timestamp)
);