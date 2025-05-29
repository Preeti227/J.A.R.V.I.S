import csv
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\rogram Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
#cursor.execute(query)
#con.commit()

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'chatgpt', 'https://chatgpt.com/')"
#cursor.execute(query)
#con.commit()

#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


#desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#    csvreader = csv.reader(csvfile)
#    for row in csvreader:
#        selected_data = [row[i] for i in desired_columns_indices]
#        cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

#con.commit()
#con.close()

#Inserting single contacts
#query = "INSERT INTO contacts VALUES (null,'xyz', '1234567890')"
#cursor.execute(query)
#con.commit()

query = 'pratyay da'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])