CREATE TABLE MEMBER_DETAILS(
ACCT_NUMBER CHAR(10)
,JOIN_DATE DATE);
CREATE	TABLE	MEMBER_EARN(
		ACCT_NUMBER	CHAR(10)
		,EARN_TYPE_CODE	INT
		,EARN_TIMESTAMP	TIMESTAMP
		,EARN_VALUE	INT
);
CREATE	TABLE	EARN_TYPE	(
		EARN_TYPE_CODE	INT
		,EARN_TYPE_NAME	VARCHAR(255)
);
insert into member_details(ACCT_NUMBER,JOIN_DATE) values('012345','20210601');
insert into member_details(ACCT_NUMBER,JOIN_DATE) values('012346','20210901');
insert into member_details(ACCT_NUMBER,JOIN_DATE) values('012347','20210801');
insert into member_details(ACCT_NUMBER,JOIN_DATE) values('012348','20210701');
insert into member_details(ACCT_NUMBER,JOIN_DATE) values('012348','20210201');

insert into member_earn(ACCT_NUMBER,EARN_TYPE_CODE,EARN_TIMESTAMP,EARN_VALUE) values('012345',1,'2021-09-15 15:00:00',5000);
insert into member_earn(ACCT_NUMBER,EARN_TYPE_CODE,EARN_TIMESTAMP,EARN_VALUE) values('012346',2,'2021-09-15 15:00:00',6000);
insert into member_earn(ACCT_NUMBER,EARN_TYPE_CODE,EARN_TIMESTAMP,EARN_VALUE) values('012341',3,'2021-09-15 15:00:00',6000);
insert into member_earn(ACCT_NUMBER,EARN_TYPE_CODE,EARN_TIMESTAMP,EARN_VALUE) values('012342',1,'2021-09-15 15:00:00',7000);

insert into earn_type(earn_type_code,earn_type_name) values(1,'sales');
insert into earn_type(earn_type_code,earn_type_name) values(2,'training');
insert into earn_type(earn_type_code,earn_type_name) values(3,'TRAVEL');
insert into earn_type(earn_type_code,earn_type_name) values(4,'CS');

select * from member_earn e join member_details m on e.acct_number=m.acct_number and datediff(m.join_date,e.earn_timestamp) < 10;

create or replace view earn_view as select e.earn_type_name,e.earn_type_code,count( distinct m.acct_number) as "members" from earn_type e join member_earn m on e.earn_type_code=m.earn_type_code;

select * from earn_view;

select earn_type_name, count(*) as cnt from earn_view group by earn_type_name order by count(*) desc limit 1;

select earn_type_name, count(*) as cnt from earn_view group by earn_type_name order by count(*) desc limit 1 offset 2;

select m.acct_number, max(m.earn_value) as Maxearn from member_earn m group by m.earn_type_code ;
