########################################
#
# Picture Arranger
#
########################################

import os
import sys
import shutil
import glob
import argparse
import logging
from PIL import Image
from PIL.ExifTags import TAGS


def parse_options() :
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
    args = parser.parse_args()
    return args

def get_image_list( input_dir ):
    files = glob.glob( os.path.join( input_dir, "*.jpg") )
    # files = glob.glob( "*.jpg" )
    logging.info( "List of " + str(len(files)) + " images found in: " + input_dir)
    return files

def process_image( path_to_image ):
    exifname2tag = exif_num_dict()
    exiftags = Image.open( path_to_image )._getexif() #gets exif dict (tag no -> tag value)
    date = exiftags[exifname2tag['DateTimeOriginal']] 
    logging.info("Creation date is: " + date)
    return date

def exif_num_dict():
    return dict((name, num) for num, name in TAGS.iteritems()) 

# date is 2015:03:29 12:45:50
def create_target_path( outdir, datetime ):
    """ Create a path when given the output directory, EXIF created datetime """
    date = (datetime.split())[0].split(':')
    basedir = os.path.join( outdir, *date )
    if os.path.exists( basedir):
        if os.path.isdir( basedir ):
            # We have the directory
            pass
        else:
            # There is a file in the way - stop
            # TODO: throw error
            pass
    else:
        # We have nothing - create the path
        # TODO: create path
        # TODO: handle dry-run
        pass 
    return basedir

def create_target_file( dir, image ):
    # TODO: optimise!!!
    newfile = image
    full_path = os.path.join( dir, newfile )
    if os.path.exists( full_path ):
        # Need to check for img_(1) etc
        logging.debug("Clash found")
        img_count = 1
        (name, ext) = os.path.splitext( image )
        while os.path.exists( full_path ):
            newfile = name + "(" + str(img_count) + ")" + ext
            logging.debug("trying: " + newfile)
            full_path = os.path.join( dir, newfile )
            img_count += 1
        logging.debug("Clash found for " + image + ", renaming to " + newfile)
    return newfile

def move_file( src, target ):
    shutil.move( src, target )

def setup_logger( logfile ):
    if logfile == "STDERR":
        logging.basicConfig( level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s' )
    else:
        logging.basicConfig( filename=logfile, level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s' ) 

if __name__ == '__main__':
    args = parse_options()
    setup_logger( args.logfile )
    images = get_image_list( args.inputdir )
    for image in images:
        logging.info( "Processing image: " + image )
        newpath = create_target_path( args.outputdir, process_image( image ) )
        newfile = create_target_file( newpath, os.path.basename( image ) )
        if args.dryrun:
            logging.info("File: "+ image + " -> " + os.path.join(newpath, newfile))
        else:
            move_file( image, os.path.join(newpath, newfile) )