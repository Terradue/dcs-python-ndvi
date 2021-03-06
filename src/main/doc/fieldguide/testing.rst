Application integration and testing
===================================

Now that the node ndvi template is defined, it is now time to create the workflow with the single node.

The workflows are Directed Acyclic Graphs (DAG) where nodes and their relation(s) and the source(s) are defined.

Each node of the DAG has:

* a unique node identifier
* a job template id reference
* one or more sources
* one or more parameters and associated values to overide the default values (if defined in the job template).

The node_ndvi node
------------------

This application's workflow has a single node. Its identifer is set to *node_ndvi* and it instantiates the :doc:`py-job <nodes/ndvi>` job template.

Here's how this simple workflow is defined:

.. literalinclude:: ../../../app-resources/application.xml
  :language: xml
  :tab-width: 1
  :lines: 13-23

As source, this node uses a comma-separated list of catalogue references, e.g.:

.. code-block:: example

  http://catalogue.terradue.int/catalogue/search/LANDSAT_SAMPLES/LT50430331995178XXX03/rdf

Change this value to one (or more) of the Landsat sample products you have in the Sandbox catalogue by going to http://<sandbox ip>/catalogue/search and copying one the dataset RDF URLs.

Testing the application
-----------------------

Application installation
^^^^^^^^^^^^^^^^^^^^^^^^

All the application files are available on a GitHub repository that can be cloned on the Sandbox with:

.. code-block:: console

  cd
  git clone https://github.com/Terradue/dcs-python-ndvi.git
  cd dcs-python-ndvi
  
Install the *tree* utility to inspect the application structure with

.. code-block:: console

  sudo yum install -y tree

Then, do:

.. code-block:: console

  tree
  
The application resources mentioned so far are under the path:

.. code-block:: console
  
  src/main/app-resources

while the Python NDVI package source is under:

.. code-block:: console
  
  src/main/python
  
To build the application, use maven [#f1]_ to:

* Compile the Python package and copy the package to /application/shared/python
* Copy the application resources to /application

To do so, from the cloned repository folder where the pom.xml is (typically in ~/dcs-python-ndvi), simply run:

.. code-block:: console

  mvn install
  
Check the contest of the installed application with:

.. code-block:: console

  tree /application
  
Application check
^^^^^^^^^^^^^^^^^
  
The Application Descriptor file can be checked with:

.. code-block:: console

  ciop-appcheck
  
If the Application Descriptor is valid, the output is:

.. code-block:: console

  /application/application.xml validates

Application submission
^^^^^^^^^^^^^^^^^^^^^^

The application can be tested by:

* Submitting every single job of the workflow with ciop-run [#f2]_,
* Submitting the complete workflow with ciop-run [node-id] [#f2]_,
* Submitting a Web Processing Service request.

With this application, there's only one node so the first two options are quite similar.

Testing a node of the workflow
------------------------------

Get the lists of nodes with: 

.. code-block:: console

  ciop-run -n
  
That will report *node_ndvi*

Trigger its execution with:

.. code-block:: console

  ciop-run node_ndvi
  
The node_ndvi will:

* Retrieve the Landsat product from the S3 storage using the online resource value found in the Sandbox catalogue
* Produce the NDVI GeoTIFF file  
* Copy the NDVI GeoTIFF file to S3 storage
* Register it in the Sandbox catalogue 

Testing the entire workflow execution
-------------------------------------

.. code-block:: console

  ciop-run
  
Wait for the workflow execution, the same results are produced.

Testing the workflow using WPS
------------------------------

Go to the Sandbox dashboard (http://<sandbox IP>/dashboard). On the **Invoke** tab, you can provide one or more Landsat products catalogue entries and submit the processing request.

.. rubric:: Footnotes

.. [#f1] `Apache maven <http://maven.apache.org/>`_
.. [#f2] :doc:`ciop-run man page </reference/man/bash_commands_functions/simulation/ciop-run>`

