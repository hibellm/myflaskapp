CREATE MULTISET TABLE DATAHUB_hibellm.ru_registry ,NO FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      userid      VARCHAR(10)  CHARACTER SET UNICODE NOT CASESPECIFIC,
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
      dbid        INTEGER,
      dbshortcode VARCHAR(100) CHARACTER SET UNICODE NOT CASESPECIFIC,
      pdflink     VARCHAR(500) CHARACTER SET UNICODE NOT CASESPECIFIC,
      added       INTEGER,
      approval    VARCHAR(100)
      )
NO PRIMARY INDEX ; 
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES(1,'CPRD','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14142',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES(2,'CHESS','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14132',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES(3,'IMSEU','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14134',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES(4,'IMSRA','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14135',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES(5,'IPSOS','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14136',current_date,NULL);
INSERT INTO DATAHUB_hibellm.ru_list(dbid,dbshortcode,pdflink,added,approval) VALUES(6,'TRUVEN','http://we3.collaboration.roche.com/team/201266f4/_layouts/DocIdRedir.aspx?ID=MDH1-1210493889-14137',current_date,NULL);







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