import rms_tools as rms
import list_tools as lists

wht_list_filename = 'test_field.filelist'

wht_list = lists.read_list(wht_list_filename)

# THIS HAS BEEN DONE - CHECK LATER
# for wht_file in wht_list:
#     rms_file = 'test_field_rms_crude/' + wht_file[:-8].split('/')[-1] + 'rms.fits'
#
#     rms.wht_to_rms(wht_file, rms_file)
