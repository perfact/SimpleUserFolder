<dtml-comment>
Connection_id : sufdb
arguments:
</dtml-comment>
create table users (name varchar, password varchar, extra1 varchar, extra2 integer)
<dtml-var sql_delimiter>
create unique index name on users (name)
<dtml-var sql_delimiter>
create table roles (name varchar, role varchar)