import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

#asks user for CSV file
filename = input ("Input the CSV file: ") 


#converts csv file into a dataframe which is a table of rows and columns
dataframe = pd.read_csv (filename) 

#prints all the columns names as a list
print (dataframe.columns.tolist())

#safeguard -> checks if column inputted is even in the list of all columns, if not, prompted again
while True:
    usertellstransaction = input ("Which column contains transaction amounts? ")
    if usertellstransaction not in dataframe.columns.tolist():
        print ("Column not found. Try again. ")
        continue 

    else:
        print ("Column found!")
        break

    
#removes blank rows from df if any missing values
removeblankrow = dataframe.dropna (axis=0, how='all')

#removes duplicate rows from df
removeduplrow = removeblankrow.drop_duplicates()

#converts the amount column from str to int
removeduplrow [usertellstransaction] = pd.to_numeric (removeduplrow [usertellstransaction], errors='coerce')


#goes through a row, grabs the description from it and categorizes it 
genai.configure (api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

#safeguard for asking user which column contains the transaction description
while True:
    usertellsdescription = input("Which column contains the transaction description? ")

    if usertellsdescription not in dataframe.columns.tolist():
        print ("Column not found. Try again. ")
        continue 

    else:
        print ("Column found! Please wait while your transactions are being categorized...")
        break


#this loop iterates it through the whole df 
for index, row in removeduplrow.iterrows():
    #this is for one singular row
    response = model.generate_content (
        contents=f"Given this transaction description: '{row[usertellsdescription]}', classify it into exactly one of these categories: Food, Transport, Shopping, Entertainment, Bills, Other. Reply with only the category name, nothing else."
    )

    removeduplrow.at [index, "category"] = response.text


#presents the data with categories and the total amount for each (series)
categorytotals = removeduplrow.groupby("category")[usertellstransaction].sum()

#sums the values of the series
total = categorytotals.sum()

print()

#formatting
print ("--- Spending Report ---")

#produces the category and its amount rounded 
for category, amount in categorytotals.items():
    print(category + ": $" + str(round(amount, 2)))

print()

#produces the total of all categories combined
print("Total: $" + str(round(total, 2)))

#provides a bar graph for a visual representation of the cleaned up data
categorytotals.plot (kind='bar')
plt.xticks(rotation=45, ha='right')
plt.title("Spending by Category")
plt.xlabel("Category")
plt.ylabel("Total Spent ($)")
plt.show()













