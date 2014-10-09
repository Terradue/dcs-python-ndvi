Node ndvi
=========

This is the first node of the workflow. As such, the platform takes cares of providing the inputs to the streaming executable: the list of Landsat catalogue entries you created earlier. 

.. tip:: ciop-copy can handle catalogue entries and download the datasets using the online resources in the metadata

A node requires a job template including:

* The path to the streaming executable:
* Default parameters
* Default configuration 

.. literalinclude:: ../src/src/main/app-resources/application.xml
  :language: xml
  :tab-width: 1
  :lines: 3-12

.. admonition:: Info 

  The code for the whole application is available here: https://github.com/Terradue/dcs-python-ndvi

While this job template doesn't define any parameter, it defines the *mapred.task.timeout* property which is the wall-time in miliseconds between two logging entries.

.. note::

  Log entries using ciop-log function in bash (or rciop.log in R and cioopy.log in Python) tell the platform the process is alive. If the wall-time is reached the execution is terminated with an error
  
