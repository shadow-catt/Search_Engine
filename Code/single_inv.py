from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import os, re
import time

start_time = time.perf_counter()
if __name__ == '__main__':
    sc = SparkContext.getOrCreate(SparkConf())
#     spark = SparkSession.builder.master("spark://p930026143:7077").getOrCreate()
    #sc = SparkContext.getOrCreate(SparkConf())
                    #.flatMap(lambda x: [((os.path.basename(x[0]).split(".")[0] ,i) ,1) for i in re.split('\\W', x[1])])\
#     sc = spark.sparkContext
    inverted_index = sc.wholeTextFiles('hdfs://master-david:9000/usr/hdusr/smallbooks')\
                    .flatMap(lambda x: [((i.lower(),os.path.basename(x[0])), 1) for i in re.split('\\W', x[1])])\
                    .reduceByKey(lambda a, b: a + b)\
                    .map(lambda x: (x[0][0],(x[0][1],x[1])))

    inverted_index.collect()
#     for i in range(inverted_index.count()):
#         print(output[i])
    sc.stop()
    end_time = time.perf_counter()
    cost_time = end_time-start_time
    print("single machine 1G runtime: " + str(cost_time))
