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

    def __init__(self, json_input_data:dict):
        
        # devices
        s_dev = json_input_data['source_device']
        d_dev = json_input_data['destination_device']
        if not self.device_exists(s_dev) or not self.device_exists(d_dev):
           raise ValueError('Unknown device')
        self.src_device :str = s_dev
        self.dst_device :str = d_dev
        # points
        self.src : shape = shape(json_input_data['source'])
        self.dst : shape = shape(json_input_data['destination'])
        # offsets
        offsets = self.getHeightOffsets(json_input_data['offsets'])
        self.auto_offset = offsets['auto']
        self.src_offset : int = offsets['src']
        self.dst_offset :int = offsets['dst']
 
        self.loss :float = self.DEFAULT_LOSS_VALUE
        self.src_orientation :float = 0
        self.dst_orientation :float = 0
        self.profile = None
        self.is_possible :bool = False
        self.bitrate :float = 0
        

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
        offset = 0
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
                    offset = x

        else:
           # fixed offsets
           bestLink = STI.get_link(source=src, destination=dst)

        # if link is possible, set data
        if(bestLink is not None):
            if(self.use_auto_offset()):
                self.src_offset = self.dst_offset = offset
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

    @classmethod
    def getHeightOffsets(cls, offsets:dict) -> dict:
        """ Parses offset data """
        retval = {}
        if('auto' in offsets):
            retval['auto'] = offsets['auto']
            retval['src'] = retval['dst'] = 0
        else:
            retval['auto'] = cls.DEFAULT_AUTO_OFFSET
            retval['src'] = offsets['source']
            retval['dst'] = offsets['destination']
        return retval

    @classmethod
    def removeInvalidProfilePoints(cls,point):
        """ Removes all profile points having invalid height """
        return True if point[2] > cls.DEFAULT_INVALID_POINT_HEIGHT else False

    @classmethod
    def device_exists(cls,device:str) -> bool:
        global DEVICES
        return device in DEVICES                

    @classmethod
    def get_devices(cls) -> dict:
        """Get the device codes that the user can choose """
        global DEVICES
        if DEVICES is None:
            ubi.load_devices()
            DEVICES = ubi.devices
        return DEVICES
        
