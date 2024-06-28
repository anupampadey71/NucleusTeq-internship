from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("WordCount") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .getOrCreate()

# Read the text file into an RDD
text_file = spark.sparkContext.textFile("/home/anupampandey/Public/pyspark/example.txt")

# Perform the word count
word_counts = text_file.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)

# Collect and print the results
for word, count in word_counts.collect():
    print(f"{word}: {count}")

# Stop the Spark session
spark.stop()
