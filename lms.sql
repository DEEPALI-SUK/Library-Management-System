create database lms;
use lms;
CREATE TABLE librarian(
L_Id int unique not null auto_increment,
lib_name varchar(50) not null,
lib_password varchar(100) not null,
address varchar(100) not null,
email varchar(100) unique not null,
primary key(L_Id)
);

CREATE TABLE lib_member(
M_Id int unique not null auto_increment,
member_password varchar(100) not null,
member_name varchar(50) not null,
address varchar(100) not null,
unpaid_fines int,
email varchar(100) unique not null,
primary key(M_Id)
);

CREATE TABLE shelf(
shelf_Id int unique not null,
capacity int not null default 75,
shelf_status varchar(100) not null,
primary key(shelf_Id)
);

CREATE TABLE book(
ISBN int unique not null,
title varchar(100) not null,
author varchar(100) not null,
year_of_publication int not null,
shelf_Id int not null,
count int not null,
borrow_count int not null,
category varchar(100) not null,
image varchar(10000) NOT NULL,
primary key(ISBN),
foreign key(shelf_Id) references shelf(shelf_Id) on delete cascade on update
cascade
);

CREATE TABLE follower_following(
M_Id1 int not null,
M_Id2 int not null,
primary key(M_Id1,M_Id2),
foreign key(M_Id1) references lib_member(M_Id) on delete
cascade on
update cascade,
foreign key(M_Id2) references lib_member(M_Id) on delete cascade on
update cascade
);


INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (1, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (2, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (3, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (4, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (5, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (6, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (7, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (8, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (9, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (10, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (11, 75, 'empty');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (12, 75, 'empty');

select * from book;
select * from shelf ;

--  use 12345 as password for admin

INSERT INTO librarian(L_Id, lib_name, lib_password, address, email) VALUES ('1', 'librarian', '$2b$12$7S/vNSsyeXeegQOoJO3rYuW3Rk8LnFnqBCCIPG.GJby2vp0pg6pJS', 'Indore', 'library@gmail.com');

select * from  librarian;