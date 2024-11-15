create database leave_management;
use leave_management;

create table STUDENT(
	 Student_name varchar(20),
     id varchar(20) primary key,
     Password int,
     Branch varchar(20)
);
select * from teachers;
rollback;
delete from Teachers where id=5;
drop table student;
insert into STUDENT values("Pramuk", "497CS22036", 3088,"Computer Science");
insert into STUDENT values("Akash", "497CS22002", 2000,"Computer Science");
insert into STUDENT values(null, "497CS22016", 2115,"Computer Science");


update Letterscount set id="006" where id=6;
alter table letterscount modify id varchar(20);
delete from student where id="497cs22016";
create table TEACHERS(
	F_name varchar(20),
    L_name varchar(20),
	id int primary key,
    Password int,
    Branch varchar(20)
);
update teachers set id="010" where id=10;
select * from STUDENT;
select * from teachers;

select * from Letterscount;
set sql_safe_updates=0;
delete from Letterscount where id=7;
insert into Letterscount values("010",0);
select * from teachers;
select * from lettersstatus;
insert into lettersstatus values(010,0,0);

update Lettersstatus set tId="010" where tId="4";
alter table Lettersstatus modify tId varchar(20);
insert into TEACHERS values("Renita", "Fernandes", 1011, 2004,"Computer Science");
insert into TEACHERS values("Rajesh", "Kakkarannaya", 1022, 2005,"Computer Science");
insert into TEACHERS values("Dinesh", "Poojari", 003, 2006,"Computer Science");
insert into TEACHERS values("Pruthvi", "Kiran", 004, 2007,"Computer Science");
insert into TEACHERS values("Vardharaj", "Ballal", 005, 2008,"Computer Science");
insert into TEACHERS values("Shashikala", null, 010, 2009,"Computer Science");
create table WARDON(
	F_name varchar(20),
    M_name varchar(20),
    L_name varchar(20),
    id int,
    Password int,
    primary key(id, Password)
);
alter table teachers modify password varchar(20) ;
insert into WARDON values("Chandru", null,"Gowda",007, 2010);
insert into LettersCount values(006,0);
create table Admin(
	id int,
    Password int,
    primary key(id, Password)
);
insert into Admin values(2011, 2011);
select * from LettersCount;
select * from Letters;
select * from teachers;
update STUDENT set id="497CS2202",Password=2000 WHERE ID="497CS22002" AND Password=2000;
 
select * from letters;

create table Letters (
	id int,
    DateFrom date,
    DateTo date,
    Name varchar(20),
    Reg_no varchar(20),
    subject varchar(255),
    reason varchar(2000),
    Application_id int primary key
);
create table LettersCount(
	id int primary key,
    L_count int
);
create table LettersApproved (
	tId int,
	Reg_no varchar(10) ,
    Name varchar(20),
    status boolean
);
create table LettersStatus(
	tId int primary key,
	Letters_approved int,
	Letters_recieved int,
    Letters_declined int
);
select * from lettersapproved;
select * from Letters;
truncate letters;
update letterscount set L_count=0 where id=1011;

create table lettersDeclined(
	tId int,
    Name varchar(20),
    Reg_no varchar(20),
	DateFrom date,
    DateTo date
);
truncate lettersapproved;
truncate lettersstatus;
rollback;
select * from lettersstatus;
insert into lettersstatus values(6,0,0);
update lettersstatus set letters_approved=0 where tId=1011;
update letterscount set l_count=0 where id=006;
set sql_safe_updates=0;
alter table lettersapproved add Application_id int primary key;
alter table lettersdeclined add Application_id int primary key;

select * from lettersstatus;
select * from lettersdeclined;
truncate letters;
rollback;
select * from Lettersstatus;
select * from letterscount;
update Letterscount set l_count=0 where id=1011;

select * from letters;
select * from teachers;
truncate letters;
insert into letterscount values("007",0);
truncate lettersdeclined;
select * from lettersapproved;
truncate lettersdeclined;
select * from teachers;
select * from Lettersstatus;
update lettersstatus set Letters_approved = 0 where tid=1011;
update letterscount set L_count =0 where id=010;
alter table student modify id varchar(10) primary key;
drop table student;
update lettersstatus set tid="010" where tId=10;