import sqlite3
import json
from models import Animal
from models.customer import Customer
from models.location import Location

def get_all_animals():
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
                a.breed,
                a.status,
                a.location_id,
                a.customer_id,
                l.name location_name,
                l.address location_address,
                c.name customer_name,
                c.address customer_address
            FROM Animal a
            JOIN Location l
            ON a.location_id = l.id
            JOIN Customer c
            ON a.customer_id = c.id
            
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        
        # a cursor is an instance of a class with certain arrays and methods
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
    
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            
            location = Location(row['id'],row['location_name'], row['location_address'])

            customer = Customer(row['id'], row['customer_name'], row['customer_address'])
            
            animal.location = (location.__dict__)
            animal.customer = (customer.__dict__)
            animals.append(animal.__dict__)

        # Use `json` package to properly serialize list as JSON
        return json.dumps(animals)

# Function with single paramenter
def get_single_animal(id):
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
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            
            FROM animal a
            WHERE a.id= ?
            """, (id, ))
        # passes in the id that will go where the question mark is
        
        data = db_cursor.fetchone()
        
        animal = Animal(data['id'], data['name'], data['breed'],
            data['status'], data['location_id'],
            data['customer_id'])

        return json.dumps(animal.__dict__)

        
# new animal is the body of the post
def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            INSERT INTO Animal
                (name, breed, status, location_id, customer_id)
            VALUES
                ( ?, ?, ?, ?, ?);    
            """, (new_animal['name'], new_animal['breed'], new_animal['status'], new_animal['location_id'], new_animal['customer_id'], ))
        
        id = db_cursor.lastrowid
        
        new_animal['id'] = id
        
    return json.dumps(new_animal)

def delete_animal(id):
    # connect with the database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        #create the cursor object that will help modifying sql data
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            DELETE
            FROM animal
            WHERE id = ?
            """, (id, ))
        
        
        


def update_animal(new_animal, id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            UPDATE Animal
            SET
                name = ?,
                breed=?,
                status = ?,
                location_id = ?,
                customer_id = ?
            WHERE id = ?
                        """, (new_animal["name"], new_animal["breed"], new_animal["status"], new_animal["location_id"], new_animal["customer_id"], id, ))
        rows_affected = db_cursor.rowcount
            
        if rows_affected == 0:
            return False
        else:
            return True
        

            

def get_animals_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            Select
                a.id,
                a.name,
                a.status,
                a.breed,
                a.customer_id,
                a.location_id,
            From animal a
            Where a.location_id = ?
            """,(location_id, ))
        
        animals = []
        database = db_cursor.fetchall()
        
        #  row is a animal, specific dictionary within the database list of dictionaries
        #  all objects in python come from classes, dictionaries do not have default values and are more temporary storage places
        for row in database:
            # creating an object of Animal, row is a dictionary
            animal=Animal(row['id'], row['name'], row['status'], row['breed'], row['customer_id'], row["location_id"])
            
            #  turing animal into a dictionary
            #  python objects and dictionaries are separate things
            animals.append(animal.__dict__)
            
        return json.dumps(animals)
    
    
def get_animals_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            Select
                a.id,
                a.name,
                a.status,
                a.breed,
                a.customer_id,
                a.location_id
            From animal a
            Where a.status = ?
            """,(status, ))
        
        animals = []
        database = db_cursor.fetchall()
        
        #  row is a animal, specific dictionary within the database list of dictionaries
        #  all objects in python come from classes, dictionaries do not have default values and are more temporary storage places
        for row in database:
            # creating an object of Animal, row is a dictionary
            animal=Animal(row['id'], row['name'], row['status'], row['breed'], row['customer_id'], row["location_id"])
            
            #  turing animal into a dictionary
            #  python objects and dictionaries are separate things
            animals.append(animal.__dict__)
            
        return json.dumps(animals)