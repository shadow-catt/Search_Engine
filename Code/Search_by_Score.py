from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, SQLContext
import os, re
import math

if __name__=="__main__":
    tfidf_RDD = sql.read.parquet("tfidf-index").rdd.map(lambda x: (x['_2'],(x['_1'],x['_3'])))

    def tokenize(s):
        return re.split("\\W+", s.lower())

    def search(query, topN):
        tokens = sc.parallelize(tokenize(query)).map(lambda x: (x, 1) ).collectAsMap()
        bcTokens = sc.broadcast(tokens)

    #connect to documents with terms in the Query. to Limit the computation space
    #so that we don't attempt to compute similarity for docs that have no words in common with our query.
        joined_tfidf = tfidf_RDD.map(lambda x: (x[0], bcTokens.value.get(x[0], '-'), x[1]) ).filter(lambda x: x[1] != '-' )

    #compute the score using aggregateByKey
        scount = joined_tfidf.map(lambda a: a[2]).aggregateByKey((0,0),
        (lambda acc, value: (acc[0] + value, acc[1] + 1)),
        (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])) )

        scores = scount.map(lambda x: ( x[1][0]*x[1][1]/len(tokens), x[0]) ).top(topN)
        return scores

    search("I love UIC", 5)
