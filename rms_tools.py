import numpy as np
from astropy.io import fits
from subprocess import check_call

def wht_to_rms(wht_fname, rms_fname):
    """Reads in data from a .fits weight map and makes an RMS map where each pixel is 1/sqrt(x) of the value x in the weight map.

    Parameters
    ----------
    wht_fname, rms_fname : str
        Filenames of the input weight map file and the output RMS file. The RMS file must NOT already be a file

    Returns
    -------
    RMS map .fits file

    """
    hdu_list = fits.open(wht_fname)
    weight_data = hdu_list[0].data

    # Changes the header of the new fits file to match the filename
    hdu_list[0].header['filename'] = rms_fname

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
