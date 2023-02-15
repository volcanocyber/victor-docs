import matplotlib.pyplot as plt
import rioxarray as rxr
import numpy as np
import cartopy.crs as ccrs
import rasterio as rio
import imageio
import h5py
import pandas as pd
import boto3
from google.cloud import storage
from botocore.exceptions import ClientError
from azure.storage.blob import BlobServiceClient
import os


def hillshade(array,azimuth,angle_altitude):
    azimuth = 360.0 - azimuth 
    
    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth*np.pi/180.
    altituderad = angle_altitude*np.pi/180.
 
    shaded = np.sin(altituderad)*np.sin(slope) + np.cos(altituderad)*np.cos(slope)*np.cos((azimuthrad - np.pi/2.) - aspect)
    
    return 255*(shaded + 1)/2
def plot_dem(dem, fig, ax, coords=None):
    dem_check = rxr.open_rasterio(dem).drop('band')[0].rename({'x':'easting', 'y':'northing'})
    nodata = dem_check.attrs["_FillValue"]
    dem_check = dem_check.where(dem_check>nodata, np.nan)
    ax.imshow(hillshade(dem_check,120,30),cmap="gray",transform=ccrs.epsg(32628), 
              extent=(min(dem_check["easting"]), max(dem_check["easting"]), min(dem_check["northing"]), max(dem_check["northing"])))
    ax.set_xticks([min(dem_check["easting"]), max(dem_check["easting"])])
    ax.set_yticks([min(dem_check["northing"]), max(dem_check["northing"])])
    if coords == None:
        pass
    elif np.array(coords.ndim) == 2:
        ax.scatter(coords[:,0],coords[:,1],marker="^",c="red")
    else:
        ax.scatter(coords[0],coords[1],marker="^",c="red")
    plt.show()
    
def plot_flow(dem, flow, fig, ax, coords,zoom=True,model=None, label="Thickness of residual (m)"):
    filename, file_extension = os.path.splitext(dem)
    if file_extension == ".tif" or file_extension == ".geotiff":
        raster = rio.open(dem)
        read_raster = raster.read()
        ax.imshow(hillshade(read_raster[0,:,:],120,30),cmap='Greys',vmin=0,vmax=300,transform=ccrs.epsg(32628),
                 extent=(raster.bounds.left, raster.bounds.right, raster.bounds.bottom, raster.bounds.top))
        ct = rxr.open_rasterio(dem).drop('band')[0].plot.contour(ax=ax,
        cmap=plt.cm.copper,
        transform=ccrs.epsg(32628)
        )
    if file_extension == ".asc" or file_extension == ".ascii":
        raster = rxr.open_rasterio(dem).drop('band')[0].rename({'x':'easting', 'y':'northing'})
        nodata = raster.attrs["_FillValue"]
        raster = raster.where(raster>nodata, np.nan)
        ax.imshow(hillshade(raster,120,30),cmap="gray",transform=ccrs.epsg(32628), 
            extent=(min(raster["easting"]), max(raster["easting"]), min(raster["northing"]), max(raster["northing"])))

        x_full_min, x_full_max = min(raster["easting"]).values, max(raster["easting"]).values
        y_full_min, y_full_max = min(raster["northing"]).values, max(raster["northing"]).values
        ct = raster.plot.contour(ax=ax,
        cmap=plt.cm.copper,
        transform=ccrs.epsg(32628)
        )
    ax.clabel(ct, ct.levels, inline=True, fontsize=9,colors="red")
    flow_thickness = rxr.open_rasterio(flow).drop('band')[0].rename({'x':'easting', 'y':'northing'})
    nodata = flow_thickness.attrs["_FillValue"]
    flow_thickness = flow_thickness.where(flow_thickness>nodata, np.nan)
    
    x_zoom_min, x_zoom_max = min(flow_thickness["easting"]).values-1000, max(flow_thickness["easting"]).values+1000
    y_zoom_min, y_zoom_max = min(flow_thickness["northing"]).values-1000, max(flow_thickness["northing"]).values+1000
    
    flow_thickness.plot(ax=ax,
        cmap=plt.cm.hot,
        cbar_kwargs={'label': label},
        transform=ccrs.epsg(32628)
    )
    if coords.ndim == 2:
        x,y = coords[:,0], coords[:,1]
    else:
        x,y = coords[0],coords[1]
    ax.scatter(x,y,marker="^",c="black")
    if not zoom:
        x_min, x_max = x_full_min,x_full_max
        y_min, y_max = y_full_min,y_full_max
    elif model=="mrlavaloba":
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
    ax.set_yticks(np.linspace(y_min, y_max,10))
    ax.clabel(ct, ct.levels, inline=True, fontsize=9,colors="white")
    ax.set_title('Lava Flow', fontsize=16)
    plt.savefig("flow_normal_contour.jpg",dpi=400)
    
def plot_geotiff(dem, fig, ax, coords=None):
    raster = rio.open(dem)
    read_raster = raster.read()
    ax.imshow(hillshade(read_raster[0,:,:],120,30),cmap='Greys',vmin=0,vmax=300,transform=ccrs.epsg(32628),
                 extent=(raster.bounds.left, raster.bounds.right, raster.bounds.bottom, raster.bounds.top))
    
def plot_titan(dem, flow, fig, ax, coords,zoom=True):
    raster = rio.open(dem)
    read_raster = raster.read()
    ax.imshow(hillshade(read_raster[0,:,:],120,30),cmap='Greys',vmin=0,vmax=300,transform=ccrs.epsg(32628),
                 extent=(raster.bounds.left, raster.bounds.right, raster.bounds.bottom, raster.bounds.top))
    x_full_min, x_full_max = raster.bounds.left, raster.bounds.right
    y_full_min, y_full_max = raster.bounds.bottom, raster.bounds.top

    sc = ax.scatter(x=flow["X_CENTER"], y=flow["Y_CENTER"], c=flow["PILE_HEIGHT"], s=1,
    cmap=plt.cm.hot)

    cb = plt.colorbar(sc)
    cb.set_label('Pile Height (m)', rotation=90)
    plt.title("Flow")
    
    x_zoom_min, x_zoom_max = min(flow["X_CENTER"])-1000, max(flow["X_CENTER"])+1000
    y_zoom_min, y_zoom_max = min(flow["Y_CENTER"])-1000, max(flow["Y_CENTER"])+1000
    ct = ax.contour(read_raster[0],
        cmap=plt.cm.copper,
        transform=ccrs.epsg(32628)
    )
    ax.clabel(ct, ct.levels, inline=True, fontsize=9,colors="red")
    x,y = coords[0],coords[1]
    ax.scatter(x,y,marker="^",c="black")
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
    ax.set_title('Lava Flow', fontsize=16)
    
def make_titan_gif(dem, fig, ax, coords, max_iter, diter, gif_name):
    num_steps = np.arange(int(np.ceil(max_iter/diter))+1)
    for step in range(int(np.ceil(max_iter/diter))+1):
        filled = str(step*diter).zfill(8)
        height = []
        filename = "".join(["./vizout/","xdmf_p0000_i",filled,".h5"])
        with h5py.File(filename, 'r')  as h5f:
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
        nonzero = df["PILE_HEIGHT"] > 0
        flow = df[nonzero]
        fig = plt.figure(figsize=(12, 8))
        ax = plt.axes(projection=ccrs.epsg(32628))
        plot_titan(dem, flow,fig, ax,coords)
        outname = "".join(("flow_",str(num_steps[step])))
        plt.savefig(outname)
        plt.close()
    frames = []
    for i in range(int(np.ceil(max_iter/diter))+1):
        image = imageio.v2.imread(f'flow_{i}.png')
        frames.append(image)
    imageio.mimsave(gif_name, # output gif
    frames,          # array of input frames
    fps = 10) 
    
def download_file_gcp(bucket_name, source_blob_name, destination_file_name, api_creds_json):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=api_creds_json

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )
    
def upload_file_gcp(bucket_name, source_file_name, destination_blob_name,api_cred_json):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=api_creds_json
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def download_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None):
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
        response = client.download_file(bucket_name, blob_name, file_name)
    except ClientError as e:
        print("Incorrect access keys: please enter valid credentials")
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            blob_name, bucket_name, file_name
        )
    )
          
def upload_file_aws(access_key, secret_access_key, bucket_name, blob_name, file_name, session_token=None):
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
        response = client.upload_file(file_name, bucket_name, blob_name)
    except ClientError as e:
        print("Incorrect access keys: please enter valid credentials")
    print(
        f"File {file_name} uploaded to {bucket_name} as {blob_name}."
    )

def download_from_azure(conn_string, container_name, local_file_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    with open(file=local_file_name, mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            blob_name, container_name, local_file_name
        )
    )
        
def upload_to_azure(conn_string, container_name, local_file_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)
    
    container_client = blob_service_client.get_container_client(container=container_name)
    with open(file=local_file_name, mode="rb") as data:
        blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(
        f"File {local_file_name} uploaded to {container_name} as {blob_name}."
    )

def download_dem(north, south, east, west, outputFormat, dataset):
    if north < south:
        print("Invalid latitude range")
        return -1
    elif east < west:
        print("Invalid longitude range")
        return -1
    url = f"https://portal.opentopography.org/API/globaldem?demtype={dataset}&south={south}&north={north}&west={west}&east={east}&outputFormat={outputFormat}&API_Key=3ac3c07f20ee63fd3babe7884f24e2c3"
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    name = txt3 = "DEM_{}N_{}S_{}W_{}E_{}_{}".format(int(north), int(south), int(east), int(west), dataset,dt_string) 
    if outputFormat == "AAIGrid":
        name = "".join((name,".asc"))
    elif outputFormat == "GTiff":
        name = "".join((name,".geotiff"))
    if os.path.isfile(name):
        print("File already exists, exiting.")
        return 1
    urllib.request.urlretrieve(url,name)
    print("DEM downloaded as {}".format(name))
    
def download_dem_utm(north, zone_north, south, zone_south, east, zone_east, west, zone_west, outputFormat, dataset):
    north,west = utm.to_latlon(north, west, int(zone_north[:-1]),zone_north[-1])
    south,east = utm.to_latlon(south, east, int(zone_south[:-1]),zone_south[-1])
    if north < south:
        print("Invalid latitude range")
        return -1
    elif east < west:
        print("Invalid longitude range")
        return -1
    url = f"https://portal.opentopography.org/API/globaldem?demtype={dataset}&south={south}&north={north}&west={west}&east={east}&outputFormat={outputFormat}&API_Key=3ac3c07f20ee63fd3babe7884f24e2c3"
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    name = txt3 = "DEM_{}N_{}S_{}W_{}E_{}_{}".format(int(north), int(south), int(east), int(west), dataset,dt_string) 
    if outputFormat == "AAIGrid":
        name = "".join((name,".asc"))
    elif outputFormat == "GTiff":
        name = "".join((name,".geotiff"))
    if os.path.isfile(name):
        print("File already exists, exiting.")
        return 1
    urllib.request.urlretrieve(url,name)
    print("DEM downloaded as {}".format(name))