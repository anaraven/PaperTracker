delete table if exists sites;
create table sites (
        site_id text unique,
        description text,
        creation_date text
);

delete table if exists table documents;
create table documents (
        doc_id text unique,
        description text,
        creation_date text
);

delete table if exists registro;
create table registro (
        loc_id text not null,
        doc_id text not null,
        direction char not null,
        datetime text not null,
        ip text
)

