from LibTerrainRestApi.link import Link

m_input = {
            Link.SRC_POINT: {
                'type': 'Point',
                'coordinates':[11.129426,43.951486]
            },
            Link.DST_POINT: {
                'type': 'Point',
                'coordinates': [11.129399,43.952413]
            },
            Link.OFFSETS: {
	            Link.SRC_OFFSET: 5,
	            Link.DST_OFFSET: 8
            },
            Link.SRC_DEVICE: 'AM-IsoStation5AC',
            Link.DST_DEVICE: 'AM-IsoStation5AC'}

m_link_ok = {
            Link.LINK_POSSIBLE: True,
            Link.SRC_ORIENTATION:(271.6683374483668,181.89205108296812),
            Link.DST_ORIENTATION:(91.66833744836678,178.10794891703188),
            Link.BITRATE:(86.7, 86.7),
            Link.LOSS:86.6133
            # TODO: add profile
}
a_input = {
            Link.SRC_POINT: {
                'type': 'Point',
                'coordinates':[11.129426,43.951486]
            },
            Link.DST_POINT: {
                'type': 'Point',
                'coordinates': [11.129399,43.952413]
            },
            Link.OFFSETS: {
                Link.AUTO_OFFSET: 5
            },
            Link.SRC_DEVICE: 'AM-IsoStation5AC',
            Link.DST_DEVICE: 'AM-IsoStation5AC'}

a_link_ok = {
            Link.LINK_POSSIBLE: True,
            Link.OFFSETS: {
                Link.AUTO_OFFSET: 0
            },
            Link.SRC_ORIENTATION:150,
            Link.DST_ORIENTATION:150,
            Link.BITRATE:90
            # TODO: add profile
}

# device that user can use
devices = ["AM-IsoStation5AC", "AM-IsoStation5AC_90",
                  "AM-LiteBeam5ACGEN2", "AM-NanoBeam5ACGEN2",
                  "AM-NanoStation5AC", "AM-NanoStation5ACL",
                  "AM-PowerBeam5AC300ISO", "AM-PowerBeam5AC400ISO",
                  "AM-PowerBeam5AC500ISO"]


#m_input_res = {
#                Link.SRC_POINT: {
#                'type': 'Point',
#                'coordinates':[11.129426,43.951486]
#                },
#                Link.DST_POINT: {
#                    'type': 'Point',
#                    'coordinates': [11.129399,43.952413]
#                },
#                Link.OFFSETS: {
#	                Link.SRC_OFFSET: 5,
#	                Link.DST_OFFSET: 8,
#                    Link.AUTO_OFFSET: 0
#                },
#                Link.SRC_DEVICE: str(m_input[Link.SRC_DEVICE]),
#                Link.DST_DEVICE: str(m_input[Link.DST_DEVICE]),
#                Link.LINK_POSSIBLE: True,
#                Link.SRC_ORIENTATION:150,
#                Link.DST_ORIENTATION:150,
#                Link.BITRATE:90
#                # TODO: add profile               
#}


