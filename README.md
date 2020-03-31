# Data Engineering Nanodegree - Redshift Data Warehouse

On this project, we were requested to build a data ingestion pipeline for a number of JSON files provided on a S3 bucket along with the development of scripts to create a data warehouse applying star schema on Redshift. 

## Project Execution
The right order to the execute this project is:
1. `create_tables.py`
2. `etl.py`

`create_table.py` creates the tables on Redshift, `etl.py` reads the JSON files into the staging tables and creates the facts and dimensions tables.


## Tables 

We had to create staging tables to store the raw data imported from the JSON files and some dimensional tables.

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

