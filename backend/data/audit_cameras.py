import json

data = json.load(open(r'D:\projects\omniscope-osint\backend\data\top_tier_cameras.json'))

new_providers = ['NYSDOT','WSDOT','PennDOT','TxDOT','UDOT','ODOT','CDOT','FDOT','TravelMidwest',
    'AutobahnGmbH','ASFINAG','FEDRO_ASTRA','Trafikverket','StatensVegvesen','Vegagerdin',
    'TfL_London','TransportScotland','NZTA','WebcamCanarias','MadeiraWeb','Feratel','Bergfex',
    'CortinaDolomiti','ZermattBergbahnen','ChamonixMontBlanc','Kitzsteinhorn','Schilthorn007',
    'Hurtigruten','PortRotterdam','PortAntwerpBruges','PortVancouver','SydneyLive','AucklandLive',
    'ShibuyaLive','AkibaLive','SeoulCityLive','SingaporeLive','DubaiLive','SantoriniLive',
    'MykonosLive','AmalfiLive','GibraltarLive','CapeTownLive','RioLive','PanamaCanalLive',
    'GoldenGateCCTV','SpaceNeedleLive','BanffParkLive','USAP_Antarctica','AWI_Antarctica','PortHamburg']

for cam in data:
    if cam.get('provider') in new_providers:
        print(f"--- {cam['provider']} / {cam['id']} ---")
        print(f"  stream_url: {cam.get('stream_url','MISSING')}")
        print(f"  preview_url: {cam.get('preview_url','MISSING')}")
        print(f"  poster_url: {cam.get('poster_url','MISSING')}")
        print(f"  live_video_url: {cam.get('live_video_url','MISSING')}")
        print(f"  stream_type: {cam.get('stream_type','MISSING')}")
        print()
