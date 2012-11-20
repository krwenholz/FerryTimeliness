Training the Data
=================
The data obtained for weather and for the ferry system is contained in this
package (or by request).  Below are the steps to cull the data into a form
usable by LibSVM and how to run it through LibSVM.

The data used spanned October 2010 through September 2012.  A lot of cleaning
and investigation into meaning was required to make the data make sense and work.

Weather Data
++++++++++++
Where does it come from?
------------------------
Quality controlled data_ from NOAA was obtained with access from the University
of Puget Sound.  This data was downloaded month by month to match the ferry
data timeline.

How does the WEATHER SCRIPT work?
---------------------------------

Ferry Data
++++++++++
Where does it come from?
------------------------

How does the FERRY DATA SCRIPT work?
------------------------------------


Joining Weather and Ferry Data
++++++++++++++++++++++++++++++
Why join the data?
------------------

How does the LIBSVM SCRIPT work?
--------------------------------

Using LibSVM (my procedure)
+++++++++++++++++++++++++++

.. _data http://cdo.ncdc.noaa.gov/qclcd/QCLCD?prior=N
