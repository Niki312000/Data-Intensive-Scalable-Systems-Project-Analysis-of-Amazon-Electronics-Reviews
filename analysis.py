import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns

conn_str = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:diss-sql-server.database.windows.net,1433;Database=ProjectResultsDB;Uid=webserver;Pwd=asdfgh@#12345;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


try:
    db_connection = pyodbc.connect(conn_str)
    print("Successfully connected to Azure SQL Database.")
except Exception as e:
    print(f"Failed to connect to database. Error: {e}")
    exit()

# Query and Visualize Analysis 1: Rating Distribution
print("\nVisualizing Analysis 1...")
sql_query_1 = "SELECT * FROM dbo.Analysis1_RatingDistribution;"
df1 = pd.read_sql(sql_query_1, db_connection)
print(df1.head())

plt.figure(figsize=(10, 6))
sns.barplot(x='overall', y='ReviewCount', data=df1, palette='viridis')
plt.title('Distribution of Product Ratings', fontsize=16)
plt.xlabel('Star Rating (overall)', fontsize=12)
plt.ylabel('Number of Reviews', fontsize=12)
plt.savefig('analysis1_rating_distribution.png')
plt.show()


# Query and Visualize Analysis 2: Helpfulness vs. Review Length
print("Visualizing Analysis 2...")
sql_query_2 = "SELECT * FROM dbo.Analysis2_HelpfulnessByRating;"
df2 = pd.read_sql(sql_query_2, db_connection)

# Plot 1: Average Helpfulness
plt.figure(figsize=(10, 6))
sns.barplot(x='overall', y='AverageHelpfulness', data=df2, palette='plasma')
plt.title('Average Helpfulness Score by Star Rating', fontsize=16)
plt.xlabel('Star Rating (overall)', fontsize=12)
plt.ylabel('Average Helpfulness Score', fontsize=12)
plt.savefig('analysis2_avg_helpfulness.png')
plt.show()

# Plot 2: Average Review Length
plt.figure(figsize=(10, 6))
sns.barplot(x='overall', y='AverageReviewLength', data=df2, palette='magma')
plt.title('Average Review Length by Star Rating', fontsize=16)
plt.xlabel('Star Rating (overall)', fontsize=12)
plt.ylabel('Average Review Length (characters)', fontsize=12)
plt.savefig('analysis2_avg_length.png')
plt.show()


# Query and Visualize Analysis 3: Summary Length Analysis
print("Visualizing Analysis 3...")
sql_query_3 = "SELECT * FROM dbo.Analysis3_SummaryLengthByRating;"
df3 = pd.read_sql(sql_query_3, db_connection)

plt.figure(figsize=(10, 6))
sns.barplot(x='overall', y='AverageSummaryLength', data=df3, palette='cividis')
plt.title('Average Review Summary Length by Star Rating', fontsize=16)
plt.xlabel('Star Rating (overall)', fontsize=12)
plt.ylabel('Average Summary Length (characters)', fontsize=12)
plt.savefig('analysis3_avg_summary_length.png')
plt.show()


# Close Connection
db_connection.close()
print("\nAll visualizations created and database connection closed.")
































# from pyspark.sql.functions import col, length



# storage_account_name = "dissprojectstorage"
# container_name = "project-data"
# file_name = "Electronics_5.json"
# access_key = 'ZSYJ0co0t9x+CjxVYR4LAsaudUwvAhW2fUC52seAIQ5wNMdXo5tC8CoB7/KePjOic/9wsH8hoJSV+AStuHMySQ=='


# sql_server_name = "diss-sql-server"
# sql_database_name = "ProjectResultsDB"
# sql_user = "webserver"
# sql_password = "asdfgh@#12345"


# print("Loading data from Azure Blob Storage...")


# spark.conf.set(
#     f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
#     access_key
# )


# input_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/{file_name}"
# df = spark.read.json(input_path)


# df.cache()

# print("Data loaded successfully.")
# df.printSchema()


# # Analysis 1: Rating Distribution
# print("\nStarting Analysis 1: Rating Distribution...")

# rating_counts_df = df.groupBy("overall").count().withColumnRenamed("count", "ReviewCount").orderBy("overall")
# rating_counts_df.show()


# sql_output_table_name_1 = "dbo.Analysis1_RatingDistribution"
# rating_counts_df.write \
#     .format("jdbc") \
#     .mode("overwrite") \
#     .option("url", f"jdbc:sqlserver://{sql_server_name}.database.windows.net;databaseName={sql_database_name};") \
#     .option("dbtable", sql_output_table_name_1) \
#     .option("user", sql_user) \
#     .option("password", sql_password) \
#     .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
#     .save()
# print(f"Analysis 1 results saved to {sql_output_table_name_1}")


# # --- Analysis 2: Helpfulness vs. Review Length ---
# print("\nStarting Analysis 2: Helpfulness vs. Review Length...")

# helpfulness_df = df.withColumn("ReviewLength", length(col("reviewText"))) \
#                      .withColumn("HelpfulnessScore", col("helpful")[0]) \
#                      .select("overall", "ReviewLength", "HelpfulnessScore")


# avg_helpfulness_df = helpfulness_df.groupBy("overall") \
#     .agg({
#         "ReviewLength": "avg",
#         "HelpfulnessScore": "avg"
#     }) \
#     .withColumnRenamed("avg(ReviewLength)", "AverageReviewLength") \
#     .withColumnRenamed("avg(HelpfulnessScore)", "AverageHelpfulness") \
#     .orderBy("overall")
# avg_helpfulness_df.show()


# sql_output_table_name_2 = "dbo.Analysis2_HelpfulnessByRating"
# avg_helpfulness_df.write \
#     .format("jdbc") \
#     .mode("overwrite") \
#     .option("url", f"jdbc:sqlserver://{sql_server_name}.database.windows.net;databaseName={sql_database_name};") \
#     .option("dbtable", sql_output_table_name_2) \
#     .option("user", sql_user) \
#     .option("password", sql_password) \
#     .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
#     .save()
# print(f"Analysis 2 results saved to {sql_output_table_name_2}")


# # Analysis 3: Review Summary Length Analysis
# print("\nStarting Analysis 3: Summary Length Analysis...")

# summary_length_df = df.withColumn("SummaryLength", length(col("summary"))) \
#                         .select("overall", "SummaryLength")


# avg_summary_length_df = summary_length_df.groupBy("overall") \
#     .agg({"SummaryLength": "avg"}) \
#     .withColumnRenamed("avg(SummaryLength)", "AverageSummaryLength") \
#     .orderBy("overall")
# avg_summary_length_df.show()


# sql_output_table_name_3 = "dbo.Analysis3_SummaryLengthByRating"
# avg_summary_length_df.write \
#     .format("jdbc") \
#     .mode("overwrite") \
#     .option("url", f"jdbc:sqlserver://{sql_server_name}.database.windows.net;databaseName={sql_database_name};") \
#     .option("dbtable", sql_output_table_name_3) \
#     .option("user", sql_user) \
#     .option("password", sql_password) \
#     .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
#     .save()
# print(f"Analysis 3 results saved to {sql_output_table_name_3}")


# df.unpersist()
# print("\nProcessing complete.")
