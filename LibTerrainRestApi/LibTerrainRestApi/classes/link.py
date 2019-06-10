from shapely.geometry import shape
import libterrain
import config.db_config as dbConfig

class Link:
    """Source, destination, offset and other data of requested link by user"""
    STI = None

    def __init__(self, json_input_data):
      self.source = shape(json_input_data['source'])
      self.destination = shape(json_input_data['destination'])
      offsets = json_input_data['offsets']
      self.auto_offset = offsets['auto']
      self.source_offset = 0 if self.auto_offset > 0 else offsets['source'] 
      self.destination_offset = 0 if self.auto_offset > 0 else offsets['destination']
      self.link = None

    def is_possible(self) -> bool:
      return self.link != None

    def link_two_points(self) -> dict : 
        """try to establish a link between two points""" 
        bestLink = None
        bestLinkLoss = -999

        # terrain interface initialization
        if(self.STI == None):
            print("STI nulla")
            STI = libterrain.SingleTerrainInterface(dbConfig.DB_CONNECTION_STRING, lidar_table = dbConfig.LIDAR_TABLE_NAME)

        src = {
        'coords': self.source,
         'height': self.source_offset,
         'optionals': 'src'
            }
        dst = {
        'coords': self.destination,
        'height': self.destination_offset,
        'optionals': 'dst'
            }
        # search for best elevation offset capped by self.auto_offset
        if(self.auto_offset > 0):
            for x in range(self.auto_offset + 1):
                # update points elevation
                src.height = self.source_offset + x
                dst.height = self.destination_offset + x

                # attempt to establish link
                tmpLink = STI.get_link(source=src, destination=dst)

                # switch if best link
                if(tmpLink != None and tmpLink['loss'] > bestLinkLoss):
                    bestLink = tmpLink
                    bestLinkLoss = tmpLink['loss']
                else:
                    bestLink = STI.get_link(source=src, destination=dst)

        self.link = bestLink
        return self.link 
