__author__ = 'juju'

import sqlite3 as lite

con = lite.connect('price_checks.db')

with con:
    cur = con.cursor()
    cur.execute("INSERT INTO price_checks VALUES(200,100,2,'3','1','teom','asd')")

    rows = cur.fetchall()
    for row in rows:
        print row