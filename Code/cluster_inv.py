from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, SQLContext
import os, re
import math
if __name__ == '__main__':
    # spark = SparkSession.builder.master("spark://p930026143:7077").getOrCreate()
    sc = SparkContext.getOrCreate(SparkConf())
                    #.flatMap(lambda x: [((os.path.basename(x[0]).split(".")[0] ,i) ,1) for i in re.split('\\W', x[1])])\
    #sc = spark.sparkContext
    sql = SQLContext(sc)
    #data = sc.wholeTextFiles('hdfs://10.20.6.126:9000/usr/hdusr/books')

#    numFiles = data.count()

#    wordcount = data.flatMap(lambda x: [((os.path.basename(x[0]) ,i) ,1) for i in re.split('\\W', x[1])]).reduceByKey(lambda a, b: a + b)

#    tf = wordcount.map(lambda x: (x[0][1],(x[0][0],x[1])))

#    idf = wordcount.map(lambda x: (x[0][1], (x[0][0], x[1], 1)))\
#        .map(lambda x: (x[0], x[1][2]))\
#        .reduceByKey(lambda x, y: x + y)\
#        .map(lambda x: (x[0], math.log10(numFiles / x[1])))

#Slightly modified map output as (doc, (term, tfidf))
#    tfidf = tf.join(idf)\
 #           .map(lambda x: (x[1][0][0], (x[0], x[1][0][1] * x[1][1])))\
  #          .sortByKey()

#Then we convert the TF-IDF to an DF, and save to the disk
   # lines = tfidf.map(lambda x: (x[0], x[1][0], x[1][1])).toDF()

   # lines.show()
   # lines.write.save("hdfs://10.20.6.126:9000/usr/hdusr/tfidf")

##############################################################
    def connect(a,b):
        try:
            c1=()+a
        except:
            c1=(a,)
        try:
            c2=()+b
        except:
            c2=(b,)
        result=tuple(set(c1+c2))
        if len(result)!=1:
            return tuple(set(c1+c2))
        else:
            return result[0]
    rdd1 = sc.wholeTextFiles('hdfs://10.20.6.126:9000/usr/hdusr/smallbooks')
    rdd2 = rdd1.flatMap(lambda x: [((i.lower(),os.path.basename(x[0])), 1) for i in re.split('\\W', x[1])])
    rdd3 = rdd2.reduceByKey(lambda a, b: a + b)
    inverted_index = rdd3.map(lambda x: (x[0][0],(x[0][1],x[1])))
    inverted_index.toDF().show()
    def connect_2(a,b):
        tmp=tuple(a)+tuple(b)
        return tuple(set([i for i in tmp if isinstance(i,str)]))

    def reform(a):
        print(a)
        if isinstance(a[1][1],int):
            return (a[0],str(a[1][0]))
        else:
            string=",".join(a[1])
            return (a[0],string)
    counts = inverted_index.reduceByKey(lambda a, b: connect_2(a,b))
    counts_fin = counts.map(lambda x: reform(x))
    result = counts_fin
    output = result.toDF()
    output.show()
   # output.write.save("hdfs://10.20.6.126:9000/usr/hdusr/inverted_index")
    
    sc.stop()
