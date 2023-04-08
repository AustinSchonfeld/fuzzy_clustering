import pandas as pd
import re
from fuzzywuzzy import fuzz, process

data = pd.read_csv("all_submissions.csv")

data = data[['title', 'id', 'author', 'created_utc']]

# Extract the category from each title using a regular expression
data["category"] = data["title"].str.extract(r"\[(.*?)\]")
data['category'] = data['category'].astype(str)

cleaned_categories = []
#Clean the categories so that they have punctuation, numbers, and all whitespace removed. Also make them all lowercase.
for index, category in data['category'].iteritems():
    #remove all characters that are not letters or spaces
    category = re.sub('[^a-zA-Z\s]', '', category)
    #remove whitespace
    category = category.strip()
    #remove numbers
    category = re.sub('[0-9]', '', category)
    #make it all lowercase
    category = category.lower()
    #append to cleaned_categories
    cleaned_categories.append(category)

#drop na values
cleaned_categories = pd.Series(cleaned_categories)

cleaned_categories = cleaned_categories.dropna()

cleaned_categories = list(cleaned_categories)

#categories are cleaned but due to user error there are misspellings and different aliases for categories that should be grouped together (i.e. "dc" and "dc comics")
#use fuzzywuzzy to perform fuzzy string matching
#dictionary to store corrected categories
corrected_categories = {}

#threshold for similarity
threshold = 75

for category in cleaned_categories:
    # find the best match in all_categories
    # best_match, score = process.extractOne(category, cleaned_categories, scorer=fuzz.token_set_ratio)
    
    # # if the score is above the threshold, add to corrected_categories
    # if score >= threshold:
    #     # if the best match already has a corrected category, use that instead
    #     corrected_category = corrected_categories.get(best_match, best_match)
    #     corrected_categories[category] = corrected_category
    # else:
    corrected_categories[category] = category
print(corrected_categories)

#make final df with corrected categories
final_df = pd.DataFrame({'category': [corrected_categories.get(cat, cat) for cat in cleaned_categories]})

# Get the unique categories and their counts
category_counts = final_df['category'].value_counts()

#turn counts into df
counts_df = pd.DataFrame({'category': category_counts.index, 'count': category_counts.values})

#export df to csv for review
counts_df.to_csv('counts.csv', index = False)
