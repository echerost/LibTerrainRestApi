from shapely.geometry import shape
import libterrain
import config.db_config as dbConfig
import LibTerrainRestApi.terrain_analysis.ubiquiti as ubi

STI = None
DEVICES = None

class Link:
    """Link data and operations"""
    DEFAULT_LOSS_VALUE = -999.9
    DEFAULT_AUTO_OFFSET = 0
    DEFAULT_INVALID_POINT_HEIGHT = -100 #this value or below
    DEFAULT_ORIENTATION = 0
    DEFAULT_BITRATE = 0
    
    # input/output rest data name
    SRC_POINT = 'source'
    DST_POINT = 'destination'
    SRC_DEVICE = 'source_device'
    DST_DEVICE = 'destination_device'
    SRC_OFFSET = 'source'
    DST_OFFSET = 'destination'
    AUTO_OFFSET = 'auto'
    SRC_ORIENTATION = 'source_orientation'
    DST_ORIENTATION = 'destination_orientation'
    LINK_POSSIBLE = 'link_is_possible'
    LOSS = 'loss'
    PROFILE = 'profile'
    OFFSETS = 'offsets'
    BITRATE = 'maximum_bitrate'

    def __init__(self, json_input_data:dict):
        
        # devices
        s_dev = json_input_data['source_device']
        d_dev = json_input_data['destination_device']
        if not self.device_exists(s_dev) or not self.device_exists(d_dev):
            raise ValueError('Unknown device')
        self.src_device :str = s_dev
        self.dst_device :str = d_dev
        # points
        self.src : shape = shape(json_input_data[self.SRC_POINT])
        self.dst : shape = shape(json_input_data[self.DST_POINT])
        # offsets
        offsets = self.getHeightOffsets(json_input_data[self.OFFSETS])
        self.auto_offset = offsets['auto']
        self.src_offset : int = offsets['src']
        self.dst_offset :int = offsets['dst']
 
        self.loss :float = self.DEFAULT_LOSS_VALUE
        self.src_orientation :float = self.DEFAULT_ORIENTATION
        self.dst_orientation :float = self.DEFAULT_ORIENTATION
        self.profile = None
        self.is_possible :bool = False
        self.bitrate :float = self.DEFAULT_BITRATE
        

    def link_two_points(self) -> dict : 
        """try to establish a link between two points""" 
        bestLink = None

        # terrain interface initialization
        global STI
        if(STI is None):
            STI = libterrain.SingleTerrainInterface(dbConfig.DB_CONNECTION_STRING,
               lidar_table = dbConfig.LIDAR_TABLE_NAME)

        src = {'coords': self.src,
               'height': self.src_offset,
               'optionals': 'src'}
        dst = {'coords': self.dst,
               'height': self.dst_offset,
               'optionals': 'dst'}
        
        # try establish link using one or multiple offsets
        best_min_offset :int = 0
        if(self.use_auto_offset()):
            # only to semplify link comparison
            bestLinkLoss = -999
            # search for best elevation offset capped by self.auto_offset
            # incrementing both points offsets each time starting from zero
            for x in range(self.auto_offset + 1):
                # update points elevation
                src['height'] = self.src_offset + x
                dst['height'] = self.dst_offset + x

                # attempt to establish link
                tmpLink = STI.get_link(source=src, destination=dst)
                #print("X: " + str(x) + "; Valid: "+ str(tmpLink!=None))

                # switch if new link is better than previous
                if(tmpLink is not None and tmpLink['loss'] > bestLinkLoss):
                    bestLink = tmpLink
                    bestLinkLoss = tmpLink['loss']
                    best_min_offset = x

        else:
            # fixed offsets
            bestLink = STI.get_link(source=src, destination=dst)

        # if link is possible, set data
        if(bestLink is not None):
            if(self.use_auto_offset()):
                self.auto_offset = best_min_offset
                self.src_offset = self.dst_offset = self.auto_offset
            self.loss = round(bestLink['loss'],4)
            self.src_orientation = bestLink['src_orient']
            self.dst_orientation = bestLink['dst_orient']
            self.is_possible = True
            profile = list(filter(self.removeInvalidProfilePoints, bestLink['profile']))
            self.profile = profile
            
            # devices and bitrate
            self.bitrate = ubi.get_maximum_rate(abs(self.loss), self.src_device, self.dst_device)
        return self

    def use_auto_offset(self) -> bool:
        """ link is calculated using fixed or auto offsets? """
        return self.auto_offset > self.DEFAULT_AUTO_OFFSET

    def __eq__(self, other): 
        if not isinstance(other, Link):
            # don't attempt to compare against unrelated types
            return NotImplemented
        o = other
        s = self
        return (s.is_possible == o.is_possible and s.src == o.src and s.dst == o.dst
                # device
                and s.src_device == o.src_device and s.dst_device == o.dst_device
                # offset
                and s.auto_offset == o.auto_offset and s.src_offset == o.src_offset and s.dst_offset == o.dst_offset
                # orientation
                and s.src_orientation == o.src_orientation and s.dst_orientation == o.dst_orientation
                # loss + bitrate
                and s.loss == o.loss and s.bitrate == o.bitrate)

    @classmethod
    def getHeightOffsets(cls, offsets:dict) -> dict:
        """ Parses offset data """
        retval = {}
        if(cls.AUTO_OFFSET in offsets):
            retval['auto'] = offsets[cls.AUTO_OFFSET]
            retval['src'] = retval['dst'] = 0
        else:
            retval['auto'] = cls.DEFAULT_AUTO_OFFSET
            retval['src'] = offsets[cls.SRC_OFFSET]
            retval['dst'] = offsets[cls.DST_OFFSET]
        return retval

    @classmethod
    def removeInvalidProfilePoints(cls,point):
        """ Removes all profile points having invalid height """
        return True if point[2] > cls.DEFAULT_INVALID_POINT_HEIGHT else False

    @classmethod
    def device_exists(cls,device:str) -> bool:
        cls.load_devices()
        return device in DEVICES                

    @classmethod
    def get_devices(cls) -> dict:
        """Get the device codes that the user can choose """
        cls.load_devices()
        global DEVICES
        return DEVICES
    
    @classmethod
    def load_devices(cls):
        global DEVICES
        if DEVICES is None:
            ubi.load_devices()
            DEVICES = ubi.devices
        
