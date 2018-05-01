########################################
#
# Picture Arranger
#
########################################

import os
import datetime
import sys
import shutil
import glob
import filecmp
import argparse
import logging
from PIL import Image
from PIL.ExifTags import TAGS

class FileSameException(Exception):
    '''
    Custom exception for the file compare
    '''

def parse_options():
    '''Setup and parse the options for this script'''
    parser = argparse.ArgumentParser(description='Process some images.')
    parser.add_argument('-o', '--outputdir', 
                        required=True, 
                        help='Output directory')
    parser.add_argument('-i', '--inputdir', 
                        required=True, 
                        help='Input directory')
    parser.add_argument('-d', '--dryrun', 
                        action='store_true', 
                        help="Dry Run - don't do anything")
    parser.add_argument('-l', '--logfile', 
                        default="STDERR", 
                        help="Logfile - defaults to STDERR")
    parser.add_argument('-c', '--copy',
                        action='store_true',
                        help="Copy images - don't move them")
    parser.add_argument('-s', '--skipsame',
                        action='store_true',
                        help="Skip image if the copy/move target is the same according to filestat")
    parser.add_argument('--debug',
                        action='store_true',
                        help="enable DEBUG (akin to verbose)")
    args = parser.parse_args()
    return args

def get_image_list( input_dir ):
    '''Get the list of images in the input directory specified on the command line'''
    files = glob.glob( os.path.join( input_dir, "*.jpg") )
    logging.info( "List of " + str(len(files)) + " images found in: " + input_dir)
    return files

def get_image_creation_date( path_to_image ):
    '''Get the creation date - 'when it was taken' for the image - if this fails, 
    use the last "modification" time from the statinfo on the file'''
    exifname2tag = exif_num_dict()
    exiftags = Image.open( path_to_image )._getexif() #gets exif dict (tag no -> tag value)
    try:
        date = exiftags[exifname2tag['DateTimeOriginal']]
    except KeyError:
        logging.debug("EXIF Tag DateTimeOriginal not found or blank - using last modified time from file info")
        date = datetime.datetime.fromtimestamp( os.path.getmtime( path_to_image ) ).strftime('%Y:%m:%d %H:%M:%S')
    
    logging.info("Creation date is: " + str(date))
    return date

def exif_num_dict():
    '''Create a dictionary of EXIF tag name => number to index the EXIF tags in an image. 
    Basically allows you to ask for EXIF["DateTimeOriginal"] instead of some arbitary number. 
    See https://sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html for names '''
    return dict((name, num) for num, name in TAGS.iteritems()) 

# date is 2015:03:29 12:45:50
def create_target_path( outdir, datetime, dryrun = True ):
    '''Create a path when given the output directory, and the created datetime. datetime must 
    be supplied as "yyyy:mm:dd HH:MM:SS". Thows exception if the created path exists and is a 
    file not a dir. Skips creation if the directory already exists, or if dryrun=True was 
    specified on the command line.'''
    date = (datetime.split())[0].split(':')
    basedir = os.path.abspath( os.path.join( outdir, *date ) )
    
    if os.path.exists( basedir ):
        if os.path.isdir( basedir ):
            logging.debug( "Directory: [{0}] exists - not creating".format( basedir ))
        else:
            # There is a file in the way - stop
            logging.fatal( "Path [{0}] is a file - remove or rename and retry".format( basedir ))
            raise IOError("Cannot create directory at: [{0}]. Path exists and is a file - remove or rename and retry".format( basedir ))
    else:
        # We have nothing - create the path
        if dryrun:
            logging.info("Dryrun: Directory path [{0}] not created".format( basedir ))
        else:
            logging.info("Creating directory path: [{0}]".format( basedir ))
            os.makedirs( basedir ) 
    return basedir

def create_target_file( dir, image, checksame=False ):
    '''
    dir - full directory path
    image - fullpath of the image we are moving/copying

    Generate file name for target image in dir. Will try (1),(2) etc if clash found. 
    If checksame is set - then on clash - check that the file isn't the same as the one 
    being copied by doing a shallow compare (stat info same on both)'''
    oldfile = image # start
    newfile = os.path.basename( image ) # image name
    full_path = os.path.join( dir, newfile ) # new/proposed path
    img_count = 1
    (name, ext) = os.path.splitext( newfile ) # bug: if you use image - it will split into the path and ext, 
                                              # so you get more then you really wanted
    while os.path.exists( full_path ):
        logging.debug("Clash found for " + newfile )
        if checksame:
            if filecmp.cmp( oldfile, full_path ):
                logging.debug( "filecmp.cmp( Orig:[{0}] Target:[{1}] ) is true - files likely the same".format( oldfile, full_path ))
                raise FileSameException
        newfile = name + "(" + str(img_count) + ")" + ext
        logging.debug("Trying: " + newfile)
        full_path = os.path.join( dir, newfile )
        img_count += 1
    
    return newfile

def move_file( src, target, copy = True ):
    '''Perform the file move - or copy. Default is copy as a non-damaging operation'''
    if copy:
        # copy filestat info
        shutil.copy2( src, target )
    else:
        shutil.move( src, target )

def setup_logger( logfile, debug=False ):
    '''Setup the logger - default is the STDERR file handle - we test for the string "STDERR" and 
    rather than try and be clever, use the appropriate basicConfig call'''
    level = logging.DEBUG if debug else logging.INFO
    if logfile == "STDERR":
        logging.basicConfig( level=level, format='%(asctime)s|%(levelname)s|%(message)s' )
    else:
        logging.basicConfig( filename=logfile, level=level, format='%(asctime)s|%(levelname)s|%(message)s' ) 

def log_startup_options( args ):
    '''capture startup args in the log'''
    logging.info( "Arguments [{0}]".format( args ))

def log_operation(image, newpath, newfile, copy, dryrun):
    '''log the operation being chosen'''
    logging.info("{3}{2} File: [{0}] -> [{1}]".format( image, os.path.join(newpath, newfile), 
                "Copying" if copy else "Moving", 
                "Dryrun: Not " if dryrun else ""))
       
def main():
    args = parse_options()
    setup_logger( args.logfile, debug=args.debug )
    log_startup_options( args )
    images = get_image_list( args.inputdir )
    for image in images:
        logging.info( "Processing image: " + image )
        newpath = create_target_path( args.outputdir, get_image_creation_date( image ), dryrun=args.dryrun )
        try:
            newfile = create_target_file( newpath, image, checksame=args.skipsame )
            logging.debug( "Newfile [{0}] Newpath [{1}]".format( newfile, newpath ))
            log_operation( image, newpath, newfile, args.copy, args.dryrun )
            if not args.dryrun:
                move_file( image, os.path.join(newpath, newfile), copy=args.copy )
        except FileSameException:
            logging.info("Files same - skipping")



if __name__ == '__main__':
    main()