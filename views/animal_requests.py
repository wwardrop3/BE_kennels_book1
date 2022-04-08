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
    # this function returns all the animals in the list
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
            

