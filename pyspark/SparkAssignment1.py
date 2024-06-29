from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("DataProcessing") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .getOrCreate()

# 1. Reading a text file and creating an RDD
text_file_rdd = spark.sparkContext.textFile("/home/anupampandey/Public/pyspark/example.txt")

# Perform a simple transformation and action
lines = text_file_rdd.collect()
print("Lines from Text File:")
for line in lines:
    print(line)

# 2. Reading a CSV file and creating a DataFrame
csv_df = spark.read.csv("/home/anupampandey/Public/pyspark/example.csv", header=True, inferSchema=True)

# Show the first few rows of the DataFrame
print("CSV DataFrame:")
csv_df.show()

# Print the schema of the DataFrame
print("Schema of CSV DataFrame:")
csv_df.printSchema()

# Get the number of rows in the DataFrame
num_csv_rows = csv_df.count()
print(f"Number of rows in CSV DataFrame: {num_csv_rows}")

# 3. Reading a JSON file and creating a DataFrame
json_df = spark.read.json("/home/anupampandey/Public/pyspark/example.json")

# Show the first few rows of the DataFrame
print("JSON DataFrame:")
json_df.show()

# Print the schema of the DataFrame
print("Schema of JSON DataFrame:")
json_df.printSchema()

# Get the number of rows in the DataFrame
num_json_rows = json_df.count()
print(f"Number of rows in JSON DataFrame: {num_json_rows}")

# Stop the Spark session
spark.stop()
