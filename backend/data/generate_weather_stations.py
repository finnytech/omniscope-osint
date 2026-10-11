import os
import sys
import json
import csv
import io
import urllib.request
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WeatherStationsGenerator")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, ".cache")
OUTPUT_FILE = os.path.join(BASE_DIR, "weather_stations.json")

CONTINENT_MAP = {
    "NA": "North America",
    "EU": "Europe",
    "AS": "Asia",
    "AF": "Africa",
    "SA": "South America",
    "OC": "Oceania",
    "AN": "Antarctica"
}

FIPS_TO_COUNTRY = {
    "AF": ("Afghanistan", "Asia"),
    "AL": ("Albania", "Europe"),
    "AG": ("Algeria", "Africa"),
    "AN": ("Andorra", "Europe"),
    "AO": ("Angola", "Africa"),
    "AR": ("Argentina", "South America"),
    "AM": ("Armenia", "Asia"),
    "AS": ("Australia", "Oceania"),
    "AU": ("Austria", "Europe"),
    "AJ": ("Azerbaijan", "Asia"),
    "BF": ("Bahamas", "North America"),
    "BA": ("Bahrain", "Asia"),
    "BG": ("Bangladesh", "Asia"),
    "BB": ("Barbados", "North America"),
    "BO": ("Belarus", "Europe"),
    "BE": ("Belgium", "Europe"),
    "BH": ("Belize", "North America"),
    "BN": ("Benin", "Africa"),
    "BT": ("Bhutan", "Asia"),
    "BL": ("Bolivia", "South America"),
    "BK": ("Bosnia and Herzegovina", "Europe"),
    "BC": ("Botswana", "Africa"),
    "BR": ("Brazil", "South America"),
    "BX": ("Brunei", "Asia"),
    "BU": ("Bulgaria", "Europe"),
    "UV": ("Burkina Faso", "Africa"),
    "BY": ("Burundi", "Africa"),
    "CB": ("Cambodia", "Asia"),
    "CM": ("Cameroon", "Africa"),
    "CA": ("Canada", "North America"),
    "CV": ("Cape Verde", "Africa"),
    "CT": ("Central African Republic", "Africa"),
    "CD": ("Chad", "Africa"),
    "CI": ("Chile", "South America"),
    "CH": ("China", "Asia"),
    "CO": ("Colombia", "South America"),
    "CN": ("Comoros", "Africa"),
    "CF": ("Congo", "Africa"),
    "CG": ("DR Congo", "Africa"),
    "CS": ("Costa Rica", "North America"),
    "IV": ("Cote d'Ivoire", "Africa"),
    "HR": ("Croatia", "Europe"),
    "CU": ("Cuba", "North America"),
    "CY": ("Cyprus", "Asia"),
    "EZ": ("Czech Republic", "Europe"),
    "DA": ("Denmark", "Europe"),
    "DJ": ("Djibouti", "Africa"),
    "DR": ("Dominican Republic", "North America"),
    "EC": ("Ecuador", "South America"),
    "EG": ("Egypt", "Africa"),
    "ES": ("El Salvador", "North America"),
    "EK": ("Equatorial Guinea", "Africa"),
    "ER": ("Eritrea", "Africa"),
    "EN": ("Estonia", "Europe"),
    "ET": ("Ethiopia", "Africa"),
    "FJ": ("Fiji", "Oceania"),
    "FI": ("Finland", "Europe"),
    "FR": ("France", "Europe"),
    "GB": ("Gabon", "Africa"),
    "GA": ("Gambia", "Africa"),
    "GG": ("Georgia", "Asia"),
    "GM": ("Germany", "Europe"),
    "GH": ("Ghana", "Africa"),
    "GR": ("Greece", "Europe"),
    "GL": ("Greenland", "North America"),
    "GT": ("Guatemala", "North America"),
    "GV": ("Guinea", "Africa"),
    "GY": ("Guyana", "South America"),
    "HA": ("Haiti", "North America"),
    "HO": ("Honduras", "North America"),
    "HU": ("Hungary", "Europe"),
    "IC": ("Iceland", "Europe"),
    "IN": ("India", "Asia"),
    "ID": ("Indonesia", "Asia"),
    "IR": ("Iran", "Asia"),
    "IZ": ("Iraq", "Asia"),
    "EI": ("Ireland", "Europe"),
    "IS": ("Israel", "Asia"),
    "IT": ("Italy", "Europe"),
    "JM": ("Jamaica", "North America"),
    "JA": ("Japan", "Asia"),
    "JO": ("Jordan", "Asia"),
    "KZ": ("Kazakhstan", "Asia"),
    "KE": ("Kenya", "Africa"),
    "KN": ("North Korea", "Asia"),
    "KS": ("South Korea", "Asia"),
    "KU": ("Kuwait", "Asia"),
    "KG": ("Kyrgyzstan", "Asia"),
    "LA": ("Laos", "Asia"),
    "LG": ("Latvia", "Europe"),
    "LE": ("Lebanon", "Asia"),
    "LT": ("Lesotho", "Africa"),
    "LI": ("Liberia", "Africa"),
    "LY": ("Libya", "Africa"),
    "LH": ("Lithuania", "Europe"),
    "LU": ("Luxembourg", "Europe"),
    "MK": ("North Macedonia", "Europe"),
    "MA": ("Madagascar", "Africa"),
    "MI": ("Malawi", "Africa"),
    "MY": ("Malaysia", "Asia"),
    "MV": ("Maldives", "Asia"),
    "ML": ("Mali", "Africa"),
    "MT": ("Malta", "Europe"),
    "MR": ("Mauritania", "Africa"),
    "MP": ("Mauritius", "Africa"),
    "MX": ("Mexico", "North America"),
    "MD": ("Moldova", "Europe"),
    "MN": ("Monaco", "Europe"),
    "MG": ("Mongolia", "Asia"),
    "MJ": ("Montenegro", "Europe"),
    "MO": ("Morocco", "Africa"),
    "MZ": ("Mozambique", "Africa"),
    "WA": ("Namibia", "Africa"),
    "NP": ("Nepal", "Asia"),
    "NL": ("Netherlands", "Europe"),
    "NZ": ("New Zealand", "Oceania"),
    "NU": ("Nicaragua", "North America"),
    "NG": ("Niger", "Africa"),
    "NI": ("Nigeria", "Africa"),
    "NO": ("Norway", "Europe"),
    "MU": ("Oman", "Asia"),
    "PK": ("Pakistan", "Asia"),
    "PS": ("Palau", "Oceania"),
    "PM": ("Panama", "North America"),
    "PP": ("Papua New Guinea", "Oceania"),
    "PA": ("Paraguay", "South America"),
    "PE": ("Peru", "South America"),
    "RP": ("Philippines", "Asia"),
    "PL": ("Poland", "Europe"),
    "PO": ("Portugal", "Europe"),
    "QA": ("Qatar", "Asia"),
    "RO": ("Romania", "Europe"),
    "RS": ("Russia", "Europe"),
    "RW": ("Rwanda", "Africa"),
    "SA": ("Saudi Arabia", "Asia"),
    "SG": ("Senegal", "Africa"),
    "RI": ("Serbia", "Europe"),
    "SE": ("Seychelles", "Africa"),
    "SL": ("Sierra Leone", "Africa"),
    "SN": ("Singapore", "Asia"),
    "LO": ("Slovakia", "Europe"),
    "SI": ("Slovenia", "Europe"),
    "BP": ("Solomon Islands", "Oceania"),
    "SO": ("Somalia", "Africa"),
    "SF": ("South Africa", "Africa"),
    "SP": ("Spain", "Europe"),
    "CE": ("Sri Lanka", "Asia"),
    "SU": ("Sudan", "Africa"),
    "OD": ("South Sudan", "Africa"),
    "NS": ("Suriname", "South America"),
    "WZ": ("Eswatini", "Africa"),
    "SW": ("Sweden", "Europe"),
    "SZ": ("Switzerland", "Europe"),
    "SY": ("Syria", "Asia"),
    "TW": ("Taiwan", "Asia"),
    "TI": ("Tajikistan", "Asia"),
    "TZ": ("Tanzania", "Africa"),
    "TH": ("Thailand", "Asia"),
    "TO": ("Togo", "Africa"),
    "TN": ("Tonga", "Oceania"),
    "TD": ("Trinidad and Tobago", "North America"),
    "TS": ("Tunisia", "Africa"),
    "TU": ("Turkey", "Asia"),
    "TX": ("Turkmenistan", "Asia"),
    "UG": ("Uganda", "Africa"),
    "UP": ("Ukraine", "Europe"),
    "AE": ("United Arab Emirates", "Asia"),
    "UK": ("United Kingdom", "Europe"),
    "US": ("United States", "North America"),
    "UY": ("Uruguay", "South America"),
    "UZ": ("Uzbekistan", "Asia"),
    "NH": ("Vanuatu", "Oceania"),
    "VE": ("Venezuela", "South America"),
    "VM": ("Vietnam", "Asia"),
    "YM": ("Yemen", "Asia"),
    "ZA": ("Zambia", "Africa"),
    "ZI": ("Zimbabwe", "Africa"),
    "AY": ("Antarctica", "Antarctica")
}

def fetch_file(url, cache_filename):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, cache_filename)
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        logger.info(f"Using cached file: {cache_path}")
        with open(cache_path, "rb") as f:
            return f.read()

    logger.info(f"Downloading {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "CyberSpectreNexus/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()
    with open(cache_path, "wb") as f:
        f.write(content)
    logger.info(f"Downloaded and cached {len(content)} bytes to {cache_path}")
    return content

STORM_CHASER_POSTS = [
    # Tornado Alley & Great Plains Severe Weather Posts
    {"id": "storm_nssl_spc_ok", "name": "NOAA National Severe Storms Laboratory & SPC", "country": "United States", "continent": "North America", "lat": 35.1809, "lon": -97.4402, "elevation": 360.0, "type": "storm_chaser_post"},
    {"id": "storm_el_reno_ok", "name": "El Reno Storm Intercept Observatory", "country": "United States", "continent": "North America", "lat": 35.5325, "lon": -97.9550, "elevation": 415.0, "type": "storm_chaser_post"},
    {"id": "storm_moore_ok", "name": "Moore Central Oklahoma Mesonet Tower", "country": "United States", "continent": "North America", "lat": 35.3395, "lon": -97.4867, "elevation": 382.0, "type": "storm_chaser_post"},
    {"id": "storm_vance_enid_ok", "name": "Vance AFB / Enid Doppler Radar Post", "country": "United States", "continent": "North America", "lat": 36.3392, "lon": -97.9164, "elevation": 398.0, "type": "storm_chaser_post"},
    {"id": "storm_hobart_ok", "name": "Hobart Southwest Oklahoma Severe Post", "country": "United States", "continent": "North America", "lat": 35.0094, "lon": -99.0514, "elevation": 467.0, "type": "storm_chaser_post"},
    {"id": "storm_altus_ok", "name": "Altus Severe Storm Observation Station", "country": "United States", "continent": "North America", "lat": 34.6670, "lon": -99.2667, "elevation": 420.0, "type": "storm_chaser_post"},
    {"id": "storm_woodward_ok", "name": "Woodward High Plains Mesonet Station", "country": "United States", "continent": "North America", "lat": 36.4258, "lon": -99.4189, "elevation": 580.0, "type": "storm_chaser_post"},
    {"id": "storm_guymon_ok", "name": "Guymon Panhandle Supercell Post", "country": "United States", "continent": "North America", "lat": 36.6828, "lon": -101.5039, "elevation": 952.0, "type": "storm_chaser_post"},
    {"id": "storm_clinton_ok", "name": "Clinton-Sherman Severe Radar Post", "country": "United States", "continent": "North America", "lat": 35.3375, "lon": -99.2008, "elevation": 586.0, "type": "storm_chaser_post"},
    {"id": "storm_wichita_ks", "name": "Wichita Mid-Continent Severe Storm Center", "country": "United States", "continent": "North America", "lat": 37.6499, "lon": -97.4331, "elevation": 406.0, "type": "storm_chaser_post"},
    {"id": "storm_dodge_city_ks", "name": "Dodge City NWS Severe Radar Post", "country": "United States", "continent": "North America", "lat": 37.7608, "lon": -99.9689, "elevation": 788.0, "type": "storm_chaser_post"},
    {"id": "storm_goodland_ks", "name": "Goodland High Plains Storm Observatory", "country": "United States", "continent": "North America", "lat": 39.3708, "lon": -101.6989, "elevation": 1114.0, "type": "storm_chaser_post"},
    {"id": "storm_russell_ks", "name": "Russell Supercell Research Station", "country": "United States", "continent": "North America", "lat": 38.8719, "lon": -98.8108, "elevation": 567.0, "type": "storm_chaser_post"},
    {"id": "storm_salina_ks", "name": "Salina Central Kansas Storm Post", "country": "United States", "continent": "North America", "lat": 38.7911, "lon": -97.6522, "elevation": 392.0, "type": "storm_chaser_post"},
    {"id": "storm_topeka_ks", "name": "Topeka Severe Weather Center", "country": "United States", "continent": "North America", "lat": 39.0733, "lon": -95.6264, "elevation": 269.0, "type": "storm_chaser_post"},
    {"id": "storm_garden_city_ks", "name": "Garden City Western Plains Observatory", "country": "United States", "continent": "North America", "lat": 37.9275, "lon": -100.7244, "elevation": 880.0, "type": "storm_chaser_post"},
    {"id": "storm_hays_ks", "name": "Hays Western Plains Storm Post", "country": "United States", "continent": "North America", "lat": 38.8447, "lon": -99.2728, "elevation": 610.0, "type": "storm_chaser_post"},
    {"id": "storm_amarillo_tx", "name": "Amarillo Panhandle Storm Tracker Station", "country": "United States", "continent": "North America", "lat": 35.2194, "lon": -101.7058, "elevation": 1099.0, "type": "storm_chaser_post"},
    {"id": "storm_lubbock_tx", "name": "Texas Tech University Mesonet Center", "country": "United States", "continent": "North America", "lat": 33.6636, "lon": -101.8228, "elevation": 992.0, "type": "storm_chaser_post"},
    {"id": "storm_plainview_tx", "name": "Plainview South Plains Weather Station", "country": "United States", "continent": "North America", "lat": 34.1697, "lon": -101.7169, "elevation": 1028.0, "type": "storm_chaser_post"},
    {"id": "storm_childress_tx", "name": "Childress Red River Storm Post", "country": "United States", "continent": "North America", "lat": 34.4339, "lon": -100.2881, "elevation": 595.0, "type": "storm_chaser_post"},
    {"id": "storm_vernon_tx", "name": "Vernon Wilbarger Mesonet Post", "country": "United States", "continent": "North America", "lat": 34.1561, "lon": -99.2817, "elevation": 385.0, "type": "storm_chaser_post"},
    {"id": "storm_wichita_falls_tx", "name": "Wichita Falls Severe Storm Tracking Post", "country": "United States", "continent": "North America", "lat": 33.9889, "lon": -98.4917, "elevation": 311.0, "type": "storm_chaser_post"},
    {"id": "storm_abilene_tx", "name": "Abilene West Texas Storm Observatory", "country": "United States", "continent": "North America", "lat": 32.4114, "lon": -99.6819, "elevation": 546.0, "type": "storm_chaser_post"},
    {"id": "storm_san_angelo_tx", "name": "San Angelo Concho Valley Weather Post", "country": "United States", "continent": "North America", "lat": 31.3578, "lon": -100.4964, "elevation": 584.0, "type": "storm_chaser_post"},
    {"id": "storm_midland_tx", "name": "Midland Permian Basin Radar Station", "country": "United States", "continent": "North America", "lat": 31.9425, "lon": -102.2019, "elevation": 875.0, "type": "storm_chaser_post"},
    {"id": "storm_stephenville_tx", "name": "Stephenville Central Texas Radar Post", "country": "United States", "continent": "North America", "lat": 32.2189, "lon": -98.1789, "elevation": 396.0, "type": "storm_chaser_post"},
    {"id": "storm_north_platte_ne", "name": "North Platte Sandhills Storm Intercept", "country": "United States", "continent": "North America", "lat": 41.1256, "lon": -100.6836, "elevation": 846.0, "type": "storm_chaser_post"},
    {"id": "storm_grand_island_ne", "name": "Grand Island Central Nebraska Storm Post", "country": "United States", "continent": "North America", "lat": 40.9675, "lon": -98.3086, "elevation": 563.0, "type": "storm_chaser_post"},
    {"id": "storm_hastings_ne", "name": "Hastings NWS Severe Warning Post", "country": "United States", "continent": "North America", "lat": 40.6053, "lon": -98.4281, "elevation": 622.0, "type": "storm_chaser_post"},
    {"id": "storm_kearney_ne", "name": "Kearney Platte River Storm Observatory", "country": "United States", "continent": "North America", "lat": 40.7270, "lon": -99.0068, "elevation": 650.0, "type": "storm_chaser_post"},
    {"id": "storm_mccook_ne", "name": "McCook Southwest Nebraska Mesonet", "country": "United States", "continent": "North America", "lat": 40.2064, "lon": -100.5925, "elevation": 787.0, "type": "storm_chaser_post"},
    {"id": "storm_valentine_ne", "name": "Valentine Cherry County Storm Post", "country": "United States", "continent": "North America", "lat": 42.8581, "lon": -100.5489, "elevation": 792.0, "type": "storm_chaser_post"},
    {"id": "storm_scottsbluff_ne", "name": "Scottsbluff High Plains Radar Post", "country": "United States", "continent": "North America", "lat": 41.8742, "lon": -103.5956, "elevation": 1205.0, "type": "storm_chaser_post"},
    {"id": "storm_rapid_city_sd", "name": "Rapid City Black Hills Severe Outpost", "country": "United States", "continent": "North America", "lat": 44.0453, "lon": -103.0572, "elevation": 964.0, "type": "storm_chaser_post"},
    {"id": "storm_aberdeen_sd", "name": "Aberdeen Northern Plains Storm Station", "country": "United States", "continent": "North America", "lat": 45.4492, "lon": -98.4217, "elevation": 397.0, "type": "storm_chaser_post"},
    {"id": "storm_pierre_sd", "name": "Pierre Missouri River Weather Station", "country": "United States", "continent": "North America", "lat": 44.3828, "lon": -100.2858, "elevation": 531.0, "type": "storm_chaser_post"},
    {"id": "storm_sioux_falls_sd", "name": "Sioux Falls Tri-State Severe Post", "country": "United States", "continent": "North America", "lat": 43.5822, "lon": -96.7419, "elevation": 436.0, "type": "storm_chaser_post"},
    {"id": "storm_des_moines_ia", "name": "Des Moines Central Iowa Storm Center", "country": "United States", "continent": "North America", "lat": 41.5339, "lon": -93.6631, "elevation": 292.0, "type": "storm_chaser_post"},
    {"id": "storm_lamoni_ia", "name": "Lamoni Southern Iowa Mesonet Station", "country": "United States", "continent": "North America", "lat": 40.6339, "lon": -93.9014, "elevation": 346.0, "type": "storm_chaser_post"},
    {"id": "storm_mason_city_ia", "name": "Mason City North Iowa Storm Post", "country": "United States", "continent": "North America", "lat": 43.1578, "lon": -93.3314, "elevation": 369.0, "type": "storm_chaser_post"},
    {"id": "storm_waterloo_ia", "name": "Waterloo Cedar Valley Severe Post", "country": "United States", "continent": "North America", "lat": 42.5572, "lon": -92.4003, "elevation": 266.0, "type": "storm_chaser_post"},
    {"id": "storm_davenport_ia", "name": "Davenport Quad Cities Radar Post", "country": "United States", "continent": "North America", "lat": 41.6103, "lon": -90.5881, "elevation": 230.0, "type": "storm_chaser_post"},
    {"id": "storm_springfield_mo", "name": "Springfield Ozarks Severe Storm Post", "country": "United States", "continent": "North America", "lat": 37.2456, "lon": -93.3886, "elevation": 386.0, "type": "storm_chaser_post"},
    {"id": "storm_joplin_mo", "name": "Joplin Tornado Memorial Observatory", "country": "United States", "continent": "North America", "lat": 37.1519, "lon": -94.4983, "elevation": 300.0, "type": "storm_chaser_post"},
    {"id": "storm_pleasant_hill_mo", "name": "Pleasant Hill Kansas City Radar Post", "country": "United States", "continent": "North America", "lat": 38.8103, "lon": -94.2644, "elevation": 290.0, "type": "storm_chaser_post"},
    {"id": "storm_fort_smith_ar", "name": "Fort Smith River Valley Storm Post", "country": "United States", "continent": "North America", "lat": 35.3367, "lon": -94.3675, "elevation": 143.0, "type": "storm_chaser_post"},
    {"id": "storm_little_rock_ar", "name": "Little Rock Central Arkansas Storm Post", "country": "United States", "continent": "North America", "lat": 34.7294, "lon": -92.2247, "elevation": 80.0, "type": "storm_chaser_post"},
    {"id": "storm_jackson_ms", "name": "Jackson Central Mississippi Severe Center", "country": "United States", "continent": "North America", "lat": 32.3117, "lon": -90.0781, "elevation": 101.0, "type": "storm_chaser_post"},
    {"id": "storm_tupelo_ms", "name": "Tupelo North Mississippi Storm Intercept", "country": "United States", "continent": "North America", "lat": 34.2681, "lon": -88.7697, "elevation": 110.0, "type": "storm_chaser_post"},
    {"id": "storm_huntsville_al", "name": "Huntsville Supercell Radar Center", "country": "United States", "continent": "North America", "lat": 34.6403, "lon": -86.7758, "elevation": 192.0, "type": "storm_chaser_post"},
    {"id": "storm_birmingham_al", "name": "Birmingham Central Alabama Severe Post", "country": "United States", "continent": "North America", "lat": 33.5639, "lon": -86.7536, "elevation": 196.0, "type": "storm_chaser_post"},
    
    # Hurricane Coasts & Tropical Cyclone Monitoring Posts
    {"id": "storm_nhc_miami_fl", "name": "National Hurricane Center HQ Station", "country": "United States", "continent": "North America", "lat": 25.7533, "lon": -80.3833, "elevation": 5.0, "type": "storm_chaser_post"},
    {"id": "storm_key_west_fl", "name": "Key West Extreme Hurricane Intercept", "country": "United States", "continent": "North America", "lat": 24.5558, "lon": -81.7597, "elevation": 1.0, "type": "storm_chaser_post"},
    {"id": "storm_marathon_fl", "name": "Marathon Middle Keys Storm Station", "country": "United States", "continent": "North America", "lat": 24.7261, "lon": -81.0514, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_naples_fl", "name": "Naples Southwest Gulf Hurricane Post", "country": "United States", "continent": "North America", "lat": 26.1525, "lon": -81.7753, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_tampa_bay_fl", "name": "Tampa Bay Hurricane Surge Observatory", "country": "United States", "continent": "North America", "lat": 27.9755, "lon": -82.5332, "elevation": 8.0, "type": "storm_chaser_post"},
    {"id": "storm_cedar_key_fl", "name": "Cedar Key Nature Coast Hurricane Station", "country": "United States", "continent": "North America", "lat": 29.1378, "lon": -83.0353, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_apalachicola_fl", "name": "Apalachicola Forgotten Coast Storm Post", "country": "United States", "continent": "North America", "lat": 29.7275, "lon": -84.9833, "elevation": 6.0, "type": "storm_chaser_post"},
    {"id": "storm_pensacola_fl", "name": "Pensacola Western Panhandle Storm Post", "country": "United States", "continent": "North America", "lat": 30.4733, "lon": -87.1867, "elevation": 34.0, "type": "storm_chaser_post"},
    {"id": "storm_mobile_bay_al", "name": "Mobile Bay Tropical Cyclone Intercept", "country": "United States", "continent": "North America", "lat": 30.6914, "lon": -88.0678, "elevation": 4.0, "type": "storm_chaser_post"},
    {"id": "storm_dauphin_island_al", "name": "Dauphin Island Hurricane Surge Post", "country": "United States", "continent": "North America", "lat": 30.2508, "lon": -88.1139, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_gulfport_ms", "name": "Gulfport Central Gulf Hurricane Station", "country": "United States", "continent": "North America", "lat": 30.4072, "lon": -89.0700, "elevation": 8.0, "type": "storm_chaser_post"},
    {"id": "storm_biloxi_ms", "name": "Biloxi Back Bay Storm Observatory", "country": "United States", "continent": "North America", "lat": 30.4100, "lon": -88.9200, "elevation": 6.0, "type": "storm_chaser_post"},
    {"id": "storm_grand_isle_la", "name": "Grand Isle Coastal Hurricane Station", "country": "United States", "continent": "North America", "lat": 29.2367, "lon": -89.9872, "elevation": 1.0, "type": "storm_chaser_post"},
    {"id": "storm_lake_pontchartrain_la", "name": "Lake Pontchartrain Hurricane Surge Post", "country": "United States", "continent": "North America", "lat": 30.0425, "lon": -90.0283, "elevation": 1.0, "type": "storm_chaser_post"},
    {"id": "storm_lake_charles_la", "name": "Lake Charles Southwest Louisiana Storm Post", "country": "United States", "continent": "North America", "lat": 30.1261, "lon": -93.2233, "elevation": 5.0, "type": "storm_chaser_post"},
    {"id": "storm_cameron_la", "name": "Cameron Coastal Hurricane Surge Station", "country": "United States", "continent": "North America", "lat": 29.7978, "lon": -93.3256, "elevation": 1.0, "type": "storm_chaser_post"},
    {"id": "storm_sabine_pass_tx", "name": "Sabine Pass Coastal Storm Station", "country": "United States", "continent": "North America", "lat": 29.7333, "lon": -93.8833, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_galveston_pier_tx", "name": "Galveston Pleasure Pier Hurricane Station", "country": "United States", "continent": "North America", "lat": 29.2858, "lon": -94.7892, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_freeport_tx", "name": "Freeport Coastal Wind & Surge Post", "country": "United States", "continent": "North America", "lat": 28.9500, "lon": -95.3500, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_matagorda_tx", "name": "Matagorda Bay Tropical Cyclone Post", "country": "United States", "continent": "North America", "lat": 28.6942, "lon": -95.9686, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_corpus_christi_tx", "name": "Corpus Christi Coastal Bend Storm Post", "country": "United States", "continent": "North America", "lat": 27.7703, "lon": -97.5011, "elevation": 13.0, "type": "storm_chaser_post"},
    {"id": "storm_port_aransas_tx", "name": "Port Aransas Mustang Island Storm Post", "country": "United States", "continent": "North America", "lat": 27.8339, "lon": -97.0611, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_south_padre_tx", "name": "South Padre Island Extreme Coastal Post", "country": "United States", "continent": "North America", "lat": 26.1119, "lon": -97.1681, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_brownsville_tx", "name": "Brownsville Rio Grande Tropical Post", "country": "United States", "continent": "North America", "lat": 25.9069, "lon": -97.4258, "elevation": 7.0, "type": "storm_chaser_post"},
    {"id": "storm_savannah_ga", "name": "Savannah Coastal Hurricane Station", "country": "United States", "continent": "North America", "lat": 32.1275, "lon": -81.2022, "elevation": 15.0, "type": "storm_chaser_post"},
    {"id": "storm_tybee_island_ga", "name": "Tybee Island Barrier Beach Storm Post", "country": "United States", "continent": "North America", "lat": 32.0003, "lon": -80.8456, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_charleston_sc", "name": "Charleston Lowcountry Hurricane Center", "country": "United States", "continent": "North America", "lat": 32.8986, "lon": -80.0405, "elevation": 14.0, "type": "storm_chaser_post"},
    {"id": "storm_myrtle_beach_sc", "name": "Myrtle Beach Grand Strand Storm Post", "country": "United States", "continent": "North America", "lat": 33.6797, "lon": -78.9283, "elevation": 8.0, "type": "storm_chaser_post"},
    {"id": "storm_cape_fear_nc", "name": "Cape Fear Coastal Cyclone Observatory", "country": "United States", "continent": "North America", "lat": 33.8500, "lon": -77.9667, "elevation": 4.0, "type": "storm_chaser_post"},
    {"id": "storm_cape_lookout_nc", "name": "Cape Lookout National Seashore Storm Post", "country": "United States", "continent": "North America", "lat": 34.6214, "lon": -76.5256, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_cape_hatteras_nc", "name": "Cape Hatteras Outer Banks Storm Center", "country": "United States", "continent": "North America", "lat": 35.2678, "lon": -75.5492, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_duck_pier_nc", "name": "Duck Pier Coastal Storm Surge Facility", "country": "United States", "continent": "North America", "lat": 36.1839, "lon": -75.7503, "elevation": 7.0, "type": "storm_chaser_post"},
    {"id": "storm_virginia_beach_va", "name": "Virginia Beach Atlantic Storm Observatory", "country": "United States", "continent": "North America", "lat": 36.8529, "lon": -75.9780, "elevation": 5.0, "type": "storm_chaser_post"},
    {"id": "storm_ocean_city_md", "name": "Ocean City Delmarva Coastal Weather Post", "country": "United States", "continent": "North America", "lat": 38.3365, "lon": -75.0849, "elevation": 2.0, "type": "storm_chaser_post"},
    {"id": "storm_cape_may_nj", "name": "Cape May Coastal Storm Station", "country": "United States", "continent": "North America", "lat": 38.9351, "lon": -74.9060, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_atlantic_city_nj", "name": "Atlantic City Ocean Pier Weather Station", "country": "United States", "continent": "North America", "lat": 39.3643, "lon": -74.4229, "elevation": 3.0, "type": "storm_chaser_post"},
    {"id": "storm_montauk_point_ny", "name": "Montauk Point Long Island Storm Post", "country": "United States", "continent": "North America", "lat": 41.0714, "lon": -71.8564, "elevation": 18.0, "type": "storm_chaser_post"},
    {"id": "storm_cape_cod_ma", "name": "Cape Cod Outer Cape Gale Station", "country": "United States", "continent": "North America", "lat": 42.0500, "lon": -70.1833, "elevation": 12.0, "type": "storm_chaser_post"},
    {"id": "storm_san_juan_pr", "name": "San Juan NWS Tropical Warning Post", "country": "Puerto Rico", "continent": "North America", "lat": 18.4325, "lon": -66.0028, "elevation": 9.0, "type": "storm_chaser_post"},
    {"id": "storm_hamilton_bda", "name": "Hamilton Bermuda Atlantic Hurricane Post", "country": "Bermuda", "continent": "North America", "lat": 32.3644, "lon": -64.6786, "elevation": 6.0, "type": "storm_chaser_post"}
]

COASTAL_STATIONS = [
    {"id": "coastal_ambrose_ny", "name": "Ambrose Light Offshore Station", "country": "United States", "continent": "North America", "lat": 40.4600, "lon": -73.8300, "elevation": 25.0, "type": "coastal_station"},
    {"id": "coastal_buzzards_bay_ma", "name": "Buzzards Bay Tower Marine Station", "country": "United States", "continent": "North America", "lat": 41.3967, "lon": -71.0333, "elevation": 20.0, "type": "coastal_station"},
    {"id": "coastal_boston_light_ma", "name": "Boston Harbor Light Marine Station", "country": "United States", "continent": "North America", "lat": 42.3278, "lon": -70.8900, "elevation": 22.0, "type": "coastal_station"},
    {"id": "coastal_portland_head_me", "name": "Portland Head Light Coastal Station", "country": "United States", "continent": "North America", "lat": 43.6231, "lon": -70.2078, "elevation": 24.0, "type": "coastal_station"},
    {"id": "coastal_mt_desert_rock_me", "name": "Mount Desert Rock Offshore Marine Post", "country": "United States", "continent": "North America", "lat": 43.9683, "lon": -68.1283, "elevation": 18.0, "type": "coastal_station"},
    {"id": "coastal_diamond_shoals_nc", "name": "Diamond Shoals Light Tower C-MAN", "country": "United States", "continent": "North America", "lat": 35.1517, "lon": -75.3000, "elevation": 30.0, "type": "coastal_station"},
    {"id": "coastal_frying_pan_nc", "name": "Frying Pan Shoals Light Tower C-MAN", "country": "United States", "continent": "North America", "lat": 33.4833, "lon": -77.5833, "elevation": 28.0, "type": "coastal_station"},
    {"id": "coastal_chesapeake_light_va", "name": "Chesapeake Light Tower Marine Station", "country": "United States", "continent": "North America", "lat": 36.9050, "lon": -75.7133, "elevation": 37.0, "type": "coastal_station"},
    {"id": "coastal_savannah_light_ga", "name": "Savannah Light Tower C-MAN Station", "country": "United States", "continent": "North America", "lat": 31.9400, "lon": -80.6833, "elevation": 25.0, "type": "coastal_station"},
    {"id": "coastal_st_augustine_fl", "name": "St. Augustine Coastal Marine Post", "country": "United States", "continent": "North America", "lat": 29.9600, "lon": -81.2650, "elevation": 6.0, "type": "coastal_station"},
    {"id": "coastal_canaveral_fl", "name": "Cape Canaveral Offshore Weather Station", "country": "United States", "continent": "North America", "lat": 28.4667, "lon": -80.5333, "elevation": 5.0, "type": "coastal_station"},
    {"id": "coastal_fowey_rocks_fl", "name": "Fowey Rocks Marine Light Station", "country": "United States", "continent": "North America", "lat": 25.5900, "lon": -80.0967, "elevation": 34.0, "type": "coastal_station"},
    {"id": "coastal_molasses_reef_fl", "name": "Molasses Reef Marine C-MAN Station", "country": "United States", "continent": "North America", "lat": 25.0117, "lon": -80.3750, "elevation": 14.0, "type": "coastal_station"},
    {"id": "coastal_sombrero_key_fl", "name": "Sombrero Key Marine Light Station", "country": "United States", "continent": "North America", "lat": 24.6267, "lon": -81.1100, "elevation": 49.0, "type": "coastal_station"},
    {"id": "coastal_sand_key_fl", "name": "Sand Key Light Marine Station", "country": "United States", "continent": "North America", "lat": 24.4533, "lon": -81.8767, "elevation": 33.0, "type": "coastal_station"},
    {"id": "coastal_dry_tortugas_fl", "name": "Dry Tortugas Marine Sanctuary Station", "country": "United States", "continent": "North America", "lat": 24.6283, "lon": -82.8733, "elevation": 3.0, "type": "coastal_station"},
    {"id": "coastal_pulley_ridge_fl", "name": "Pulley Ridge Deep Gulf Marine Station", "country": "United States", "continent": "North America", "lat": 24.8500, "lon": -83.7000, "elevation": 0.0, "type": "coastal_station"},
    {"id": "coastal_sw_pass_delta_la", "name": "Southwest Pass Mississippi River Delta", "country": "United States", "continent": "North America", "lat": 28.9317, "lon": -89.4283, "elevation": 18.0, "type": "coastal_station"},
    {"id": "coastal_south_timbalier_la", "name": "South Timbalier Offshore Oil Platform", "country": "United States", "continent": "North America", "lat": 28.8417, "lon": -90.4833, "elevation": 22.0, "type": "coastal_station"},
    {"id": "coastal_eugene_island_la", "name": "Eugene Island Offshore Marine Platform", "country": "United States", "continent": "North America", "lat": 28.3667, "lon": -91.6433, "elevation": 24.0, "type": "coastal_station"},
    {"id": "coastal_galveston_offshore_tx", "name": "Galveston Offshore Platform 12 C-MAN", "country": "United States", "continent": "North America", "lat": 29.1767, "lon": -94.6983, "elevation": 20.0, "type": "coastal_station"},
    {"id": "coastal_port_aransas_tx", "name": "Port Aransas Marine C-MAN Station", "country": "United States", "continent": "North America", "lat": 27.8383, "lon": -97.0500, "elevation": 5.0, "type": "coastal_station"},
    {"id": "coastal_point_arguello_ca", "name": "Point Arguello Coastal Marine Station", "country": "United States", "continent": "North America", "lat": 34.5767, "lon": -120.6500, "elevation": 28.0, "type": "coastal_station"},
    {"id": "coastal_point_conception_ca", "name": "Point Conception Marine Station", "country": "United States", "continent": "North America", "lat": 34.4483, "lon": -120.4717, "elevation": 38.0, "type": "coastal_station"},
    {"id": "coastal_farallon_islands_ca", "name": "Farallon Islands Marine Observatory", "country": "United States", "continent": "North America", "lat": 37.6989, "lon": -123.0033, "elevation": 85.0, "type": "coastal_station"},
    {"id": "coastal_point_reyes_ca", "name": "Point Reyes Marine Weather Station", "country": "United States", "continent": "North America", "lat": 37.9967, "lon": -123.0233, "elevation": 62.0, "type": "coastal_station"},
    {"id": "coastal_cape_mendocino_ca", "name": "Cape Mendocino Coastal Marine Post", "country": "United States", "continent": "North America", "lat": 40.4400, "lon": -124.4083, "elevation": 98.0, "type": "coastal_station"},
    {"id": "coastal_trinidad_head_ca", "name": "Trinidad Head Coastal Observatory", "country": "United States", "continent": "North America", "lat": 41.0550, "lon": -124.1500, "elevation": 32.0, "type": "coastal_station"},
    {"id": "coastal_cape_blanco_or", "name": "Cape Blanco Light Marine Station", "country": "United States", "continent": "North America", "lat": 42.8367, "lon": -124.5650, "elevation": 75.0, "type": "coastal_station"},
    {"id": "coastal_columbia_river_bar_or", "name": "Columbia River Bar Marine Post", "country": "United States", "continent": "North America", "lat": 46.2167, "lon": -124.0667, "elevation": 12.0, "type": "coastal_station"},
    {"id": "coastal_cape_disappointment_wa", "name": "Cape Disappointment Coastal Station", "country": "United States", "continent": "North America", "lat": 46.2783, "lon": -124.0517, "elevation": 65.0, "type": "coastal_station"},
    {"id": "coastal_destruction_island_wa", "name": "Destruction Island Marine Station", "country": "United States", "continent": "North America", "lat": 47.6750, "lon": -124.4850, "elevation": 27.0, "type": "coastal_station"},
    {"id": "coastal_tatoosh_island_wa", "name": "Tatoosh Island Weather Observatory", "country": "United States", "continent": "North America", "lat": 48.3917, "lon": -124.7367, "elevation": 31.0, "type": "coastal_station"},
    {"id": "coastal_neah_bay_wa", "name": "Neah Bay Coastal Observation Post", "country": "United States", "continent": "North America", "lat": 48.3700, "lon": -124.6200, "elevation": 5.0, "type": "coastal_station"},
    {"id": "coastal_westdahl_rock_ak", "name": "Westdahl Rock Aleutian Marine Post", "country": "United States", "continent": "North America", "lat": 54.5167, "lon": -164.7167, "elevation": 15.0, "type": "coastal_station"},
    {"id": "coastal_cape_decision_ak", "name": "Cape Decision Southeast Alaska Post", "country": "United States", "continent": "North America", "lat": 56.0017, "lon": -134.1350, "elevation": 29.0, "type": "coastal_station"},
    {"id": "coastal_point_barrow_ak", "name": "Point Barrow Arctic Marine Station", "country": "United States", "continent": "North America", "lat": 71.3250, "lon": -156.6117, "elevation": 4.0, "type": "coastal_station"},
    {"id": "coastal_helgoland_de", "name": "Helgoland North Sea Marine Station", "country": "Germany", "continent": "Europe", "lat": 54.1817, "lon": 7.8900, "elevation": 25.0, "type": "coastal_station"},
    {"id": "coastal_arkona_de", "name": "Arkona Baltic Coastal Observatory", "country": "Germany", "continent": "Europe", "lat": 54.6789, "lon": 13.4333, "elevation": 42.0, "type": "coastal_station"},
    {"id": "coastal_fino1_de", "name": "FINO1 Offshore North Sea Platform", "country": "Germany", "continent": "Europe", "lat": 54.0147, "lon": 6.5878, "elevation": 30.0, "type": "coastal_station"},
    {"id": "coastal_fino3_de", "name": "FINO3 Offshore North Sea Platform", "country": "Germany", "continent": "Europe", "lat": 55.1950, "lon": 7.1583, "elevation": 30.0, "type": "coastal_station"},
    {"id": "coastal_bishop_rock_uk", "name": "Bishop Rock Lighthouse Marine Post", "country": "United Kingdom", "continent": "Europe", "lat": 49.8733, "lon": -6.4450, "elevation": 44.0, "type": "coastal_station"},
    {"id": "coastal_fastnet_rock_ie", "name": "Fastnet Rock Atlantic Marine Post", "country": "Ireland", "continent": "Europe", "lat": 51.3889, "lon": -9.6050, "elevation": 48.0, "type": "coastal_station"},
    {"id": "coastal_cap_gris_nez_fr", "name": "Cap Gris-Nez Strait of Dover Post", "country": "France", "continent": "Europe", "lat": 50.8714, "lon": 1.5833, "elevation": 45.0, "type": "coastal_station"},
    {"id": "coastal_cabo_da_roca_pt", "name": "Cabo da Roca Atlantic Coastal Post", "country": "Portugal", "continent": "Europe", "lat": 38.7806, "lon": -9.4989, "elevation": 140.0, "type": "coastal_station"},
    {"id": "coastal_cape_leeuwin_au", "name": "Cape Leeuwin Southern Ocean Post", "country": "Australia", "continent": "Oceania", "lat": -34.3750, "lon": 115.1361, "elevation": 56.0, "type": "coastal_station"},
    {"id": "coastal_cape_grim_au", "name": "Cape Grim Baseline Marine Station", "country": "Australia", "continent": "Oceania", "lat": -40.6833, "lon": 144.6833, "elevation": 94.0, "type": "coastal_station"},
    {"id": "coastal_cape_byron_au", "name": "Cape Byron Eastern Pacific Post", "country": "Australia", "continent": "Oceania", "lat": -28.6381, "lon": 153.6369, "elevation": 110.0, "type": "coastal_station"},
    {"id": "coastal_cape_reinga_nz", "name": "Cape Reinga Northern Marine Post", "country": "New Zealand", "continent": "Oceania", "lat": -34.4283, "lon": 172.6797, "elevation": 165.0, "type": "coastal_station"},
    {"id": "coastal_ushuaia_ar", "name": "Ushuaia Beagle Channel Coastal Station", "country": "Argentina", "continent": "South America", "lat": -54.8072, "lon": -68.3044, "elevation": 28.0, "type": "coastal_station"},
    {"id": "coastal_cape_agulhas_za", "name": "Cape Agulhas Atlantic-Indian Ocean Post", "country": "South Africa", "continent": "Africa", "lat": -34.8331, "lon": 20.0097, "elevation": 15.0, "type": "coastal_station"},
    {"id": "coastal_cape_point_za", "name": "Cape Point Marine Research Station", "country": "South Africa", "continent": "Africa", "lat": -34.3572, "lon": 18.4975, "elevation": 230.0, "type": "coastal_station"},
    {"id": "coastal_walvis_bay_na", "name": "Walvis Bay Atlantic Coastal Station", "country": "Namibia", "continent": "Africa", "lat": -22.9575, "lon": 14.5053, "elevation": 5.0, "type": "coastal_station"},
    {"id": "coastal_guardafui_so", "name": "Cape Guardafui Horn of Africa Post", "country": "Somalia", "continent": "Africa", "lat": 11.8300, "lon": 51.2800, "elevation": 60.0, "type": "coastal_station"},
    {"id": "coastal_ras_al_hadd_om", "name": "Ras al Hadd Arabian Sea Coastal Post", "country": "Oman", "continent": "Asia", "lat": 22.5333, "lon": 59.8000, "elevation": 12.0, "type": "coastal_station"}
]

def generate_stations():
    stations = []
    seen_ids = set()

    # 1. Load Countries Map
    countries = {}
    try:
        raw_countries = fetch_file(
            "https://raw.githubusercontent.com/davidmegginson/ourairports-data/master/countries.csv",
            "countries.csv"
        )
        for r in csv.DictReader(io.StringIO(raw_countries.decode("utf-8", errors="ignore"))):
            countries[r["code"]] = (r["name"], r["continent"])
    except Exception as e:
        logger.warning(f"Could not load countries.csv: {e}")

    # 2. Add Storm Chaser & Coastal Stations
    for s in STORM_CHASER_POSTS:
        seen_ids.add(s["id"])
        stations.append(s)

    for s in COASTAL_STATIONS:
        seen_ids.add(s["id"])
        stations.append(s)

    # 3. Load Major Worldwide Airport METAR Stations
    try:
        raw_airports = fetch_file(
            "https://raw.githubusercontent.com/davidmegginson/ourairports-data/master/airports.csv",
            "airports.csv"
        )
        airport_count = 0
        for r in csv.DictReader(io.StringIO(raw_airports.decode("utf-8", errors="ignore"))):
            atype = r.get("type", "")
            icao = r.get("icao_code", "").strip().upper()
            if not icao and len(r.get("ident", "").strip()) == 4 and r.get("ident", "").strip().isalpha():
                icao = r.get("ident", "").strip().upper()

            if atype in ("large_airport", "medium_airport") and icao and len(icao) == 4:
                st_id = f"icao_{icao}"
                if st_id in seen_ids:
                    continue
                try:
                    lat = round(float(r["latitude_deg"]), 4)
                    lon = round(float(r["longitude_deg"]), 4)
                    elev_ft = r.get("elevation_ft")
                    elev = round(float(elev_ft) * 0.3048, 1) if elev_ft and elev_ft.strip() else 0.0
                except (ValueError, KeyError):
                    continue

                if lat < -90.0 or lat > 90.0 or lon < -180.0 or lon > 180.0:
                    continue

                iso_c = r.get("iso_country", "")
                c_info = countries.get(iso_c, (iso_c, r.get("continent", "NA")))
                country_name = c_info[0] if c_info[0] else iso_c
                cont_code = c_info[1] if c_info[1] else r.get("continent", "NA")
                continent_name = CONTINENT_MAP.get(cont_code, "North America")

                seen_ids.add(st_id)
                stations.append({
                    "id": st_id,
                    "name": r.get("name", "").strip(),
                    "country": country_name,
                    "continent": continent_name,
                    "lat": lat,
                    "lon": lon,
                    "elevation": elev,
                    "type": "airport_metar"
                })
                airport_count += 1
        logger.info(f"Loaded {airport_count} real Airport METAR stations")
    except Exception as e:
        logger.error(f"Error loading airports: {e}")

    # 4. Load WMO Stations from NOAA ISD History
    try:
        raw_isd = fetch_file(
            "https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv",
            "isd-history.csv"
        )
        wmo_count = 0
        for r in csv.DictReader(io.StringIO(raw_isd.decode("utf-8", errors="ignore"))):
            usaf = r.get("USAF", "").strip()
            icao = r.get("ICAO", "").strip().upper()
            end = r.get("END", "").strip()

            # Filter active synoptic stations (recent, valid USAF, no duplicate ICAO)
            if end >= "20230101" and usaf and usaf != "999999" and not icao:
                st_id = f"wmo_{usaf}"
                if st_id in seen_ids:
                    continue
                try:
                    lat = round(float(r["LAT"]), 4)
                    lon = round(float(r["LON"]), 4)
                    elev = round(float(r["ELEV(M)"]), 1)
                    if lat == 0.0 and lon == 0.0:
                        continue
                    if lat < -90.0 or lat > 90.0 or lon < -180.0 or lon > 180.0:
                        continue
                except (ValueError, KeyError):
                    continue

                raw_name = r.get("STATION NAME", "").strip()
                if not raw_name:
                    continue
                name = raw_name.title()

                fips_c = r.get("CTRY", "").strip().upper()
                c_info = FIPS_TO_COUNTRY.get(fips_c)
                if c_info:
                    country_name, continent_name = c_info
                else:
                    # Fallback continent based on coordinates
                    if lat > 20 and -130 < lon < -50:
                        continent_name = "North America"
                    elif -60 < lat < 15 and -85 < lon < -30:
                        continent_name = "South America"
                    elif lat > 35 and -15 < lon < 45:
                        continent_name = "Europe"
                    elif -35 < lat < 38 and -20 < lon < 55:
                        continent_name = "Africa"
                    elif lat > 0 and 45 < lon < 150:
                        continent_name = "Asia"
                    elif lat < -10 and 110 < lon < 180:
                        continent_name = "Oceania"
                    elif lat < -60:
                        continent_name = "Antarctica"
                    else:
                        continent_name = "Global"
                    country_name = fips_c if fips_c else "Global"

                seen_ids.add(st_id)
                stations.append({
                    "id": st_id,
                    "name": name,
                    "country": country_name,
                    "continent": continent_name,
                    "lat": lat,
                    "lon": lon,
                    "elevation": elev,
                    "type": "wmo"
                })
                wmo_count += 1
        logger.info(f"Loaded {wmo_count} real WMO synoptic stations")
    except Exception as e:
        logger.error(f"Error loading WMO stations: {e}")

    logger.info(f"Total compiled stations: {len(stations)}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(stations, f, indent=2)

    logger.info(f"Successfully saved {len(stations)} weather stations to {OUTPUT_FILE}")
    return stations

if __name__ == "__main__":
    stations = generate_stations()
    types_count = {}
    continents_count = {}
    for s in stations:
        t = s["type"]
        c = s["continent"]
        types_count[t] = types_count.get(t, 0) + 1
        continents_count[c] = continents_count.get(c, 0) + 1
    print(f"\n--- WEATHER STATIONS SUMMARY ---")
    print(f"Total Stations: {len(stations)}")
    print(f"Breakdown by Type: {types_count}")
    print(f"Breakdown by Continent: {continents_count}")
