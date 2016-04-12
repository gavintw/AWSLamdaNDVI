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

s3_client = boto3.client('s3')

def NDVI_Processing(image_path, resized_path):
    with Image.open(image_path) as image:
        imgR, imgG, imgB = image.split()
        arrR = np.asarray(imgR).astype('float64')
        arrB = np.asarray(imgB).astype('float64')
        num = (arrR-arrB)
        denom = (arrR+arrB)
        arr_ndvi = (num/denom) + 1.42 #add 1.42 to make max value 1.00
        image = Image.fromarray(np.uint8(cm.hsv(arr_ndvi)*(255)))
        image.save(resized_path)


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)

        s3_client.download_file(bucket, key, download_path)
        NDVI_Processing(download_path, upload_path)
        s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)
