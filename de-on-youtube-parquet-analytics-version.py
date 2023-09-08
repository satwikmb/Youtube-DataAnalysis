import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1694116147513 = glueContext.create_dynamic_frame.from_catalog(
    database="de_youtube_satwik_raw",
    table_name="cleaned_statistics_reference_data",
    transformation_ctx="AWSGlueDataCatalog_node1694116147513",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1694115002796 = glueContext.create_dynamic_frame.from_catalog(
    database="de_youtube_satwik_raw",
    table_name="raw_statistics",
    transformation_ctx="AWSGlueDataCatalog_node1694115002796",
)

# Script generated for node Join
Join_node1694116435266 = Join.apply(
    frame1=AWSGlueDataCatalog_node1694116147513,
    frame2=AWSGlueDataCatalog_node1694115002796,
    keys1=["id"],
    keys2=["category_id"],
    transformation_ctx="Join_node1694116435266",
)

# Script generated for node Amazon S3
AmazonS3_node1694116453308 = glueContext.getSink(
    path="s3://de-on-youtube-analytics-useast1-dev-satwik",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=["region", "category_id"],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1694116453308",
)
AmazonS3_node1694116453308.setCatalogInfo(
    catalogDatabase="db_youtube_analytics_satwik",
    catalogTableName="final_analytics_satwik",
)
AmazonS3_node1694116453308.setFormat("glueparquet")
AmazonS3_node1694116453308.writeFrame(Join_node1694116435266)
job.commit()
