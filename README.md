# Data-warehouse-with-amazon-redshift
## Introduction
This project aims to extract songs metadata and user activity data from JSON  files residing in an AWS S3 bucket and save them in a database star schema in AWS redshift. 

## Project Dataset
The following two datasets used in this project are two subsets of real data from the [Million Song Dataset](http://millionsongdataset.com/) and of generated data by this [event simulator](https://github.com/Interana/eventsim).

AWS S3 links for each:
-   Song data: `s3://udacity-dend/song_data`
-   Log data: `s3://udacity-dend/log_data`

Log data json path: `s3://udacity-dend/log_json_path.json`

## Project steps
- Staging tables for songs and events namely staging_events and staging_songs are created on AWS redshift
- Star schema with one fact table namely songplays and four dimension tables namely users, songs, artists and time is created on AWS redshift
- Data is loaded from an S3 bucket to the stating tables using COPY statement.
- SQL insert statements are created to select data from Staging tables and insert it into the star schema tables.

## Database staging tables
