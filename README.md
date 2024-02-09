Prototype app using flask for the frontend and FastAPI for the backend

How to setup:

Frontend
* in the root directory run
*  `python3 -m venv venv`
* `source venv/bin/activate`
* cd frontend
* `pip install -r requirements.txt`
* `cd ..` # to return to the root directory
* set env_var by running `export FLASK_APP=frontend`
* `flask run`
* visit `http://localhost:5000/` in a browser

Backend
Open a new terminal window
* in the root directory run:
* `source venv/bin/activate`
* `cd backend`
* `pip install requirements.txt`
* `cd ..` # to return to the root directory
* `uvicorn backend.fast_api_refer:app --reload`
* visit `http://localhost:8000/` in a browser

To try the service you can enter a string in the flask front end and submit, it will return a success message which includes a USERID

Go to `http://localhost:8000/get_data/{USERID}`
And you should see the name you entered

Things I am not sure of:
Database migrations - 
I had to run:
`alembic revision --autogenerate -m "initial"`
and then
`alembic upgrade head`
You may also need to do this to get the SQLALCHEMY DB running for this to work. If so these are run in the root directory.

