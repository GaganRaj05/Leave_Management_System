create database studentportal;
use studentportal;

create table STUDENT(
	Name varchar(20),
    id varchar(20)  primary key,
    password varchar(20),
    Branch varchar(20)
);
alter table Student rename column Name to F_name;

create table queries(
	Application_id int primary key,
    F_name varchar(20),
    L_name varchar(20),
    Phone varchar(20),
    email varchar(20),
    query varchar(1000)
);
select max(Application_id) from queries;
create table Admin(
	id int primary key,
    password varchar(20)
);
select * from student;
delete from student where password=2115;
set sql_safe_updates=0;
insert into STUDENT values("Gagan","497cs22015","2115","Computer Science","Raj");
insert into Admin values(897,"IamAdmin");
alter table queries modify email varchar(40);
drop table STUDENT;
select * from queries;
truncate queries;
delete from queries where application_id=2;
