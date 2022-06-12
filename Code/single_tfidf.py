from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, SQLContext
import os, re
import math
import time
if __name__ == '__main__':
    begin_time = time.perf_counter()
    #spark = SparkSession.builder.master("spark://p930026143:7077").getOrCreate()
    sc = SparkContext.getOrCreate(SparkConf())
    sql = SQLContext(sc)
    data = sc.wholeTextFiles('hdfs://10.20.6.126:9000/usr/hdusr/books')

    numFiles = data.count()

    wordcount = data.flatMap(lambda x: [((os.path.basename(x[0]) ,i) ,1) for i in re.split('\\W', x[1])]).reduceByKey(lambda a, b: a + b)

    tf = wordcount.map(lambda x: (x[0][1],(x[0][0],x[1])))

    idf = wordcount.map(lambda x: (x[0][1], (x[0][0], x[1], 1)))\
         .map(lambda x: (x[0], x[1][2]))\
         .reduceByKey(lambda x, y: x + y)\
         .map(lambda x: (x[0], math.log10(numFiles / x[1])))

# Slightly modified map output as (doc, (term, tfidf))
    tfidf = tf.join(idf)\
            .map(lambda x: (x[1][0][0], (x[0], x[1][0][1] * x[1][1])))\
            .sortByKey()
    end_time = time.perf_counter()
#Then we convert the TF-IDF to an DF, and save to the disk
    lines = tfidf.map(lambda x: (x[0], x[1][0], x[1][1])).toDF()

    lines.show()
    cost_time = begin_time-end_time
    print("The cost time of 100M tfidf is " + str(cost_time))

##############################################################
#    inverted_index = sc.wholeTextFiles('hdfs://10.20.6.126:9000/usr/hdusr/smallbooks')\
#            .flatMap(lambda x: [((i.lower(),os.path.basename(x[0])), 1) for i in re.split('\\W', x[1])])\
#            .reduceByKey(lambda a, b: a + b)\
#            .map(lambda x: (x[0][0],(x[0][1],x[1])))
#
#    output = inverted_index.toDF()
#    output.show()
#    output.write.save("hdfs://10.20.6.126:9000/usr/hdusr/inverted_index")

    sc.stop()

