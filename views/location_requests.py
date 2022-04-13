import sqlite3
import json
from models import Location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
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
                a.address
            FROM location a
        """)

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        
        # a cursor is an instance of a class with certain arrays and methods
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
    
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # location class above.
            location = location(row['id'], row['name'], row['address'])

            locations.append(location.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(locations)

# Function with single paramenter
def get_single_location(id):
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
                a.address
            
            FROM location a
            WHERE a.id= ?
            """, (id, ))
        # passes in the id that will go where the question mark is
        
        data = db_cursor.fetchone()
        
        location = Location(data['id'], data['name'], data['address'])

        return json.dumps(location.__dict__)


# this function is going to be run when we post a new location to the database.  Takes in the new dictionary, POSTS, and returns the new dictionary
def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    
    new_id = max_id + 1
    
    location["id"] = new_id
    
    LOCATIONS.append(location)
    
    return location

def delete_location(id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
            LOCATIONS.pop(location_index)
            
            
def update_location(post_body, id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
            
    LOCATIONS[location_index]["status"] = post_body