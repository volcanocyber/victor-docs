victor.py
=========

Victor Library Overview
-----------------------

The VICTOR library is, at its core, a collection of convenient custom functions for
downloading, accessing, manipulating, and visualizing datum that are vital to a volcano scientist's
research. As more models and wider functionality are added, the VICTOR library will grow.

.. code-block:: python
    
    plot_dem(dem, fig, ax, coords=None)

``dem``: The relative or absolute filepath to DEM. Must be an ascii shapefile or GeoTIFF format, as georeferencing is necessary for proper formatting.

``fig``: A ``matplotlib.figure`` object. This is the complete plot, both within the axes and outside.

``ax``: A ``matplotlib.axes`` object. This is the area concerning the data itself, as well as labels, titles, and the like.

``coords``: Optional parameter to add coordinates. If adding more than one set,
provide in [[x_1,y_1],[x_2,y_2],...] format in multidimensional array.

.. code-block:: python
    
    plot_flow(dem, flow, fig, ax, coords,zoom=True,model=None, label="Thickness of residual (m)"):

``dem``: The relative or absolute filepath to DEM. Must be an ASCII shapefile or GeoTIFF format, as georeferencing is necessary for proper formatting.

``flow``: The relative or absolute file path to the flow data. Can be ASCII, geoTIFF, or csv formatted (without headers).

``fig``: A ``matplotlib.figure`` object. This is the complete plot, both within the axes and outside.

``ax``: A ``matplotlib.axes`` object. This is the area concerning the data itself, as well as labels, titles, and the like.

``coords``: Optional parameter to add coordinates. If adding more than one set,
provide in [[x_1,y_1],[x_2,y_2],...] format in multidimensional array.

``zoom``: Optional parameter to toggle between close-up view around flow only, and view at the scale of the overall raster.

``model``: Optional parameter, can be ignored unless using MrLavaLoba model, where this should be set to "mrlavaloba" to account for a slight
variation in formatting.

``label``: Optional parameter to set the label for the color map in the plot, defaults to description of flow thickness.

.. code-block:: python

    def plot_titan(dem, flow, fig, ax, coords,zoom=True):

``dem``: The relative or absolute filepath to DEM. Must be in geoTIFF format, as georeferencing is necessary for proper formatting.

``flow``: Must be a Pandas dataframe.

``fig``: A ``matplotlib.figure`` object. This is the complete plot, both within the axes and outside.

``ax``: A ``matplotlib.axes`` object. This is the area concerning the data itself, as well as labels, titles, and the like.

``coords``: Optional parameter to add coordinates. If adding more than one set,
provide in [[x_1,y_1],[x_2,y_2],...] format in multidimensional array.

``zoom``: Optional parameter to toggle between close-up view around flow only, and view at the scale of the overall raster.

.. code-block:: python

    make_titan_gif(dem, fig, ax, coords, max_iter, diter, gif_name):

``dem``: The relative or absolute filepath to DEM. Must be in geoTIFF format, as georeferencing is necessary for proper formatting.

``fig``: A ``matplotlib.figure`` object. This is the complete plot, both within the axes and outside.

``ax``: A ``matplotlib.axes`` object. This is the area concerning the data itself, as well as labels, titles, and the like.

``coords``: Optional parameter to add coordinates. If adding more than one set,
provide in [[x_1,y_1],[x_2,y_2],...] format in multidimensional array.

``max_iter``: The maximium number of iterations provided by the user in Titan2D.

``diter``: The number of iterations between outputs, set by the user in the Titan2D input file.

``gif_name``: The name used to save the gif to your current directory.

.. code-block:: python

    def download_file_gcp(bucket_name, source_blob_name, destination_file_name, api_creds_json):

``bucket_name``: The name of the Google Cloud bucket that you would like to access.

``source_blob_name``: The name of the file you would like to download from the bucket.

``destination_file_name``: The name you would like the file to have when it is downloaded locally.

``api_creds_json``: The relative or absolute path to the JSON file with the user's credentials. To obtain this file
, refer to `this documentation from Google. <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating>`_ . Make sure
the IAM API is active, and follow the directions linked.

.. code-block:: python

    def upload_file_gcp(bucket_name, source_file_name, destination_blob_name,api_cred_json):

``bucket_name``: The name of the Google Cloud bucket that you would like to access.

``source_file_name``: The name of the local file that you would like to upload to the specified bucket.

``destination_blob_name``: The name you would like the file to have when it is uploaded.

``api_creds_json``: The relative or absolute path to the JSON file with the user's credentials. To obtain this file
, refer to `this documentation from Google. <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating>`_ . Make sure
the IAM API is active, and follow the directions linked.

.. code-block:: python

    def download_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None):

``access_key`` and ``secret_access_key``: These are unique identifiers for your AWS root or IAM account. `Refer to instructions here <https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/>`_
to learn how to get these identifiers.

``bucket_name``: The name of the S3 bucket that you would like to access.

``blob_name``: The name of the file you would like to download from the bucket.

``file_name``: The name you would like the file to have when it is downloaded locally.

``session_token``: An optional field, used for time-limited access to a bucket. Recommended only for advanced users, or those familar with AWS.

.. code-block:: python

    def upload_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None):

``access_key`` and ``secret_access_key``: These are unique identifiers for your AWS root or IAM account. `Refer to instructions here <https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/>`_
to learn how to get these identifiers.

``bucket_name``: The name of the S3 bucket that you would like to access.

``blob_name``: The name the file should have when uploaded to the S3 bucket.

``file_name``: The name (and path if not in the current directory) of the local file to upload. 

``session_token``: An optional field, used for time-limited access to a bucket. Recommended only for advanced users, or those familar with AWS.

.. code-block:: python

    def download_from_azure(conn_string, container_name, blob_name, local_file_name)

``conn_string``: A unique identifer to connect to an Azure storage. `Refer to Microsoft's documentation <https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json&tabs=azure-portal>`_ 
for information on how to get your connection string.

``container_name``: The name of the Azure storage module that you would like to access.

``blob_name``: The name of the file you would like to download from Azure storage.

``local_file_name``: The name you would like the file to have when downloaded locally.

.. code-block:: python

    def upload_to_azure(conn_string, container_name, blob_name, local_file_name)

``conn_string``: A unique identifer to connect to an Azure storage. `Refer to Microsoft's documentation <https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json&tabs=azure-portal>`_ 
for information on how to get your connection string.

``container_name``: The name of the Azure storage module that you would like to access.

``blob_name``: The name you would like the uploaded file to have in Azure storage.

``local_file_name``: The name (and path if not in the current directory) of the local file that should be uploaded.

.. code-block:: python

    def download_dem(north, south, east, west, outputFormat, dataset)

``north``: Upper bound for latitude.

``south``: Lower bound for latitude.

``east``: Right bound for longitude.

``west``: Left bound for longitude.

``outputFormat``: Allows you to request either an ASCII shapefile (AAIGrid) or GeoTIFF (GTiff) formatted DEM.

``dataset``: Allows you to choose from different DEM providers. This allows for for varying resolutions, as well as alternatives in case of missing data.
Additionally, some of the datasets include bathymetry, or unique coverage. The sets are defined as:
SRTMGL3, SRTMGL1, SRTMGL1_E, AW3D30, AW3D30_E, SRTM15Plus, NASADEM, COP30, COP90, EU_DTM.

.. code-block:: python

    def download_dem_utm(north, zone_north, south, zone_south, east, zone_east, west, zone_west, outputFormat, dataset):

``north``: Upper bound for northing in UTM.

``zone_north``: UTM zone for the upper bound northing coordinate, format as a string with the number, then the letter, i.e. "10S"

``south``: Lower bound for northing in UTM.

``zone_south``: UTM zone for the lower bound northing coordinate.

``east``: Right bound for easting in UTM.

``zone_west``: UTM zone for the right bound easting coordinate.

``west``: Left bound for easting in UTM.

``zone_west``: UTM zone for the left bound easting coordinate.

``outputFormat``: Allows you to request either an ASCII shapefile (AAIGrid) or GeoTIFF (GTiff) formatted DEM.

``dataset``: Allows you to choose from different DEM providers. This allows for for varying resolutions, as well as alternatives in case of missing data.
Additionally, some of the datasets include bathymetry, or unique coverage. The sets are defined as:
SRTMGL3, SRTMGL1, SRTMGL1_E, AW3D30, AW3D30_E, SRTM15Plus, NASADEM, COP30, COP90, EU_DTM.