from flask import Flask, flash
from flask_cors import CORS
from utils import make_celery

# Create Flask App Instance
app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

# Enable CORS
CORS(app)


# Create Celery Instance w/ .Task 
celery = make_celery(app)

# Function to be run asynchronously
@celery.task
def my_function():
    with app.app_context():
        print("Task run")
  

# Endpoint that uses Asynchronous function
@app.route('/', methods=['POST'])
def index():
    # This function will run in the background
    my_function.delay()
    flash("Message scheduled")
    # This response will be sent almost instantaneously
    return "Message sent"

if __name__ == '__main__':
    app.run(debug=True)
