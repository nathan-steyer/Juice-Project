# Juice-Project
[Check it out on Heroku](https://juicy-juice-juices.herokuapp.com/)

To run the app locally:
  + Use `pip install -r requirements.txt` to install modules
  + Use `set FLASK_APP=server.py` (Windows) or `export FLASK_APP=server.py` (Unix)
  + Use `flask run` to start the server
  + Open a browser and go to http://localhost:5000/ to view the web page

At /total, the server will return the total number of Juicy Juice products in JSON format
At /average, the server will return the average calories per fluid ounce of Juicy Juice products in JSON format
