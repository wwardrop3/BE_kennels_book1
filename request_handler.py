
from http.server import BaseHTTPRequestHandler, HTTPServer
# from multiprocessing.sharedctypes import Value
from views.animal_requests import get_all_animals, get_single_animal, create_animal
from views.customer_requests import get_all_customers, get_single_customer
from views.employee_requests import create_employee, get_all_employees, get_single_employee
from views.location_resquests import get_all_locations, get_single_location, create_location
import json



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.



class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        
        #sets the response code to send when this is run (201 means successfully written)
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        post_body = json.loads(post_body)
        
        (resource, id) =  self.parse_url(self.path)
        
        new_animal = None
        
        
        if resource =="animals":
            new_animal = create_animal(post_body)
            
            self.wfile.write(f"{new_animal}".encode())
        
        if resource == "locations":
            new_loaction = create_location(post_body)
            
            self.wfile.write(f"{new_loaction}". encode())
        
        if resource == "employees":
            new_employee = create_employee(post_body)
            
            self.wfile.write(f"{new_employee}".encode())
        
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server
        """
        self.do_POST()

# Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)
        # set response to empty dictionary
        response = {}
        
        # self.path is /animal/# or /animal then sets resource and id to
        (resource, id) = self.parse_url(self.path)
        
        if resource == "animals":
            if id is not None:
                response = f"{get_single_animal(id)}"
            else:
                response = f"{get_all_animals()}"
                
        if resource == "locations":
            if id is not None:
                response = f"{get_single_location(id)}"
            else:
                response = f"{get_all_locations()}"
                
        if resource == "employees":
            if id is not None:
                response = f"{get_single_employee(id)}"
            else:
                response = f"{get_all_employees()}"
                
        if resource == "customers":
            if id is not None:
                response = f"{get_single_customer(id)}"
            else:
                response = f"{get_all_customers()}"
        
        
        # this sends a response back to the client
        self.wfile.write(response.encode())
        
        
# ALL OF THESE METHODS ARE JUST TAILORED TOOLS FOR THIS CLASS. PARSE URL IS A SMALL HELPER THAT EXTRACTS WHAT WE NEED TO IN ANOTHER PART OF THE CLASS
    #path is everything after it
    def parse_url(self, path):
        # splits the /animals/1 path into (None, animals, 1) tuple
        path_params = path.split("/")
        resource = path_params[1]
        id = None
        
        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass
        
        return (resource, id)

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()
    print("asdf")


if __name__ == "__main__":
    main()
    