# frontend/__init__.py
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

FASTAPI_URL = "http://127.0.0.1:8000/save_input"

@app.route("/")
def index():
    return render_template("index.html")

# this is a bit like the routes file in rails
#  add a route to confirm the submission

@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.form.get("user_input")

    #  send data to fastapi
    response = requests.post(FASTAPI_URL, json={"user_input": user_input})

    if response.status_code == 200:
        # Extract user_id from the FastAPI response
        fastapi_response = response.json()
        user_id = fastapi_response.get("user_id", None)

        if user_id is not None:
            return f"Congratulations {user_input} (User ID: {user_id}) - it worked"
        else:
            return f"Failed to retrieve User ID from FastAPI response"
    else:
        return f"Failed to submit data to FastAPI. Status code: {response.status_code}"