--CODE TO EXTRACT CURENT ROLES AND INSERT IN TO THE RU_REGISTRY

--CODE TO SEE WHAT WE HAVE
select a.*,b.dbid from
(select grantee as userid
      ,CASE 
       WHEN rolename like 'RO_PUB_SELECT_DS%' THEN strtok(rolename,'_',5)
       ELSE 'UNKNOWN'
       END dbtmp
      ,CASE
       WHEN dbtmp in ('CCAE','MARKETSCAN') THEN 'TRUVEN'
       ELSE dbtmp
       END dbshortcode
       ,rolename
      ,whengranted as requestdate
      ,1 as requested
      ,whengranted as granteddate
      ,1 as granted
from dbc.rolemembersV
where rolename not like all 
('labs%','BACKUP%','RO_DEV%','RO_TST%','RO_PRD%','RO_FS%,','RA_PDIL%','RO_DLG%','RESTORE%','RO_MD5%','%ADMD%','RO_DBC%')) as a
join (select dbshortcode,dbid from DATAHUB_hibellm.ru_list) as b
on a.dbshortcode=b.dbshortcode;



--CODE TO EXTRACT CURENT ROLES AND INSERT IN TO THE RU_REGISTRY
INSERT INTO datahub_hibellm.ru_registry (userid,dbid,dbshortcode,requestdate,requested,granteddate,granted)

SELECT userid,dbid,dbshortcode,requestdate,requested,granteddate,granted FROM 
(
select a.*,b.dbid from
(select grantee as userid
      ,CASE 
       WHEN rolename like 'RO_PUB_SELECT_DS%' THEN strtok(rolename,'_',5)
       ELSE 'UNKNOWN'
       END dbtmp
      ,CASE
       WHEN dbtmp in ('CCAE','MARKETSCAN') THEN 'TRUVEN'
       ELSE dbtmp
       END dbshortcode
       ,rolename
      ,whengranted as requestdate
      ,1 as requested
      ,whengranted as granteddate
      ,1 as granted
from dbc.rolemembersV
where rolename not like all 
('labs%','BACKUP%','RO_DEV%','RO_TST%','RO_PRD%','RO_FS%,','RA_PDIL%','RO_DLG%','RESTORE%','RO_MD5%','%ADMD%','RO_DBC%')) as a
join (select dbshortcode,dbid from DATAHUB_hibellm.ru_list) as b
on a.dbshortcode=b.dbshortcode
) as c;

--NOW CHECK ALL IS OK
select *
from datahub_hibellm.ru_registry;
