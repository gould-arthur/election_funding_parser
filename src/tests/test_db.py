#!/usr/bin/env python3
from src.efp_populator import Populator, TABLES_MAP
from os import path
from sys import stderr
from os import remove


CUR_DIR = path.abspath("./src/tests")

def _log(any: any, blank: bool = False):
    fd = open(f"{CUR_DIR}/testing.log", "w" if blank else "a")
    print(any, file=fd, end='\n\n')
    fd.close()


def test_table_creation():
    db_name = f"{CUR_DIR}/testing.db"
    with Populator(db_name) as p:
        p.populate(1980)
        for table in TABLES_MAP.keys():
            result = p._cur.execute(f"SELECT * from sqlite_master WHERE name='{table}'").fetchone()
            assert result is not None

        result = p._cur.execute(f"SELECT name from sqlite_master").fetchall()
        #assert len(result) == len(list(TABLES_MAP.keys())) + 1  # one added for sqlite ROWID

    #remove(db_name)


def test_data_insert():
    pass

