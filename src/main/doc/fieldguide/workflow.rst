Workflow design
===============
Data 
****

You will use the Landsat 5&7 sample products made available by the `USGS <http://www.usgs.gov/>`_ at `<http://landsat.usgs.gov/product_samples.php>`_

The list of products used as test data is:

* Landsat 5 TM

  Acquired June 16, 1991: L5 TM 30-meter thermal - .tgz (175 MB)

  Acquired June 27, 1995: L5 TM 30-meter thermal - .tgz (171 MB)

* Landsat 7 ETM+

  Acquired August 17, 1999: L7 ETM+ 30-meter thermal - .tgz (316 MB)

  Acquired April 22, 2009: L7 ETM+ 30-meter thermal - .tgz (274 MB)

Software and COTS
*****************

GDAL and GDAL Python
--------------------

You will use GDAL [#f1]_ to:

* pre-process each of the Landsat sample products to convert from a multi GeoTIFF files to a single ERDAS .img product 

and GDAL Python libraries [#f2]_ to: 

* implement a Python module to calculate the NDVI GeoTIFF 

.. [#f1] `GDAL Geospatial Data Abstraction Library <http://www.gdal.org/>`_

.. [#f2] `GDAL Geospatial Data Abstraction Library Python package <https://pypi.python.org/pypi/GDAL/>`_

Workflow design
***************

The application's data pipeline activities can be defined as follows:

Use the Python NDVI package to apply the band arithmetic expression to calculate the NDVI to all Landsat products passed as references to the Sandbox catalogue.

.. uml::

  !define DIAG_NAME Workflow example

  !include includes/skins.iuml

  skinparam backgroundColor #FFFFFF
  skinparam componentStyle uml2

  start
  
  while (check stdin?) is (line)
    :Stage-in data;
    :Apply Python NDVI;
    :Stage-out ndvi_result;
    :Register ndvi_result in Sandbox catalogue;
  endwhile (empty)

  stop

This translates into a very simple workflow containing a single processing step: py-ndvi 

The simple workflow can be represented as:

.. uml::

  !define DIAG_NAME Workflow example

  !include includes/skins.iuml

  skinparam backgroundColor #FFFFFF
  skinparam componentStyle uml2

  start

  :node_ndvi;
  
  stop

The *node_ndvi* is described in details in :doc:`/field/vegetation/lib_python_ndvi/nodes/index`

