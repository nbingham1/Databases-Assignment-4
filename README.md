Databases-Assignment-4
======================

CS 5320 Introduction to Databases Homework Assignment 4

python 3.4 is used throughout

Neo4J uses the py2neo connector

pip install py2neo


MongoDB uses the pymongo connector

pip install pymongo


Redis uses the redis connector

pip install redis


MySQL uses the pymysql connector

pip install pymysql

create user "client"@"localhost";
create database assignment4;
grant all on assignment4.* to "client"@"localhost";
