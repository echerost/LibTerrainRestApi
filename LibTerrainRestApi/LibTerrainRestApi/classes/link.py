from shapely.geometry import shape
import libterrain
import config.db_config as dbConfig

STI = None

class Link:
    """Source, destination, offset and other data of link"""
    DEFAULT_LOSS_VALUE = -999.9
    DEFAULT_AUTO_OFFSET = 0
    DEFAULT_INVALID_POINT_HEIGHT = -100 #this value or below

    def __init__(self, json_input_data:dict):
      # points
      self.source : shape = shape(json_input_data['source'])
      self.destination : shape = shape(json_input_data['destination'])
      # offsets
      offsets = self.getHeightOffsets(json_input_data['offsets'])
      self.auto_offset = offsets['auto']
      self.source_offset : int = offsets['src']
      self.destination_offset :int = offsets['dst']
 
      self.loss :float = self.DEFAULT_LOSS_VALUE
      self.source_orientation :float = 0
      self.destination_orientation :float = 0
      self.profile = None
      self.is_possible :bool = False

    def link_two_points(self) -> dict : 
        """try to establish a link between two points""" 
        bestLink = None

        # terrain interface initialization
        global STI
        if(STI is None):
            STI = libterrain.SingleTerrainInterface(dbConfig.DB_CONNECTION_STRING,
               lidar_table = dbConfig.LIDAR_TABLE_NAME)

        src = {'coords': self.source,
               'height': self.source_offset,
               'optionals': 'src'}
        dst = {'coords': self.destination,
               'height': self.destination_offset,
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
                src['height'] = self.source_offset + x
                dst['height'] = self.destination_offset + x

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
                self.source_offset = self.destination_offset = offset
            self.loss = bestLink['loss']
            self.source_orientation = bestLink['src_orient']
            self.destination_orientation = bestLink['dst_orient']
            self.is_possible = True
            profile = list(filter(self.removeInvalidProfilePoints, bestLink['profile']))
            print("Profile: " + str(len(bestLink['profile'])))
            self.profile = profile
        return self

    def use_auto_offset(self) -> bool:
        """ link is calculated using fixed or auto offsets? """
        return self.auto_offset > self.DEFAULT_AUTO_OFFSET

    @classmethod
    def getHeightOffsets(cls, offsets:dict) -> dict:
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
        return True if point[2] > cls.DEFAULT_INVALID_POINT_HEIGHT else False
        
