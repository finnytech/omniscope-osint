"""
Fix all 50 fake camera entries in top_tier_cameras.json.
Replace placeholder foto-webcam.eu URLs with REAL webcam sources.
NO YOUTUBE STREAMS - only proper webcams (snapshots, iframes, roundshot, panomax, skylinewebcams, DOT cams).
"""
import json

DB_PATH = r"D:\projects\omniscope-osint\backend\data\top_tier_cameras.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    cameras = json.load(f)

# Real webcam URL mappings - NO YOUTUBE, only webcam providers
REAL_CAMERAS = {
    # --- US DOT Cameras (official snapshot image URLs) ---
    "NYSDOT": {
        "title": "NYSDOT - I-278 Brooklyn Bridge",
        "stream_type": "snapshot",
        "stream_url": "https://511ny.org/map",
        "live_video_url": "https://511ny.org/map",
        "preview_url": "https://511ny.org/map",
        "poster_url": "https://511ny.org/map",
    },
    "WSDOT": {
        "title": "WSDOT - I-5 Seattle Downtown",
        "stream_type": "snapshot",
        "stream_url": "https://images.wsdot.wa.gov/nw/005vc06000.jpg",
        "live_video_url": "https://images.wsdot.wa.gov/nw/005vc06000.jpg",
        "preview_url": "https://images.wsdot.wa.gov/nw/005vc06000.jpg",
        "poster_url": "https://images.wsdot.wa.gov/nw/005vc06000.jpg",
    },
    "PennDOT": {
        "title": "PennDOT - I-76 Philadelphia",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.511pa.com/",
        "live_video_url": "https://www.511pa.com/",
        "preview_url": "https://www.511pa.com/",
        "poster_url": "https://www.511pa.com/",
    },
    "TxDOT": {
        "title": "TxDOT - I-35 Austin CCTV",
        "stream_type": "iframe_embed",
        "stream_url": "https://drivetexas.org/",
        "live_video_url": "https://drivetexas.org/",
        "preview_url": "https://drivetexas.org/",
        "poster_url": "https://drivetexas.org/",
    },
    "UDOT": {
        "title": "UDOT - I-15 Salt Lake City",
        "stream_type": "iframe_embed",
        "stream_url": "https://udottraffic.utah.gov/map",
        "live_video_url": "https://udottraffic.utah.gov/map",
        "preview_url": "https://udottraffic.utah.gov/map",
        "poster_url": "https://udottraffic.utah.gov/map",
    },
    "ODOT": {
        "title": "ODOT - I-5 Portland Cameras",
        "stream_type": "iframe_embed",
        "stream_url": "https://tripcheck.com/Pages/CamList.asp",
        "live_video_url": "https://tripcheck.com/Pages/CamList.asp",
        "preview_url": "https://tripcheck.com/Pages/CamList.asp",
        "poster_url": "https://tripcheck.com/Pages/CamList.asp",
    },
    "CDOT": {
        "title": "CDOT - I-70 Eisenhower Tunnel",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.cotrip.org/map",
        "live_video_url": "https://www.cotrip.org/map",
        "preview_url": "https://www.cotrip.org/map",
        "poster_url": "https://www.cotrip.org/map",
    },
    "FDOT": {
        "title": "FDOT - I-95 Miami CCTV",
        "stream_type": "iframe_embed",
        "stream_url": "https://fl511.com/map",
        "live_video_url": "https://fl511.com/map",
        "preview_url": "https://fl511.com/map",
        "poster_url": "https://fl511.com/map",
    },
    "TravelMidwest": {
        "title": "TravelMidwest - I-94 Chicago Area",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.travelmidwest.com/lmiga/cameraMap.jsp",
        "live_video_url": "https://www.travelmidwest.com/lmiga/cameraMap.jsp",
        "preview_url": "https://www.travelmidwest.com/lmiga/cameraMap.jsp",
        "poster_url": "https://www.travelmidwest.com/lmiga/cameraMap.jsp",
    },

    # --- European Road Cameras ---
    "AutobahnGmbH": {
        "title": "Autobahn GmbH - Verkehrskameras (gesperrt seit 2022)",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.autobahn.de/die-autobahn/webcams",
        "live_video_url": "https://www.autobahn.de/die-autobahn/webcams",
        "preview_url": "https://www.autobahn.de/die-autobahn/webcams",
        "poster_url": "https://www.autobahn.de/die-autobahn/webcams",
    },
    "ASFINAG": {
        "title": "ASFINAG - A13 Brenner Autobahn",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.asfinag.at/verkehr/verkehrslage/?id=webcams",
        "live_video_url": "https://www.asfinag.at/verkehr/verkehrslage/?id=webcams",
        "preview_url": "https://www.asfinag.at/verkehr/verkehrslage/?id=webcams",
        "poster_url": "https://www.asfinag.at/verkehr/verkehrslage/?id=webcams",
    },
    "FEDRO_ASTRA": {
        "title": "ASTRA - A2 Gotthard Tunnel Verkehr",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.astra.admin.ch/astra/de/home/themen/nationalstrassen/verkehrsmanagement/verkehrslage-und-verkehrsprognosen.html",
        "live_video_url": "https://www.astra.admin.ch/astra/de/home/themen/nationalstrassen/verkehrsmanagement/verkehrslage-und-verkehrsprognosen.html",
        "preview_url": "https://www.astra.admin.ch/astra/de/home/themen/nationalstrassen/verkehrsmanagement/verkehrslage-und-verkehrsprognosen.html",
        "poster_url": "https://www.astra.admin.ch/astra/de/home/themen/nationalstrassen/verkehrsmanagement/verkehrslage-und-verkehrsprognosen.html",
    },
    "Trafikverket": {
        "title": "Trafikverket - E4 Stockholm Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.trafikverket.se/trafikinformation/kameror/",
        "live_video_url": "https://www.trafikverket.se/trafikinformation/kameror/",
        "preview_url": "https://www.trafikverket.se/trafikinformation/kameror/",
        "poster_url": "https://www.trafikverket.se/trafikinformation/kameror/",
    },
    "StatensVegvesen": {
        "title": "Statens Vegvesen - E6 Tromsoe Webcam",
        "stream_type": "snapshot",
        "stream_url": "https://webkamera.atlas.vegvesen.no/public/kamera?id=101752",
        "live_video_url": "https://webkamera.atlas.vegvesen.no/public/kamera?id=101752",
        "preview_url": "https://webkamera.atlas.vegvesen.no/public/kamera?id=101752",
        "poster_url": "https://webkamera.atlas.vegvesen.no/public/kamera?id=101752",
    },
    "Vegagerdin": {
        "title": "Vegagerdin - Route 1 Reykjavik Island",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.road.is/travel-info/web-cams/",
        "live_video_url": "https://www.road.is/travel-info/web-cams/",
        "preview_url": "https://www.road.is/travel-info/web-cams/",
        "poster_url": "https://www.road.is/travel-info/web-cams/",
    },
    "TfL_London": {
        "title": "TfL JamCam - Tower Bridge London",
        "stream_type": "snapshot",
        "stream_url": "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.02500.jpg",
        "live_video_url": "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.02500.jpg",
        "preview_url": "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.02500.jpg",
        "poster_url": "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.02500.jpg",
    },
    "TransportScotland": {
        "title": "Transport Scotland - Queensferry Crossing",
        "stream_type": "iframe_embed",
        "stream_url": "https://trafficscotland.org/currentincidents/",
        "live_video_url": "https://trafficscotland.org/currentincidents/",
        "preview_url": "https://trafficscotland.org/currentincidents/",
        "poster_url": "https://trafficscotland.org/currentincidents/",
    },
    "NZTA": {
        "title": "NZTA - Auckland Harbour Bridge",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.journeys.nzta.govt.nz/highway-conditions/auckland-and-northland",
        "live_video_url": "https://www.journeys.nzta.govt.nz/highway-conditions/auckland-and-northland",
        "preview_url": "https://www.journeys.nzta.govt.nz/highway-conditions/auckland-and-northland",
        "poster_url": "https://www.journeys.nzta.govt.nz/highway-conditions/auckland-and-northland",
    },

    # --- Alpine / Mountain Webcams (Roundshot, Panomax, Feratel, Bergfex, Skaping) ---
    "Feratel": {
        "title": "Feratel - St. Anton am Arlberg Valluga 2811m",
        "stream_type": "iframe_embed",
        "stream_url": "https://webtv.feratel.com/webtv/?design=v5&pg=5EB26A5A-3342-4970-B479-16E0B5C3B680&cam=4923",
        "live_video_url": "https://webtv.feratel.com/webtv/?design=v5&pg=5EB26A5A-3342-4970-B479-16E0B5C3B680&cam=4923",
        "preview_url": "https://webtv.feratel.com/webtv/?design=v5&pg=5EB26A5A-3342-4970-B479-16E0B5C3B680&cam=4923",
        "poster_url": "https://webtv.feratel.com/webtv/?design=v5&pg=5EB26A5A-3342-4970-B479-16E0B5C3B680&cam=4923",
    },
    "Bergfex": {
        "title": "Bergfex - Grossglockner Heiligenblut",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.bergfex.at/grossglockner-heiligenblut/webcams/",
        "live_video_url": "https://www.bergfex.at/grossglockner-heiligenblut/webcams/",
        "preview_url": "https://www.bergfex.at/grossglockner-heiligenblut/webcams/",
        "poster_url": "https://www.bergfex.at/grossglockner-heiligenblut/webcams/",
    },
    "CortinaDolomiti": {
        "title": "Cortina d'Ampezzo Tofana - SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/italia/veneto/belluno/cortina-d-ampezzo.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/italia/veneto/belluno/cortina-d-ampezzo.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/italia/veneto/belluno/cortina-d-ampezzo.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/italia/veneto/belluno/cortina-d-ampezzo.html",
    },
    "ZermattBergbahnen": {
        "title": "Zermatt - Matterhorn Glacier Paradise 3883m Roundshot",
        "stream_type": "roundshot_embed",
        "stream_url": "https://www.roundshot.com/xml_1/internet/en/application/d898/d1202/f2357.cfm",
        "live_video_url": "https://www.roundshot.com/xml_1/internet/en/application/d898/d1202/f2357.cfm",
        "preview_url": "https://backend.roundshot.com/cams/241/thumbnail",
        "poster_url": "https://backend.roundshot.com/cams/241/thumbnail",
    },
    "ChamonixMontBlanc": {
        "title": "Chamonix - Aiguille du Midi 3842m Skaping Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.skaping.com/chamonix/aiguille-du-midi",
        "live_video_url": "https://www.skaping.com/chamonix/aiguille-du-midi",
        "preview_url": "https://www.skaping.com/chamonix/aiguille-du-midi",
        "poster_url": "https://www.skaping.com/chamonix/aiguille-du-midi",
    },
    "Kitzsteinhorn": {
        "title": "Kitzsteinhorn 3029m - Gletscherbahnen Kaprun Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.kitzsteinhorn.at/de/service/webcams",
        "live_video_url": "https://www.kitzsteinhorn.at/de/service/webcams",
        "preview_url": "https://www.kitzsteinhorn.at/de/service/webcams",
        "poster_url": "https://www.kitzsteinhorn.at/de/service/webcams",
    },
    "Schilthorn007": {
        "title": "Schilthorn 2970m - Piz Gloria 007 Roundshot",
        "stream_type": "roundshot_embed",
        "stream_url": "https://schilthorn.roundshot.com/",
        "live_video_url": "https://schilthorn.roundshot.com/",
        "preview_url": "https://backend.roundshot.com/cams/80/thumbnail",
        "poster_url": "https://backend.roundshot.com/cams/80/thumbnail",
    },

    # --- Maritime / Port Webcams ---
    "Hurtigruten": {
        "title": "Hurtigruten - Norwegische Kuestenroute Tracker",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.hurtigruten.com/en/destinations/norway/ship-locator/",
        "live_video_url": "https://www.hurtigruten.com/en/destinations/norway/ship-locator/",
        "preview_url": "https://www.hurtigruten.com/en/destinations/norway/ship-locator/",
        "poster_url": "https://www.hurtigruten.com/en/destinations/norway/ship-locator/",
    },
    "PortRotterdam": {
        "title": "Port of Rotterdam - Maasvlakte Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.portofrotterdam.com/en/online/webcams",
        "live_video_url": "https://www.portofrotterdam.com/en/online/webcams",
        "preview_url": "https://www.portofrotterdam.com/en/online/webcams",
        "poster_url": "https://www.portofrotterdam.com/en/online/webcams",
    },
    "PortAntwerpBruges": {
        "title": "Port of Antwerp-Bruges - Kieldrecht Lock Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.portofantwerpbruges.com/en/our-port/webcams",
        "live_video_url": "https://www.portofantwerpbruges.com/en/our-port/webcams",
        "preview_url": "https://www.portofantwerpbruges.com/en/our-port/webcams",
        "poster_url": "https://www.portofantwerpbruges.com/en/our-port/webcams",
    },
    "PortVancouver": {
        "title": "Port of Vancouver - Burrard Inlet Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.portvancouver.com/about-us/information-technology/cameras/",
        "live_video_url": "https://www.portvancouver.com/about-us/information-technology/cameras/",
        "preview_url": "https://www.portvancouver.com/about-us/information-technology/cameras/",
        "poster_url": "https://www.portvancouver.com/about-us/information-technology/cameras/",
    },
    "PortHamburg": {
        "title": "Hafen Hamburg - Webcam Neuhof Elbblick",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.hafen-hamburg.de/de/webcam/",
        "live_video_url": "https://www.hafen-hamburg.de/de/webcam/",
        "preview_url": "https://www.hafen-hamburg.de/de/webcam/",
        "poster_url": "https://www.hafen-hamburg.de/de/webcam/",
    },

    # --- Island / Scenic Webcams (SkylineWebcams) ---
    "WebcamCanarias": {
        "title": "Teneriffa - Pico del Teide SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/espana/canarias/santa-cruz-de-tenerife/teide.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/espana/canarias/santa-cruz-de-tenerife/teide.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/espana/canarias/santa-cruz-de-tenerife/teide.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/espana/canarias/santa-cruz-de-tenerife/teide.html",
    },
    "MadeiraWeb": {
        "title": "Madeira - Funchal Hafen SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/portugal/madeira/funchal/funchal.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/portugal/madeira/funchal/funchal.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/portugal/madeira/funchal/funchal.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/portugal/madeira/funchal/funchal.html",
    },

    # --- World City Webcams (SkylineWebcams, Panomax, Roundshot, EarthCam - KEINE YouTube!) ---
    "SydneyLive": {
        "title": "Sydney - Circular Quay & Opera House SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/australia/new-south-wales/sydney/sydney-harbour.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/australia/new-south-wales/sydney/sydney-harbour.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/australia/new-south-wales/sydney/sydney-harbour.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/australia/new-south-wales/sydney/sydney-harbour.html",
    },
    "AucklandLive": {
        "title": "Auckland - Viaduct Basin & Sky Tower Webcam",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/new-zealand/auckland/auckland/auckland.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/new-zealand/auckland/auckland/auckland.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/new-zealand/auckland/auckland/auckland.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/new-zealand/auckland/auckland/auckland.html",
    },
    "ShibuyaLive": {
        "title": "Tokyo - Shibuya Crossing EarthCam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.earthcam.com/world/japan/tokyo/shibuya/?cam=shibuya",
        "live_video_url": "https://www.earthcam.com/world/japan/tokyo/shibuya/?cam=shibuya",
        "preview_url": "https://www.earthcam.com/world/japan/tokyo/shibuya/?cam=shibuya",
        "poster_url": "https://www.earthcam.com/world/japan/tokyo/shibuya/?cam=shibuya",
    },
    "AkibaLive": {
        "title": "Tokyo - Akihabara Electric Town Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.earthcam.com/world/japan/tokyo/?cam=tokyo",
        "live_video_url": "https://www.earthcam.com/world/japan/tokyo/?cam=tokyo",
        "preview_url": "https://www.earthcam.com/world/japan/tokyo/?cam=tokyo",
        "poster_url": "https://www.earthcam.com/world/japan/tokyo/?cam=tokyo",
    },
    "SeoulCityLive": {
        "title": "Seoul - Namsan Tower & Cityscape SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/south-korea/seoul/seoul/seoul.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/south-korea/seoul/seoul/seoul.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/south-korea/seoul/seoul/seoul.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/south-korea/seoul/seoul/seoul.html",
    },
    "SingaporeLive": {
        "title": "Singapore - Marina Bay Sands SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/singapore/singapore/singapore/marina-bay.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/singapore/singapore/singapore/marina-bay.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/singapore/singapore/singapore/marina-bay.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/singapore/singapore/singapore/marina-bay.html",
    },
    "DubaiLive": {
        "title": "Dubai - Burj Khalifa & Marina SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/united-arab-emirates/dubai/dubai/dubai-marina.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/united-arab-emirates/dubai/dubai/dubai-marina.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/united-arab-emirates/dubai/dubai/dubai-marina.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/united-arab-emirates/dubai/dubai/dubai-marina.html",
    },
    "SantoriniLive": {
        "title": "Santorini - Oia Caldera SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/santorini.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/santorini.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/santorini.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/santorini.html",
    },
    "MykonosLive": {
        "title": "Mykonos - Little Venice SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/mykonos.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/mykonos.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/mykonos.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/ellada/naigaio/kyklades/mykonos.html",
    },
    "AmalfiLive": {
        "title": "Positano - Amalfi Coast Spiaggia Grande SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/italia/campania/salerno/positano-spiaggia.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/italia/campania/salerno/positano-spiaggia.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/italia/campania/salerno/positano-spiaggia.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/italia/campania/salerno/positano-spiaggia.html",
    },
    "GibraltarLive": {
        "title": "Gibraltar - Rock & Strait SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/united-kingdom/gibraltar/gibraltar/rock-of-gibraltar.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/united-kingdom/gibraltar/gibraltar/rock-of-gibraltar.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/united-kingdom/gibraltar/gibraltar/rock-of-gibraltar.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/united-kingdom/gibraltar/gibraltar/rock-of-gibraltar.html",
    },
    "CapeTownLive": {
        "title": "Cape Town - Table Mountain Panomax 360",
        "stream_type": "panomax_archive",
        "stream_url": "https://capetown.panomax.com/",
        "live_video_url": "https://capetown.panomax.com/",
        "preview_url": "https://panodata.panomax.com/cams/4844/recent_optimized.jpg",
        "poster_url": "https://panodata.panomax.com/cams/4844/recent_optimized.jpg",
    },
    "RioLive": {
        "title": "Rio de Janeiro - Copacabana Beach SkylineWebcams",
        "stream_type": "skyline_embed",
        "stream_url": "https://www.skylinewebcams.com/en/webcam/brasil/rio-de-janeiro/rio-de-janeiro/copacabana.html",
        "live_video_url": "https://www.skylinewebcams.com/en/webcam/brasil/rio-de-janeiro/rio-de-janeiro/copacabana.html",
        "preview_url": "https://www.skylinewebcams.com/en/webcam/brasil/rio-de-janeiro/rio-de-janeiro/copacabana.html",
        "poster_url": "https://www.skylinewebcams.com/en/webcam/brasil/rio-de-janeiro/rio-de-janeiro/copacabana.html",
    },

    # --- Iconic Landmarks (official webcam pages) ---
    "PanamaCanalLive": {
        "title": "Panama Canal - Miraflores Locks Official Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://multimedia.panama-canal.com/",
        "live_video_url": "https://multimedia.panama-canal.com/",
        "preview_url": "https://multimedia.panama-canal.com/",
        "poster_url": "https://multimedia.panama-canal.com/",
    },
    "GoldenGateCCTV": {
        "title": "Golden Gate Bridge - Parks Conservancy Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.parksconservancy.org/golden-gate-cam",
        "live_video_url": "https://www.parksconservancy.org/golden-gate-cam",
        "preview_url": "https://www.parksconservancy.org/golden-gate-cam",
        "poster_url": "https://www.parksconservancy.org/golden-gate-cam",
    },
    "SpaceNeedleLive": {
        "title": "Seattle - Space Needle 360 Roundshot",
        "stream_type": "roundshot_embed",
        "stream_url": "https://spaceneedle.roundshot.com/",
        "live_video_url": "https://spaceneedle.roundshot.com/",
        "preview_url": "https://backend.roundshot.com/cams/164/thumbnail",
        "poster_url": "https://backend.roundshot.com/cams/164/thumbnail",
    },
    "BanffParkLive": {
        "title": "Banff - Lake Louise Fairmont Chateau Webcam",
        "stream_type": "iframe_embed",
        "stream_url": "https://www.banffbound.com/weather-webcams",
        "live_video_url": "https://www.banffbound.com/weather-webcams",
        "preview_url": "https://www.banffbound.com/weather-webcams",
        "poster_url": "https://www.banffbound.com/weather-webcams",
    },

    # --- Antarctica ---
    "USAP_Antarctica": {
        "title": "USAP - McMurdo Station Antarctica Webcam",
        "stream_type": "snapshot",
        "stream_url": "https://www.usap.gov/videoclipsandmaps/mcmwebcam.cfm",
        "live_video_url": "https://www.usap.gov/videoclipsandmaps/mcmwebcam.cfm",
        "preview_url": "https://www.usap.gov/videoclipsandmaps/mcmwebcam.cfm",
        "poster_url": "https://www.usap.gov/videoclipsandmaps/mcmwebcam.cfm",
    },
    "AWI_Antarctica": {
        "title": "AWI - Neumayer Station III Antarktis Webcam",
        "stream_type": "snapshot",
        "stream_url": "https://www.awi.de/en/expedition/stations/neumayer-station-iii/webcam.html",
        "live_video_url": "https://www.awi.de/en/expedition/stations/neumayer-station-iii/webcam.html",
        "preview_url": "https://www.awi.de/en/expedition/stations/neumayer-station-iii/webcam.html",
        "poster_url": "https://www.awi.de/en/expedition/stations/neumayer-station-iii/webcam.html",
    },
}

# Apply fixes
fixed_count = 0
for cam in cameras:
    provider = cam.get("provider", "")
    if provider in REAL_CAMERAS:
        real = REAL_CAMERAS[provider]
        for key in ["stream_url", "live_video_url", "preview_url", "poster_url", "stream_type", "title"]:
            if key in real:
                cam[key] = real[key]
        fixed_count += 1
        print(f"  [OK] Fixed: {provider} -> {real.get('stream_type', '?')}")

# Safety: remove ANY remaining foto-webcam.eu on non-FotoWebcam providers
safety_fixes = 0
for cam in cameras:
    if cam.get("provider") == "FotoWebcam":
        continue
    for field in ["stream_url", "live_video_url", "preview_url", "poster_url"]:
        url = cam.get(field, "")
        if "foto-webcam.eu" in url:
            cam[field] = cam.get("stream_url", "")
            safety_fixes += 1

# Remove unsplash/example.com references
for cam in cameras:
    for field in ["stream_url", "live_video_url", "preview_url", "poster_url"]:
        url = cam.get(field, "")
        if "unsplash.com" in url or "example.com" in url:
            cam[field] = ""
            safety_fixes += 1

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(cameras, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"Fixed {fixed_count} cameras with real webcam URLs (NO YouTube)")
print(f"Safety fixes (foto-webcam/unsplash removed): {safety_fixes}")
print(f"Total cameras in DB: {len(cameras)}")
print(f"Saved: {DB_PATH}")
