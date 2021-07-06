# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extras import DictCursor

table = 'dndbotdb';

def sql_select(userid):
    string = 'select * from ' + table + ' where userid = ' + str(userid) + ';';
    return string;

def sql_count(userid):
    string = 'select count(*) from ' + table + ' where userid = ' + str(userid) + ';';
    return string;
    
def sql_insert(userid):
    string = 'insert into ' + table + ' (userid,hp_now,hp_full) values (' + str(userid) + ',' + '0' + ',' + '0' + ');';
    return string;

def sql_update(userid, hp_type, hp):
    string = 'update ' + table + ' set ' + hp_type + ' = ' + str(hp) + ' where userid = ' + str(userid) + ';'
    return string

conn = psycopg2.connect(database="postgres", user="postgres", 
                        password="oleg",port=5432);
cursor = conn.cursor(cursor_factory=DictCursor);

def check(userid):
    conn = psycopg2.connect(database="postgres", user="postgres", password="oleg",port=5432);
    cursor = conn.cursor(cursor_factory=DictCursor);
    cursor.execute(sql_count(userid));
    answer = cursor.fetchone();
    string_exists = answer[0];
    cursor.close();
    conn.close();
    return string_exists
        
def init(userid, hp_full):
    conn = psycopg2.connect(database="postgres", user="postgres", password="oleg",port=5432);
    cursor = conn.cursor(cursor_factory=DictCursor);
    request = sql_insert(userid);
    cursor.execute(request); #добавляем userid
    request = sql_update(userid, 'hp_full', hp_full);
    cursor.execute(request); #записываем full
    print(request);
    request = sql_update(userid, 'hp_now', hp_full);
    cursor.execute(request); #записываем now
    print(request);
    conn.commit();
    cursor.close();
    conn.close();

def ask(userid):
    conn = psycopg2.connect(database="postgres", user="postgres", password="oleg",port=5432);
    cursor = conn.cursor(cursor_factory=DictCursor);
    request = sql_select(userid);
    cursor.execute(request);
    print(request);
    answer = cursor.fetchone();
    cursor.close();
    conn.close();
    return answer;
    
def write(userid, hp_type, hp):
    conn = psycopg2.connect(database="postgres", user="postgres", password="oleg",port=5432);
    cursor = conn.cursor(cursor_factory=DictCursor);
    request = sql_update(userid, hp_type, hp);
    cursor.execute(request);
    print(request);
    conn.commit();
    cursor.close();
    conn.close();