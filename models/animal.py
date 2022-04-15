class Animal():
    # this is a constructor method ON INITIALIZATION
    def __init__(self, id, name, breed, status, customer_id, location_id):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.customer_id = customer_id
        self.location_id = location_id
        self.location = None
        self.customer = None
        
        
    