import sqlite3
from models import Customer
import json

CUSTOMERS = [
    {
        "id": 1,
        "name": "Johnny"
    },
     {
        "id": 2,
        "name": "Billy"
    },
      {
        "id": 3,
        "name": "Willy"
    },
       {
        "id": 4,
        "name": "Chewy"
    }
]

def get_all_customers():
    # first create a connection object from the database imported above
    with sqlite3.connect("./kennel.sqlite3") as conn:
        # translate sql data into readable data using Row
        conn.row_factory = sqlite3.Row
        
        # create cursor object that contains the data manipulation tools
        db_cursor = conn.cursor()
        
        # selection syntax to target customer data 
        db_cursor.execute("""
            SELECT
                c.id,
                c.name
                
            FROM customer c
                """)
        
        # create empty python list for the results
        customers = []
        
        # use FETCHALL to return all customers
        dataset = db_cursor.fetchall()
        
        # call an instance of the Customer class to create new objects
        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])
        
        
        # add the newly created objects to the empty python array
        # __dict__ is part of every class and includes the objects attributes
            customers.append(customer.__dict__)
        
    return json.dumps(customers)



def get_single_customer(id):
    
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
                c.id,
                c.name
            
            FROM customer c
            WHERE c.id= ?
            """, (id, ))
        # passes in the id that will go where the question mark is
        
        data = db_cursor.fetchone()
        
        customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])

        return json.dumps(customer.__dict__)



def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    new_id = max_id + 1
    customer["id"] = new_id
    CUSTOMERS.append(customer)
    
    return customer


# this finds the index of the object we are deleting and then removes it from list
def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index
            CUSTOMERS.pop(customer_index)
            
            
def update_customer(post_body, id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index =index
            CUSTOMERS[customer_index]["status"] = post_body
            
    return CUSTOMERS[customer_index]


def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)