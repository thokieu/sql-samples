import sqlite3

# Opens a connection with SQLite Database and creates a new table called "emaildbTHK101719".
con = sqlite3.connect('emaildbTHK111419.sqlite') # Invokes the "connect" method with the sqlite3 library.
cur = con.cursor() # Creates a cursor object that interacts with SQLite. Think of it as an actual mouse cursor within a database that's clicking on a UI.

cur.execute('DROP TABLE IF EXISTS Counts') # Overwrites table if an existing one already exists with the same name of "Counts".
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)') # Creates a table with 2 attributes (columns) called "org" and "count" as a string and integer data type respectively.

fname = input('Enter file name: ') # Create file handle within Python.

if len(fname) < 1:
    fname = 'mbox-short.txt'

fhand = open(fname) # Intermediary to read in data from file input.

for line in fhand:
    if line.startswith('From: '):
        spline = line.split()
        email = spline[1] # Places email address into variable named "email"
        org = email.split('@')
        # Places cursor on the counts attribute (column) within the "Counts" table using the email as a positional reference point. Notice the "?" within the SQL command. It's a placeholder for the email.
        # If the email address has not been added into the table then think of the cursor as being on dead space of the UI.
        cur.execute('SELECT count FROM Counts WHERE org = ?', (org[1],))
        row = cur.fetchone() # The method invocation returns one row where the cursor is pointed. If the table isn't populated, the return value will be None.
        if row is None:
            cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org[1],)) # Creates a new entry into the table.
        else:
            cur.execute('UPDATE Counts Set count = count + 1 WHERE org = ?', (org[1],)) # Increments the attribute (column) of count within the table called "Counts" by one.
con.commit()
cur.close() # Remember to close the cursor.
con.close() # Remember to close the connection once done.

print('All Done')
