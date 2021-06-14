# -----------------------------------------------------------------------------
# File : DataCreation.py
# Author :
# Date :
# Purpose : Read raw input and create a cloudant db
# ------------------------------------------------------------------------------


from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey
import json
import time

in_file_path = "C:/Users/Shubhi_Tiwari/Documents/Downloads/HacakthonWit/data/Recipes.json"

in_file = open(in_file_path, 'r')
in_data = json.load(in_file)

serviceUsername = "apikey-v2-1hwi0xckzpyno4jtrpm3e6jjf5g9bm3qg8h0q1qrh77h"
servicePassword = "48e8957ee820970b81782957545371cd"
serviceURL = "https://apikey-v2-1hwi0xckzpyno4jtrpm3e6jjf5g9bm3qg8h0q1qrh77h:48e8957ee820970b81782957545371cd@708250c4-cfae-4fff-b9e9-654450538ddc-bluemix.cloudantnosqldb.appdomain.cloud"

print("before connecting")
# Establish a connection to the service instance.
client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

print("connected")

databaseName = "recipedata"

# # db creation
# recipeDb = client.create_database(databaseName)
#
# # Verify that the database was created successfully
# if recipeDb.exists():
#     print("'{0}' successfully created.\n".format(databaseName))
# open db
recipeDb = client[databaseName]



num = 0
count = 0
for key, value in in_data.items():
    if 'name' in value:
        name = value['name']
        if 'ingredients' in value and 'steps' in value:
            ingredients = value['ingredients']
            steps = value['steps']
            if ' Total Time' in value:
                total_time = value[' Total Time']
            else:
                total_time = ''

            if ' Prep Time' in value:
                prep_time = value[' Prep Time']
            else:
                prep_time = ''

            if ' Cook Time' in value:
                cook_time = value[' Cook Time']
            else:
                cook_time = ''

            if ' Servings' in value:
                servings = value[' Servings']
            else:
                servings = ''

            if ' Course' in value:
                course = value[' Course']
            else:
                course = ''

            if ' Cuisine' in value:
                cuisine = value[' Cuisine']
            else:
                cuisine = ''
            num = num + 1
        else:
            continue
    else:
        continue
    #    Create a JSON document that represents all the data in the row.
    jsonDocument = {
        "num": num,
        "name": name,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "total_time": total_time,
        "servings": servings,
        "course": course,
        "cuisine": cuisine,
        "ingredients": ingredients,
        "steps": steps
    }
    print(jsonDocument)
    # Create a document by using the Database API.
    newDocument = recipeDb.create_document(jsonDocument)
    count = count+1
    # Check that the document exists in the database.
    # if newDocument.exists():
    #     print("Document '{0}' successfully created.".format(num))
    if count == 10:
        time.sleep(2)
        count = 0


# closing connection
client.disconnect()