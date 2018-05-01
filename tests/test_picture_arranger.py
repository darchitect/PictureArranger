import unittest
import os
import sys
import picture_arranger
from picture_arranger import FileSameException

class TestPictureArranger(unittest.TestCase):

    def test_arguments(self):
        sys.argv[1:] = []
        with self.assertRaises(SystemExit):
            picture_arranger.parse_options()
    
    def test_arguments_only_input(self):
        sys.argv[1:] = ['-o moo']
        with self.assertRaises(SystemExit):
            picture_arranger.parse_options()

    def test_arguments_input_and_output(self):
        sys.argv[1:] = ['-o moo', '-i in']
        args = picture_arranger.parse_options()
        self.assertEquals( args.outputdir, " moo" )
        self.assertEquals( args.inputdir, " in" )    

    def test_get_image_list(self):
        images = picture_arranger.get_image_list( os.path.join( os.getcwd(), "tests/1" ) )
        test_images = [ os.path.join( os.getcwd(), 'tests/1\\IMG-20140626-00774.jpg') ]
        self.assertListEqual(test_images, images)

    def test_get_image_creation_date_from_exif(self):
        date = picture_arranger.get_image_creation_date( os.path.join( os.getcwd(), 'tests/1\\IMG-20140626-00774.jpg') )
        self.assertEquals( date, "2014:06:26 16:45:58" )

    def test_get_image_creation_date_from_mtime(self):
        date = picture_arranger.get_image_creation_date( os.path.join( os.getcwd(), 'tests/2\\IMG-20140626-00774_no_exif.jpg') )
        self.assertEquals( date, "2018:05:01 22:37:22" )

    def test_create_target_path_file_in_way(self):
        outputdir = os.path.join( os.getcwd(), 'tests/3' )
        with self.assertRaises(IOError):
            picture_arranger.create_target_path( outputdir, "2018:04:01 22:15:00")

    def test_create_target_path_exists(self):
        outputdir = os.path.join( os.getcwd(), 'tests/3' )
        dir = picture_arranger.create_target_path( outputdir, "2018:04:02 22:17:00", dryrun=False )
        self.assertEquals( dir, os.path.join( os.getcwd(), 'tests', '3', '2018', '04', '02') )

    def test_create_target_path_dryrun(self):
        outputdir = os.path.join( os.getcwd(), 'tests/3' )
        picture_arranger.create_target_path( outputdir, "2018:04:03 22:17:00" , dryrun=True)
        self.assertFalse( os.path.exists( os.path.join( os.getcwd(), 'tests', '3', '2018', '04', '03')  ) )

    def test_create_target_path_create(self):
        outputdir = os.path.join( os.getcwd(), 'tests/3' )
        picture_arranger.create_target_path( outputdir, "2018:04:04 22:17:00" , dryrun=False)
        path = os.path.join( os.getcwd(), 'tests', '3', '2018', '04', '04')
        self.assertTrue( os.path.exists( path ) )
        os.removedirs( path )
        
    def test_create_target_file_clash(self):
        image = os.path.join( os.getcwd(), 'tests', '1', 'IMG-20140626-00774.jpg')
        outdir = os.path.join( os.getcwd(), 'tests', '4' )
        expected_filename = 'IMG-20140626-00774(1).jpg'
        filename = picture_arranger.create_target_file( outdir, image )
        self.assertEquals( filename, expected_filename )

    def test_create_target_file_compare_true(self):
        image = os.path.join( os.getcwd(), 'tests', '1', 'IMG-20140626-00774.jpg')
        outdir = os.path.join( os.getcwd(), 'tests', '4' )
        with self.assertRaises(FileSameException):
            picture_arranger.create_target_file( outdir, image, checksame=True )
 
    def test_create_target_file_clash_multiple(self):
        image = os.path.join( os.getcwd(), 'tests', '1', 'IMG-20140626-00774.jpg')
        outdir = os.path.join( os.getcwd(), 'tests', '5' )
        expected_filename = 'IMG-20140626-00774(4).jpg'
        filename = picture_arranger.create_target_file( outdir, image )
        self.assertEquals( filename, expected_filename )

def main():
    unittest.main()

if __name__ == '__main__':
    main()