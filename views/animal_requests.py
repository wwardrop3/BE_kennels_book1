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
    """_summary_"""
    return ANIMALS


# Function with single paramenter
def get_single_animal(id):
    # definine the requested animal and set value to None
    requested_animal = None
    
    # iterate through Animals array above
    for animal in ANIMALS:
        # checks the id parameter against every animal id property and will set the requested animal object if the id matches
        if animal ["id"]  == id:
            requested_animal = animal
    
    return requested_animal


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