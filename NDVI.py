from PIL import Image
import PIL.Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import cm

def main():
  print "NDVI Processing..."
  #img = Image.open("/Users/Daniel/Desktop/CropDrone/FunctionalTesting/NDVITest/InputImages/DJI_0005.JPG")
  #img = Image.open("/Users/Daniel/Desktop/CropDrone/FunctionalTesting/NDVITest/InputImages/DJI_0003.JPG")
  img = Image.open("/Users/Daniel/Desktop/CropDrone/FunctionalTesting/NDVITest/InputImages/DJI_0004.JPG")

  imgR, imgG, imgB = img.split() #get channels
  #convert to double precision floating point..is this overkill? probably, could try 'float32' or 'float16'
  arrR = np.asarray(imgR).astype('float64')
  arrB = np.asarray(imgB).astype('float64')
  num = (arrR-arrB)
  denom = (arrR + arrB)
  #print(arr_ndvi)
  arr_ndvi = (num/denom)
  #arr_ndvi = num

  AUTO_CONTRAST = False
  img_w, img_h = img.size

  dpi   = 600#int(img_w/fig_w)
  
  '''
  vmin and vmax are variables to calibrate the NDVI algorithm
  The NDVI value of vmin should be a value for known unhealthy vegetation
  The NDVI value of vmax should be a value for known healthy vegetation
  In this way, it is possible to determine the relative health difference of vegetation or crops
  '''

  vmin  =  np.min(arr_ndvi) #most negative NDVI value
  vmax  =  np.amax(arr_ndvi) #most positive NDVI value
  
  #fig_w = img_w/dpi
  fig_h = img_h/dpi
  fig = plt.figure(figsize=(img_w/dpi,fig_h), dpi=dpi)
  fig.set_frameon(False)

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
  cbar = fig.colorbar(axes_img, cax=cax)  #this resizes the axis


  fig.savefig("/Users/Daniel/Desktop/CropDrone/FunctionalTesting/NDVITest/OutputImages/DJI_0004_NDVI.JPG"#, 
            #dpi=dpi,
            #bbox_inches='tight'
            #pad_inches=0.0, 
           )

  #img = Image.fromarray(np.uint8(cm.hsv(arr_ndvi)*(255)))
  #img.save("/Users/Daniel/Desktop/CropDrone/ImageProcessing/TestImages/NDVIlense/Leaves/DJI_0005_NDVI_NEW.JPG")
  

if __name__ == '__main__':
  main()