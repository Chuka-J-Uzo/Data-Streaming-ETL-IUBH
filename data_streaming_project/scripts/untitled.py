def write_to_mysql(df, epoch_id):
    df.writeStream \
    .outputMode("update") \
    .option("checkpointLocation", "./../spark_job_outputs/df_checkpoint_folder") \
    .option("url", "jdbc:mysql://MySQL_Container:3306/KAFKA_DB") \
    .option("dbtable", "SPARK_TABLE_TRANSFORMED") \
    .option("user", "root") \
    .option("password", "root") \
    .format("jdbc") \
    .option("driver", "com.mysql.jdbc.Driver") \
    .option("truncate", "false") \
    .option("mode", "append") \
    .option("createTableOptions", "ENGINE=InnoDB") \
    .option("numPartitions", "10") \
    .option("batchsize", "1000") \
    .option("isolationLevel", "NONE") \
    .option("fetchSize", "100000") \
    .option("path", "./../spark_job_outputs/sql-files_folder/output.sql") \
    .start()

df.writeStream \
    .outputMode("update") \
    .option("checkpointLocation", "./../spark_job_outputs/df_checkpoint_folder") \
    .option("path", "./../spark_job_outputs/sql-files_folder/output.sql") \
    .foreachBatch(write_to_mysql) \
    .start()