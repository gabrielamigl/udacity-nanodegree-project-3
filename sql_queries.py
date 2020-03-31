import configparser



# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS fact_plays"
user_table_drop = "DROP TABLE IF EXISTS dim_users"
song_table_drop = "DROP TABLE IF EXISTS dim_songs"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists"
time_table_drop = "DROP TABLE IF EXISTS dim_times"

# CREATE TABLES

staging_songs_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_songs (
num_songs int,
artist_id varchar,
artist_latitude decimal(9,6),
artist_longitude decimal(9,6),
artist_location varchar(max),
artist_name varchar(max),
song_id varchar,
title varchar,
duration float,
year int
)
""")

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events (
artist varchar,
auth varchar,
firstName varchar,
gender varchar,
itemInSession int,
lastName varchar,
length float,
level varchar,
location varchar,
method varchar,
page varchar,
registration bigint,
sessionId int,
song varchar,
status int,
ts bigint,
userAgent varchar,
userId int
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS fact_plays (
songplay_id INT IDENTITY(0,1) not null,
start_time timestamp not null,
user_id int not null,
level varchar,
song_id varchar,
artist_id varchar,
session_id int,
location varchar,
user_agent varchar,
PRIMARY KEY (songplay_id)
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_users (
user_id int not null sortkey,
first_name varchar,
last_name varchar,
gender varchar,
level varchar,
PRIMARY KEY(user_id)
)
diststyle all;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_songs (
song_id varchar not null,
title varchar,
artist_id varchar not null sortkey distkey,
year int ,
duration float,
PRIMARY KEY(song_id)
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_artists (
artist_id varchar not null sortkey distkey,
name varchar not null,
location varchar,
latitude decimal(9,6),
longitude decimal(9,6),
PRIMARY KEY (artist_id)
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_times (
start_time timestamp not null sortkey,
hour int not null,
day int not null,
week int not null,
month int not null,
year int not null,
weekday int not null,
PRIMARY KEY (start_time)
)
""")

# STAGING TABLES

staging_events_copy = ("""
COPY 
staging_events 
from {}
iam_role {} 
format as json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs from {}
iam_role {}
format as json 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO fact_plays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT
distinct '1970-01-01'::date + staging_events.ts/1000 * interval '1 second' as start_time,
staging_events.userid as user_id,
staging_events.level,
staging_songs.song_id,
staging_songs.artist_id,
staging_events.sessionid,
staging_events.location,
staging_events.useragent
FROM staging_events 
LEFT JOIN staging_songs on staging_events.artist = staging_songs.artist_name and staging_events.song = staging_songs.title
WHERE staging_events.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO dim_users (user_id, first_name, last_name, gender, level)
SELECT 
distinct userid as user_id, 
firstname as first_name,
lastname as last_name,
gender,
level
FROM staging_events 
WHERE page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO dim_songs (song_id, title, artist_id, year, duration)
SELECT 
distinct song_id, 
title, 
artist_id, 
year, 
duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO dim_artists (artist_id, name, location, latitude, longitude)
SELECT
distinct artist_id as artist_id, 
artist_name as name, 
artist_location as location, 
artist_latitude as latitude, 
artist_longitude as longitude
FROM
staging_songs;
""")

time_table_insert = ("""
DROP TABLE IF EXISTS start_times;
CREATE TEMPORARY TABLE start_times as
SELECT distinct('1970-01-01'::date + ts/1000 * interval '1 second') as start_time
FROM staging_events;
INSERT into dim_times (start_time, hour, day, week, month, year, weekday)
SELECT start_time, 
extract(hour from start_time) as hour,
extract(day from start_time) as day,
extract(week from start_time) as week,
extract(month from start_time) as month,
extract(year from start_time) as year,
extract(weekday from start_time) as weekday
FROM start_times;
DROP TABLE IF EXISTS start_times;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]