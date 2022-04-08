


EMPLOYEES = [
    {
        "id":1,
        "name":"Carl"
    },
    {
        "id":2,
        "name":"John"
    },
    {
        "id":3,
        "name":"Steve"
    },
    {
        "id":4,
        "name":"Bill"
    }
]

def get_all_employees():
    return EMPLOYEES

def get_single_employee(id):
    requested_employee=None
    for employee in EMPLOYEES:
        if id == employee ["id"]:
            requested_employee = employee
    
    return requested_employee


# this takes an existing employee and simply adds a unique id to it
def create_employee(employee):
    # first get the last id of the existing list
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    
    employee["id"] = new_id
    
    EMPLOYEES.append(employee)
    
    return employee