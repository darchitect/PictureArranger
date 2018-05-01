import unittest
import shutil
import os
import sys
import picture_arranger
from picture_arranger import FileSameException

class TestIntegrationPictureArranger(unittest.TestCase):

    def _env(self):
        return { 'test_data': r"C:\Users\franc\Documents\workspace\PictureArranger\tests\integration\test_data", 
        'in': r"C:\Users\franc\Documents\workspace\PictureArranger\tests\integration\in", 
        'out': r"C:\Users\franc\Documents\workspace\PictureArranger\tests\integration\out" }

    def test_clean_copy(self):
        '''
        Copy image then do a -f on src and target
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'], '-c']
        picture_arranger.main()
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' )
        out_dir_dd = os.path.join(self._env()['out'], '2015', '03', '29' )
        out_dir_mm = os.path.join(self._env()['out'], '2015', '03')
        out_dir_yy = os.path.join(self._env()['out'], '2015' )

        self.assertTrue( os.path.exists( in_file ), msg="Check source exists") # Is the original there
        self.assertTrue( os.path.exists( out_file ), msg="Check original is still there"  ) # Is the target there
        
        os.unlink( in_file )
        os.unlink( out_file )
        os.rmdir( out_dir_dd )
        os.rmdir( out_dir_mm )
        os.rmdir( out_dir_yy )

    def test_clean_move(self):
        '''
        Move image then do a -f on src and target
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'] ]
        picture_arranger.main()
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' )
        out_dir_dd = os.path.join(self._env()['out'], '2015', '03', '29' )
        out_dir_mm = os.path.join(self._env()['out'], '2015', '03')
        out_dir_yy = os.path.join(self._env()['out'], '2015' )

        self.assertFalse( os.path.exists( in_file ), msg="Check original has gone") # Is the original there
        self.assertTrue( os.path.exists( out_file ), msg="Check file has been moved"  ) # Is the target there
        
        os.unlink( out_file )
        os.rmdir( out_dir_dd )
        os.rmdir( out_dir_mm )
        os.rmdir( out_dir_yy )

    def test_clash_copy(self):
        '''
        Copy image then do a -f on src and target. In this case the target image is (1)
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        os.makedirs( os.path.join( self._env()['out'], '2015', '03', '29') )
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), 
                    os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) )

        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'], '-c']
        picture_arranger.main()
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030(1).jpg' )
        clash_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) 
        out_dir_dd = os.path.join(self._env()['out'], '2015', '03', '29' )
        out_dir_mm = os.path.join(self._env()['out'], '2015', '03')
        out_dir_yy = os.path.join(self._env()['out'], '2015' )

        self.assertTrue( os.path.exists( in_file ), msg="Check source exists") # Is the original there
        self.assertTrue( os.path.exists( clash_file ), msg="Clash file exists") # Is the clash there
        self.assertTrue( os.path.exists( out_file ), msg="Check original is still there"  ) # Is the target there
        
        os.unlink( in_file )
        os.unlink( out_file )
        os.unlink( clash_file )
        os.rmdir( out_dir_dd )
        os.rmdir( out_dir_mm )
        os.rmdir( out_dir_yy )


    def test_clash_move(self):
        '''
        Copy image then do a -f on src and target. In this case the target image is (1)
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        os.makedirs( os.path.join( self._env()['out'], '2015', '03', '29') )
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), 
                    os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) )

        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'] ]
        picture_arranger.main() 
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030(1).jpg' )
        clash_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) 
        out_dir_dd = os.path.join(self._env()['out'], '2015', '03', '29' )
        out_dir_mm = os.path.join(self._env()['out'], '2015', '03')
        out_dir_yy = os.path.join(self._env()['out'], '2015' )

        self.assertFalse( os.path.exists( in_file ), msg="Check source exists") # Is the original there
        self.assertTrue( os.path.exists( clash_file ), msg="Clash file exists") # Is the clash there
        self.assertTrue( os.path.exists( out_file ), msg="Check original is still there"  ) # Is the target there
        
        os.unlink( out_file )
        os.unlink( clash_file )
        os.rmdir( out_dir_dd )
        os.rmdir( out_dir_mm )
        os.rmdir( out_dir_yy )

    def test_src_target_is_copy(self):
        '''
        Copy image then do a -f and diff on src and target.
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        os.makedirs( os.path.join( self._env()['out'], '2015', '03', '29') )
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), 
                    os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) )

        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'], '-s' ]
        picture_arranger.main() 
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030(1).jpg' )
        clash_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) 
        out_dir_dd = os.path.join(self._env()['out'], '2015', '03', '29' )
        out_dir_mm = os.path.join(self._env()['out'], '2015', '03')
        out_dir_yy = os.path.join(self._env()['out'], '2015' )

        self.assertTrue( os.path.exists( in_file ), msg="Check source exists") # Is the original there
        self.assertTrue( os.path.exists( clash_file ), msg="Clash file exists") # Is the clash there
        self.assertFalse( os.path.exists( out_file ), msg="Check target has NOT been created"  ) # Is the target there
        
        os.unlink( in_file )
        os.unlink( clash_file )
    
        os.rmdir( out_dir_dd )
        os.rmdir( out_dir_mm )
        os.rmdir( out_dir_yy )

    def test_noclash_dryrun(self):
        '''
        Copy image then do a -f on src and target
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'], '-d']
        picture_arranger.main()
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' )
 
        self.assertTrue( os.path.exists( in_file ), msg="Check source exists") # Is the original there
        self.assertFalse( os.path.exists( out_file ), msg="Check target is not there"  ) # Is the target there
        
        os.unlink( in_file )
        

    def test_clash_dryrun(self):
        '''
        Copy image then do a -f on src and target. In this case the target image is (1)
        '''
        test_data_dir = self._env()['test_data']
        
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), self._env()['in'] )
        os.makedirs( os.path.join( self._env()['out'], '2015', '03', '29') )
        shutil.copy2( os.path.join(test_data_dir, 'IMG_1030.jpg' ), 
                    os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) )

        sys.argv[1:] = ['-i' + self._env()['in'], '-o' + self._env()['out'], '-d']
        picture_arranger.main()
        
        in_file = os.path.join(self._env()['in'], 'IMG_1030.jpg' )
        out_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030(1).jpg' )
        clash_file = os.path.join(self._env()['out'], '2015', '03', '29', 'IMG_1030.jpg' ) 
        out_dir_dd = os.path.join(self._env()['out'], '2015', '03', '29' )
        out_dir_mm = os.path.join(self._env()['out'], '2015', '03')
        out_dir_yy = os.path.join(self._env()['out'], '2015' )

        self.assertTrue( os.path.exists( in_file ), msg="Check source exists" ) # Is the original there
        self.assertTrue( os.path.exists( clash_file ), msg="Clash file exists" ) # Is the clash there
        self.assertFalse( os.path.exists( out_file ), msg="Check target is not there" ) # Is the target there
        
        os.unlink( in_file )
        os.unlink( clash_file )
        os.rmdir( out_dir_dd )
        os.rmdir( out_dir_mm )
        os.rmdir( out_dir_yy )


def main():
    unittest.main()

if __name__ == '__main__':
    main()