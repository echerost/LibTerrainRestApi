import unittest
import libterrain
from LibTerrainRestApi.link import Link
import LibTerrainRestApi.test.testdata as tdata
import configs.config as cfg

STI = None
class Test_test_link(unittest.TestCase):
    
    def setUp(self):
        global STI
        STI = libterrain.SingleTerrainInterface(cfg.DB_CONNECTION_STRING,
               lidar_table = cfg.LIDAR_TABLE_NAME)

    def test_link_auto_offset(self):
        data = tdata.a_input
        test_link = Link(data)
        test_link = test_link.link_two_points()

        link = Link(data)
        link = self.helper_patch_link(link,tdata.a_link_ok)
        self.assertEqual(test_link,link)

    def test_link_manual_offset(self):
        data = tdata.m_input
        test_link = Link(data)
        test_link = test_link.link_two_points()

        link = Link(data)
        link = self.helper_patch_link(link,tdata.m_link_ok)
        self.assertEqual(test_link,link)

    @classmethod
    def helper_patch_link(cls, link:Link, patch:dict) -> Link:
        """ cache some data in link
            Patch can have only data to change, not all 'Link' instance data
        """
        # device (antenna)
        if Link.SRC_DEVICE in patch: link.src_device = patch[Link.SRC_DEVICE]
        if Link.DST_DEVICE in patch: link.dst_device = patch[Link.DST_DEVICE]
        # offsets
        if Link.OFFSETS in patch:
            offsets=patch[Link.OFFSETS]             
            if Link.AUTO_OFFSET in offsets:
                link.auto_offset = offsets[Link.AUTO_OFFSET]
                link.src_offset =link.dst_offset= offsets[Link.AUTO_OFFSET]
            else:
                if Link.SRC_OFFSET in offsets:
                    link.src_offset = offsets[Link.SRC_OFFSET]
                if Link.DST_OFFSET in offsets:
                    link.dst_offset = offsets[Link.DST_OFFSET]
        
        if Link.LOSS in patch:link.loss = patch[Link.LOSS]
        if Link.SRC_ORIENTATION in patch:link.src_orientation = patch[Link.SRC_ORIENTATION]
        if Link.DST_ORIENTATION in patch:link.dst_orientation = patch[Link.DST_ORIENTATION]
        if Link.PROFILE in patch:link.profile = patch[Link.PROFILE]
        if Link.LINK_POSSIBLE in patch:link.is_possible = patch[Link.LINK_POSSIBLE]
        if Link.BITRATE in patch: link.bitrate = patch[Link.BITRATE]
        return link       
        

if __name__ == '__test__':
    unittest.main()
