Data preparation
================

The data preparation step foresees:

* Copying the Landsat sample products to the Sandbox
* The conversion of the multiple GeoTFF files that compose a Landsat product into a single ERDAS .img product
* Copying the ERDAS .img products to the Laboratory S3 storage
* Registering the ERDAS .img products in the Sandbox local catalogue

Copying Landsat sample products to the Sandbox
**********************************************

Log on the Sandbox shell and run:

.. code::bash

  curl http://landsat.usgs.gov/documents/L5_30m19910616.tgz | tar xvfz -
  curl http://landsat.usgs.gov/documents/L5_30m19950627.tgz | tar xvfz -
  curl http://landsat.usgs.gov/documents/L7_30m19990817.tgz | tar xvfz -
  curl http://landsat.usgs.gov/documents/L7_30m20090422.tgz | tar xvfz -

This will download and extract the files from the compressed archives.

Format conversion
*****************

Use GDAL to convert the several GeoTIFF files (one for each Landsat band) to ERDAS .img format by creating a GDAL Virtual Format [#f1]_

On the Sandbox shell run the command:

.. code-block:: bash

  gdalbuildvrt -separate myvrt L5043033_03319950627_B10.TIF \
    L5043033_03319950627_B20.TIF \
    L5043033_03319950627_B30.TIF \
    L5043033_03319950627_B40.TIF \
    L5043033_03319950627_B50.TIF \
    L5043033_03319950627_B60.TIF \
    L5043033_03319950627_B70.TIF 
  
and finally:

.. code-block:: bash
  
  gdal_translate -of HFA myvrt L5043033_03319950627.img
  
Repeat the two steps above with the other three Landsat products.

Copying the ERDAS .img products to S3 storage
*********************************************

On the Sandbox shell run the command:

.. code-block:: bash

  s3cmd put *.img s3://<your_laboratory>-private/data/
  
List the uploaded files:

.. code-block:: bash

  s3cmd ls s3://<your_laboratory>-private/data/
  
Registering the ERDAS .img products in the Sandbox local catalogue
******************************************************************

To register the Landsat products converted to ERDAS .img format, you need to create a dataset series which is a container for the datasets.

Copy the contents of the file below into a file named *series.rdf* in your home.

:download:`Landsat series <files/series.rdf>`

For each Landsat product, generate a file containing the dataset metadata.

.. todo:: FABIO!!

Finally go to the Sandbox catalogue Web Interface at the address http://<sandbox IP>/catalogue/search and click search, you will see the Landsat products!

.. admonition:: Congrats!

  There is now Landsat 5&7 data available on the Laboratory S3 storage and registered on the Sandbox catalogue!
  
.. rubric:: Footnotes

.. [#f1] `GDAL Virtual format <http://www.gdal.org/gdal_vrttut.html>`_
