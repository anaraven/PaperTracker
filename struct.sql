drop table if exists sites;
create table sites (
        site_id text unique,
        description text,
        creation_date text
);

drop table if exists table documents;
create table documents (
        doc_id text unique,
        description text,
        creation_date text
);

drop table if exists registro;
create table registro (
        site_id text not null,
        doc_id text not null,
        direction char not null,
        datetime text not null,
        ip text
);

drop table if exists log;
create table log (
        site_id text not null,
        direction char not null,
        datetime text not null,
        ip text
);
