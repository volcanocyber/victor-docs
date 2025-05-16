Remote Sensing
=====

Remote Sensing Overview
----------------
Remote sensing is a vital tool for earth scientists, and volcanologists in particular, as it allows for high frequency and high spatial resolution observations of volcanic activity.
Through our partnership with NASA's JPL, we are able to provide access to a wide range of remote sensing data, including thermal infrared and multispectral imagery.
VICTOR includes a number of tools for working with remote sensing data, including those from the Landsat and Sentinel satellites.
These tools are designed to help users analyze and visualize remote sensing data, as well as to perform various image processing tasks.


DIST_VICTOR
----------------

Using the Observational Products for End-Users from Remote Sensing Analysis (OPERA_) project, we have built a tool using the surface disturbance product suite.
The initial notebook is set up for users to have a painless experience with aquiring data, while also providing a detailed overview of the data and how to use it.
Before beginning, the user must register for an account_ with NASA's Earthdata, which is free and easy to do. Once registered, run the first two cells, and the workflow will ask the user to enter their username and password,
which wull be stored securely for later sessions.


Now, the notebook is ready to go. We provide an example using the Iceland 2024 eruption, though any eruption can be applied. The user can select their area of interest interactively on the embedded map, which
will then be extracted and formatted for downloading. The user must also select a time range, which will be used to filter the data. Finally, pick a name for the project, and specify thresholds for the cloud cover and overall overlap of the 
data granules that fit the spatiotemporal criteria. There are no more required user inputs, so technically, every cell can be run to the end of the notebook without fail. However,
the VICTOR team recommends a deeper analysis for users to familarize themselves with remote sensing data and its formatting. Intermediate cells demonstrate the filtering process,
the granules placement, and the layering of the data towards a raster format that is easier for programs to read. Continuing on, the first timestamp and some of its layers are overlaid
on a map. The final cells give a full time series of the eruption, as well as a binarized version of the data for use in calculating the area. This data is stored in the `vam` variable for further exploration.

This workflow is meant to serve as a comprehensive introduction to remote sensing, without diving too deep into the processing or analysis. Users are highly encouraged
to explore Earthdata and OPERA, as the uses and community for remote sensing data rapidly grows.

.. _account: https://urs.earthdata.nasa.gov/users/new

.. _OPERA: https://www.jpl.nasa.gov/go/opera/

FIRMS
-------

The Fire Information for Resource Management System (FIRMS) is a NASA project that provides near real-time fire data from the MODIS and VIIRS satellites. 
The FIRMS data is available through the NASA Earthdata API, which allows users to programmatically access the data. The FIRMS workflow, similar to the DIST
VICTOR workflow, allows users to download and process data from FIRMS, as well as to visualize and analyze the data. Once the user provides spatial and temporal bounds,
the data is all read into a Pandas dataframe and plotted, ready for further analysis by the user.