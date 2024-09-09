import os
import requests
import sys, traceback
import json
from types import SimpleNamespace
import dto
import psycopg2

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def dbSearchBookByTitle(con, title) -> list[dto.BookDto]:
    ret = []
    cur = con.cursor()
    searchSql = """SELECT id, title, publish_date, lang, series, note
        FROM book
        WHERE title ILIKE %s
        ORDER BY title"""

    cur.execute(searchSql, ("%"+title+"%",))

    rows = cur.fetchall()

    for row in rows:
        ret.append(dto.BookDto(id=row[0], title=row[1], publish_date=row[2],
                                    lang = row[3], series = row[4], note = row[5]))
    return ret


def searchBookByTitle(dbcon, title: str) -> tuple[str | None, list[SimpleNamespace]]:
    err_msg = None
    resultList = []
    try:
        resultList = dbSearchBookByTitle(dbcon, title)
        if not len(resultList) > 0:
            err_msg = 'Nothing found'
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        err_msg=f'Error querying work matcher: {str(exc_value)}'
    return err_msg, resultList
