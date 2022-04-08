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
    return CUSTOMERS

def get_single_customer(id):
    requested_customer = None
    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = customer
    
    return requested_customer


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