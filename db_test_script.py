import sqlite3
from sqlite3 import Error
from venv import create

'''
def create_table(db):
    con = sqlite3.connect('sensors.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sensor_data (time datetime PRIMARY KEY, pH real NOT NULL, EC real NOT NULL)")
'''
def insert_data(db, data):
#    con = sqlite3.connect('sensors.db')

    sql = '''INSERT INTO sensor_data(time, pH, EC) VALUES (julianday('now'), ?, ?)'''

    cur = db.cursor() 
    cur.execute(sql, data)
    db.commit()

def get_data(db):
    sql =  '''SELECT date(time), time(time), pH, EC FROM sensor_data'''
    cur.execute(sql)
    row = cur.fetchall()
    return row

if __name__ == '__main__':
    con = sqlite3.connect('sensors.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sensor_data (time datetime PRIMARY KEY, pH real NOT NULL, EC real NOT NULL)")

    data = (0.0, 0.0)
    #insert_data(con, data)
    output = get_data(con)
    print("output : ", output)

