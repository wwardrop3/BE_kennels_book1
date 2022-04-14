import sqlite3
import json
from models.employee import Employee


EMPLOYEES = [
    {
        "id":1,
        "name":"Carl"
    },
    {
        "id":2,
        "name":"John"
    },
    {
        "id":3,
        "name":"Steve"
    },
    {
        "id":4,
        "name":"Bill"
    }
]

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.location_id
            
            FROM employee a
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        
        # a cursor is an instance of a class with certain arrays and methods
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
    
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # employee class above.
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)

# Function with single paramenter
def get_single_employee(id):
    # this allows the page to access data in the sqlite3 database, conn is a connection
    with sqlite3.connect("./kennel.sqlite3") as conn:
    
    #with creates a connection with the database and disconnects once its done
    #gives back connection OBJECT
    
        #row_factory is a method of the connection object 
        # Row is built in way to process the database information we get back
        conn.row_factory = sqlite3.Row
        
        # cursor object with methods for executing sql in python..
        # python object that works with sql
        db_cursor = conn.cursor()



        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.location_id

            
            FROM employee a
            WHERE a.id= ?
            """, (id, ))
        # passes in the id that will go where the question mark is
        
        data = db_cursor.fetchone()
        
        employee = Employee(data['id'], data['name'], data['address'],
            data['location_id'])

        return json.dumps(employee.__dict__)


# this takes an existing employee and simply adds a unique id to it
def create_employee(employee):
    # first get the last id of the existing list
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    
    employee["id"] = new_id
    
    EMPLOYEES.append(employee)
    
    return employee


def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
            EMPLOYEES.pop(employee_index)
            
            
def update_employee(post_body, id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
    
    EMPLOYEES[employee_index]["status"] = post_body
    
    
def get_employees_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.location_id

            
            FROM employee a
            WHERE a.location_id= ? """, (location_id, ))
        
        employees = []
        database = db_cursor.fetchall()
        
        for row in database:
            employee = Employee(row['id'], row['name'], row['address'],
            row['location_id'])
            
            employees.append(employee.__dict__)

        return json.dumps(employees)