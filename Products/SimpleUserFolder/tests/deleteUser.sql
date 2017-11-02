<dtml-comment>
Connection_id : sufdb
arguments: name
</dtml-comment>
delete from users where users.name=<dtml-sqlvar name type="string">
<dtml-var sql_delimiter>
delete from roles where roles.name=<dtml-sqlvar name type="string">
