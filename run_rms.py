import rms_tools as rms
import list_tools as lists
import noise
from os.path import isfile
from os import remove

sci_data_dir = 'test_field_data/'
master_bands = ['f606w', 'f600lp', 'f098m', 'f125w', 'f160w']
fields = ['0808+3946']

field_data = lists.field_band_list(fields, sci_data_dir, master_bands=master_bands)
field_data = lists.full_filename_list(field_data)

for field in field_data:
    for band in field_data[field]['bands']:
        print "\n\n****************\n****************\nField %s, band %s : \n" % (field, band)
        if not isfile(field_data[field][band]['rms_crude']):
            rms.wht_to_rms(field_data[field][band]['wht'], field_data[field][band]['rms_crude'])
        else:
            print "First pass RMS map for field %s band %s already exists!" % (field, band)

        print "SExtracting...\n"
        # rms.crude_SExtract(field_data[field][band])

        if not isfile(field_data[field][band]['false_img']):
            print "Generating false sources..."
            noise.false_sources(field_data[field][band])
        else:
            print "False sources image for field %s band %s already exists!" % (field, band)

        print "SExtracting false sources...\n"
        # noise.false_SExtract(field_data[field][band])

        print "Calculating normalisation constant..."
        norm_constant = noise.rms_norm_constant(field_data[field][band]['cat_false'])

        print "Creating normalised RMS map..."
        if isfile(field_data[field][band]['rms_norm']):
            remove(field_data[field][band]['rms_norm'])
        rms.norm_rms_map(field_data[field][band]['rms_crude'], field_data[field][band]['rms_norm'], norm_constant)
