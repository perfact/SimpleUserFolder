<dtml-comment>
Connection_id : sufdb
arguments: name password roles extra1='' extra2=0
</dtml-comment>
insert into users(name,password,extra1,extra2) values (<dtml-sqlvar name type="string">,
                                                       <dtml-sqlvar password type="string">,
                                                       <dtml-sqlvar extra1 type="string">,
                                                       <dtml-sqlvar extra2 type="int">)
<dtml-var sql_delimiter>
<dtml-in roles>
insert into roles(name,role) values (<dtml-sqlvar name type="string">,<dtml-sqlvar sequence-item type="string">)
<dtml-unless sequence-end>
<dtml-var sql_delimiter>
</dtml-unless>
<dtml-else>
insert into roles(name,role) values (<dtml-sqlvar name type="string">,'')
</dtml-in>