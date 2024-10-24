import sqlite3

# Function to create a table in the database
def create_table(database, fields):
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    sql = "CREATE TABLE " + database['tblname'] + "("
    for f in fields:
        sql += f['name'] + " " + f['dtype'] + " " + f['modify'] + ","
    sql = sql[:-1]
    sql += ")"
    cursor.execute("DROP TABLE IF EXISTS " + database['tblname'])
    cursor.execute(sql)
    conn.commit()
    conn.close()

# Function to insert a row into the table
def insertRow(database, _fields, _fieldata):
    if len(_fields) != len(_fieldata):
        print("Field list does not equal data provided")
        return
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    sql = "INSERT INTO " + database['tblname'] + "("
    for f in _fields:
        sql += f + ","
    sql = sql[:-1] + ") VALUES("
    for f in range(len(_fieldata)):
        sql += "?" + ","
    sql = sql[:-1] + ")"
    cursor.execute(sql, _fieldata)
    conn.commit()
    conn.close()

# Function to retrieve and display records from the table
def getRecords(database, wclause):
    title = "All records from the table " + database['tblname'] + ":"
    if len(wclause) > 0:
        title = title[:-1] + " " + wclause
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    sql = "SELECT * FROM " + database['tblname'] + " " + wclause
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(title)
    for row in rows:
        print(row)
    conn.close()

# Function to delete records from the table based on a condition
def delRecord(database, whereclause):
    """Deletes a record(s) from the table based on the given whereclause."""
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    sql = "DELETE FROM " + database['tblname'] + " " + whereclause
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print(f"Deleted records where {whereclause}")

# Function to update a record in the table based on the provided information
def updateRec(database):
    """Updates a record based on the information from the database dictionary."""
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    sql = f"UPDATE {database['tblname']} SET {database['updatenamefield']} = ? WHERE {database['primarykeyfield']} = ?"
    cursor.execute(sql, (database['newname'], database['primarykeyvalue']))
    conn.commit()
    conn.close()
    print(f"Updated {database['updatenamefield']} to {database['newname']} for {database['primarykeyfield']} = {database['primarykeyvalue']}")
    
    # After updating, get the updated record
    getRecords(database, "WHERE " + database["primarykeyfield"] + " = " + str(database["primarykeyvalue"]))

# Main function to run the CRUD operations
def main():
    database = {'dbname': 'info.db', 'tblname': 'contacts',
                'primarykeyfield': 'contactid', 'primarykeyvalue': 1,
                'updatenamefield': 'last', 'newname': 'Yuto'}

    fieldlist = [
        {'name': 'contactid', 'dtype': 'int', 'modify': 'primary key'},
        {'name': 'last', 'dtype': 'varchar(30)', 'modify': ''},
        {'name': 'first', 'dtype': 'varchar(20)', 'modify': ''},
        {'name': 'address', 'dtype': 'varchar(50)', 'modify': ''},
        {'name': 'city', 'dtype': 'varchar(20)', 'modify': ''},
        {'name': 'state', 'dtype': 'char(2)', 'modify': ''},
        {'name': 'postalcode', 'dtype': 'varchar(15)', 'modify': ''}
    ]

    create_table(database, fieldlist)

    fields = ['contactid', 'last', 'first', 'address', 'city', 'state', 'postalcode']

    # Insert sample data
    fieldata = [1, 'Washington', 'George', '3200 Mount Vernon Memorial Highway', 'Mt. Vernon', 'VA', '22121']
    insertRow(database, fields, fieldata)
    fieldata = [2, 'Lincoln', 'Abraham', '123 Main ST', 'Springfield', 'MO', '65803']
    insertRow(database, fields, fieldata)
    fieldata = [3, 'Monroe', 'James', '2050 James Monroe Pkwy', 'Charlottesville', 'VA', '22902']
    insertRow(database, fields, fieldata)

    whereclause = ""
    getRecords(database, whereclause)

    print("-" * 25)

    whereclause = "WHERE state = 'MO'"
    getRecords(database, whereclause)

    print("-" * 25)

    # Delete a record using a whereclause
    whereclause = "WHERE contactid = 2"
    delRecord(database, whereclause)

    print("-" * 25)

    # Display all records after deletion
    getRecords(database, "")

    print("-" * 25)

    # Update a record based on database dictionary
    updateRec(database)

    print("-" * 25)

    # Display all records after update
    getRecords(database, "")

main()
