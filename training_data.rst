Training the Data
=================
The data obtained for weather and for the ferry system is contained in this
package (or by request).  Below are the steps to cull the data into a form
usable by LibSVM and how to run it through LibSVM.

The data used spanned October 2010 through September 2012.  A lot of cleaning
and investigation into meaning was required to make the data make sense and work.
All source files are in the 'src' directory, and any data files are expected to
be in or go in the '../Data' directory.

Weather Data
++++++++++++
Where does it come from?
------------------------
Quality controlled data_ from NOAA was obtained with access from the University
of Puget Sound.  This data was downloaded month by month to match the ferry
data timeline.

How does weather_data_reader.py work?
-------------------------------------
The weather_data_reader.py script is used to parse all of the weather data pulled
from the NOAA source into a single CSV file (header included).  To adjust this
file, all you need to do is adjust the printed header at the top (line 17) and
the tuple of column numbers (line 21) to include the columns you want.  To run
from the command line you use

    python weather_data_reader.py

The output is a file, "weather_data.csv", in the data directory (line 15).
Command line output will indicate how many points are dropped due to empty
or bad data type entries in the desired columns.


Ferry Data
++++++++++
Where does it come from?
------------------------

How does wsdot_data_request_reader.py work?
-------------------------------------------
The script is designed to clean up the state data a bit: remove rows with
null entries, bad types, etc.  You'll get some console output indicating how
many good rows are found.  Almost all of the configuration happens at the
bottom of the file.  By default, expect the file to be read in from
'../Data/data_request_October2012.csv' and output to '../Data/ferry_data.csv'.
A nice header is even included.  To use, simply run

    python wsdot_data_request_reader.py

In theory, the output CSV file should be ready for a database (Postgres) using
simple inserts (i.e. you shouldn't even need to format the dates).


Joining Weather and Ferry Data
++++++++++++++++++++++++++++++
Why join the data?
------------------

How does libsvm_data_format.py work?
--------------------------------

Using LibSVM (my procedure)
+++++++++++++++++++++++++++

.. _data: http://cdo.ncdc.noaa.gov/qclcd/QCLCD?prior=N
