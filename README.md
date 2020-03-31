# Data Engineering Nanodegree - Redshift Data Warehouse

On this project, we were requested to build a data ingestion pipeline for a number of JSON files provided on a S3 bucket along with the development of scripts to create a data warehouse applying star schema on Redshift. The JSON files should be read into staging tables and from those tables we should create facts and dimensions tables applying the table design patterns we learnt during the lesson.

## Project Execution
The right order to the execute this project is:
1. `create_tables.py`
2. `etl.py`

The scripts must be executed on this order in order to correctly finish the processing. While `create_table.py` creates the tables on Redshift, `etl.py` reads the JSON files into the staging tables and creates the facts and dimensions tables, also populating them.

## Files Structure
### `sql_queries.py`
The purpose of this script is to define the SQL statements that are going to be executed on the creation, deleting and populating process of the tables.

It is important to mention that the copy commands need a config from `dwh.cfg`. That config is the ARN from the IAM_ROLE. Without that configuration the operations on this file won't be sucessful.

### `create_tables.py`
This script is the one in charge of the database creation and tables dropping and creation. The following functions can be found on the script: 

`drop_tables(cur, conn)` receives the connection and cursor and execute the scripts that are included on the list  `drop_table_queries` that is generated by the `sql_queries.py` script.

`create_tables(cur, conn)` also accepts as parameters the cursor and the database connection and executes the creation of table statements. These scripts are included on `create_table_queries` list that was defined on `sql_queries.py`.

`main()` is entry function and sets how the process occurs when the script is executed. The scope is create the to connect to the Redshift cluster, drop the tables and create the tables.

### `etl.py`
This is the script that executes the ETL job logic itself. Its job is to load the JSON files into staging tables and then process the data into dimension and fact tables.

## Tables 

According to the instructions, we had to create staging tables to store the raw data imported from the JSON files and some dimensional tables.

### Staging Tables

The staging tables have the purpose to store the data exactly how it comes from the the JSON files seating on the S3 bucket.

#### staging_events
The `staging_events` table store the information from the log_data folder and none filter is applied during the reading. 
On this table is possible to find every log stored from Sparkify users. Not just song execution but logging in process are stored there as well. The type of the operation is defined by the page attribute.

#### staging_songs
The `staging_events` table store the information from the song_data folder and none filter is applied during the reading. These files content is related to songs and artists that are present on Sparkify.

### Dimensions and Fact

Dimensions and facts are important to give the data a business view and to make simpler the queries. The schema utilised on this project was the Star schema that accepts some denormalised data, in special on dimensions.

#### fact_plays

The fact_plays table is the **fact** table and store the facts related to songs listenings. Every user's song execution is store here. It is possible to find the references to the dimensions, like `user_id`, `song_id` and `artist_id`. The reference with `dim_times` is the `start_time` attribute. 
I've chosen to use the `level` attribute as my distkey as I see that it's a very important attribute to be used on the queries and that's why that information is stored both on the fact and on the dim_users dimension.

#### dim_users

The table dim_users is a **dimension** that store information about the users, such as name, genre and level.

#### dim_songs

The table dim_songs is a **dimension** that store information about the songs, such as title, duration, year and artist reference.

#### dim_artists
The table dim_artists is a **dimension** that store information about the artists, such as name and location.

#### dim_times
The table dim_times is a **dimension** that store information about the times utilised on the DWH. It has mostly parts extracted from the timestamp, like year, month, day, hour and etc.

