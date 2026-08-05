"""pyVICTOR: utilities for volcano science raster, DEM, and cloud workflows."""

import glob
import math
import os
import subprocess
import urllib
from datetime import datetime
from pathlib import Path

import boto3
import geopandas as gpd
import h5py
import imageio
import intake
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyproj
import rasterio as rio
import requests
import rioxarray as rxr
import utm
import xarray as xr
import xrspatial as xrs
from botocore.exceptions import ClientError
from geocube.api.core import make_geocube
from google.cloud import storage
from osgeo import gdal
from pyproj import CRS
from rasterio.transform import from_bounds, from_origin
from rasterio.warp import Resampling, calculate_default_transform, reproject


def hillshade(array, azimuth, angle_altitude):
    """
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
    """
    # Subtract azimuth from 360 to get azimuth in Cartesian coordinates
    azimuth = 360.0 - azimuth 
    
    # Calculate gradient in x and y directions
    x, y = np.gradient(array)
    
    # Calculate slope and aspect
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    
    # Convert azimuth and angle_altitude to radians
    azimuthrad = azimuth*np.pi/180.
    altituderad = angle_altitude*np.pi/180.
    
    # Calculate shaded raster data
    shaded = np.sin(altituderad)*np.sin(slope) + \
             np.cos(altituderad)*np.cos(slope)* \
             np.cos((azimuthrad - np.pi/2.) - aspect)
    
    # Scale shaded raster data to range [0, 255]
    return 255*(shaded + 1)/2

def plot_dem(dem, markercoords=np.array([]), axes=None, title=None):
    """
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
    """
    if axes:
        ax = axes
    else:
        # Create a new axes object
        fig, ax = plt.subplots()
    
    # Open raster file using rasterio
    raster = rxr.open_rasterio(dem)
    # Select the first band of the raster
    raster = raster.sel({"band": 1})
    # Apply hillshade to the raster and plot it
    render = xrs.hillshade(raster, 45, 30)
    render.plot(ax=ax,cmap="gray",add_colorbar=False)
    # If coordinates are provided, scatter plot them
    if markercoords.any():
        if markercoords.ndim == 2:
            plt.scatter(markercoords[:, 0], markercoords[:, 1], color="red", marker="^")
        elif markercoords.ndim == 1:
            plt.scatter(markercoords[0], markercoords[1], color="red", marker="^")
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    # Set title of the plot
    ax.set_aspect("equal")
    if title is None:
        plt.title(dem)
    else:
        plt.title(title)
    return fig, ax
    
def plot_flow(dem, flow, coords=np.array([]), zoom=True, label="Thickness (m)", title=None, lognorm=False,axes=None,minimum=None, scale=None,colorbar=False):
    """
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
    """
    if axes:
        ax = axes
    else:
        # Create a new axes object
        ax = plt.axes()

    raster = rxr.open_rasterio(dem)
    bounds = raster.rio.bounds()
    # Select the first band of the raster
    raster = raster.sel({"band": 1})
    # Apply hillshade to the raster and plot it
    render = xrs.hillshade(raster, 45, 30)
    render.plot(ax=ax,cmap="gray",add_colorbar=False)
    # If coordinates are provided, scatter plot them
    if coords.any():
        if coords.ndim == 2:
            plt.scatter(coords[:, 0], coords[:, 1], color="red", marker="^")
        elif coords.ndim == 1:
            plt.scatter(coords[0], coords[1], color="red", marker="^")
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    # ax.axis('equal')
    
    # Check the file extension of the flow data
    filename, file_extension = os.path.splitext(flow)
    if file_extension == ".csv":
        # If the flow data is in CSV format, read it into a pandas DataFrame
        flow_data = pd.read_csv(flow)
        # Plot the flow data with color mapping to the 'THICKNESS' column
        sc = plt.plot(x=flow_data["EAST"], y=flow_data["NORTH"], c=flow_data["THICKNESS"], cmap="hot")
        plt.colorbar(sc, label=label, shrink=.6)
        
        # If zoom is True, set the x and y limits of the plot to the min and max values of the 'EAST' and 'NORTH' columns
        if zoom:
            ax.set_xlim(flow_data["EAST"].min(), flow_data["EAST"].max())
            ax.set_ylim(flow_data["NORTH"].min(), flow_data["NORTH"].max())
    else:
        # If the flow data is in raster format, open it using rasterio and select the first band
        
        flow_raster = rxr.open_rasterio(flow,masked=True)
        
        maxval = flow_raster.max()
        flow_raster = flow_raster.sel({"band": 1})
        flow_raster = flow_raster.where(flow_raster > 0)
        flow_raster = flow_raster.dropna(dim='x',how='all')
        flow_raster = flow_raster.dropna(dim='y',how='all')
        
        if lognorm:
            flow_render = flow_raster.plot(ax=ax, cmap="hot", norm=colors.LogNorm(vmin=flow_raster.min(), vmax=flow_raster.max()), cbar_kwargs={'label': label, 'shrink': .6})
        elif scale:
            if minimum:
                flow_render = flow_raster.plot(ax=ax, cmap="hot", norm=colors.LogNorm(vmin=minimum, vmax=scale), add_colorbar=False)
            else:
                flow_render = flow_raster.plot(ax=ax, cmap="hot", norm=colors.LogNorm(vmin=.1, vmax=scale), add_colorbar=False)
        else:
            if colorbar:
                flow_render = flow_raster.plot(ax=ax, cmap="hot", cbar_kwargs={'label': label, 'shrink': .6})
            else: 
                flow_render = flow_raster.plot(ax=ax, cmap="hot" ,add_colorbar=False)
        
        # If zoom is True, set the x and y limits of the plot to the min and max values of the x and y coordinates
        if zoom:
            padding_x = (flow_raster.x.max() - flow_raster.x.min())/4
            padding_y = (flow_raster.y.max() - flow_raster.y.min())/4
            ax.set_xlim(flow_raster.x.min()-padding_x, flow_raster.x.max()+padding_x)
            ax.set_ylim(flow_raster.y.min()-padding_y, flow_raster.y.max()+padding_y)
        else:
            ax.set_xlim(bounds[0],bounds[2])
            ax.set_ylim(bounds[1],bounds[3])
    ax.set_aspect('equal', adjustable='box')
    # Set title of the plot
    if title is None:
        ax.set_title(dem)
    else:
        ax.set_title(title)
    return flow_render
    
      
def plot_titan(dem, step, fig, ax, coords, zoom=True, epsg=32628, save_csv=True, sim_dir = '.'):
    """
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
    """

    # Format step number
    out = glob.glob('vizout/xdmf_p0000_*.h5')
    out = sorted(out)
    filename = out[step]
    # Read xdmf file and extract relevant data
    height = []
    with h5py.File(filename, 'r')  as h5f: # file will be closed when we exit from WITH scope
        connections = h5f.get("Mesh/Connections")
        points = h5f.get("Mesh/Points")
        height = h5f.get("Properties/PILE_HEIGHT")[:]
        centers = []
        for i in range(connections.shape[0]):
            midpoint = points[np.sort(connections[i,:])]
            out = np.mean(midpoint,axis=0)
            centers = np.append(centers,out,axis=0)
        centers = np.reshape(centers,(connections.shape[0],3))
    height = np.ndarray.flatten(height)
    df = {"X_CENTER": centers[:,0], 'Y_CENTER': centers[:,1], 'Z_CENTER': centers[:,2],'PILE_HEIGHT': height}
    df = pd.DataFrame(df)

    # Save data to CSV if save_csv flag is True
    if save_csv:
        df.to_csv("./titandata.csv")

    # Filter data based on nonzero pile height
    nonzero = df["PILE_HEIGHT"] > 0
    flow = df[nonzero]

    # Plot raster data
    raster = rio.open(dem)
    read_raster = raster.read()
    ax.imshow(hillshade(read_raster[0,:,:],120,30),cmap='Greys',vmin=0,vmax=300,transform=ccrs.epsg(epsg),
                 extent=(raster.bounds.left, raster.bounds.right, raster.bounds.bottom, raster.bounds.top))
    x_full_min, x_full_max = raster.bounds.left, raster.bounds.right
    y_full_min, y_full_max = raster.bounds.bottom, raster.bounds.top

    # Plot scatter plot of flow data
    sc = ax.scatter(x=flow["X_CENTER"], y=flow["Y_CENTER"], c=flow["PILE_HEIGHT"], s=1,
    cmap=plt.cm.hot)

    # Add colorbar
    cb = plt.colorbar(sc, shrink=.6)
    cb.set_label('Pile Height (m)', rotation=90)
    plt.title("Flow")

    # Set plot extent based on zoom flag
    x_zoom_min, x_zoom_max = min(flow["X_CENTER"])-1000, max(flow["X_CENTER"])+1000
    y_zoom_min, y_zoom_max = min(flow["Y_CENTER"])-1000, max(flow["Y_CENTER"])+1000
    ct = ax.contour(read_raster[0],
        cmap=plt.cm.copper,
        transform=ccrs.epsg(epsg)
    )
    ax.clabel(ct, ct.levels, inline=True, fontsize=9,colors="red")

    # Plot coordinates if provided
    x,y = coords[0],coords[1]
    ax.scatter(x,y,marker="^",c="black")

    # Set plot extent based on zoom flag or model
    if not zoom:
        x_min, x_max = x_full_min,x_full_max
        y_min, y_max = y_full_min,y_full_max
    else:
        x_min, x_max = x_zoom_min,x_zoom_max
        y_min, y_max = y_zoom_min,y_zoom_max
    ax.set_xlim(x_min,x_max)
    ax.set_ylim(y_min,y_max)
    ax.set_xticks(np.linspace(x_min, x_max,5))
    ax.set_yticks(np.linspace(y_min, y_max,10))
    ax.clabel(ct, ct.levels, inline=True, fontsize=9,colors="white")
    ax.set_title(f'''TITAN2D @ step {step}''', fontsize=16)

    return None
    
def plot_benchmark(dem, flow, fig, ax, coords=None, zoom=True, model=None, label="Thickness of residual (m)", vmax=None, epsg=32628, outline=None):
    """
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
    """
    # Extract file extension and open raster
    filename, file_extension = os.path.splitext(dem)
    if file_extension.lower() in [".tif", ".tiff", ".geotiff"]:
        raster = rio.open(dem)
        read_raster = raster.read()
    elif file_extension in [".asc", ".ascii"]:
        raster = rxr.open_rasterio(dem).drop('band')[0].rename({'x':'easting', 'y':'northing'})
        nodata = raster.attrs["_FillValue"]
        raster = raster.where(raster != nodata, np.nan)
    # Plot raster data
    ax.imshow(hillshade(read_raster[0,:,:] if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else raster,
                       225,25),cmap='Greys',vmin=0,transform=ccrs.epsg(epsg),
              extent=(raster.bounds.left if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else min(raster["easting"]),
                      raster.bounds.right if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else max(raster["easting"]),
                      raster.bounds.bottom if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else min(raster["northing"]),
                      raster.bounds.top if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else max(raster["northing"])))

    # Plot outline if specified
    if outline is not None:
        ct = rxr.open_rasterio(outline).drop('band')[0].plot.contour(ax=ax,
                                                                     cmap="white",
                                                                     transform=ccrs.epsg(epsg))

    # Plot flow data
    flow_thickness = rxr.open_rasterio(flow).drop('band')[0].rename({'x':'easting', 'y':'northing'})
    nodata = flow_thickness.attrs["_FillValue"]
    flow_thickness = flow_thickness.where(flow_thickness!=nodata, np.nan)
    maxval = float(flow_thickness.max())
    x_zoom_min, x_zoom_max = min(flow_thickness["easting"]).values-1000, max(flow_thickness["easting"]).values+1000
    y_zoom_min, y_zoom_max = min(flow_thickness["northing"]).values-1000, max(flow_thickness["northing"]).values+1000

    # Plot flow data with or without specified maximum value
    if vmax is None:
        flow_plotted = flow_thickness.plot(ax=ax,
                                           cmap=plt.cm.Wistia,
                                           add_colorbar=False,
                                           vmin=0, transform=ccrs.epsg(epsg))
    else:
        flow_plotted = flow_thickness.plot(ax=ax,
                                           cmap=plt.cm.Wistia,
                                           add_colorbar=False,
                                           vmin=0, vmax=vmax,
                                           transform=ccrs.epsg(epsg))

    # Plot coordinates if provided
    if coords is not None:
        if coords.ndim == 2:
            x, y = coords[:, 0], coords[:, 1]
        elif coords.ndim == 1:
            x, y = coords[0], coords[1]
        ax.scatter(x, y, marker="^", c="black")

    # Set plot extent based on zoom flag or model
    if not zoom:
        x_min, x_max = raster.bounds.left if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else min(flow_thickness["easting"]), raster.bounds.right if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else max(flow_thickness["easting"])
        y_min, y_max = raster.bounds.bottom if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else min(flow_thickness["northing"]), raster.bounds.top if file_extension.lower() in [".tif", ".tiff", ".geotiff"] else max(flow_thickness["northing"])
    elif model == "mrlavaloba":
        y1 = flow_thickness.idxmin(dim="northing")
        x1 = flow_thickness.idxmin(dim="easting")
        y2 = flow_thickness.idxmax(dim="northing")
        x2 = flow_thickness.idxmax(dim="easting")
        x_min = min(x1[~np.isnan(x1)]) - 1000
        x_max = max(x2[~np.isnan(x2)]) + 1000
        y_min = min(y1[~np.isnan(y1)]) - 1000
        y_max = max(y2[~np.isnan(y2)]) + 1000
    else:
        x_min, x_max = x_zoom_min,x_zoom_max
        y_min, y_max = y_zoom_min,y_zoom_max
        ax.set_xlim(x_min,x_max)
        ax.set_ylim(y_min,y_max)
        ax.set_xticks(np.linspace(x_min, x_max,5))
        ax.set_yticks(np.linspace(y_min, y_max,5))

    return flow_plotted,maxval
    
def make_titan_gif(dem, fig, ax, coords, max_iter, diter, gif_name, epsg=32628, sim_dir='.'):
    """
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
    """

    # Generate step numbers
    out = sorted(glob.glob('vizout/xdmf_p0000_*.h5'))

    # Generate frames for gif
    for step in range(len(out)):
        # Initialize figure and axes for each step
        fig = plt.figure(figsize=(12, 8))
        ax = plt.axes(projection=ccrs.epsg(epsg))

        # Plot TITAN output for current step
        plot_titan(dem, step, fig, ax, coords, zoom=False, sim_dir=sim_dir)
        print(step)
        # Save figure as png
        outname = "".join(("gif_files/flow_", str(step)))
        plt.savefig(outname)
        plt.close()

    # Read in frames for gif
    frames = []
    for i in range(len(out)):
        image = imageio.v2.imread(f'gif_files/flow_{i}.png')
        frames.append(image)

    # Create gif
    imageio.mimsave(gif_name,  # output gif
                    frames,  # array of input frames
                    duration=100)
    
def download_file_gcp(bucket_name, source_blob_name, destination_file_name, api_creds_json):
    """
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
    """

    # Set the environment variable for the Google Cloud API credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_creds_json

    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket using the bucket name
    bucket = storage_client.bucket(bucket_name)

    # Get the blob using the source blob name
    blob = bucket.blob(source_blob_name)

    # Download the blob to the destination file name
    blob.download_to_filename(destination_file_name)

    # Print a confirmation message
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )
    
def upload_file_gcp(bucket_name, source_file_name, destination_blob_name, api_cred_json):
    """
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
    """
    # Set the environment variable for the Google Cloud API credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_cred_json

    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket using the bucket name
    bucket = storage_client.bucket(bucket_name)

    # Get the blob using the destination blob name
    blob = bucket.blob(destination_blob_name)

    # Upload the file from the source file name to the blob
    blob.upload_from_filename(source_file_name)

    # Print a confirmation message
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def download_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None):
    """Downloads a file from AWS S3 Bucket.

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
    """
    # Create an S3 client with the provided access key and secret access key.
    # If a session token is provided, use it to establish the connection.
    if session_token == None:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
        )
    else:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token
        )

    try:
        # Download the file from the bucket to the specified file path.
        response = client.download_file(bucket_name, blob_name, file_name)
    except ClientError as e:
        # Print an error message if the access keys are incorrect.
        print("Incorrect access keys: please enter valid credentials")

    # Print a confirmation message indicating the file was successfully downloaded.
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            blob_name, bucket_name, file_name
        )
    )

def upload_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None):
    """Uploads a file to AWS S3 Bucket.

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
    """
    # Create an S3 client with the provided access key and secret access key.
    # If a session token is provided, use it to establish the connection.
    if session_token is None:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
        )
    else:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token
        )

    try:
        # Upload the file from the specified file path to the bucket with the specified object name.
        response = client.upload_file(file_name, bucket_name, blob_name)
    except ClientError as e:
        # Print an error message if the access keys are incorrect.
        print("Incorrect access keys: please enter valid credentials")

    # Print a confirmation message indicating the file was successfully uploaded.
    print(
        f"File {file_name} uploaded to {bucket_name} as {blob_name}."
    )

def download_from_azure(conn_string, container_name, blob_name, local_file_name):
    """
    Downloads a file from Azure container service

    Args:
        conn_string (str): Connection string to create session with Azure
        container_name (str): The ID of the Azure bucket
        blob_name (str): The ID of the file to download
        local_file_name (str): The name to assign once the file is downloaded
    """
    # Create a blob service client from the connection string
    from azure.storage.blob import BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)
    
    # Get a blob client for the specified container and blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Download the blob and write it to the specified local file
    with open(file=local_file_name, mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())
    
    # Print a confirmation message
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            blob_name, container_name, local_file_name
        )
    )
        
def upload_to_azure(conn_string, container_name, blob_name, local_file_name):
    """
    Uploads a file to Azure container service.

    Args:
        conn_string (str): Connection string to create session with Azure.
        container_name (str): The ID of the Azure bucket.
        blob_name (str): The ID of the file once uploaded to the container.
        local_file_name (str): The name/path of the local file to upload.
    """
    # Create a blob service client from the connection string
    from azure.storage.blob import BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)
    
    # Get a container client for the specified container
    container_client = blob_service_client.get_container_client(container=container_name)
    
    # Open the local file in binary mode and upload it to the container
    with open(file=local_file_name, mode="rb") as data:
        blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    
    # Print a confirmation message
    print(
        f"File {local_file_name} uploaded to {container_name} as {blob_name}."
    )

def download_dem(north, south, east, west, outputFormat, dataset,filename="",api_key="3ac3c07f20ee63fd3babe7884f24e2c3"):
    """Download a DEM from the OpenTopography API based on latitude and longitude bounds.

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
    """
    # Check if latitude and longitude bounds are valid
    if north < south:
        print("Invalid latitude range")
        return -1
    elif east < west:
        print("Invalid longitude range")
        return -1


    # Construct the URL for the API request
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    name = (
    f"{abs(int(north))}{'N' if north >= 0 else 'S'}_"
    f"{abs(int(east))}{'E' if east >= 0 else 'W'}_"
    f"{dataset}_{dt_string}"
)
    completedName = f"DEM_{name}"
    # Set the output format
    if outputFormat in ["ascii","asc","a"]:
        out = "AAIGrid"
        name = f"{name}.asc"
        completedName = f"{completedName}.asc"
    elif outputFormat in ["tif","tiff","geotiff","t"]:
        out = "GTiff"
        name = f"{name}.geotiff"
        completedName = f"{completedName}.geotiff"
    else:
        print("Invalid format. Choose from ['ascii', 'asc','a','tif','tiff','geotiff','t']")
        return -2

    # Check if the file already exists
    if os.path.isfile(completedName):
        print(f"File already exists with name {completedName}, exiting.")
        return completedName

    # Download the DEM file
    url = (
        f"https://portal.opentopography.org/API/globaldem?demtype={dataset}&south={south}&north={north}&west={west}&east={east}&outputFormat={out}&API_Key={api_key}"
    )
    response = urllib.request.urlopen(url)
    status_code = response.getcode()
    if status_code == 204:
        print("No coverage for specified dataset. Please choose another.")
        return 1
    elif status_code in [400, 401, 404]:
        print("Error in accessing OpenTopography. Check your input parameters or the site.")
        return -1
    urllib.request.urlretrieve(url, completedName)

    # Read the downloaded file
    with rio.open(completedName) as src:
        profile = src.profile
        data = src.read()

        # Set the new nodata value in the profile
        profile.update(nodata=0)
    
        if filename == "":
            # Write the output raster with the updated nodata value
            with rio.open(completedName, "w", **profile) as dst:
                dst.write(data)
            print(f"DEM downloaded as {completedName}")
            return completedName
        else:
            with rio.open(filename, "w", **profile) as dst:
                dst.write(data)
            print(f"DEM downloaded as {filename}")
            return filename

def search_opentopo(minx, maxx, miny, maxy, detail = False, federated = True):
    """
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
    """
    if miny > maxy:
        print("Invalid latitude range")
        return []
    elif minx > maxx:
        print("Invalid longitude range")
        return []
    include_federated = "true" if federated else "false"
    output_format = "json"
    url = (
        f"https://portal.opentopography.org/API/otCatalog?minx={minx}&miny={miny}"
        f"&maxx={maxx}&maxy={maxy}&detail={repr(detail)}&outputFormat={output_format}"
        f"&include_federated={include_federated}"
    )
    response = requests.get(url)
    jason = response.json()
    return jason.get("Datasets", [])

def download_dem_usgs(north: float, south: float, east: float, west: float,
                      outputFormat: str, res: str, filename=""):
    """Download USGS DEM using OpenTopography API.

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
    """
    # Check if latitude and longitude bounds are valid
    if north < south:
        print("Invalid latitude range")
        return -1
    elif east < west:
        print("Invalid longitude range")
        return -1

    # Construct URL for API request
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    name = f"{int(north)}N_{int(south)}S_{int(east)}W_{int(west)}E_usgs{res}_{dt_string}"
    completedName = f"DEM_{name}"
    # Set the output format
    if outputFormat in ["ascii","asc","a"]:
        out = "AAIGrid"
        name = f"{name}.asc"
        completedName = f"{completedName}.asc"
    elif outputFormat in ["tif","tiff","geotiff","t"]:
        out = "GTiff"
        name = f"{name}.geotiff"
        completedName = f"{completedName}.geotiff"
    else:
        print("Invalid format. Choose from ['ascii', 'asc','a','tif','tiff','geotiff','t']")
        return -2

    # Download DEM if it does not already exist
    if os.path.isfile(completedName):
        print(f"File already exists with name {completedName}, exiting.")
        return 1
    url = f"https://portal.opentopography.org/API/usgsdem?datasetName=USGS{res}&south={south}&north={north}&west={west}&east={east}&outputFormat={out}&API_Key=3ac3c07f20ee63fd3babe7884f24e2c3"
    urllib.request.urlretrieve(url, name)

    # Set nodata value to 0 and export the DEM
    with rio.open(name) as src:
        profile = src.profile
        data = src.read()

        # Set the new nodata value in the profile
        profile.update(nodata=0)

        # Write the output raster with the updated nodata value
    if filename == "":
        # Write the output raster with the updated nodata value
        with rio.open(completedName, "w", **profile) as dst:
            dst.write(data)
        os.remove(name)
        print(f"DEM downloaded as {completedName}")
        return completedName
    else:
        with rio.open(filename, "w", **profile) as dst:
            dst.write(data)
        os.remove(name)
        print(f"DEM downloaded as {filename}")
        return filename

    # Remove temporary file
    os.remove(name)
    
def download_dem_utm(north, south, east, west, hemisphere, utm_zone, outputFormat, dataset,filename=""):
    """
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
    """
    # Convert UTM coordinates to lat/lon
    if hemisphere.upper() == 'N':
        zone_str = f"{utm_zone}N"
    else:
        zone_str = f"{utm_zone}S"

    transformer = pyproj.Transformer.from_crs(
        f"+proj=utm +zone={utm_zone} +{hemisphere.lower()}", 
        "EPSG:4326", 
        always_xy=True
    )

    east, south = transformer.transform(east, south)
    west, north = transformer.transform(west, north)
    # Check if latitude and longitude bounds are valid
    if north < south:
        print("Invalid latitude range")
        return -1
    elif east < west:
        print("Invalid longitude range")
        return -1

    # Construct URL for API request
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    name = f"DEM_utm_{int(north)}N_{int(south)}S_{int(east)}W_{int(west)}E_{dataset}_{dt_string}" if filename == "" else filename 
    # Set output format
    if outputFormat in ["ascii","asc","a"]:
        out = "AAIGrid"
        name = f"{name}.asc"
    elif outputFormat in ["tif","tiff","geotiff","t"]:
        out = "GTiff"
        name = f"{name}.geotiff"
    else:
        print("Invalid format. Choose from ['ascii', 'asc','a','tif','tiff','geotiff','t']")
        return -2

    # Download DEM if it does not already exist
    if os.path.isfile(name):
        print(f"File already exists with name {name}, exiting.")
        return 1
    url = (f"https://portal.opentopography.org/API/globaldem?demtype={dataset}&south={south}"
           f"&north={north}&west={west}&east={east}&outputFormat={out}&API_Key=3ac3c07f20ee63fd3babe7884f24e2c3")
    urllib.request.urlretrieve(url, name)
    print(f"DEM downloaded as {name}")
    
def dem_to_utm(infile, outfile=None):
    """
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
    """
    # Read DEM file
    f = open(infile,'r').readlines()
    
    # Extract coordinates and spacing
    xll = f[2]
    long = float(xll.split()[1])
    yll = f[3]
    lat = float(yll.split()[1])
    spacing = f[4]
    
    # Convert dx and dy to UTM coordinates
    if spacing.split()[0] == "dx":
        convert_dx = float(spacing.split()[1])*111319.48
        new_dx = "".join(("dx","    ",str(convert_dx),"\n"))
        dy = f[5]
        convert_dy = float(dy.split()[1])*111319.48
        new_dy = "".join(("dy","    ",str(convert_dy),"\n"))
        f[4] = new_dx
        f[5] = new_dy
    else:
        convert_spacing = float(spacing.split()[1])*111319.48
        new_spacing = "".join(("cellsize","    ",str(convert_spacing),"\n"))
        f[4] = new_spacing
    
    # Convert latitude and longitude to UTM coordinates
    translated = utm.from_latlon(lat,long)
    new_xll = "".join(("xllcorner","    ",str(translated[0]),"\n"))
    new_yll = "".join(("yllcorner","    ",str(translated[1]),"\n"))
    f[2] = new_xll
    f[3] = new_yll
    
    # Write new file
    if outfile == None:
        outfile = infile
    f2 = open(outfile,"w")
    f2.writelines(f)

def dem_to_latlong(infile, utm_zone, outfile=None):
    """Converts an ascii file in UTM to lat/lon

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
    """
    # Read DEM file
    f = open(infile,'r').readlines()
    
    # Extract coordinates and spacing
    xll = f[2]
    long = float(xll.split()[1])
    yll = f[3]
    lat = float(yll.split()[1])
    spacing = f[4]
    
    # Convert dx and dy to UTM coordinates
    if spacing.split()[0] == "dx":
        convert_dx = float(spacing.split()[1])/111319.48
        new_dx = "".join(("dx","    ",str(convert_dx),"\n"))
        dy = f[5]
        convert_dy = float(dy.split()[1])/111319.48
        new_dy = "".join(("dy","    ",str(convert_dy),"\n"))
        f[4] = new_dx
        f[5] = new_dy
    else:
        convert_spacing = float(spacing.split()[1])/111319.48
        new_spacing = "".join(("cellsize","    ",str(convert_spacing),"\n"))
        f[4] = new_spacing
    
    # Convert latitude and longitude to UTM coordinates
    if len(utm_zone) == 2:
        translated = utm.to_latlon(long,lat,int(utm_zone[0]),utm_zone[1])
    elif len(utm_zone) == 3:
        translated = utm.to_latlon(long,lat,int(utm_zone[0:2]),utm_zone[2])
    new_xll = "".join(("xllcorner", "    ", str(translated[0]),"\n"))
    new_yll = "".join(("yllcorner", "    ", str(translated[1]),"\n"))
    f[2] = new_xll
    f[3] = new_yll
    
    # Write new file
    if outfile == None:
        outfile = infile
    f2 = open(outfile,"w")
    f2.writelines(f)

def find_arctic_cell(lat, lon):
    """
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
    """
    easting = int(np.floor((lon+4000000)/100000))+1
    northing = int(np.floor((lat+4000000)/100000))+1
    easting_subtile = 1 if (((lon+4000000)/100000)+1 - easting) < .5 else 2
    northing_subtile = 1 if (((lat+4000000)/100000)+1 - northing) < .5 else 2
    return [northing, easting, northing_subtile, easting_subtile]

def download_arcticdem(lat, lon):
    """
    Downloads Arctic DEM tiles based on the given latitude and longitude.

    Parameters:
        lat (float): The latitude of the point.
        lon (float): The longitude of the point.

    Returns
    -------
    None

    Example usage:
        download_arcticdem(60.0, -10.0)
    """
    myProj = pyproj.Proj("+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs")
    transformed = myProj.transform(lat, lon)
    tile_data= np.array([find_arctic_cell(transformed[0], transformed[1])])
    boundaries = np.array([[transformed[0] + 5000, transformed[1] + 5000],[transformed[0] - 5000, transformed[1] + 5000], [transformed[0] - 5000, transformed[1] - 5000], [transformed[0] + 5000, transformed[1] - 5000]])
    for edge in boundaries:
        cell = find_arctic_cell(edge[0],edge[1])
        if (cell not in tile_data.tolist()):
            tile_data = np.vstack([tile_data,cell])
    for i in range(len(tile_data)):
        filename = f"""{tile_data[i,0]}_{tile_data[i,1]}/{tile_data[i,0]}_{tile_data[i,1]}_{tile_data[i,2]}_{tile_data[i,3]}_2m_v3.0.tar.gz"""
        string = f"""wget -r -N -nH -np -R index.html* --cut-dirs=6 https://data.pgc.umn.edu/elev/dem/setsm/ArcticDEM/mosaic/v3.0/2m/{filename}"""
        subprocess.run(string,shell=True)
        subprocess.run(f"tar -xvzf {filename}",shell=True)

def search_volcano(name):
    """
    Searches for a volcano with a given name in the Excel file "/home/jovyan/shared/Libraries/GVP_Volcano_List_Holocene.xlsx" and returns an array of volcano information.

    Parameters
    ----------
    name : str
        The name of the volcano to search for.

    Returns
    -------
    vals: numpy.ndarray
        An array of volcano information, with each row containing the volcano name, latitude, longitude, and elevation (in meters).

    """
    # Read the Excel file containing volcano information
    df = pd.read_excel("/home/jovyan/shared/Libraries/GVP_Volcano_List_Holocene.xlsx", header=1)

    # Search for a volcano with a name matching the given input
    parsed = df.loc[df['Volcano Name'].str.contains(name, case=False)]

    # Convert the filtered data to a numpy array
    vals = np.array((parsed["Volcano Name"].values, parsed["Latitude"].values, parsed["Longitude"].values, parsed["Elevation (m)"].values))

    return vals

# def download_volcano_dem(name):

def convert_molasses(output_name, resolution=20):
    """
    Converts molasses data from a CSV file to a raster format using GeoPandas and rasterio.

    Parameters
    ----------
    output_name : str
        The name of the output raster file without the file extension.

    Returns
    -------
    None

    """
    colnames=['EAST', 'NORTH', 'THICKNESS', 'NEW_ELEV', 'ORIG_ELEV'] 
    lava = pd.read_csv('./flow_-0', skiprows=3, names=colnames, sep='\s+', header= None)
    lava.to_csv("flow.csv",header=colnames,index=False)
    df = gpd.pd.read_csv('flow.csv')
    gf = gpd.GeoDataFrame(df, 
                          geometry=gpd.points_from_xy(df.EAST, df.NORTH), 
                          crs=4326)
    geo_grid = make_geocube(vector_data=gf, measurements=['THICKNESS'], resolution=resolution)
    geo_grid = geo_grid.THICKNESS.rio.write_nodata(-9999)
    geo_grid = geo_grid.fillna(-9999)
    geo_grid.rio.to_raster("".join([output_name,".asc"]))

def jaccard_similarity(observed, simulated):
    """
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
    """
    with rio.open(observed) as src:
        profile = src.profile
        transform = src.transform
        observed_feature = src.read(1)
        print(f"Observed Feature Raster Geographic Coordinates --> {src.crs}") 
        # implicitely prints the coordinate system and explicitely prints
        # the coordinates

    # Open and read the simulated feature raster
    with rio.open(simulated) as src: # input your simulater raster 
        # GeoTIFF file here
        profile = src.profile
        transform = src.transform
        simulated_feature = src.read(1)
        print(f"Simulated Feature Raster Geographic Coordinates --> {src.crs}") 
        # implicitely prints the coordinate system and explicitely prints
        # the coordinates

    # Calculate the areas inundated: True Positives (TP), False Positives (FP), 
    # and False Negatives (FN)
    
    TP = np.sum(np.logical_and(observed_feature > 0, simulated_feature > 0))
    FP = np.sum(np.logical_and(observed_feature == 0, simulated_feature > 0)) 
    FN = np.sum(np.logical_and(observed_feature > 0, simulated_feature == 0)) 

    # Calculate the Bayesian Metrics: Jaccard similarity coefficient (Rj), 
    # model precision (Rmp), and model sensitivity (Rms)
    Rj = (np.sum(TP) / (np.sum(TP) + np.sum(FN) + np.sum(FP))) * 100
    return Rj

def create_geotiff(
    data, 
    output_path, 
    x_min, 
    y_min, 
    pixel_width, 
    pixel_height, 
    crs=None, 
    nodata_value=None
):
    """
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
    """
    try:
        # Ensure data is a numpy array
        data = np.array(data)
        
        # Handle 2D and 3D arrays
        if data.ndim == 2:
            data = data[np.newaxis, :, :]
        
        # Create transformation from origin
        transform = from_origin(x_min, y_min + abs(data.shape[1] * pixel_height), 
                                pixel_width, abs(pixel_height))
        
        # Determine data type and number of bands
        dtype = data.dtype
        count = data.shape[0]
        
        # Write the raster
        with rio.open(
            output_path, 
            'w', 
            driver='GTiff',
            height=data.shape[1], 
            width=data.shape[2], 
            count=count,
            dtype=dtype,
            crs=crs,
            transform=transform,
            nodata=nodata_value
        ) as dst:
            for i in range(count):
                dst.write(data[i], i+1)
        
        print(f"GeoTIFF created successfully with rasterio at {output_path}")
        return True
    
    except Exception as e:
        print(f"Error creating GeoTIFF with rasterio: {e}")
        return False

def get_firms_data(map_key, bounds, num_days, date=None):
    area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + map_key + f'/VIIRS_NOAA21_NRT/{bounds[0]},{bounds[2]},{bounds[1]},{bounds[3]}/{num_days}/'
    if date is not None:
        area_url += date
    df_area = pd.read_csv(area_url)
    df_custom_day = df_area[((df_area['confidence'] == 'n') | (df_area['confidence'] == 'h')) & (df_area['frp'] >= 5)]
    return df_custom_day

def tiff_to_utm_ascii(input_tiff, output_ascii, utm_zone=None, utm_north=True):
    """
    Convert a georeferenced DEM TIFF to UTM ASCII format
    
    Parameters:
        input_tiff (str): Path to input TIFF file
        output_ascii (str): Path to output ASCII file
        utm_zone (int, optional): UTM zone number. If None, will be determined from input
        utm_north (bool): True for northern hemisphere, False for southern
    """
    gdal.UseExceptions()
    # Open the input TIFF file
    print(f"Opening {input_tiff}...")
    src = rio.open(input_tiff)
    
    # Determine UTM zone if not provided
    if utm_zone is None:
        # Calculate the central longitude of the image
        bounds = src.bounds
        center_lon = (bounds.left + bounds.right) / 2
        utm_zone = int((center_lon + 180) / 6) + 1
        print(f"Automatically determined UTM zone: {utm_zone}")
    
    # Define UTM projection
    hemisphere = "north" if utm_north else "south"
    dst_crs = f"EPSG:{32600 + utm_zone}" if utm_north else f"EPSG:{32700 + utm_zone}"
    print(f"Using UTM zone {utm_zone} {hemisphere} (CRS: {dst_crs})")

    # Calculate the transform parameters
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    
    # Create temporary reprojected TIFF
    temp_tiff = f"{os.path.splitext(output_ascii)[0]}_utm_temp.tif"
    
    # Create the output raster
    dst_profile = src.profile.copy()
    dst_profile.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })
    
    print("Reprojecting to UTM...")
    with rio.open(temp_tiff, 'w', **dst_profile) as dst:
        # Reproject the data
        for i in range(1, src.count + 1):
            reproject(
                source=rio.band(src, i),
                destination=rio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear)
    
    # Convert to ASCII grid
    print(f"Converting to ASCII format: {output_ascii}")
    gdal_options = gdal.TranslateOptions(format='AAIGrid')
    gdal.Translate(output_ascii, temp_tiff, options=gdal_options)
    
    # Clean up temporary file
    if os.path.exists(temp_tiff):
        os.remove(temp_tiff)
        os.remove("".join((output_ascii,".aux.xml")))
        
    print(f"Conversion complete. ASCII file saved to: {output_ascii}")
    
def convert_dem_format(input_tiff, output_path, output_format='ascii', utm_zone=None, utm_north=True):
    """
    Convert a georeferenced DEM TIFF to UTM ASCII or UTM GeoTIFF format
    
    Parameters:
        input_tiff (str): Path to input TIFF file
        output_path (str): Path to output file (extension will be adjusted based on format)
        output_format (str): Output format - 'ascii' or 'geotiff'
        utm_zone (int, optional): UTM zone number. If None, will be determined from input
        utm_north (bool): True for northern hemisphere, False for southern
    """
    gdal.UseExceptions()
    
    # Validate output format
    if output_format.lower() not in ['ascii', 'geotiff']:
        raise ValueError("output_format must be 'ascii' or 'geotiff'")
    
    # Open the input TIFF file
    print(f"Opening {input_tiff}...")
    src = rio.open(input_tiff)
    
    # Check if reprojection is needed
    needs_reprojection = False
    
    # Check if input is in geographic coordinates (EPSG:4326 or similar)
    if src.crs and src.crs.is_geographic:
        needs_reprojection = True
        print(f"Input CRS is geographic: {src.crs}")
    elif src.crs and 'utm' not in str(src.crs).lower():
        # Check if it's already in UTM
        needs_reprojection = True
        print(f"Input CRS: {src.crs}")
    else:
        print(f"Input appears to already be in UTM: {src.crs}")
    
    # Determine output file extension and path
    base_path = os.path.splitext(output_path)[0]
    if output_format.lower() == 'ascii':
        final_output = f"{base_path}.asc"
    else:  # geotiff
        final_output = f"{base_path}.tif"
    
    if needs_reprojection:
        # Determine UTM zone if not provided
        if utm_zone is None:
            # Calculate the central longitude of the image
            bounds = src.bounds
            center_lon = (bounds.left + bounds.right) / 2
            utm_zone = int((center_lon + 180) / 6) + 1
            print(f"Automatically determined UTM zone: {utm_zone}")
        
        # Define UTM projection
        hemisphere = "north" if utm_north else "south"
        dst_crs = f"EPSG:{32600 + utm_zone}" if utm_north else f"EPSG:{32700 + utm_zone}"
        print(f"Reprojecting to UTM zone {utm_zone} {hemisphere} (CRS: {dst_crs})")
        
        # Calculate the transform parameters
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        
        # Create temporary reprojected TIFF
        temp_tiff = f"{base_path}_utm_temp.tif"
        
        # Create the output raster profile
        dst_profile = src.profile.copy()
        dst_profile.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        
        print("Reprojecting to UTM...")
        with rio.open(temp_tiff, 'w', **dst_profile) as dst:
            # Reproject the data
            for i in range(1, src.count + 1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.bilinear)
        
        # Use the reprojected file as source for final output
        source_file = temp_tiff
    else:
        # Use original file directly
        source_file = input_tiff
        temp_tiff = None
    
    # Convert to final output format
    if output_format.lower() == 'ascii':
        print(f"Converting to ASCII format: {final_output}")
        gdal_options = gdal.TranslateOptions(format='AAIGrid')
        gdal.Translate(final_output, source_file, options=gdal_options)
        
        # Clean up auxiliary files
        aux_file = f"{final_output}.aux.xml"
        if os.path.exists(aux_file):
            os.remove(aux_file)
            
    else:  # geotiff
        if needs_reprojection:
            # Rename temp file to final output
            print(f"Saving UTM GeoTIFF: {final_output}")
            if temp_tiff != final_output:
                os.rename(temp_tiff, final_output)
                temp_tiff = None  # Prevent cleanup since we renamed it
        else:
            # Copy original file to output location if different
            if input_tiff != final_output:
                print(f"Copying to output location: {final_output}")
                import shutil
                shutil.copy2(input_tiff, final_output)
            else:
                print("Input is already in correct format and location")
    
    # Clean up temporary files
    if temp_tiff and os.path.exists(temp_tiff):
        os.remove(temp_tiff)
    
    src.close()
    
    if needs_reprojection:
        print(f"Conversion complete. Reprojected {output_format.upper()} file saved to: {final_output}")
    else:
        print(f"Conversion complete. {output_format.upper()} file saved to: {final_output}")
    
    return final_output

def ensure_utm(raster, input_crs=None, fallback="EPSG:4326"):
    """
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
    """

    # Assign CRS if missing
    if raster.rio.crs is None:
        if input_crs is None:
            raise ValueError(
                "Raster has no CRS. Provide input_crs='EPSG:32605' (or appropriate CRS)."
            )
        return raster.rio.write_crs(input_crs)

    crs_obj = CRS.from_user_input(raster.rio.crs)

    if crs_obj.is_projected and "UTM" in crs_obj.name.upper():
        return raster

    if crs_obj.is_geographic:

        bounds = raster.rio.bounds()
        lon_center = (bounds[0] + bounds[2]) / 2
        lat_center = (bounds[1] + bounds[3]) / 2

        zone = int(math.floor((lon_center + 180) / 6) + 1)

        epsg = f"EPSG:{32600 + zone}" if lat_center >= 0 else f"EPSG:{32700 + zone}"

        return raster.rio.reproject(epsg)

    return raster.rio.reproject(fallback)


def standardize_raster(
    r1,
    r2,
    r1_crs=None,
    r2_crs=None,
    folder=None,
    r1_output=None,
    r2_output=None,
):
    """
    Standardize two rasters to a common grid.

    Parameters
    ----------
    r1, r2 : str
        Raster filenames.
    r1_crs, r2_crs : str, optional
        CRS to assign if the raster has no CRS.
    """

    raster_one = rxr.open_rasterio(r1, masked=True)
    raster_two = rxr.open_rasterio(r2, masked=True)

    raster_one = raster_one.dropna(dim="x", how="all").dropna(dim="y", how="all")
    raster_two = raster_two.dropna(dim="x", how="all").dropna(dim="y", how="all")

    raster_one = ensure_utm(raster_one, input_crs=r1_crs)
    raster_two = ensure_utm(raster_two, input_crs=r2_crs)

    minx = min(raster_one.rio.bounds()[0], raster_two.rio.bounds()[0])
    miny = min(raster_one.rio.bounds()[1], raster_two.rio.bounds()[1])
    maxx = max(raster_one.rio.bounds()[2], raster_two.rio.bounds()[2])
    maxy = max(raster_one.rio.bounds()[3], raster_two.rio.bounds()[3])
    
    # Use absolute values for resolution to ensure positive dimensions
    res_x = max(abs(raster_one.rio.resolution()[0]), abs(raster_two.rio.resolution()[0]))
    res_y = max(abs(raster_one.rio.resolution()[1]), abs(raster_two.rio.resolution()[1]))
    
    # Build union grid using coarsest resolution
    width  = int(np.ceil((maxx - minx) / res_x))
    height = int(np.ceil((maxy - miny) / res_y))
    
    transform = from_bounds(minx, miny, maxx, maxy, width, height)
    
    # Create template DataArray with union grid + CRS
    # Note: y coordinates go from max to min (top to bottom)
    union_template = xr.DataArray(
        np.empty((height, width), dtype=raster_one.dtype),
        dims=("y", "x"),
        coords={
            "x": np.linspace(minx + res_x/2, maxx - res_x/2, width),
            "y": np.linspace(maxy - res_y/2, miny + res_y/2, height),  # This goes high to low
        },
    ).rio.write_crs(raster_one.rio.crs).rio.write_transform(transform)
    
    # Reproject both rasters to union template
    r1_union = raster_one.rio.reproject_match(union_template)
    r2_union = raster_two.rio.reproject_match(union_template)

    r1name = Path(r1).name
    r2name = Path(r2).name

    if folder:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)

        r1_out = folder / (r1_output or f"union_{r1name}")
        r2_out = folder / (r2_output or f"union_{r2name}")
    else:
        r1_out = Path(r1_output or f"union_{r1name}")
        r2_out = Path(r2_output or f"union_{r2name}")

    r1_union.rio.to_raster(r1_out)
    r2_union.rio.to_raster(r2_out)
    
    
    print("Rasters standardized to identical CRS, bounds, and resolution.")
    return r1_union, r2_union

def load_future_winds(
    experiment_id,
    source_id,
    variant_label,
    activity_id="ScenarioMIP",
    frequency="Amon",
    grid_label="gn",
):
    """
    Load paired ua/va pressure-level winds from CMIP6.

    Returns
    -------
    xr.Dataset with variables:
        ua, va, wind_speed, wind_direction
    """
    cat = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)

    # 1. Search catalog
    query = dict(
        activity_id=activity_id,
        experiment_id=experiment_id,
        source_id=source_id,
        member_id=variant_label,
        variable_id=["ua", "va"],
        table_id=frequency,
        grid_label=grid_label,
    )

    cat_sub = cat.search(**query)

    if len(cat_sub.df) == 0:
        raise ValueError("No matching ua/va datasets found")

    # 2. Enforce pairing
    vars_found = set(cat_sub.df["variable_id"].unique())
    if vars_found != {"ua", "va"}:
        raise ValueError(f"Incomplete wind pair found: {vars_found}")

    # 3. Load to xarray
    ds = cat_sub.to_dataset_dict(
        zarr_kwargs={"consolidated": True},
        xarray_open_kwargs={"chunks": "auto"},
    )

    # Intake returns a dict keyed by dataset_id — merge safely
    ds = xr.merge(ds.values(), compat="equals")

    # 5. Compute speed and direction
    u = ds["ua"]
    v = ds["va"]

    speed = np.sqrt(u**2 + v**2)
    direction = (270 - np.degrees(np.arctan2(v, u))) % 360

    speed.attrs.update({
        "standard_name": "wind_speed",
        "units": "m s-1",
        "description": "Computed from ua/va"
    })

    direction.attrs.update({
        "standard_name": "wind_from_direction",
        "units": "degrees",
        "convention": "meteorological"
    })

    ds["wind_speed"] = speed
    ds["wind_direction"] = direction

    return ds


def points_to_raster(df, east_col, north_col, value_col, output_path,
                     epsg=None, resolution=1000, interpolation='linear',
                     nodata=np.nan):
    """
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
    """
    from scipy.interpolate import griddata

    east  = df[east_col].values.astype(float)
    north = df[north_col].values.astype(float)
    vals  = df[value_col].values.astype(float)

    # --- Infer EPSG from point centroid if not supplied ---
    if epsg is None:
        print("No EPSG code provided, defaulting to zone 1N")
        lat, lon = utm.to_latlon(east.mean(), north.mean(),
                                 *utm.from_latlon(0, east.mean() / 111320)[2:4])
        # Re-derive zone from mean easting/northing using a rough lat estimate
        # Use pyproj for a clean zone lookup instead
        crs_guess = CRS.from_dict({
            'proj': 'utm',
            'zone': int((east.mean() % 6_000_000) // 100_000) or 1,
            'ellps': 'WGS84'
        })
        # Simpler: convert centroid back to lat/lon via utm library
        # We need a zone number — estimate from the easting magnitude
        zone_number = int(np.clip(round((east.mean() - 166022) / 111320 / 6) + 1, 1, 60))
        north_hemi  = north.mean() > 0
        epsg = 32600 + zone_number if north_hemi else 32700 + zone_number

    # --- Build regular grid ---
    east_min,  east_max  = east.min(),  east.max()
    north_min, north_max = north.min(), north.max()

    grid_east  = np.arange(east_min,  east_max  + resolution, resolution)
    grid_north = np.arange(north_min, north_max + resolution, resolution)
    ge, gn = np.meshgrid(grid_east, grid_north)

    # --- Interpolate ---
    grid_vals = griddata(
        points=(east, north),
        values=vals,
        xi=(ge, gn),
        method=interpolation,
        fill_value=nodata
    )

    # Flip rows: rasterio expects origin at top-left (north_max)
    grid_vals = np.flipud(grid_vals).astype(np.float32)

    transform = from_origin(
        west=east_min,
        north=north_max,
        xsize=resolution,
        ysize=resolution
    )

    crs = rio.crs.CRS.from_epsg(epsg)

    # Replace nan nodata with a finite sentinel if needed for GeoTIFF
    write_nodata = nodata if not np.isnan(nodata) else -9999.0
    if np.isnan(nodata):
        grid_vals = np.where(np.isnan(grid_vals), write_nodata, grid_vals)

    output_path = os.path.abspath(output_path)
    with rio.open(
        output_path,
        mode='w',
        driver='GTiff',
        height=grid_vals.shape[0],
        width=grid_vals.shape[1],
        count=1,
        dtype=grid_vals.dtype,
        crs=crs,
        transform=transform,
        nodata=write_nodata
    ) as dst:
        dst.write(grid_vals, 1)

    print(f"GeoTIFF saved to: {output_path}")
    return output_path
