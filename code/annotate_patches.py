# test import 
import os 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from skimage.io import imread, imsave
from matplotlib.patches import Rectangle
import matplotlib



root_dir = '/home/giorgia/Desktop/MAI/Thesis/images/selected_50m'
outdir = '/home/giorgia/Desktop/MAI/Thesis/images/patches'

#os.path.join('/content', 'drive', 'MyDrive', 'selected_50m/')
img_paths = []
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.endswith('.JPG'):
            img_paths.append(os.path.join(root, f))


dims = 256
patches = []
patch_info = pd.DataFrame(columns=['imfilename','patch_filename', 'x','y'])
for imf in img_paths:
    im = imread(imf)
    for i in range (0,im.shape[0],dims):
        for j in range (0, im.shape[1], dims):
            patch_filename = imf.replace('.JPG', '_X' + str(j) + '_Y' + str(i) + '.JPG')
            patch_info = patch_info.append(pd.Series(data={'imfilename':imf,'patch_filename': patch_filename, 'x':j, 'y':i}), ignore_index=True)
            p = im[i:i+dims, j:j+dims, :]
            patches.append(p)
            #imsave(os.path.join(outdir, os.path.basename(patch_filename)), p)
patch_info['plastic']=pd.Series(np.ones(len(patch_info))*-1)

#patch_info.to_csv('/home/giorgia/Desktop/MAI/Thesis/patch_info.csv')
matplotlib.use('TkAgg')

for ind in range(5) : #len(patches)):
    row = patch_info.loc[ind,:]
    if row['plastic'] == -1:
        imf = row['imfilename']
        plt.figure(figsize=(8,8))
        plt.imshow(patches[ind]) 
        f, ax = plt.subplots()
        f.set_figheight(10)
        f.set_figwidth(30)
        ax.imshow(imread(imf))
        rect = Rectangle( ( row['x'], row['y']), dims, dims, linewidth=3, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.pause(5)
        plt.close('all')
        b = input('type class 1/0 ')
        while b!='0' and b!='1':
            b = input('class must be either 1 or 0. retype class 1/0 ')
        patch_info.loc[ind,'plastic'] = int(b)
        

print(patch_info['plastic'])
