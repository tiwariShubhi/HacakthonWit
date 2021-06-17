# -----------------------------------------------------------------------------
# File : ParserEngine.py
# Author :
# Date :
# Purpose : Fetch data from db on basis of a query
# ------------------------------------------------------------------------------

from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey
from cloudant.query import Query
from cloudant.query import QueryResult
import time


# Global Data

# -------------------------------------------------------------------------------
# To find all recipes, primary and secondary ing.  in db
# in: recipe database object
# out : primary and secondary ing. as set()
# --------------------------------------------------------------------------------
def find_all_recipes(recipeDb):
    primary = set()
    secondary = set()
    count = 0
    result_collection = Result(recipeDb.all_docs, include_docs=True)
    for recipe in result_collection:
        #print(recipe["doc"]["primary_ingredients"])

        for ingredient in recipe["doc"]["primary_ingredients"]:
            primary.add(ingredient)

        for ingredient in recipe["doc"]["secondary_ingredients"]:
            secondary.add(ingredient)

        count += 1
        if count > 400 :
            time.sleep(1)
            count = 0

    return primary,secondary


# -------------------------------------------------------------------------------
# To find all recipes in db
# in:
# out :
# --------------------------------------------------------------------------------
def search_by_primary_ingredients(recipeDb,primary_ingredients):
    result_collection = Result(recipeDb.all_docs, include_docs=True)
    timer=0
    final_recipe = []
    for recipe in result_collection:
        count =0
        for ing in primary_ingredients:
            if ing in recipe['doc']['primary_ingredients']:
                count+=1
        if count>0:
            recipe['doc']['score']=count
            recipe['score']=count
            final_recipe.append(recipe)
        timer+= 1
        if timer> 400:
            time.sleep(1)
            timer= 0
    final_recipe = sorted(final_recipe, key = lambda i: i['score'],reverse=True)
    return final_recipe





recipeDb = ''


serviceUsername = "apikey-v2-1hwi0xckzpyno4jtrpm3e6jjf5g9bm3qg8h0q1qrh77h"
servicePassword = "48e8957ee820970b81782957545371cd"
serviceURL = "https://apikey-v2-1hwi0xckzpyno4jtrpm3e6jjf5g9bm3qg8h0q1qrh77h:48e8957ee820970b81782957545371cd@708250c4-cfae-4fff-b9e9-654450538ddc-bluemix.cloudantnosqldb.appdomain.cloud"

print("before connecting")
# Establish a connection to the service instance.
client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

print("connected")

databaseName = "recipedata2"
# open db
recipeDb = client[databaseName]

#primary, secondary = find_all_recipes(recipeDb)

primary_ing = ['curd','milk']
res = search_by_primary_ingredients(recipeDb,primary_ing)
print(res)
print(len(res))
client.disconnect()
