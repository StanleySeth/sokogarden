#Flask is a lightweight web framework used to build web applications and APIs using Python.
#It allows us to:
                 #Create web routes
                 #Handle HTTP requests (GET, POST)
                 #Send responses (JSON, HTML, etc.)

                 #Work with forms and APIs
#Import flask and its components

from flask import *
#Import the operating system module
import os
#Import the pymysql module -> it helps us to create a connection between python flask and mysql database
import pymysql 

#Create a fask application and give it a name
app = Flask(__name__)

#Configure the location to where your product images will be saved on your application 
app.config["UPLOAD_FOLDER"] = "static/images"

#Below is a sign up route
@app.route("/api/signup", methods = ["POST"])
def signup():
    #This function is executed wheneever a POST request is sent to /api/signup.
    if request.method == "POST":
        #Extract the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        #by use of the print function lets print all these details with the upcoming request
        #print(username, email, password, phone)
        #Establish a connection between flask/python and my sql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        #Create a cursor to execute the sql queries
        #Cursor -> An object used to execute SQL queries
        cursor = connection.cursor()

        #Structure an sql to insert the details received from the form
        #The %s is a place holder -> It stands in plac of actual values
        sql = "INSERT INTO product_details(username, email, password, phone) VALUES (%s, %s, %s, %s)"

        #Create a tuple that will hold all the data gotten from the form
        data = (username, email, password, phone)

        #by use of the cursor, execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        #commit the changes to the database
        connection.commit()


        return jsonify({"message" : "User registered successfully"})





#Below is the login/sign in Route
@app.route("/api/signin", methods =["POST"])
def signin():
    if request.method == "POST":
        #Extract the two details entered on the form
        email = request.form["email"]
        password = request.form["password"]
     #print the two details entered on the form
     #print(email, password)
     #Create/establish a connection to the database
    connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

    #Create a cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    #Sructure the SQL query that will check whether the email and the password entered are correct
    sql = "SELECT * FROM users WHERE email = %s AND password = %s"

    #Put the data received from the form into a tuple
    data = (email, password)

    #By use of the cursor execute the sql
    cursor.execute(sql, data)

    #Check whether there are rows and store the same on a variable
    count = cursor.rowcount

    #If there are records returned it means the password and the email are correct otherwise it means they are wrong
    if count == 0:
        return jsonify({"message":"Login Failed"})
    else:
        #There must be a user so we create a variable that will hold all the details fetched from the database
        user=cursor.fetchone()
        #Return the details to the frontend as well as a message
        return jsonify({"message":"user Logged in Successfully",  "user":user})


    return jsonify({"message" : "signin Route Accessed"})


#Below is the route for adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        #Extract the data entered on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        #For the product photo, we shall fetch it from files as shown below
        product_photo = request.files["product_photo"]

        #Extract the file name of the product photo to the vrible filename
        filename = product_photo.filename

        #By use of the os module we can extract the file path where the image is currently saved
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        #Sve the product photo image into the new location
        product_photo.save(photo_path)

        #Print them out to test whether you are receiving the details sent with the request.
        #print(product_name, product_description, product_cost, product_photo) 
        #Establish a connection to other db
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        #Create a cursor
        cursor = connection.cursor()

        #Structure the sql query to insert the product details to the database
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

        #Create a tuple that will hold the data from the form which are current held onto the different vriable declred.
        data = (product_name, product_description, product_cost, filename)

        #Use the cursor to execute the sql as you replce the placeholders with the actual data.
        cursor.execute(sql, data)

        #Commit the changes to the database
        connection.commit()



        return jsonify({"message": "Product added successfully"}) 



#Below is the route for fetching products
@app.route("/api/get_products")
def get_products():
    #Create a connection to the database
    connection=pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")
    #Create a cursor
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    #Structure the query to fetch all the products from the table product_details
    sql = "SELECT * FROM product_details"

    #Execute the query
    cursor.execute(sql)   
    #Create a variable that holds the data fetched from the table
    products = cursor.fetchall()        

    
    return jsonify(products) 

#Run the application
app.run(debug=True)