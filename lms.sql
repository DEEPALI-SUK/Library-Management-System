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
shelf_status varchar(100) not null default 'available',
primary key(shelf_Id)
);

CREATE TABLE book(
book_id int unique not null auto_increment,
ISBN int not null,
title varchar(100) not null,
author varchar(100) not null,
year_of_publication int not null,
shelf_Id int not null,
count int not null default 0,
borrow_count int not null,
category varchar(100) not null,
book_shelf_status varchar(100) not null,
image varchar(10000) NOT NULL,
primary key(book_id),
foreign key(shelf_Id) references shelf(shelf_Id) on delete cascade on update
cascade
);

CREATE TABLE borrow(
     M_Id int not null,
     book_id int not null,
     start_date date not null,
     due_date date not null,
     primary key(M_Id, book_id),
     foreign key(M_Id) references lib_member(M_Id) on delete cascade on update cascade,
     foreign key(book_id) references book(book_id) on delete cascade on update cascade
);
CREATE TABLE book_status(
     M_Id int not null,
     book_id int not null,
     status1 varchar(100) not null,
     primary key(M_Id, book_id),
     foreign key(M_Id) references lib_member(M_Id) on delete cascade on update cascade,
     foreign key(book_id) references book(book_id) on delete cascade on update cascade
);

CREATE TABLE onhold(
     M_Id int not null,
     book_id int not null,
     hold_date date not null,
     hold_time time(0) not null,
     primary key(M_Id, book_id),
     foreign key(M_Id) references lib_member(M_Id) on delete cascade on update cascade,
     foreign key(book_id) references book(book_id) on delete cascade on update cascade
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


INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (1, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (2, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (3, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (4, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (5, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (6, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (7, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (8, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (9, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (10, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (11, 75, 'available');
INSERT INTO shelf (shelf_Id, capacity, shelf_status) VALUES (12, 75, 'available');

select * from book;
select * from shelf ;
select * from borrow;
select * from book_status;
select * from onhold;

select * from  lib_member;