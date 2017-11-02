<dtml-comment>
Connection_id : sufdb
arguments: name
</dtml-comment>
SELECT users.name, 
       users.password, 
       roles.role,
       users.extra1,
       users.extra2
FROM users,roles 
WHERE users.name=<dtml-sqlvar name type="string"> and users.name=roles.name