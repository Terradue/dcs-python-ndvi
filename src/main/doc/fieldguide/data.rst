Data preparation
================

The data preparation step foresees:

* Copying the Landsat sample products from the S3 storage to the Sandbox
* The conversion of the multiple GeoTFF files that compose a Landsat product into a single ERDAS .img product
* Repeat this for the four Landsat products
* Copying the ERDAS .img products to the Laboratory S3 storage

Copying Landsat sample products to the Sandbox
**********************************************

Log on the Sandbox shell and run:

.. code-block:: console

  mkdir -p /tmp/input_data
  ciop-copy -O /tmp/input_data s3://landsat-samples/L5_30m19910616.tgz 
  ciop-copy -O /tmp/input_data s3://landsat-samples/L5_30m19950627.tgz
  ciop-copy -O /tmp/input_data s3://landsat-samples/L7_30m19990817.tgz
  ciop-copy -O /tmp/input_data s3://landsat-samples/L7_30m20090422.tgz

This will download and extract the files from the compressed archives.

.. note::

  ciop-copy does the archive extraction by default

Format conversion
*****************

Use GDAL to convert the several GeoTIFF files (one for each Landsat band) to ERDAS .img format by creating a GDAL Virtual Format [#f1]_

On the Sandbox shell run the command:

.. code-block:: console

  gdalbuildvrt -separate myvrt L5043033_03319950627_B10.TIF \
    L5043033_03319950627_B20.TIF \
    L5043033_03319950627_B30.TIF \
    L5043033_03319950627_B40.TIF \
    L5043033_03319950627_B50.TIF \
    L5043033_03319950627_B60.TIF \
    L5043033_03319950627_B70.TIF 
  
and finally:

.. code-block:: console
  
  gdal_translate -of HFA myvrt L5043033_03319950627.img
  
Repeat the two steps above with the other three Landsat products.

Copying the ERDAS .img products to S3 storage
*********************************************

On the Sandbox shell run the command:

.. code-block:: console

  s3cmd put *.img s3://<your_laboratory>-private/data/
  
List the uploaded files:

.. code-block:: console

  s3cmd ls s3://<your_laboratory>-private/data/
  
Finally go to the Sandbox catalogue Web Interface at the address http://<sandbox IP>/catalogue/search and click search, you will see the Landsat products!

.. admonition:: Congrats!

  There is now Landsat 5&7 data available on the Laboratory S3 storage in the ERDAS format ready to be processed by the application!
  
.. rubric:: Footnotes

.. [#f1] `GDAL Virtual format <http://www.gdal.org/gdal_vrttut.html>`_
