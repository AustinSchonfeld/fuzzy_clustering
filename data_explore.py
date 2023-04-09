import pandas as pd
import re
from fuzzywuzzy import fuzz, process
import numpy as np

data = pd.read_csv("all_submissions.csv")

data = data[['title', 'id', 'author', 'created_utc']]

# Extract the category from each title using a regular expression (only works with a particular subreddit with strict rules on title format)
data["category"] = data["title"].str.extract(r"\[(.*?)\]")
data['category'] = data['category'].astype(str)

cleaned_categories = []
#Clean the categories so that they have punctuation, numbers, and all whitespace removed. Also make them all lowercase. This will make fuzzy matching and clustering easier.
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

#drop na values and get a list of unique categories
cleaned_categories = list(filter(None, cleaned_categories))
x = np.array(cleaned_categories)
unique_cats = list(np.unique(x))

#categories are cleaned but due to user error there are misspellings and different aliases for categories that should be grouped together (i.e. "dc" and "dc comics")
#use fuzzywuzzy to perform fuzzy string matching with the help of clustering

# Step 1: Start creating matching clusters using the first available string in the cleaned_categories list, then create a new cluster when there are no more strings above the matching threshhold for the current cluster.
#         Every match above a certain threshhold should be extracted and placed into the cluster, not just the highest matching value.
#         Clusters should be class objects so that they can easily be assigned ID numbers and contain functions for removing/adding strings and recalculating "best" cluster identifiers.
#         Each cluster should be created by iterating through the list of all categories, getting a list of matches above the threshhold for each string in categories, and then initializing a cluster object with that list as an argument.
#         There should also be a counter that increments  
#         Initially there will be strings that exist in multiple clusters. As strings are added to clusters, keep track of which clusters a string belongs to.
#
# set the matching thresshold for fuzzy string matching
threshhold = 75
cluster_list = []
string_assignments = {k:[] for k in unique_cats}
cluster_dict = {}

class Cluster:
    def __init__(self, entry, strings, id):
        self.id = id
        self.label = entry
        self.accuracy = 0
        allowed_matches = []
        all_matches = process.extract(entry, strings, scorer = fuzz.token_set_ratio, limit = None)
        for match in all_matches:
            if match[1] > threshhold:
                allowed_matches.append(match[0])
        self.strings = allowed_matches
        for string in allowed_matches:
            string_assignments[string].append(id)

    # Get the "best" match by looping through each string in the cluster, comparing that string to every other string. Get an average score for each string and pick the one with the highest average.
    def calc_best_name(self):
        best_average = 0
        best_name = ""
        for option in self.strings:
            score_list = process.extract(option, self.strings, scorer = fuzz.ratio, limit = None)
            for selection in score_list:
                scores = []
                scores.append(selection[1])
            for i in scores:
                total =+ i 
            average = total/len(scores)
            if average > best_average:
                best_name = option
                best_average = average
        self.label = best_name
        self.accuracy = best_average

    def calc_single_score(self, string):
        score_list = process.extract(string, self.strings, scorer = fuzz.ratio, limit = None)
        for selection in score_list:
            scores = []
            scores.append(selection[1])
        for i in scores:
            total =+ i 
        average = total/len(scores)
        return average

    def remove_string(self, string):
        self.strings.remove(string)

id_count = 0

for item in unique_cats:
    id_count += 1
    cluster = Cluster(item, unique_cats, id_count)
    cluster.calc_best_name()
    cluster_list.append(cluster)

for cluster in cluster_list:
    cluster_dict[cluster.id] = cluster
#
# Step 2: After all the intial clusters have been created, overlapping strings need to be assigned to just one cluster based on an average Levenshtein distance. Begin looping through strings with more than one cluster. 
# 
# Step 3: Where a suspect string exists in multiple clusters, calcuate the average match score for each cluster using the suspect string. Leave the string in the highest scoring cluster and remove the string from all others. 
#       

for string in unique_cats:
    cluster_scores = {}
    if len(string_assignments[string]) > 1:
        suspect_clusters = string_assignments[string]
        for id in suspect_clusters:
            cluster_scores[id] = cluster_dict[id].calc_single_score(string)
        highest = max(cluster_scores, key = cluster_scores.get)
        suspect_clusters.remove(highest)
        string_assignments[string] = highest
        for cluster in suspect_clusters:
            # for value in string_assignments.values():
            #     value.remove(cluster)
            cluster_list.remove(cluster_dict[cluster])
            del cluster
            
#
# Step 4: After re-calculating the best name for each cluster there will still be clusters that should be combined. Compare the labels of each cluster and combine similar clusters.
#         
for cluster in cluster_list:
    print(cluster.label)

    
#
# Step 5: There should now be no strings that exist in multiple clusters. Each cluster should have a single identifier that "best" represents its contents. Extract those identifiers, get value counts, and export to csv. 

# ****************ORIGINAL CODE BLOCK FOR STRING MATCHING WHICH ESSENTIALLY COMPARES A STRING TO ITSELF, WHICH DOESNT WORK***************************
# corrected_categories = {}

# #threshold for similarity
# threshold = 75

# for category in cleaned_categories:
#     # find the best match in all_categories
#     # best_match, score = process.extractOne(category, cleaned_categories, scorer=fuzz.token_set_ratio)
    
#     # # if the score is above the threshold, add to corrected_categories
#     # if score >= threshold:
#     #     # if the best match already has a corrected category, use that instead
#     #     corrected_category = corrected_categories.get(best_match, best_match)
#     #     corrected_categories[category] = corrected_category
#     # else:
#     corrected_categories[category] = category
# print(corrected_categories)
# make final df with corrected categories
# final_df = pd.DataFrame({'category': [corrected_categories.get(cat, cat) for cat in cleaned_categories]})
# ***************************************************************************************************************************************************


# # Get the unique categories and their counts
# category_counts = final_df['category'].value_counts()

# #turn counts into df
# counts_df = pd.DataFrame({'category': category_counts.index, 'count': category_counts.values})

# #export df to csv for review
# counts_df.to_csv('counts.csv', index = False)
