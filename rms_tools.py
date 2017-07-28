import numpy as np
from astropy.io import fits
from subprocess import check_call

def wht_to_rms(wht_fname, rms_fname, zero_handle='inf'):
    """Reads in data from a .fits weight map and makes an RMS map where each pixel is 1/sqrt(x) of the value x in the weight map.

    Parameters
    ----------
    wht_fname, rms_fname : str
        Filenames of the input weight map file and the output RMS file. The RMS file must NOT already be a file
    zero_handle : str 'inf' or '100'
        What to put in the RMS map for a value of 0 in the wht map

    Returns
    -------
    RMS map .fits file

    """
    hdu_list = fits.open(wht_fname)
    weight_data = hdu_list[0].data

    # Changes the header of the new fits file to match the filename
    hdu_list[0].header['filename'] = rms_fname

    if zero_handle == 'inf':
        for x in np.nditer(weight_data, op_flags = ['readwrite']):
            x[...] = 1/np.sqrt(np.absolute(x))
    else:
        try:
            big_num = float(zero_handle)
            for x in np.nditer(weight_data, op_flags = ['readwrite']):
                if not x == 0:
                    x[...] = 1/np.sqrt(np.absolute(x))
                else:
                    x[...] = big_num
        except ValueError:
            for x in np.nditer(weight_data, op_flags = ['readwrite']):
                x[...] = 1/np.sqrt(np.absolute(x))

    try:
        hdu_list.writeto(rms_fname)
    except IOError:
        print "Error: Unable to write to file. %s already exists." % rms_fname
        print "Try again with new output filename."

    hdu_list.close()

    return None

def crude_SExtract(field_band_dict):
    """Runs SExtractor in dual mode on one science image with one RMS map to produce a segmentaion map and a catalog

    Parameters
    ----------
    field_band_dict : dict
        Dict of the various filenames etc relevant to the field and band being SExtracted

    Returns
    -------
    SExtractor outputs

    """
    sci_image = field_band_dict['sci']
    rms_map = field_band_dict['rms_crude']
    cat_fname = field_band_dict['cat_crude']
    segm_chk_fname = field_band_dict['segmap']
    gain = str(field_band_dict['gain'])
    magzeropoint = str(field_band_dict['magz'])

    # Running it in dual mode
    dual_sci = sci_image + ',' + sci_image
    dual_rms = rms_map + ',' + rms_map

    # Run SExtractor
    check_call(['sextractor', dual_sci, '-c', 'crude.sex', '-WEIGHT_IMAGE', dual_rms, '-CHECKIMAGE_NAME', segm_chk_fname, '-CATALOG_NAME', cat_fname, '-GAIN', gain, '-MAG_ZEROPOINT', magzeropoint])

def norm_rms_map(crude_rms_map, norm_rms_fname, norm_const):
    """Normalises a 'crude' RMS map according to a normalisation constant.

    Parameters
    ----------
    crude_rms_map, norm_rms_fname : str
        Filenames of the input RMS map to be normalised, and the ouput normalised RMS map respectively
    norm_const : float
        The normalisation constant to be applied

    Returns
    -------
    Normalised RMS map

    """
    hdu_list = fits.open(crude_rms_map)
    rms_data = hdu_list[0].data
    hdu_list[0].header['filename'] = norm_rms_fname

    for x in np.nditer(rms_data, op_flags = ['readwrite']):
        x[...] = x * norm_const

    # Writes the output to file
    hdu_list.writeto(norm_rms_fname)
    hdu_list.close()
