
from http.server import BaseHTTPRequestHandler, HTTPServer
# from multiprocessing.sharedctypes import Value
from views.animal_requests import delete_animal, get_all_animals, get_single_animal, create_animal, update_animal
from views.customer_requests import create_customer, delete_customer, get_all_customers, get_single_customer, update_customer
from views.employee_requests import create_employee, delete_employee, get_all_employees, get_single_employee, update_employee
from views.location_requests import delete_location, get_all_locations, get_single_location, create_location, update_location
import json




# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


# class is the blueprint for an object...self is a reference to the class itself...self is "my " pronoun...makes instance first then passes instance into the class to attach the properties
# init creates empty object, then calls its own init method, passes the object into init method to attach properties to it

# this is a unique request handler
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
        # this is building up the response to the request
        self._set_headers(201)
        
        # creating a variable of a number of bytes 
        # headers are the meta data to the body text that we are sending
        # the second argument 0 is a fallback that avoids breaking the server
        content_len = int(self.headers.get('content-length', 0))
        
        # we need to know the byte length because it tells rfile when to turn itself off and stop reading, NEED TO TELL RFILE TO STOP AFTER THE BYTES
        # telling rfile how far to read
        post_body = self.rfile.read(content_len)
        print(post_body)
        post_body = json.loads(post_body)
        
        # tuple unpacking
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
            
        if resource == "customers":
            new_customer = create_customer(post_body)
            
            self.wfile.write(f"{new_customer}".encode())
        
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            
        elif resource == "customers":
            delete_customer(id)
            
        elif resource == "employees":
            delete_employee(id)
            
        elif resource == "locations":
            delete_location(id)
            

        # Encode the new animal and send in response
        self.wfile.write("".encode())
        
        
    #this method is going to override the parent's method.  Handles modifying PUT requests
    def do_PUT(self):
        """Handles PUT requests to the server
        """
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        # This overwrites the post body with the returned json formatted data
        post_body = json.loads(post_body)
        
        # then we need to parse the url request
        (resource, id) = self.parse_url(self.path)
        print(resource)
        # pass in the id from the request to the function that modifies the array
        if resource == "animals":
            update_animal(post_body, id)
            
        elif resource == "employees":
            update_employee(post_body, id)
            
        elif resource == "locations":
            update_location(post_body, id)
        
        elif resource == "employees":
            update_customer(post_body, id)
        
        
        
        # empty string because we dont send anything back
        self.wfile.write("".encode())

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
        
        
        # this sends a response back to the client, it is WRITING THE MESSAGE BACK TO SENDER (this is a get so its ht epurpose)
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
    # this is where the external server address would go
    host = ''
    # a host can have multiple things, so the 8088 is the apartment unit of the building
    port = 8088
    # port is basically the event listener, where the httpserver is listening for changes
    #inside http server will instantiate the new handle requests object
    HTTPServer((host, port), HandleRequests).serve_forever() 
    # it will only make 1 instance of handle requests at the outset before an actual request is made


if __name__ == "__main__":
    main()
    