<dtml-comment>
Connection_id : sufdb
arguments: name password roles
</dtml-comment>

<dtml-unless "password is None">
update users set password=<dtml-sqlvar password type="string"> where name=<dtml-sqlvar name type="string">
<dtml-var sql_delimiter>
</dtml-unless>
delete from roles where name=<dtml-sqlvar name type="string">
<dtml-var sql_delimiter>
<dtml-in roles>
insert into roles(name,role) values (<dtml-sqlvar name type="string">,<dtml-sqlvar sequence-item type="string">)
<dtml-unless sequence-end>
<dtml-var sql_delimiter>
</dtml-unless>
<dtml-else>
insert into roles(name,role) values (<dtml-sqlvar name type="string">,,'')
</dtml-in>
