
from http.server import BaseHTTPRequestHandler, HTTPServer
# from multiprocessing.sharedctypes import Value
from views.animal_requests import delete_animal, get_all_animals, get_animals_by_location, get_animals_by_status, get_single_animal, create_animal, update_animal
from views.customer_requests import create_customer, delete_customer, get_all_customers, get_customers_by_email, get_single_customer, update_customer
from views.employee_requests import create_employee, delete_employee, get_all_employees, get_employees_by_location, get_single_employee, update_employee
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
    # tv guide of the API
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
        # telling rfile (read file) how far to read
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        
        # tuple unpacking
        (resource, id) =  self.parse_url(self.path) # animals/3
        new_animal = None
        
        
        if resource =="animals":
            # new animal is the new object created from the create animal method that will use the Animal class to create a new object
            new_animal = create_animal(post_body)
            
            self.wfile.write(f"{new_animal}".encode())
        
        if resource == "locations":
            new_loaction = create_location(post_body)
            
            self.wfile.write(f"{new_loaction}".encode())
        
        if resource == "employees":
            new_employee = create_employee(post_body)
            
            self.wfile.write(f"{new_employee}".encode())
            
        if resource == "customers":
            new_customer = create_customer(post_body)
            
            self.wfile.write(f"{new_customer}".encode())
        
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    # self contains a path that includes the id we are going to delete
    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

        # extracts the information contained in the url
        parsed = self.parse_url(self.path)
        
        print(parsed)
        if len(parsed) == 2:
            print("asdfsd")
            (resource, id) = parsed
            if resource == "animals":
                delete_animal(id)
                
            
            
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
        # pass in the id from the request to the function that modifies the array
        
        success = False
        
        if resource == "animals":
            success = update_animal(post_body, id)
            
        elif resource == "employees":
            update_employee(post_body, id)
            
        elif resource == "locations":
            update_location(post_body, id)
        
        elif resource == "employees":
            update_customer(post_body, id)
        
        
        if success:
            self._set_headers(200)
        else:
            self._set_headers(404)
            
        # empty string because we dont send anything back
        self.wfile.write("".encode())

# Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)
        
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        
        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed
  

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
                    
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
                    
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
                
            elif key =="location_id" and resource =="animals":
                
                # this results as a json string
                response = get_animals_by_location(value)
                
            elif key =="location_id" and resource =="employees":
                print(key)
                
                # this results as a json string
                response = get_employees_by_location(value)
                
                
            elif key =="status" and resource =="animals":
                print(key)
                
                # this results as a json string
                response = get_animals_by_status(value)

        # this sends back the encoded response to the client
        self.wfile.write(response.encode())
        
        
        
# ALL OF THESE METHODS ARE JUST TAILORED TOOLS FOR THIS CLASS. PARSE URL IS A SMALL HELPER THAT EXTRACTS WHAT WE NEED TO IN ANOTHER PART OF THE CLASS
    #path is everything after it
    def parse_url(self, path):
        # splits the /animals/1 path into (None, animals, ) tuple
        path_params = path.split("/")
        resource = path_params[1]

        
        # ****this is taking the url from the client and breaking it up so we can use it to target SQL database
        
        # check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com
            param = resource.split("?")[0]# customers
            resource = resource.split("?")[1]# 'email=jenna@solis.com'
            pair = resource.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]
            value = pair[1]
            
            return (param, key, value)
        
        else:
            id = None
            
            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

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


# this protects the file from being called elsewhere
if __name__ == "__main__":
    main()
    