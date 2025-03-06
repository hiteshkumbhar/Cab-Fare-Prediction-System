# import sys
# from awsglue.transforms import *
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from awsglue.context import GlueContext
# from awsglue.job import Job

# ## @params: [JOB_NAME]
# args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
# job = Job(glueContext)
# job.init(args['JOB_NAME'], args)
# job.commit()



# import sys
# from awsglue.transforms import *
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from awsglue.context import GlueContext
# from awsglue.job import Job
# from pyspark.sql.functions import col, when
# from awsglue.dynamicframe import DynamicFrame

# # Initialize Glue job
# args = getResolvedOptions(sys.argv, ["JOB_NAME"])
# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
# job = Job(glueContext)
# job.init(args["JOB_NAME"], args)

# # Load data from the Glue Data Catalog
# datasource = glueContext.create_dynamic_frame.from_catalog(
#     database="farepricedb",
#     table_name="rawdata_csv"
# )

# # Convert DynamicFrame to DataFrame for easier transformations
# clean_data = datasource.toDF()

# # Task 1: Map 'day_type' column values
# clean_data = clean_data.withColumn(
#     "day_type",
#     when(col("day_type") == "Weekday", 0).otherwise(1)
# )

# # Task 2: Filter the dataset to include only the specified columns
# columns_to_keep = [
#     "total_amount", "vendor_id", "mta_tax", "distance", "num_passengers",
#     "toll_amount", "payment_method", "improvement_charge", "extra_charges",
#     "trip_duration", "day_type"
# ]
# fdf = clean_data.select(columns_to_keep)

# # Convert back to DynamicFrame for writing
# filtered_dynamic_frame = DynamicFrame.fromDF(fdf, glueContext, "filtered_dynamic_frame")

# # Write the filtered data back to S3
# glueContext.write_dynamic_frame.from_options(
#     frame=filtered_dynamic_frame,
#     connection_type="s3",
#     connection_options={"path": "s3://fareprice/filtered/"},
#     format="csv"  # or "csv", "json", etc.
# )

# # Commit the job
# job.commit()
