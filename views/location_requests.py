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

def get_all_locations ():
    return LOCATIONS

def get_single_location (id):
    requested_location = None
    for location in LOCATIONS:
        if id == location ["id"]:
            requested_location=location

    return requested_location


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