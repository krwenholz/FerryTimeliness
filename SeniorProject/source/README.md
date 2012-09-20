# A Project for WA State's Ferry Timeliness #
### Author: Kyle Wenholz ###
### Director: Brad Richards ###

## Some documentation for other used resources #
[Selenium](http://selenium.googlecode.com/svn/trunk/docs/api/py/api.html)
[PostgreSQL basic usage](https://mohsinpage.wordpress.com/2010/05/16/use-of-python-db-apis-psycopg2-for-a-postgresql-database/)
[Basic PostgreSQL tables](http://www.postgresqlguide.com/creating-tables-in-postgresql.aspx)

## My database schema ##
site_data( id bigserial PRIMARY KEY, vessel varchar(20), knots real, departing varchar(40), arriving varchar(40), scheduled_departure time, actual_departure time, estimated_arrival time, route varchar(20), date timestamp);
