import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO mapData (lon, lat, damageType, minorMajor) VALUES (?, ?, ?, ?)",
            ('Longitude', 'Latitude', 'Type of Damage', 'Extent of Damage')
            )

cur.execute("INSERT INTO mapData (lon, lat, damageType, minorMajor) VALUES (?, ?, ?, ?)",
            ('38.8951', '-77.0364', 'Flood', 'Major')
            )


cur.execute("INSERT INTO mapData (lon, lat, damageType, minorMajor) VALUES (?, ?, ?, ?)",
            ('3123.8951', '71327.0364', 'Fire', 'Minor')
            )

connection.commit()
connection.close()
