from os import listdir
from astropy.io import fits

magzeros = {
'f606w':25.090,
'f600lp':25.879,
'f098m':25.6674,
'f125w':26.2303,
'f160w':25.9463
}

def read_list(list_fname):
    """Takes a flat file list where each item is on a separate line and returns in list format.

    Parameters
    ----------
    list_fname : str
        Filename of the list

    Returns
    -------
    final_list : list
        List generated from file

    """
    list_file = open(list_fname)
    split_list = list_file.read().split('\n')
    list_file.close()

    final_list = []

    for item in split_list:
        if not len(item) == 0:
            final_list.append(item)

    return final_list

def field_band_list(fields, data_dir, master_bands=['f606w', 'f600lp', 'f098m', 'f125w', 'f160w']):
    """Takes a list of fields and science files and identifies which fields are present with which bands.

    Parameters
    ----------
    fields : list
        List of fields to get bands for
    data_dir : str
        Directory in which the data is stored
    master_bands : list
        List of all the bands in the survey

    Returns
    -------
    field_data : dict
        Contains each field as a dict in which the bands are stored as a list

    """
    file_list = listdir(data_dir)
    field_data = {}
    for field in fields:
        this_field = {}
        bands = []
        for fname in file_list:
            if fields[0] in fname:
                for band in master_bands:
                    if band in fname:
                        bands.append(band)
        this_field['bands'] = bands
        field_data[field] = this_field

    return field_data

def full_filename_list(field_data):
    """Finds and generates various filenames that will come in handy later

    Parameters
    ----------
    field_data : dict
        The dict that we're collecting values relevant to our field in

    Returns
    -------
    field_data : dict
        With new entries.

    """
    sci_dir = 'test_field_data/'
    wht_dir = 'test_field_wht/'
    rms_crude_dir = 'test_field_rms_crude/'
    rms_final_dir = 'test_field_rms_norm/'
    cat_crude_dir = 'test_field_cat_crude/'
    seg_crude_dir = 'test_field_seg_crude/'
    fake_dir = 'test_field_false_source_imgs/'

    sci_file_list = listdir(sci_dir)
    wht_file_list = listdir(wht_dir)

    for field in field_data:
        for band in field_data[field]['bands']:
            band_dict = {}
            for scifile in sci_file_list:
                if field in scifile and band in scifile:
                    band_dict['sci'] = sci_dir + scifile
            for whtfile in wht_file_list:
                if field in whtfile and band in whtfile:
                    band_dict['wht'] = wht_dir + whtfile

            band_dict['cat_crude'] = cat_crude_dir + field + '_' + band + '_crude.cat'
            band_dict['cat_false'] = fake_dir + field + '_' + band + '_false.cat'
            band_dict['rms_crude'] = rms_crude_dir + field + '_' + band + '_rms_crude.fits'
            band_dict['rms_norm'] = rms_final_dir + field + '_' + band + '_rms_norm.fits'
            band_dict['segmap'] = seg_crude_dir + field + '_' + band + '_seg_crude.fits'
            band_dict['seg_false'] = fake_dir + field + '_' + band + '_seg_false.fits'
            band_dict['false_img'] = fake_dir + field + '_' + band + '_false_sources.fits'

            band_dict['magz'] = magzeros[band]

            hdu_list = fits.open(band_dict['sci'])
            exptime = hdu_list[0].header['exptime']
            hdu_list.close()
            band_dict['gain'] = exptime

            field_data[field][band] = band_dict

    return field_data
