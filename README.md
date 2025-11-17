# Data-Intensive-Scalable-Systems-Project-Analysis-of-Amazon-Electronics-Reviews
 The goal here is twofold. First, to build a cloud-based data pipeline that can take in, process, and analyze large collections of customer reviews. And second, to use that pipeline on a real-world dataset — the Amazon Electronics reviews — to find patterns and insights in how people talk about products. 

To focus the analysis, I came up with a few main questions:
What does the distribution of customer ratings look like for electronics, and what can that tell us about overall customer sentiment?

Is there any relationship between how long a review is and how helpful other users find it?

Do the short review titles (summaries) relate in any way to the star ratings customers give?

By answering these questions, this project not only looks at online consumer habits but also shows how modern cloud tools can be used to tackle and make sense of huge, messy datasets. This report walks through the entire process — starting with a look at related research, then diving into how the system was built, followed by a discussion of the results, what they mean, and where things could go from here.

To tackle my research questions, I followed a quantitative approach centered on analyzing existing data through statistical methods.

My methodology revolved around using a massive, publicly available dataset and processing it through a custom-designed cloud-based pipeline. This approach wasn’t just a preference — it was necessary. The scale of the data was far beyond what a single machine could handle, so I needed a distributed, scalable setup to manage it efficiently.
The dataset I used was the “Electronics_5.json” file from the Amazon product review archive, which has become a standard in academic studies. This particular subset contains millions of verified customer reviews. Each review is tied to a confirmed purchase, adding an extra layer of reliability to the data. One of the key features of this dataset is that it’s been pre-filtered — it only includes users and products that have at least five reviews. This filtering step helps reduce noise from one-off reviewers and gives the analysis a more stable and consistent base.
Each review in the JSON file includes a range of details, but for this project, I narrowed my focus to a few important fields:
overall: The star rating, ranging from 1.0 to 5.0. I used this as my main indicator of sentiment.

helpful: A two-element array that shows how many users found the review helpful versus the total number of votes (e.g., [4, 5]). This served as my measure of a review’s perceived usefulness.
reviewText: The full written review. I used this field to calculate the length of each review.

summary: The short title of the review. I also measured the length of this text to look for possible patterns.

Since the data came in a semi-structured JSON format, parsing and analyzing it required a well-planned strategy. The size of the file made it a perfect candidate to test out the power and scalability of cloud-based big data tools — exactly the kind of challenge this project was designed to take on.

The implementation of my project followed a clear, step-by-step data processing pipeline, which I executed using PySpark scripts inside a Synapse Notebook. Each stage played a specific role in moving the data from raw form to meaningful insights.
Data Ingestion

The process began with a simple manual step: I uploaded the Electronics_5.json file into a container on Azure Blob Storage. This became the single, centralized source of raw data for the entire project.
Data Loading and Schema Definition

Using PySpark, I loaded the JSON file directly from Blob Storage into a Spark DataFrame. Although Spark is great at automatically detecting schemas from JSON, I wanted more control and reliability — so I explicitly defined the schema for the key columns I’d be working with. This helped catch any inconsistencies and ensured smoother processing later on.

Data Caching

Since Spark operations are lazy by default, re-reading the large JSON file repeatedly would have made things painfully slow. So, to improve performance — especially during the exploratory phase — I cached the main DataFrame in memory. This simple step made a huge difference in speed and responsiveness during development and testing.

Analytical Computations

This was the heart of the pipeline — where I actually crunched the numbers to answer my research questions:

Rating Distribution: I used a basic groupBy('overall') followed by a count() to calculate how many reviews fell under each star rating.

Helpfulness vs. Review Length: I engineered two new features here. First, I added a review_length column by calculating the number of characters in the reviewText. Then I computed a helpfulness_score based on the values in the helpful array. I grouped the data by star rating and calculated the average review length and helpfulness score for each group.

Review Summary Length: Using the same approach, I created a summary_length column and calculated its average, grouped by star rating. This helped me explore whether shorter or longer summaries correlated with the final rating.

Result Storage

Once the computations were complete, I wrote the final, cleaned, and aggregated DataFrames to an Azure SQL Database. I used Spark’s built-in JDBC connector to do this. To keep things clean and consistent, I set the write operation to overwrite any existing tables. That way, I could re-run the whole pipeline without worrying about duplicate entries or messy data — everything stayed reproducible and easy to manage.

Overall, this pipeline let me break down the complex dataset into manageable parts and process them in a modular, scalable way. Each stage fed clean, structured data into the next, making it easy to analyze the results and draw meaningful conclusions.

In summary, my key findings were:

There is a pronounced J-shaped distribution in ratings, with a strong bias towards positive reviews.
The perceived helpfulness of a review is highest for critical (1-star) and balanced (3-star) feedback, suggesting users value reviews that help them assess risk and nuance.
Review length is greatest for mid-range ratings, indicating that users with mixed opinions tend to provide more detailed explanations.
These findings contribute to our understanding of online consumer behavior and reaffirm the value of applying big data technologies to analyze it at scale. The project also serves as a practical demonstration of a modern data engineering pipeline.
However, this research is just a starting point. The limitations I discussed open up several meaningful avenues for future work. A clear next step would be to move beyond metadata and integrate Natural Language Processing. Performing sentiment analysis on the review text itself could validate the star ratings and even detect sarcasm or nuanced emotions. Aspect-based sentiment analysis could further identify which specific product features (e.g., "battery life," "screen quality") are driving positive or negative opinions.
Another promising direction would be to develop a predictive model for review helpfulness. This model could use a richer set of features, including textual metrics (like readability scores), sentiment scores, and reviewer metadata (like their review history), to build a more sophisticated and accurate predictor than simple correlations.
Finally, the scope of the analysis could be expanded. A cross-category comparison would be fascinating to see if the patterns observed in electronics hold true for other domains like clothing or home goods. A temporal analysis could also be performed to see how review patterns and helpfulness perceptions evolve over a product's lifecycle. Such extensions would build directly upon the foundation laid by this project, leading to a deeper and more holistic understanding of the complex world of online reviews.
