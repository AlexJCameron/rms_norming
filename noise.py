"""A module for analysing the noise in a fits image using SExtractor outputs.

"""

import numpy as np
from astropy.io import fits
from subprocess import check_call

def gest(r):
    """A simple Gaussian estimate to model the light profile of the false sources we'll create

    """
    return np.exp(-(r**2/16))

def inrad(x0, y0, r):
    """Generates a set of points considered to be within radius r of ponit x0, y0

    """
    points = []
    for x in range(x0-r,x0+r+1):
        for y in range(y0-r,y0+r+1):
            if np.sqrt((x0-x)**2+(y0-y)**2) <= r:
                # if x <= xmax and y <= ymax:
                points.append((y,x))
    return points

def false_sources(field_band_dict):
    """Generates .fits file containing false sources in empty regions of the image.

    This enables analysis of the background noise level of an image if SExtractor is used to detect in this false image, but then do photometry in the original science image.

    Parameters
    ----------
    field_band_dict : dict
        Dict containing the necessary filenames.

    Returns
    -------
    FITS file conataining false sources
    """
    ############################
    ##### Load in the data #####
    ############################
    hdu_list_wht = fits.open(field_band_dict['wht'])
    wht_data = hdu_list_wht[0].data
    hdu_list_wht.close()

    hdu_list = fits.open(field_band_dict['sci'])
    sci_data = hdu_list[0].data
    hdu_list.close()

    hdu_list_seg = fits.open(field_band_dict['segmap'])
    seg_data = hdu_list_seg[0].data
    hdu_list_seg.close()
    ############################

    # x and y bounds
    xmax = sci_data.shape[1]
    ymax = sci_data.shape[0]

    x_seg = []
    y_seg = []

    # Pick our random points
    Npoints = 100
    break_point = 0
    while len(x_seg) < Npoints:
        new_x = np.random.randint(0,xmax)
        new_y = np.random.randint(0,ymax)
        region = inrad(new_x-1, new_y-1,4)
        q_append = True
        for point in region:
            try:
                if wht_data[point] == 0:
                    q_append = False
            except IndexError:
                q_append = False
        if q_append:
            objcount = 0
            for point in region:
                objcount += seg_data[point]
            if objcount == 0:
                x_seg.append(new_x)
                y_seg.append(new_y)
        p_count = len(x_seg)
        break_point += 1
        if break_point >= 1000000:
            print "ERROR: Random placements unable to generate enough false sources for %s" % field_band_dict['sci']
            p_count = N_points

    falsedata = np.random.randn(sci_data.shape[0],sci_data.shape[1]) / 1000

    for n in range(len(x_seg)):
        f_pixs = inrad(x_seg[n]-1,y_seg[n]-1, 12)
        for pixel in f_pixs:
            falsedata[pixel] = 10 * gest(np.sqrt((x_seg[n]-1-pixel[1])**2+(y_seg[n]-1-pixel[0])**2))

    print "%d false sources generated" % len(x_seg)
    fits.writeto(field_band_dict['false_img'], falsedata)

def false_SExtract(field_band_dict):
    """Runs SExtractor in dual mode, detecting on a false sources image and performing photometry with the science image.

    Parameters
    ----------
    field_band_dict : dict
        Dict of the various filenames etc relevant to the field and band being SExtracted

    Returns
    -------
    SExtractor outputs

    """
    false_image = field_band_dict['false_img']
    sci_image = field_band_dict['sci']
    rms_map = field_band_dict['rms_crude']
    cat_fname = field_band_dict['cat_false']
    segmap_false = field_band_dict['seg_false']
    gain = str(field_band_dict['gain'])
    magzeropoint = str(field_band_dict['magz'])

    # Running it in dual mode
    dual_sci = false_image + ',' + sci_image
    dual_rms = rms_map + ',' + rms_map

    # Run SExtractor
    check_call(['sextractor', dual_sci, '-c', 'crude.sex', '-WEIGHT_IMAGE', dual_rms, '-CHECKIMAGE_NAME', segmap_false, '-CATALOG_NAME', cat_fname, '-GAIN', gain, '-MAG_ZEROPOINT', magzeropoint])
