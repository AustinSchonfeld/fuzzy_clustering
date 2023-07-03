# fuzzy_clustering

*Due to Reddit's 2023 policy changes regarding their API and 3rd party apps, collect.py will no longer work for gathering user submission data*

This project was done for the purpose of learning how to perform fuzzy string matching. Data from user submissions such as author, date submitted, and title of the post are gathered.
Then, pulling from the post titles, similar strings such as "dc" and "dc comics" are grouped into clusters. The end goal of this is to find a common string in each cluster to "best" represent the category. 
After comparing each string within a cluster to every other string in the cluster, a "best" category title is determined.  
