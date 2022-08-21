# test import 
import os 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from skimage.io import imread, imsave
from matplotlib.patches import Rectangle
import matplotlib


root_dir = '/home/giorgia/Desktop/MAI/Thesis/images/selected_50m'
outdir = '/home/giorgia/Desktop/MAI/Thesis/images/patches_new/'
"""
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
            area = os.path.dirname(imf).split('/')[-1]
            patch_filename = os.path.join(outdir, area + "_" + os.path.basename(imf).replace('.JPG', '_X' + str(j) + '_Y' + str(i) + '.JPG'))
            patch_info = patch_info.append(pd.Series(data={'imfilename':imf,'patch_filename': patch_filename, 'x':j, 'y':i}), ignore_index=True)
            p = im[i:i+dims, j:j+dims, :]
            patches.append(p)
            imsave(os.path.join(outdir, os.path.basename(patch_filename)), p)
patch_info['plastic']=pd.Series(np.ones(len(patch_info))*-1)

patch_info.to_csv('/home/giorgia/Desktop/MAI/Thesis/patch_info_new.csv')
"""
matplotlib.use('TkAgg')

dims = 256
img_to_skip = None
patch_info = pd.read_csv('/home/giorgia/Desktop/MAI/Thesis/patch_info_new.csv')
for ind in range(len(patch_info)):
    row = patch_info.loc[ind,:]    
    if row['plastic'] == -1:
        imf = row['imfilename']
        if imf==img_to_skip: ###### fix 
            continue
        img_to_skip = None
        plt.figure(figsize=(30,60)) 
        plt.suptitle(os.path.basename(imf), fontsize=25, y=.9,)       
        plt.subplot(121)
        #patch = imread(os.path.join(outdir, os.path.basename(row['patch_filename'])))
        patch = imread(row['patch_filename'])
        plt.imshow(patch) 
        #plt.subplot(122)
        #from_im = imread(imf)[ row['y']: row['y']+dims, row['x']: row['x']+dims]
        #plt.imshow(from_im)

        ax = plt.subplot(122)
        plt.imshow(imread(imf))
        rect = Rectangle( ( row['x'], row['y']), dims, dims, linewidth=3, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        plt.waitforbuttonpress()
        plt.close('all')
        b = input('type class 1/0 or "sp" for skipping patch and or "si" for skipping image ')
        while b!='0' and b!='1' and b!="sp" and b!="si":
            b = input('class must be either 1 or 0. retype class 1/0 or skip patch "sp" or image "si"')
        if b=='0' or b=='1':
            patch_info.loc[ind,'plastic'] = int(b)
        elif b=='sp':
            continue
        else:
            img_to_skip = imf
        # save every 20 annotated patches 
        if ind!=0 and ind%20 == 0:
            print('saving labels of latest annotated 20 patches')
            patch_info.to_csv('/home/giorgia/Desktop/MAI/Thesis/patch_info_new.csv', index=False)
