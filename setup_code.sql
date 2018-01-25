CREATE MULTISET TABLE DATAHUB_hibellm.ru_registry ,NO FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      userid      VARCHAR(10)  CHARACTER SET UNICODE NOT CASESPECIFIC,
      dbid        VARCHAR(5)   CHARACTER SET UNICODE NOT CASESPECIFIC,      
      dbshortcode VARCHAR(100) CHARACTER SET UNICODE NOT CASESPECIFIC,
      requestdate TIMESTAMP(6),
      requested   INTEGER,
      granteddate TIMESTAMP(6),
      granted     INTEGER)
NO PRIMARY INDEX ;

CREATE MULTISET TABLE DATAHUB_hibellm.ru_list ,NO FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      dbid        VARCHAR(5)   CHARACTER SET UNICODE NOT CASESPECIFIC,
      dbshortcode VARCHAR(100) CHARACTER SET UNICODE NOT CASESPECIFIC,
      pdflink     VARCHAR(500) CHARACTER SET UNICODE NOT CASESPECIFIC,
      added       INTEGER,
      approval    VARCHAR(100)
      )
NO PRIMARY INDEX ; 
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('1','CPRD','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14142',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('2','CHESS','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14120',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('3','IMSEU','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14122',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('4','IMSRA','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14128',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('5','IPSOS','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14123',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('6','TRUVEN','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14124',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('7','PREMIER','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14127',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('8','SEERM','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14129',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('9','UNOS','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14130',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('10','OPTUM','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14174',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('11','NHANES','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14125',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('12','CPT','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14121',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES('13','IMSPM','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14187',current_date,NULL);

--CODE TO CHECK IF WE NEED TO UPDATE THE RU_LIST
/*
select * from
(select 1 as "id",count(*) as rucount
from DATAHUB_hibellm.ru_list) as a
left join
(select 1 as "id",count(*) as tpcount
from RWD_META_MDH.MDHTPDetailsC
where tp_lvl1='TRAINING' and dbcode like '03_Compliance%' and TP_lvl2 is null) as b
on a.id=b.id;
*/

--THIS WILL UPDATE THE RU_LIST TABLE WITH THE RU PDF LINKS
INSERT INTO DATAHUB_hibellm.ru_list (dbid,dbshortcode,pdflink,added,approval) 
select a.dbid
      ,a.dbshortcode
      ,a.reflink
      ,current_date
      ,NULL
from
(select TPTitle as dbshortcode
       ,reflink
       ,ROW_NUMBER() OVER (ORDER BY reflink DESC ) as dbid
from RWD_META_MDH.MDHTPDetailsC
where tp_lvl1='TRAINING' 
      and dbcode like '03_Compliance%' 
      and TP_lvl2 is null
      and TPtitle not like ('reference%')) as a;




select * from RWD_META_MDH.TDUserlist
where username is not null and accountcreation is not null;
select databasename,commentstring,createtimestamp
   from DBC.databasesV
   where ownername like 'PUSER';
   
select * from dbc.userdbv
where name like 'V%';

SELECT ldap.*,CAST(tduser.grantee AS VARCHAR(30)) as TDUserName,tduser.InTD
FROM (
SELECT ldap.*,CAST('Yes' AS CHAR(3)) AS InLdap  from RWD_META_MDH.ldap) AS ldap
FULL JOIN (
SELECT distinct grantee, CAST('Yes' AS CHAR(3)) AS InTD
FROM DBC.RoleMembersV
WHERE
substr(lower(grantee),1,1) in ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
AND grantee NOT LIKE ('%/_%') escape '/' AND grantor='SYSDBA') AS tduser
ON lower(ldap.username)=lower(tduser.grantee)