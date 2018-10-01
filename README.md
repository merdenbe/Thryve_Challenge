Food Nutrition API

Backend: Python/Flask

Frontend: HTML/CSS/Javascript with Bootstrap and Datatables API

Problem: Allow user to search for foods based on nutritional constraints

Approach: I set up a mysql database on a DigitalOcean server. I then wrote a
python script to upload the original json file to the database according to my
schema. Next, I implemented a simple Frontend that uses a Bootstrap template for
styling and the Datatables API for a better display of data. The backend is
performing queries on the database based on the constraints and returning the
information on each food that abides by the constraints.

Use:
  1. Select nutrient from dropdown
  2. Add upper and lower bounds for amount of that nutrient
  3. Click "Add Constraint" to constrict the foods table below
  4. Continue to add constraints using step 3
  5. At any time, click "Clear Constraints" to begin a new search
