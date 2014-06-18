## Developer Cloud Service - Landsat NDVI Python tutorial

The Landsat NDVI Python tutorial uses the Developer Cloud Sandbox service to implement a Python package using GDAL to   calculate the [NDVI](http://en.wikipedia.org/wiki/Normalized_Difference_Vegetation_Index) in [Landsat TM 5 and 7](http://en.wikipedia.org/wiki/Landsat_program) data.

This tutorial builds upon the [Python Scripting for Remote Sensing course](http://www.landmap.ac.uk/index.php/Learning-Materials/Python-Scripting/9.1-Introduction) by [Landmap](http://www.landmap.ac.uk/) and extends it to exploit a Cloud computing platform for its development, test and exploitation.

### Getting Started 

To run this application, you will need a Developer Cloud Sandbox that can be requested from Terradue's [Portal](http://www.terradue.com/partners), provided user registration approval. 

A Developer Cloud Sandbox provides Earth Science data access services, and assistance tools for a user to implement, test and validate his application.
It runs in two different lifecycle modes: Sandbox mode and Cluster mode. 
Used in Sandbox mode (single virtual machine), it supports cluster simulation and user assistance functions in building the distributed application.
Used in Cluster mode (collections of virtual machines), it supports the deployment and execution of the application with the power of distributed computing processing over large datasets (leveraging the Hadoop Streaming MapReduce technology). 

### Installation 

Log on the developer sandbox and run these commands in a shell:

* Install **cioppy**

```bash
sudo yum install -y cioppy
```

* Install this application

```bash
cd
git clone git@github.com:Terradue/dcs-python-ndvi.git
cd dcs-python-ndvi
mvn install
```

### Submitting the workflow

Run this command in a shell:

```bash
ciop-simwf
```

Or invoke the Web Processing Service via the Sandbox dashboard.

### Community and Documentation

To learn more and find information go to 

* [Developer Cloud Sandbox](http://docs.terradue.com/developer) service 
* [USGS Landsat sample products](http://landsat.usgs.gov/product_samples.php) 

### Authors (alphabetically)

* Emmannuel Mathot 
* Fabrice Brito

### License

Copyright 2014 Terradue Srl

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
