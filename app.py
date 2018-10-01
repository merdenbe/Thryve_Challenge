from flask import Flask, render_template, request
import json
import mysql.connector
import os
app = Flask(__name__)

mydb = mysql.connector.connect(
    host="206.189.202.2",
    user="root",
    password="some_pass",
    database="nutrition_info"
)

@app.route("/")
@app.route("/foods")
def hello():
    return render_template('index.html')

@app.route('/getTable')
def getTable():
    response = {}
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM foods", ()) # returns all food entries in foods table
    row_headers=[x[0] for x in mycursor.description]
    result = mycursor.fetchall()
    json_data = []
    for result in result:
        json_data.append(dict(zip(row_headers,result)))
    response['data'] = json_data
    return json.dumps(response)

@app.route('/constrainTable')
def constrainTable():
    response = {}
    json_data = []
    mycursor = mydb.cursor()
    constraints = json.loads(request.args.get('constraints'))
    sql = """SELECT DISTINCT foods.ndbno, foods.name, foods.weight, foods.measure FROM foods, contain WHERE nutrient_id = %s AND value >= %s AND value <= %s AND foods.ndbno = contain.ndbno"""
    # Executes query on each set of constraints building bag of foods (with duplicates)
    for constraint in constraints:
        val = (constraint[0], constraint[1], constraint[2])
        mycursor.execute(sql, val)
        row_headers=[x[0] for x in mycursor.description]
        result = mycursor.fetchall()
        print(len(result))
        for result in result:
            json_data.append(dict(zip(row_headers,result)))
    # Converts bag to set (no duplicates)
    json_set = list({row['ndbno']:row for row in json_data}.values())
    response['data'] = json_set
    return json.dumps(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
