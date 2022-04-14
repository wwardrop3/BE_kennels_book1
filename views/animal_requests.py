import sqlite3
import json
from models import Animal

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
                a.customer_id
            FROM animal a
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

        

def create_animal(animal):
    # gets the id value of the last object in the list
    max_id = ANIMALS[-1]["id"]
    
    # creates a new unique id for the object we are going to add
    new_id = max_id + 1
    
    #sets the id of the new animal dictionary to the new unique id
    animal["id"] = new_id
    
    #adds the animal dictionary to the list
    ANIMALS.append(animal)
    
    #return the new dictionary that was added to the list
    return animal

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
                location_id = ?
                customer_id = ?
            WHERE id = ?
                        """, (new_animal["name"], new_animal["breed"], new_animal["status"], new_animal["location_id"], new_animal["customer_id"], id, ))
        rows_affected = db_cursor.rowcount
            
        if rows_affected == 0 #no rows affected means that it did not find anything to update and a 404 code
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
                a.location_id
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