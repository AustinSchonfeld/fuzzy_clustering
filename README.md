# fuzzy_clustering

*Due to Reddit's 2023 policy changes regarding their API and 3rd party apps, collect.py will no longer work for gathering user submission data*
*The "clustering" branch contains the most up-to-date code, but is not complete. Clustering the data is still a work in progress*

This project was done for the purpose of learning how to perform fuzzy string matching. Data from user submissions such as author, date submitted, and title of the post are gathered.
Then, pulling from the post titles, similar strings such as "dc" and "dc comics" are grouped into clusters. The end goal of this is to find a common string in each cluster to "best" represent the category. 
After comparing each string within a cluster to every other string in the cluster, a "best" category title is determined. 

At this point, the remainder of the code remains a work in progress. Next steps are to compare the "best" cluster titles to one another to determine if a second round of string matching is necessary.
Assuming that each cluster has a unique title, the end goal is then to count how many of the user submissions fall into each of those "best" titles for categories. This will show the most popular categories of recent submissions. 

Ex: Out of the last 5000 posts, the top three most popular categories are...
1) Legend of Zelda with 426 submissions
2) Mario with 359 submissions
3) Pokemon with 289 submissions

Posts that might fall into the "Legend of Zelda" category after fuzzy string matching and clustering might include mispellings, variations of the title, or differences in capitalization:
- Legend of zedla
- Legend of Zelda: Tears of the Kingdom
- legend of zelda wind waker

