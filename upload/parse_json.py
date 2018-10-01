#!/usr/bin/env python3

import json
import mysql.connector

# Script that uploads original json file

if __name__ == "__main__":

    # Connect to DB
    mydb = mysql.connector.connect(
        host="206.189.202.2",
        user="root",
        password="some_pass",
        database="nutrition_info"
    )
    mycursor = mydb.cursor()

    # Read JSON and Populate
    inserted_nutrients = set()
    with open('food_data.json') as json_data:
        foods = json.load(json_data)['report']['foods']
        for food in foods:
            # Insert food
            sql = "INSERT INTO foods (ndbno, name, weight, measure) VALUES (%s, %s, %s, %s)"
            val = (food['ndbno'], food['name'], food['weight'], food['measure'])
            mycursor.execute(sql, val)
            for nutrient in food['nutrients']:
                # Insert nutrient if not in Set
                if nutrient['nutrient_id'] not in inserted_nutrients:
                    sql = "INSERT INTO nutrients (nutrient_id, nutrient, unit) VALUES (%s, %s, %s)"
                    val = (nutrient['nutrient_id'], nutrient['nutrient'], nutrient['unit'])
                    mycursor.execute(sql, val)
                    inserted_nutrients.add(nutrient['nutrient_id'])
                    mydb.commit()
                # Handle null values for value and gm
                value = nutrient['value']
                if value == '--':
                    value = None
                gm = nutrient['gm']
                if nutrient['gm'] == '--':
                    gm = None
                # Insert contain relationship
                sql = "INSERT INTO contain (ndbno, nutrient_id, value, gm) VALUES (%s, %s, %s, %s)"
                val = (food['ndbno'], nutrient['nutrient_id'], value, gm)
                mycursor.execute(sql, val)
                mydb.commit()
