import sqlite3 as sq

def sql_start():
    base = sq.connect('database.db')
    cur = base.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS model(ip_model INT PRIMARY KEY, id_brand INT, name_model VARCHAR(255), href VARCHAR(255), FOREIGN KEY (id_brand) REFERENCES brand(id_brand))')
    base.commit()
    base.close()

def sql_add_command(id_model, id_brand, name_model, href):
    base = sq.connect('database.db')
    cur = base.cursor()
    cur.execute('INSERT INTO model (ip_model, id_brand, name_model, href) VALUES(?, ?, ?, ?)', (id_model, id_brand, name_model, href))
    base.commit()
    base.close()