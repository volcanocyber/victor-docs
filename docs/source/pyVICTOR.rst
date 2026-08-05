pyVICTOR Library
===============

pyVICTOR Overview
-----------------

The `pyVICTOR` module provides raster, DEM, and cloud utilities for volcano science workflows.
It is designed for rapid access to geospatial data, visualization helpers, and common model output preprocessing tasks.

Function reference
------------------

.. function:: hillshade(array, azimuth, angle_altitude)

    Shades a raster with a given azimuth and angle for clearer visuals.
    
    Parameters
    ----------
    array : ndarray
        Raster data
    azimuth : float
        Horizontal angle from north (degrees)
    angle_altitude : float
        Angle of "sun" shading (degrees)
    
    Returns
    -------
    ndarray
        Shaded raster data

.. function:: plot_dem(dem, markercoords=np.array([]), axes=None, title=None)

    Experimental raster plotting function that does not require figure and axes to be passed.
    
    Parameters
    ----------
    dem : str
        Relative or absolute path to raster (can be either ASCII or TIFF)
    markercoords : ndarray, optional
        Optional ndarray to plot points for coordinates
    axes : matplotlib.axes.Axes, optional
        Existing axes object to plot into.
    title : str, optional
        Optional string to title plotted raster
    
    Returns
    -------
    tuple
        Matplotlib ``(fig, ax)`` objects used for the plot.

.. function:: plot_flow(dem, flow, coords=np.array([]), zoom=True, label='Thickness (m)', title=None, lognorm=False, axes=None, minimum=None, scale=None, colorbar=False)

    Raster+flow plotting, does not require figure and axes to be passed.
    
    Parameters
    ----------
    dem : str
        Relative or absolute path to raster (can be either ASCII or TIFF)
    flow : str
        Relative or absolute path to flow data (can be ASCII, TIFF, or CSV)
    coords : ndarray, optional
        ndarray to plot points for coordinates
    zoom : bool, optional
        Flag to display a section more tightly around AOI.
    label : str, optional
        String to label flow colorbar descriptor
    title : str, optional
        Optional string to title plotted raster
    lognorm : bool, optional
        If True, use logarithmic scaling for flow raster values.
    axes : matplotlib.axes.Axes, optional
        Existing axes object to plot into.
    minimum : float, optional
        Minimum value for logarithmic color scaling.
    scale : float, optional
        Maximum value for logarithmic color scaling.
    colorbar : bool, optional
        If True, add a colorbar for the flow raster.
    
    Returns
    -------
    matplotlib.collections.QuadMesh
        Flow raster plot object.

.. function:: plot_titan(dem, step, fig, ax, coords, zoom=True, epsg=32628, save_csv=True, sim_dir='.')

    Specialized plotting function for TITAN2D.
    
    Parameters
    ----------
    dem : str
        Relative or absolute path to raster (can be either ASCII or TIFF)
    step : int
        Integer to specify step number of titan output.
    fig : matplotlib.figure.Figure
        Matplotlib figure to assign raster.
    ax : cartopy.mpl.geoaxes.GeoAxesSubplot
        Matplotlib geoaxes to assign raster.
    coords : numpy.ndarray or None
        Optional ndarray to plot points for coordinates.
    step : int
        Simulation step index used to select TITAN2D output.
    zoom : bool, optional
        Flag to display a section more tightly around AOI.
    epsg : int, optional
        Projection, recommended to include same input as geoaxes.
    save_csv : bool, optional
        Flag to save output fdata to CSV format (more readable than xdmf).
    sim_dir : str, optional
        Parent directory of vizout.
    
    Returns
    -------
    None

.. function:: plot_benchmark(dem, flow, fig, ax, coords=None, zoom=True, model=None, label='Thickness of residual (m)', vmax=None, epsg=32628, outline=None)

    Plots benchmark data and flow data on a geoaxes.
    
    Requires geoaxes and figure to be passed along with simulation step number.
    
    Parameters
    ----------
    dem : str
        Relative or absolute path to raster (can be either ASCII or TIFF)
    flow : str
        Relative or absolute path to flow data (can be ASCII, TIFF, or CSV)
    fig : matplotlib.figure.Figure
        Matplotlib figure to assign raster
    ax : cartopy.mpl.geoaxes.GeoAxesSubplot
        Matplotlib geoaxes to assign raster
    coords : numpy.ndarray or None, optional
        Optional ndarray to plot points for coordinates
    zoom : bool, optional
        Flag to display a section more tightly around AOI.
    model : str or None, optional
        String specifically used to specify Mr Lava Loba due to unique output format
    label : str, optional
        Optional string to label flow colorbar descriptor
    vmax : int or None, optional
        Optional integer to limit/scale maximum value
    epsg : int, optional
        Projection, recommended to include same input as geoaxes.
    outline : str or None, optional
        Relative or absolute path to raster to be used for contour outline
    
    Returns
    -------
    flow_plotted : matplotlib.collections.QuadMesh
        Plot object
    maxval : float
        Maximum value in flow data

.. function:: make_titan_gif(dem, fig, ax, coords, max_iter, diter, gif_name, epsg=32628, sim_dir='.')

    Creates a gif from all TITAN2D steps.
    
    Requires geoaxes and figure to be passed along with simulation step number.
    
    Parameters
    ----------
    dem : str
        Relative or absolute path to raster (can be either ASCII or TIFF)
    fig : matplotlib.figure.Figure
        Matplotlib figure to assign raster
    ax : cartopy.mpl.geoaxes.GeoAxesSubplot
        Matplotlib geoaxes to assign raster
    coords : numpy.ndarray
        Array to plot points for coordinates
    max_iter : int
        Total iterations TITAN2D output (for calculations)
    diter : int
        Time interval chosen for TITAN2D output
    gif_name : str
        Name of output gif
    epsg : int, optional
        Projection, recommended to include same input as geoaxes. Defaults to 32628.
    sim_dir : str, optional
        Parent directory of vizout. Defaults to '.'.

.. function:: download_file_gcp(bucket_name, source_blob_name, destination_file_name, api_creds_json)

    Downloads a blob from the specified Google Cloud bucket.
    
    Parameters
    ----------
    bucket_name : str
        The ID of your Google Cloud bucket.
    source_blob_name : str
        The ID of your Google Cloud object.
    destination_file_name : str
        The path to which the file should be downloaded.
    api_creds_json : str
        The relative or absolute path to the JSON file containing the Google Cloud API credentials.
    
    Returns
    -------
    None

.. function:: upload_file_gcp(bucket_name, source_file_name, destination_blob_name, api_cred_json)

    Uploads a file to the specified Google Cloud bucket.
    
    Parameters
    ----------
    bucket_name : str
        The ID of your Google Cloud bucket.
    source_file_name : str
        The path to your file to upload.
    destination_blob_name : str
        The ID of your GCS object.
    api_cred_json : str
        The relative or absolute path to the JSON file containing the Google Cloud API credentials.
    
    Returns
    -------
    None

.. function:: download_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None)

    Downloads a file from AWS S3 Bucket.
    
    Parameters
    ----------
    access_key : str
        Public access key for bucket.
    secret_access_key : str
        Private IAM access key for bucket.
    bucket_name : str:
        The ID of your AWS S3 bucket.
    blob_name:
        The ID of your AWS S3 object.
    file_name : str
        The path to which the file should be downloaded.
    session_token: str, optional
        Optional string to continue an existing S3 connection. Defaults to None.
    
    Returns
    -------
    None

.. function:: upload_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None)

    Uploads a file to AWS S3 Bucket.
    
    Parameters
    ----------
    access_key : str
        Public access key for bucket.
    secret_access_key : str
        Private IAM access key for bucket.
    bucket_name : str:
        The ID of your AWS S3 bucket.
    blob_name:
        The ID of your AWS S3 object.
    file_name : str
        The path to the file going to be uploaded.
    session_token: str, optional
        Optional string to continue an existing S3 connection. Defaults to None.
    
    Returns
    -------
    None

.. function:: download_from_azure(conn_string, container_name, blob_name, local_file_name)

    Downloads a file from Azure container service
    
    Args:
        conn_string (str): Connection string to create session with Azure
        container_name (str): The ID of the Azure bucket
        blob_name (str): The ID of the file to download
        local_file_name (str): The name to assign once the file is downloaded

.. function:: upload_to_azure(conn_string, container_name, blob_name, local_file_name)

    Uploads a file to Azure container service.
    
    Args:
        conn_string (str): Connection string to create session with Azure.
        container_name (str): The ID of the Azure bucket.
        blob_name (str): The ID of the file once uploaded to the container.
        local_file_name (str): The name/path of the local file to upload.

.. function:: download_dem(north, south, east, west, outputFormat, dataset, filename='', api_key='3ac3c07f20ee63fd3babe7884f24e2c3')

    Download a DEM from the OpenTopography API based on latitude and longitude bounds.
    
    Parameters:
        north : float
            North latitude bound of the Area of Interest (AOI).
        south : float
            South latitude bound of the AOI.
        east : float
            East longitude bound of the AOI.
        west : float
            West longitude bound of the AOI.
        outputFormat : str
            Format of the output file. Choose between 'ascii' and 'tiff'.
        dataset : str
            Satellite dataset to pull data from.
            Available datasets:
                SRTMGL3 (SRTM GL3 90m)
                SRTMGL1 (SRTM GL1 30m)
                SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)
                AW3D30 (ALOS World 3D 30m)
                AW3D30_E (ALOS World 3D Ellipsoidal, 30m)
                SRTM15Plus (Global Bathymetry SRTM15+ V2.1)
                NASADEM (NASADEM Global DEM)
                COP30 (Copernicus Global DSM 30m)
                COP90 (Copernicus Global DSM 90m)
                EU_DTM (DTM 30m)
    
    Returns
    -------
    File name on success
    File name if exact file already exists
    -1 on failure

.. function:: search_opentopo(minx, maxx, miny, maxy, detail=False, federated=True)

    Allows user to search for available datasets in the OpenTopography library.
    
    Parameters
    ----------
    minx : float
        Leftmost longitude bound of AOI
    maxx : float
        Rightmost longitude bound of AOI
    miny : float
        Lowest latitude bound of AOI
    maxy : float
        Highest latitude bound of API
    detail : bool, optional
        Toggle to show detailed metadata. Default is False.
    federated : bool, optional
        Toggle to ignore non federated datasets, such as USGS. Default is True.
    
    Returns
    -------
    list of dict
        Datasets available in the specified AOI and API range.

.. function:: download_dem_usgs(north, south, east, west, outputFormat, res, filename='')

    Download USGS DEM using OpenTopography API.
    
    Parameters
    ----------
    north : float
        North latitude bound of Area of Interest (AOI).
    south : float
        South latitude bound of AOI.
    east : float
        East longitude bound of AOI.
    west : float
        West longitude bound of AOI.
    outputFormat : str
        Output format of the DEM file. Choose between 'ascii' and 'tif'.
    res : str
        Resolution of the DEM. Choose between '1m', '10m', and '30m'.
    
    Returns
    -------
    None on success
    -1 if latitude or longitude range is invalid
    1 if file already exists,

.. function:: download_dem_utm(north, south, east, west, hemisphere, utm_zone, outputFormat, dataset, filename='')

    Download a DEM from the OpenTopography API based on UTM coordinates and respective zones.
    
    Parameters
    ----------
    north : float
        North bound of the Area of Interest (AOI).
    south : float
        South bound of the AOI.
    east : float
        East bound of the AOI.
    west : float
        West bound of the AOI.
    nw_zone : str
        Zone of the top left corner of the AOI.
    se_zone : str
        Zone of the bottom right corner of the AOI.
    outputFormat : str
        Format of the output file. Choose between 'ascii' and 'tif'.
    dataset : str
        Satellite dataset to pull data from.
        Available datasets:
            SRTMGL3 (SRTM GL3 90m)
            SRTMGL1 (SRTM GL1 30m)
            SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)
            AW3D30 (ALOS World 3D 30m)
            AW3D30_E (ALOS World 3D Ellipsoidal, 30m)
            SRTM15Plus (Global Bathymetry SRTM15+ V2.1)
            NASADEM (NASADEM Global DEM)
            COP30 (Copernicus Global DSM 30m)
            COP90 (Copernicus Global DSM 90m)
            EU_DTM (DTM 30m)
    
    Returns
    -------
    None on success
    -1 if latitude or longitude range is invalid
    1 if file already exists,

.. function:: dem_to_utm(infile, outfile=None)

    Converts an ascii file in lat/lon to UTM.
    
    Parameters
    ----------
    infile : str
        Relative or absolute path to DEM.
    outfile : str, optional
        Optional string to save new file to, will overwrite original otherwise.
    
    Returns
    -------
    None

.. function:: dem_to_latlong(infile, utm_zone, outfile=None)

    Converts an ascii file in UTM to lat/lon
    
    Parameters
    ----------
    infile : str
        Relative or aboslute path to DEM
    utm_zone : str
        Required string in number-letter format to specify area
    outfile : str, optional
        Optional string to save new file to, will overwrite original otherwise.
    
    Returns
    -------
    None

.. function:: find_arctic_cell(lat, lon)

    Find the Arctic cell coordinates based on the given latitude and longitude.
    
    Parameters
    ----------
    lat : float
        The latitude of the point.
    lon : float
        The longitude of the point.
    
    Returns
    -------
    list : str
        A list containing the northing, easting, northing_subtile, and easting_subtile coordinates.

.. function:: download_arcticdem(lat, lon)

    Downloads Arctic DEM tiles based on the given latitude and longitude.
    
    Parameters:
        lat (float): The latitude of the point.
        lon (float): The longitude of the point.
    
    Returns
    -------
    None
    
    Example usage:
        download_arcticdem(60.0, -10.0)

.. function:: search_volcano(name)

    Searches for a volcano with a given name in the Excel file "/home/jovyan/shared/Libraries/GVP_Volcano_List_Holocene.xlsx" and returns an array of volcano information.
    
    Parameters
    ----------
    name : str
        The name of the volcano to search for.
    
    Returns
    -------
    vals: numpy.ndarray
        An array of volcano information, with each row containing the volcano name, latitude, longitude, and elevation (in meters).

.. function:: convert_molasses(output_name, resolution=20)

    Converts molasses data from a CSV file to a raster format using GeoPandas and rasterio.
    
    Parameters
    ----------
    output_name : str
        The name of the output raster file without the file extension.
    
    Returns
    -------
    None

.. function:: jaccard_similarity(observed, simulated)

    Calculate the Jaccard similarity coefficient between two rasters.
    
    Parameters
    ----------
    observed: str
        The path to the observed raster.
    simulated : str
        The path to the simulated raster.
    
    Returns
    -------
    Rj: float
        The Jaccard similarity coefficient between the two rasters.

.. function:: create_geotiff(data, output_path, x_min, y_min, pixel_width, pixel_height, crs=None, nodata_value=None)

    Create a georeferenced GeoTIFF using rasterio.
    
    Parameters:
    -----------
    data : numpy.ndarray
        2D or 3D array of raster data
    output_path : str
        Path to save the output GeoTIFF
    x_min : float
        Minimum x coordinate (left edge of the raster)
    y_min : float
        Minimum y coordinate (bottom edge of the raster)
    pixel_width : float
        Width of each pixel in geographic units
    pixel_height : float
        Height of each pixel in geographic units (usually negative)
    crs : str or rasterio.crs.CRS, optional
        Coordinate Reference System 
    nodata_value : float, optional
        Value to represent no data
    
    Returns:
    --------
    bool
        True if successful, False otherwise

.. function:: get_firms_data(map_key, bounds, num_days, date=None)

    No docstring available.

.. function:: tiff_to_utm_ascii(input_tiff, output_ascii, utm_zone=None, utm_north=True)

    Convert a georeferenced DEM TIFF to UTM ASCII format
    
    Parameters:
        input_tiff (str): Path to input TIFF file
        output_ascii (str): Path to output ASCII file
        utm_zone (int, optional): UTM zone number. If None, will be determined from input
        utm_north (bool): True for northern hemisphere, False for southern

.. function:: convert_dem_format(input_tiff, output_path, output_format='ascii', utm_zone=None, utm_north=True)

    Convert a georeferenced DEM TIFF to UTM ASCII or UTM GeoTIFF format
    
    Parameters:
        input_tiff (str): Path to input TIFF file
        output_path (str): Path to output file (extension will be adjusted based on format)
        output_format (str): Output format - 'ascii' or 'geotiff'
        utm_zone (int, optional): UTM zone number. If None, will be determined from input
        utm_north (bool): True for northern hemisphere, False for southern

.. function:: ensure_utm(raster, input_crs=None, fallback='EPSG:4326')

    Ensures raster is in a UTM CRS.
    
    Parameters
    ----------
    raster : xarray.DataArray
    input_crs : str or CRS, optional
        CRS to assign if raster has none.
    fallback : str
        CRS to use if reprojection fails.
    
    Returns
    -------
    DataArray

.. function:: standardize_raster(r1, r2, r1_crs=None, r2_crs=None, folder=None, r1_output=None, r2_output=None)

    Standardize two rasters to a common grid.
    
    Parameters
    ----------
    r1, r2 : str
        Raster filenames.
    r1_crs, r2_crs : str, optional
        CRS to assign if the raster has no CRS.

.. function:: load_future_winds(experiment_id, source_id, variant_label, activity_id='ScenarioMIP', frequency='Amon', grid_label='gn')

    Load paired ua/va pressure-level winds from CMIP6.
    
    Returns
    -------
    xr.Dataset with variables:
        ua, va, wind_speed, wind_direction

.. function:: points_to_raster(df, east_col, north_col, value_col, output_path, epsg=None, resolution=1000, interpolation='linear', nodata=np.nan)

    Interpolates scattered point data from a DataFrame onto a regular grid
    and saves the result as a GeoTIFF raster.
    
    Coordinates in the DataFrame are expected to be in UTM (meters). If the
    EPSG code is not provided, it is inferred automatically from the centroid
    of the point cloud.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing easting, northing, and value columns.
    east_col : str
        Name of the column holding UTM easting values (meters).
    north_col : str
        Name of the column holding UTM northing values (meters).
    value_col : str
        Name of the column holding the values to rasterize (e.g. 'Kg/m^2').
    output_path : str
        File path for the output GeoTIFF (e.g. 'tephra_mass.tif').
    epsg : int, optional
        EPSG code for the UTM CRS (e.g. 32612). If None, inferred from the
        centroid of the point cloud via the utm library.
    resolution : float, optional
        Cell size of the output raster in the same units as the coordinates
        (meters). Default is 1000 (1 km).
    interpolation : str, optional
        Interpolation method passed to scipy.interpolate.griddata.
        Options are 'linear' (default), 'nearest', or 'cubic'.
    nodata : float, optional
        Value to assign to cells outside the convex hull of input points.
        Default is np.nan.
    
    Returns
    -------
    str
        Absolute path to the saved GeoTIFF file.
    
    Examples
    --------
    >>> victor.points_to_raster(
    ...     tephra_out,
    ...     east_col='#EAST',
    ...     north_col='NORTH',
    ...     value_col='Kg/m^2',
    ...     output_path='tephra_mass.tif',
    ...     resolution=1000
    ... )

