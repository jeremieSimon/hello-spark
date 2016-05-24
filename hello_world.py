"""
run from command line
spark-submit --master yarn-client --conf key=value --conf someotherkey=someothervalue you_code.py
"""

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row

conf = SparkConf().setAppName("hello-world").setMaster('yarn-client')
conf.set("spark.files.overwrite","true")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

#log
log4jLogger = sc._jvm.org.apache.log4j
LOG = log4jLogger.LogManager.getLogger("hello.world.spark")
LOG.info("Args = " + conf.getAll().__str__())

inputFile = conf.get("spark.input")
outputFile = conf.get("spark.output")

wordcount = sc.textFile(inputFile).map(lambda line: line.replace("\"", " ").replace("{", " ").replace("}", " ").replace(".", " ").replace(":", " ")) \
    .flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .map(lambda (k, v): (v, k)) \
    .sortByKey(ascending=False) \
    .map(lambda (k, v): (v, k))

df = wordcount.toDF(['word', 'count'])
df.save(path=outputFile, source='json', mode='overwrite')
