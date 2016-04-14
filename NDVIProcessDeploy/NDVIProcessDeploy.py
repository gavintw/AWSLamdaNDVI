from __future__ import print_function
import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import cm
from matplotlib import pyplot as plt

s3_client = boto3.client('s3')

def NDVI_Processing(image_path, resized_path):
    with Image.open(image_path) as image:
        
        #Split Image into RED, GREEN, and BLUE Band
        imgR, imgG, imgB = image.split()
        
        #Get Red(NIR) and Blue(VIS) bands for NDVI Computation
        arrR = np.asarray(imgR).astype('float64')
        arrB = np.asarray(imgB).astype('float64')
        
        #Compute NDVI
        num = (arrR-arrB)
        denom = (arrR+arrB)
        arr_ndvi = (num/denom) 
        #arr_ndvi = (num/denom) + 1.25

        
        AUTO_CONTRAST = False
        image_w, image_h = image.size
        dpi   = 100#int(img_w/fig_w)

        
        #vmin and vmax are variables to calibrate the NDVI algorithm
        #The NDVI value of vmin should be a value for known unhealthy vegetation
        #The NDVI value of vmax should be a value for known healthy vegetation
        #In this way, it is possible to determine the relative health difference of vegetation or crops
        
        vmin  =  np.min(arr_ndvi) #most negative NDVI value
        vmax  =  np.amax(arr_ndvi) #most positive NDVI value

        #fig_w = img_w/dpi
        #fig_h = img_h/dpi
        fig = plt.figure(figsize=(image_w/dpi,image_h/dpi), dpi=dpi)
        fig.set_frameon(False)
        print("width: ",image_w/dpi, "height: ", image_h/dpi)

        ax_rect = [0.0, #left
               0.0, #bottom
               1.0, #width
               1.0] #height
        ax = fig.add_axes(ax_rect)
        ax.yaxis.set_ticklabels([])
        ax.xaxis.set_ticklabels([])   
        ax.set_axis_off()
        ax.patch.set_alpha(0.0)

        axes_img = ax.imshow(arr_ndvi,
                      cmap = cm.gist_ncar, 
                      vmin = vmin,
                      vmax = vmax,
                      aspect = 'equal',
                      #interpolation="nearest"
                     )
        cax = fig.add_axes([0.95,
                    0.05,
                    0.025,
                    0.90]
                   ) #fill the whole figure
        
        #Color scale
        cbar = fig.colorbar(axes_img, cax=cax)  #this resizes the axis
        
        #Save to Target Bucket
        
        fig.savefig(resized_path, 
            dpi=dpi,
            bbox_inches='tight',
            pad_inches=0.0, 
           )
        

        #fig.savefig(resized_path, dpi=dpi, bbox_inches='tight', pad_inches = 0.0)
    

        #image = Image.fromarray(np.uint8(cm.gist_ncar(arr_ndvi)*(255)))
        #image.save(resized_path)


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)

        s3_client.download_file(bucket, key, download_path)
        NDVI_Processing(download_path, upload_path)
        s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)
