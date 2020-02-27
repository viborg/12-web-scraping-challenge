# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request

# import pymongo and the helper function
import pymongo
import scrape_mars as sm

# test connection to the scrape_mars module
print(sm.hello())

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_data_db
collection = db.items

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    # invoke the helper function to scrape
    sm.scrape_mars_data()

    # extract the Mars_data document from Mongo, which is a pymongo cursor (ugh)
    Mars_data_db = db.items.find()

    # convert the pymongo cursor to a python dictionary
    for cursor in Mars_data_db:
        Mars_dict = cursor

    return render_template('Mars_data_report.html', Mars_data=Mars_dict)  # render a template


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
