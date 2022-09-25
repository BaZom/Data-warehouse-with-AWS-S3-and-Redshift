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

## Staging tables

![enter image description here](https://github.com/BaZom/Data-warehouse-with-AWS-S3-and-Redshift/blob/4361dc1f49353701d142e70bcecdf2d2b8fe0633/staging_tables.png)

## Star schema tables
![enter image description here](https://github.com/BaZom/Data-warehouse-with-AWS-S3-and-Redshift/blob/848476c6f991f098374eba1e0247dcb8d3350468/star_schema.png)

## Schema Design
- The data is loaded in a star schema with a fact table having foreign keys to four dimensional tables
- user_id from table songplays is used as a redshift distribution key.
- The primary key of each dimensional table is used as a sorting key for that table.
## Test queries
#####  SELECT count(*) FROM "dev"."public"."staging_events" where page = 'NextSong';
 || count | |
|-|-------|-|
||6820  | |

##### SELECT count(*) FROM "dev"."public"."staging_songs";
 || count | |
|-|-------|-|
||14896| |

##### SELECT count(*) FROM "dev"."public"."songplays";
 || count | |
|-|-------|-|
||333| |

#### SELECT count(*) FROM "dev"."public"."users" where user_id = '';
 || count | |
|-|-------|-|
||107| |

#### SELECT count(*) FROM "dev"."public"."time";
 || count | |
|-|-------|-|
||8023| |

#### SELECT count(*) FROM "dev"."public"."artists";
 || count | |
|-|-------|-|
||10025| |

#### SELECT count(*) FROM "dev"."public"."songs";
 || count | |
|-|-------|-|
||14896| |

#### SELECT song_id, count(*) as county FROM "dev"."public"."songplays"group by song_id order by county DESC limit 10;
 || song_id| county||
|-|-------|-|-|
||SOBONKR12A58A7A7E0	|37	||
||SOHTKMO12AB01843B0	|9||
||SOUNZHU12A8AE47481	|9||
||SOULTKQ12AB018A183	|9||
||SOLZOBD12AB0185720	|6||
||SOARUPP12AB01842E0	|5||
||SOTNHIP12AB0183131	|5||
||SOIOESO12A6D4F621D	|4||
||SONQEYS12AF72AABC9	|4||
||SOIZLKI12A6D4F7B61	|5||


