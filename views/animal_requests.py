import sqlite3
import json
from models import Animal


ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4
    },
    {
        "id": 2,
        "name": "Gypsy",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1
    }
]



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
    animal_index = -1
    
    # this is finding the animal id of the one that is passed in and then getting the index of the matching id object
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            animal_index = index
    
    if animal_index >=0:
        ANIMALS.pop(animal_index)
    

def update_animal(post_body, id):
    animal_index = -1
    for index, animal in enumerate(ANIMALS):
        if id == animal["id"]:
            animal_index = index
    
    ANIMALS[animal_index]["status"] = post_body
    
    return ANIMALS[animal_index]
            

