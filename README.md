rms_norming

A tool for creating normalised RMS maps for astronomical FITS images

Requirements: numpy, pandas, astropy SourceExtractor

Description: (Proper documentation is yet to be written) Accurate analysis of astronomical data in FITS images generally requires properly normalised weight maps. rms_norming requires an installation of SourceExtractor. It will use SExtractor to perform photometry on the background of the science image to get a measure for the nosie of the image. It will then create a new normalised RMS weight map to properly reflect the noise in the science image.

Usage: python run_rms.py

TEST.CONFIG: Directories of science images and corresponding weight maps must be specified in test.config. test.config also allows you to specify directories of output files.

'fields' : the filename of a text file containing a list of image identifiers 'master_bands' : this is a list of image sub-identifiers. The situation for which I wrote this script involved analysis of a series of pointings on the sky ('fields'), each of which had several images taken from different exposures through different waveband filters. The script will search every combination of field+band in the science and weight map directories and perform the analysis on every combination it finds. The field/band must be in the filename and be wary of duplicates in those names.


Added capability to create rms map with a large values that correspond to bad pixels (wht_map = 0) in ANY image for that field.

Usage: python make_detection_rms.py

DETECTION.CONFIG: Same as TEST.CONFIG but needs make_bands (the bands in which to make this RMS map) and mask_dir to be specified

** Make sure the correct config file is specified in rms_config.py -- I should definitely make this user specified...
