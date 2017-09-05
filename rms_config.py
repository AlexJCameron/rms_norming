from os import listdir, makedirs
from astropy.io import fits
from os.path import exists

# #### BORG z8 #### #
magzeros = {
'f606w':26.090,
'f600lp':25.879,
'f098m':25.6674,
'f125w':26.2303,
'f160w':25.9463
}

# #### BORG z9 #### #
# magzeros = {
# 'F105':26.2687,
# 'F125':26.2303,
# 'F140':26.4524,
# 'F160':25.9463,
# 'F350':26.957
# }

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

def auto_config(config_file='detection.config'):
    """Reads in config file and determines various setup variable from that.

    Parameters
    ----------
    config_file : str
        Filename of the config file

    Returns
    -------
    config_dict : dict
        A dict containing the relevant information extracted from the config file.

    """
    config_list = []
    config_dict = {}
    for line in read_list(config_file):
        if not line[0] == '#':
            config_list.append(line)

    for item in config_list:
        [key, val] = item.split('=')
        config_dict[key] = val
        if key[-3:] == 'dir' and not exists(val):
            makedirs(val)

    bands = config_dict['master_bands'].split(',')
    config_dict['master_bands'] = bands

    if 'make_bands' in config_dict:
        bands = config_dict['make_bands'].split(',')
        config_dict['make_bands'] = bands

    return config_dict

config_dict = auto_config()

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
            if field in fname:
                for band in master_bands:
                    if band in fname:
                        bands.append(band)
        this_field['bands'] = bands
        field_data[field] = this_field

    return field_data

def full_filename_list_z8(field_data):
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
    sci_dir = config_dict['sci_dir']
    wht_dir = config_dict['wht_dir']
    rms_crude_dir = config_dict['rms_crude_dir']
    rms_final_dir = config_dict['rms_final_dir']
    cat_crude_dir = config_dict['cat_crude_dir']
    seg_crude_dir = config_dict['seg_crude_dir']
    fake_dir = config_dict['fake_dir']

    sci_file_list = listdir(sci_dir)
    wht_file_list = listdir(wht_dir)

    for field in field_data:
        for band in field_data[field]['bands']:
            band_dict = {}
            for scifile in sci_file_list:
                if field in scifile and band in scifile:
                    band_dict['sci'] = sci_dir + scifile
            for whtfile in wht_file_list:
                if field in whtfile and band in whtfile and not 'rms' in whtfile:
                    band_dict['wht'] = wht_dir + whtfile


            band_dict['cat_crude'] = cat_crude_dir + field + '_' + band + '_crude.cat'
            band_dict['cat_false'] = fake_dir + field + '_' + band + '_false.cat'
            band_dict['rms_crude'] = rms_crude_dir + field + '_' + band + '_rms_crude.fits'
            band_dict['rms_norm'] = rms_final_dir + field + '_' + band + '_rms_norm.fits'
            band_dict['segmap'] = seg_crude_dir + field + '_' + band + '_seg_crude.fits'
            band_dict['seg_false'] = fake_dir + field + '_' + band + '_seg_false.fits'
            band_dict['false_img'] = fake_dir + field + '_' + band + '_false_sources.fits'

            band_dict['no_false_srcs'] = 100
            band_dict['magz'] = magzeros[band]

            hdu_list = fits.open(band_dict['sci'])
            exptime = hdu_list[0].header['exptime']
            hdu_list.close()
            band_dict['gain'] = exptime

            field_data[field][band] = band_dict

    return field_data

def full_filename_list_z9(field_data):
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
    data_dir = config_dict['data_dir']
    rms_crude_dir = config_dict['rms_crude_dir']
    rms_final_dir = config_dict['rms_final_dir']
    cat_crude_dir = config_dict['cat_crude_dir']
    seg_crude_dir = config_dict['seg_crude_dir']
    fake_dir = config_dict['fake_dir']

    for field in field_data:
        for band in field_data[field]['bands']:
            band_dict = {}
            band_dict['sci'] = data_dir + 'borg_' + field + '/borg_' + field + '_' + band + '_drz_sci.fits'
            band_dict['wht'] = data_dir + 'borg_' + field + '/borg_' + field + '_' + band + '_drz_wht.fits'

            band_dict['cat_crude'] = cat_crude_dir + field + '_' + band + '_crude.cat'
            band_dict['cat_false'] = fake_dir + field + '_' + band + '_false.cat'
            band_dict['rms_crude'] = rms_crude_dir + field + '_' + band + '_rms_crude.fits'
            band_dict['rms_norm'] = rms_final_dir + field + '_' + band + '_rms_norm.fits'
            band_dict['segmap'] = seg_crude_dir + field + '_' + band + '_seg_crude.fits'
            band_dict['seg_false'] = fake_dir + field + '_' + band + '_seg_false.fits'
            band_dict['false_img'] = fake_dir + field + '_' + band + '_false_sources.fits'

            band_dict['no_false_srcs'] = 100
            band_dict['magz'] = magzeros[band]

            hdu_list = fits.open(band_dict['sci'])
            exptime = hdu_list[0].header['exptime']
            hdu_list.close()
            band_dict['gain'] = exptime

            field_data[field][band] = band_dict

    return field_data

def write_flags(flagged_imgs, flag_log_fname=config_dict['flag_log'], verbose=True):
    """Writes a log of the flagged imaages from the RMS normalisation.

    Parameters
    ----------
    flagged_imgs : list
        A list of the flagged images to be written to file
    flag_log_fname : str
        Filename of the output file
    verbose : bool
        Set True to print to console output as well

    """
    log_file = open(flag_log_fname, 'w')
    log_file.truncate()

    if verbose:
        print "\nFlagged images:"

    for flag_img in flagged_imgs:
        if verbose:
            print flag_img
        log_file.write(flag_img + '\n')

    log_file.close()
