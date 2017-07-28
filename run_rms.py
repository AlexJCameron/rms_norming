import rms_tools as rms
import rms_config as config
import noise
from os.path import isfile
from os import remove

sci_data_dir = config.config_dict['sci_dir']
master_bands = config.config_dict['master_bands']
fields = config.read_list(config.config_dict['fields'])

flagged_imgs = []

field_data = config.field_band_list(fields, sci_data_dir, master_bands=master_bands)
field_data = config.full_filename_list(field_data)

for field in field_data:
    for band in field_data[field]['bands']:
        flags = ''
        print "\n\n****************\n****************\nField %s, band %s : \n" % (field, band)
        if not isfile(field_data[field][band]['rms_crude']):
            print "Making initial RMS map..."
            rms.wht_to_rms(field_data[field][band]['wht'], field_data[field][band]['rms_crude'])
        else:
            print "First pass RMS map for field %s band %s already exists!" % (field, band)

        print "SExtracting...\n"
        rms.crude_SExtract(field_data[field][band])

        if not isfile(field_data[field][band]['false_img']):
            print "Generating false sources..."
            noise.false_sources(field_data[field][band], no_sources=field_data[field][band]['no_false_srcs'])
        else:
            print "False sources image for field %s band %s already exists!" % (field, band)

        print "SExtracting false sources...\n"
        noise.false_SExtract(field_data[field][band])

        print "Calculating normalisation constant..."
        norm_constant, fal_src_count = noise.rms_norm_constant(field_data[field][band]['cat_false'])

        if not fal_src_count == field_data[field][band]['no_false_srcs']:
            flags = flags + ' falsecount '

        print "Creating normalised RMS map..."
        if isfile(field_data[field][band]['rms_norm']):
            remove(field_data[field][band]['rms_norm'])
        rms.norm_rms_map(field_data[field][band]['rms_crude'], field_data[field][band]['rms_norm'], norm_constant)

        noise.test_SExtract(field_data[field][band])
        test_norm, test_count = noise.rms_norm_constant('test.cat')

        print "noise_measured / noise_estimated = ", test_norm

        if not 0.99 < test_norm < 1.001:
            flags = flags + ' normacc:' + str(test_norm) + ' '

        if not flags == '':
            flagged_imgs.append(field+'_'+band+flags)

# Clean up
if not len(flagged_imgs) == 0:
    config.write_flags(flagged_imgs)
remove('test.cat')
