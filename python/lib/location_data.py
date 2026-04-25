#!/usr/bin/env python3
"""
lib/location_data.py
--------------------
ALL location lookup tables ported EXACTLY from the demo's
ematch_const_struct.h file.

This includes:
  - US regions list        (us_regions[])
  - US states list         (us_states[])
  - US cities list         (us_cities[])
  - States in each region  (us_states_in_regions[])
  - Neighbor state ratings (us_neighbor_state_rating_list[])
  - Neighbor city ratings  (us_neighbor_city_rating_list[])
  - Region compatibility   (region_compability[][])

Used by: lib/rating.py for location-based rating

Folder: lib/location_data.py
"""


# -----------------------------------------------
# US REGIONS
# Index matches demo's region index numbers exactly
# All lowercase to match demo's to_lower() behavior
# -----------------------------------------------
US_REGIONS = [
    "atlantic coast",   # 0
    "east",             # 1
    "great lakes",      # 2
    "middle",           # 3
    "middleeast",       # 4
    "middlewest",       # 5
    "mountain",         # 6
    "new england",      # 7
    "north",            # 8
    "northeast",        # 9
    "northwest",        # 10
    "pacific",          # 11
    "pacific coast",    # 12
    "south",            # 13
    "southeast",        # 14
    "southwest",        # 15
    "west",             # 16
]

# -----------------------------------------------
# REGION NAME -> INDEX LOOKUP
# Written out fully - no shorthand
# Used in find_region_index() below
# -----------------------------------------------
REGION_INDEX = {
    "atlantic coast": 0,
    "east":           1,
    "great lakes":    2,
    "middle":         3,
    "middleeast":     4,
    "middlewest":     5,
    "mountain":       6,
    "new england":    7,
    "north":          8,
    "northeast":      9,
    "northwest":      10,
    "pacific":        11,
    "pacific coast":  12,
    "south":          13,
    "southeast":      14,
    "southwest":      15,
    "west":           16,
}


# -----------------------------------------------
# US STATES
# Index matches demo's state index numbers exactly
# All lowercase to match demo's to_lower() behavior
# -----------------------------------------------
US_STATES = [
    "alabama",          # 0
    "alaska",           # 1
    "arizona",          # 2
    "arkansas",         # 3
    "california",       # 4
    "colorado",         # 5
    "connecticut",      # 6
    "delaware",         # 7
    "florida",          # 8
    "georgia",          # 9
    "hawaii",           # 10
    "idaho",            # 11
    "illinois",         # 12
    "indiana",          # 13
    "iowa",             # 14
    "kansas",           # 15
    "kentucky",         # 16
    "louisiana",        # 17
    "maine",            # 18
    "maryland",         # 19
    "massachusetts",    # 20
    "michigan",         # 21
    "minnesota",        # 22
    "mississippi",      # 23
    "missouri",         # 24
    "montana",          # 25
    "nebraska",         # 26
    "nevada",           # 27
    "new hampshire",    # 28
    "new jersey",       # 29
    "new mexico",       # 30
    "new york",         # 31
    "north carolina",   # 32
    "north dakota",     # 33
    "ohio",             # 34
    "oklahoma",         # 35
    "oregon",           # 36
    "pennsylvania",     # 37
    "rhode island",     # 38
    "south carolina",   # 39
    "south dakota",     # 40
    "tennessee",        # 41
    "texas",            # 42
    "utah",             # 43
    "vermont",          # 44
    "virginia",         # 45
    "washington",       # 46
    "west virginia",    # 47
    "wisconsin",        # 48
    "wyoming",          # 49
]

# -----------------------------------------------
# STATE NAME -> INDEX LOOKUP
# Written out fully - no shorthand
# Used in find_state_index() below
# -----------------------------------------------
STATE_INDEX = {
    "alabama":        0,
    "alaska":         1,
    "arizona":        2,
    "arkansas":       3,
    "california":     4,
    "colorado":       5,
    "connecticut":    6,
    "delaware":       7,
    "florida":        8,
    "georgia":        9,
    "hawaii":         10,
    "idaho":          11,
    "illinois":       12,
    "indiana":        13,
    "iowa":           14,
    "kansas":         15,
    "kentucky":       16,
    "louisiana":      17,
    "maine":          18,
    "maryland":       19,
    "massachusetts":  20,
    "michigan":       21,
    "minnesota":      22,
    "mississippi":    23,
    "missouri":       24,
    "montana":        25,
    "nebraska":       26,
    "nevada":         27,
    "new hampshire":  28,
    "new jersey":     29,
    "new mexico":     30,
    "new york":       31,
    "north carolina": 32,
    "north dakota":   33,
    "ohio":           34,
    "oklahoma":       35,
    "oregon":         36,
    "pennsylvania":   37,
    "rhode island":   38,
    "south carolina": 39,
    "south dakota":   40,
    "tennessee":      41,
    "texas":          42,
    "utah":           43,
    "vermont":        44,
    "virginia":       45,
    "washington":     46,
    "west virginia":  47,
    "wisconsin":      48,
    "wyoming":        49,
}


# -----------------------------------------------
# US CITIES
# Index matches demo's city index numbers exactly
# "dummy" entries preserved to keep indexes aligned
# All lowercase to match demo's to_lower() behavior
# -----------------------------------------------
US_CITIES = [
    "albuquerque",      # 0
    "alexandria",       # 1
    "allentown",        # 2
    "anchorage",        # 3
    "atlanta",          # 4
    "augusta",          # 5
    "austin",           # 6
    "baltimore",        # 7
    "boise",            # 8
    "boston",           # 9
    "broomfield",       # 10
    "dummy1",           # 11  placeholder - keeps indexes aligned with demo
    "dummy2",           # 12
    "dummy3",           # 13
    "dummy4",           # 14
    "dummy5",           # 15
    "buffalo",          # 16
    "burlington",       # 17
    "charleston_sc",    # 18
    "charleston_wv",    # 19
    "charlotte",        # 20
    "chicago",          # 21
    "cincinnati",       # 22
    "cleveland",        # 23
    "colorado springs", # 24
    "dummy6",           # 25
    "dummy7",           # 26
    "dummy8",           # 27
    "dummy9",           # 28
    "dummy0",           # 29
    "columbia",         # 30
    "columbus",         # 31
    "concord",          # 32
    "cupertino",        # 33
    "dallas",           # 34
    "dayton",           # 35
    "denver",           # 36
    "des moines",       # 37
    "detroit",          # 38
    "el paso",          # 39
    "fort worth",       # 40
    "fremont",          # 41
    "green bay",        # 42
    "harrisburg",       # 43
    "hartford",         # 44
    "haywood",          # 45
    "hillsboro",        # 46
    "honolulu",         # 47
    "dummya",           # 48
    "dummyb",           # 49
    "dummyc",           # 50
    "dummyd",           # 51
    "dummye",           # 52
    "houston",          # 53
    "indianapolis",     # 54
    "kansas city",      # 55
    "las vegas",        # 56
    "lexington",        # 57
    "lincoln",          # 58
    "little rock",      # 59
    "los angeles",      # 60
    "louisville",       # 61
    "memphis",          # 62
    "miami",            # 63
    "dummyf",           # 64
    "dummyg",           # 65
    "dummyh",           # 66
    "dummyi",           # 67
    "dummyj",           # 68
    "milpitas",         # 69
    "milwaukee",        # 70
    "minneapolis",      # 71
    "mobile",           # 72
    "morristown",       # 73
    "mountain view",    # 74
    "nashville",        # 75
    "new orleans",      # 76
    "new york",         # 77
    "newark",           # 78
    "oakland",          # 79
    "oklahoma city",    # 80
    "omaha",            # 81
    "orlando",          # 82
    "palo alto",        # 83
    "dummyk",           # 84
    "dummyl",           # 85
    "dummym",           # 86
    "dummyn",           # 87
    "dummyo",           # 88
    "philadelphia",     # 89
    "phoenix",          # 90
    "pittsburgh",       # 91
    "portland",         # 92
    "providence",       # 93
    "raleigh",          # 94
    "reno",             # 95
    "richmond",         # 96
    "sacramento",       # 97
    "salt lake city",   # 98
    "san antonio",      # 99
    "san diego",        # 100
    "dummyp",           # 101
    "dummyq",           # 102
    "dummyr",           # 103
    "dummys",           # 104
    "dummyt",           # 105
    "saint louis",      # 106
    "san francisco",    # 107
    "san jose",         # 108
    "santa fe",         # 109
    "santa clara",      # 110
    "st louis",         # 111
    "seattle",          # 112
    "shreveport",       # 113
    "sunnyvale",        # 114
    "syracuse",         # 115
    "dummyu",           # 116
    "dummyv",           # 117
    "dummyw",           # 118
    "dummyx",           # 119
    "tampa bay",        # 120
    "tempe",            # 121
    "toledo",           # 122
    "tucson",           # 123
    "tulsa",            # 124
    "washington",       # 125
    "washington, d.c.", # 126
    "wichita",          # 127
    "wilmington",       # 128
    "dummyy",           # 129
    "dummyz",           # 130
]

# -----------------------------------------------
# CITY NAME -> INDEX LOOKUP
# Written out fully - no shorthand
# Only real cities included (no dummy entries)
# Used in find_city_index() below
# -----------------------------------------------
CITY_INDEX = {
    "albuquerque":      0,
    "alexandria":       1,
    "allentown":        2,
    "anchorage":        3,
    "atlanta":          4,
    "augusta":          5,
    "austin":           6,
    "baltimore":        7,
    "boise":            8,
    "boston":           9,
    "broomfield":       10,
    "buffalo":          16,
    "burlington":       17,
    "charleston_sc":    18,
    "charleston_wv":    19,
    "charlotte":        20,
    "chicago":          21,
    "cincinnati":       22,
    "cleveland":        23,
    "colorado springs": 24,
    "columbia":         30,
    "columbus":         31,
    "concord":          32,
    "cupertino":        33,
    "dallas":           34,
    "dayton":           35,
    "denver":           36,
    "des moines":       37,
    "detroit":          38,
    "el paso":          39,
    "fort worth":       40,
    "fremont":          41,
    "green bay":        42,
    "harrisburg":       43,
    "hartford":         44,
    "haywood":          45,
    "hillsboro":        46,
    "honolulu":         47,
    "houston":          53,
    "indianapolis":     54,
    "kansas city":      55,
    "las vegas":        56,
    "lexington":        57,
    "lincoln":          58,
    "little rock":      59,
    "los angeles":      60,
    "louisville":       61,
    "memphis":          62,
    "miami":            63,
    "milpitas":         69,
    "milwaukee":        70,
    "minneapolis":      71,
    "mobile":           72,
    "morristown":       73,
    "mountain view":    74,
    "nashville":        75,
    "new orleans":      76,
    "new york":         77,
    "newark":           78,
    "oakland":          79,
    "oklahoma city":    80,
    "omaha":            81,
    "orlando":          82,
    "palo alto":        83,
    "philadelphia":     89,
    "phoenix":          90,
    "pittsburgh":       91,
    "portland":         92,
    "providence":       93,
    "raleigh":          94,
    "reno":             95,
    "richmond":         96,
    "sacramento":       97,
    "salt lake city":   98,
    "san antonio":      99,
    "san diego":        100,
    "saint louis":      106,
    "san francisco":    107,
    "san jose":         108,
    "santa fe":         109,
    "santa clara":      110,
    "st louis":         111,
    "seattle":          112,
    "shreveport":       113,
    "sunnyvale":        114,
    "syracuse":         115,
    "tampa bay":        120,
    "tempe":            121,
    "toledo":           122,
    "tucson":           123,
    "tulsa":            124,
    "washington":       125,
    "washington, d.c.": 126,
    "wichita":          127,
    "wilmington":       128,
}


# -----------------------------------------------
# STATES IN EACH REGION
# Ported from us_states_in_regions[] in demo
# Each region index maps to a list of state indexes
# -----------------------------------------------
STATES_IN_REGIONS = {
    0:  [29, 19, 45, 32, 39, 9,  8],              # Atlantic Coast
    1:  [18, 28, 44, 20, 38, 6,                    # East
         31, 37, 29, 19, 47, 45, 32, 39, 9, 8],
    2:  [21, 34, 37, 31, 13, 12, 48],             # Great Lakes
    3:  [40, 14, 15, 24, 26, 35],                 # Middle
    4:  [24, 12, 13, 34, 16, 41],                 # Middle East
    5:  [49, 5,  43, 27, 11],                     # Middle West
    6:  [11, 43, 5,  27, 49],                     # Mountain
    7:  [18, 28, 44, 20, 38, 6],                  # New England
    8:  [46, 11, 25, 49, 33, 40, 22, 48, 14, 12,  # North
         13, 21, 34, 18, 28, 44, 20, 38, 6,
         31, 37, 29, 19],
    9:  [18, 28, 44, 20, 38, 6,  31, 37, 29, 19], # Northeast
    10: [46, 11, 36],                             # Northwest
    11: [4,  46, 36, 10],                         # Pacific
    12: [4,  46, 36],                             # Pacific Coast
    13: [8,  9,  39, 41, 0,  23, 3,  17, 42, 35, # South
         30, 2],
    14: [8,  9,  39, 41, 0],                      # Southeast
    15: [42, 30, 2,  35],                         # Southwest
    16: [4,  46, 36, 27, 11, 2,  43],             # West
}


# -----------------------------------------------
# REGION COMPATIBILITY MATRIX
# Ported from region_compability[][] in demo
#
# REGION_COMPATIBILITY[job_region][asked_region]
#   1 = job region is contained in asked region (perfect/near match)
#   2 = job region overlaps with asked region   (partial, 70 deduction)
#   0 = no overlap at all                       (100 deduction)
#
# Used in compute_region_rating() in rating.py
# -----------------------------------------------
REGION_COMPATIBILITY = [
#        0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
    [1,  1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0],  # 0  Atlantic Coast
    [2,  1, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 2, 2, 0, 0],  # 1  East
    [0,  0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 2  Great Lakes
    [0,  0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3  Middle
    [0,  0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4  Middle East
    [0,  0, 0, 0, 0, 1, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2],  # 5  Middle West
    [0,  0, 0, 0, 0, 2, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0],  # 6  Mountain
    [0,  1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 7  New England
    [2,  2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 0, 0, 0, 0],  # 8  North
    [2,  1, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 9  Northeast
    [0,  0, 0, 0, 0, 2, 2, 0, 1, 0, 1, 2, 2, 0, 0, 0, 2],  # 10 Northwest
    [0,  0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 2, 0, 0, 0, 2],  # 11 Pacific
    [0,  0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 1, 0, 0, 0, 1],  # 12 Pacific Coast
    [2,  2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 0],  # 13 South
    [2,  2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # 14 Southeast
    [0,  0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],  # 15 Southwest
    [0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1],  # 16 West
]


# -----------------------------------------------
# NEIGHBOR STATE RATINGS
# Ported from us_neighbor_state_rating_list[] in demo
#
# Structure:
#   state_index -> list of (neighbor_state_index, penalty)
#
# penalty = 0  means it IS that state (exact match)
# penalty > 0  means it is a neighbor with that deduction
# -----------------------------------------------
NEIGHBOR_STATE_RATINGS = {
    0:  [                                          # Alabama
        (0,  0),   # Alabama       - exact match
        (8,  50),  # Florida       - neighbor
        (9,  40),  # Georgia       - neighbor
        (23, 30),  # Mississippi   - neighbor
        (41, 40),  # Tennessee     - neighbor
    ],
    1:  [                                          # Alaska
        (1,  0),   # Alaska        - exact match
    ],
    2:  [                                          # Arizona
        (2,  0),   # Arizona       - exact match
        (4,  30),  # California    - neighbor
        (5,  40),  # Colorado      - neighbor
        (27, 30),  # Nevada        - neighbor
        (30, 30),  # New Mexico    - neighbor
        (43, 40),  # Utah          - neighbor
    ],
    3:  [                                          # Arkansas
        (3,  0),   # Arkansas      - exact match
        (17, 40),  # Louisiana     - neighbor
        (23, 40),  # Mississippi   - neighbor
        (24, 30),  # Missouri      - neighbor
        (35, 40),  # Oklahoma      - neighbor
        (41, 40),  # Tennessee     - neighbor
        (42, 40),  # Texas         - neighbor
    ],
    4:  [                                          # California
        (4,  0),   # California    - exact match
        (2,  30),  # Arizona       - neighbor
        (27, 30),  # Nevada        - neighbor
        (36, 40),  # Oregon        - neighbor
    ],
    5:  [                                          # Colorado
        (5,  0),   # Colorado      - exact match
        (2,  40),  # Arizona       - neighbor
        (15, 30),  # Kansas        - neighbor
        (26, 30),  # Nebraska      - neighbor
        (30, 40),  # New Mexico    - neighbor
        (35, 40),  # Oklahoma      - neighbor
        (43, 30),  # Utah          - neighbor
        (49, 40),  # Wyoming       - neighbor
    ],
    6:  [                                          # Connecticut
        (6,  0),   # Connecticut   - exact match
        (20, 30),  # Massachusetts - neighbor
        (31, 40),  # New York      - neighbor
        (38, 20),  # Rhode Island  - neighbor
    ],
    7:  [                                          # Delaware
        (7,  0),   # Delaware      - exact match
        (19, 30),  # Maryland      - neighbor
        (29, 30),  # New Jersey    - neighbor
        (37, 40),  # Pennsylvania  - neighbor
    ],
    8:  [                                          # Florida
        (8,  0),   # Florida       - exact match
        (0,  40),  # Alabama       - neighbor
        (9,  30),  # Georgia       - neighbor
    ],
    9:  [                                          # Georgia
        (9,  0),   # Georgia       - exact match
        (0,  30),  # Alabama       - neighbor
        (8,  30),  # Florida       - neighbor
        (32, 40),  # North Carolina- neighbor
        (39, 30),  # South Carolina- neighbor
        (41, 30),  # Tennessee     - neighbor
    ],
    10: [                                          # Hawaii
        (10, 0),   # Hawaii        - exact match
    ],
    11: [                                          # Idaho
        (11, 0),   # Idaho         - exact match
        (25, 40),  # Montana       - neighbor
        (27, 30),  # Nevada        - neighbor
        (36, 30),  # Oregon        - neighbor
        (43, 30),  # Utah          - neighbor
        (46, 40),  # Washington    - neighbor
        (49, 40),  # Wyoming       - neighbor
    ],
    12: [                                          # Illinois
        (12, 0),   # Illinois      - exact match
        (13, 30),  # Indiana       - neighbor
        (14, 40),  # Iowa          - neighbor
        (24, 30),  # Missouri      - neighbor
        (16, 40),  # Kentucky      - neighbor
        (48, 40),  # Wisconsin     - neighbor
    ],
    13: [                                          # Indiana
        (13, 0),   # Indiana       - exact match
        (12, 30),  # Illinois      - neighbor
        (16, 40),  # Kentucky      - neighbor
        (21, 35),  # Michigan      - neighbor
        (34, 30),  # Ohio          - neighbor
    ],
    14: [                                          # Iowa
        (14, 0),   # Iowa          - exact match
        (12, 30),  # Illinois      - neighbor
        (22, 40),  # Minnesota     - neighbor
        (24, 30),  # Missouri      - neighbor
        (26, 40),  # Nebraska      - neighbor
        (40, 40),  # South Dakota  - neighbor
        (48, 40),  # Wisconsin     - neighbor
    ],
    15: [                                          # Kansas
        (15, 0),   # Kansas        - exact match
        (5,  30),  # Colorado      - neighbor
        (24, 30),  # Missouri      - neighbor
        (26, 30),  # Nebraska      - neighbor
        (35, 30),  # Oklahoma      - neighbor
    ],
    16: [                                          # Kentucky
        (16, 0),   # Kentucky      - exact match
        (12, 35),  # Illinois      - neighbor
        (13, 30),  # Indiana       - neighbor
        (24, 40),  # Missouri      - neighbor
        (34, 40),  # Ohio          - neighbor
        (41, 20),  # Tennessee     - neighbor
        (45, 50),  # Virginia      - neighbor
        (47, 45),  # West Virginia - neighbor
    ],
    17: [                                          # Louisiana
        (17, 0),   # Louisiana     - exact match
        (3,  30),  # Arkansas      - neighbor
        (23, 30),  # Mississippi   - neighbor
        (42, 40),  # Texas         - neighbor
    ],
    18: [                                          # Maine
        (18, 0),   # Maine         - exact match
        (28, 30),  # New Hampshire - neighbor
        (44, 40),  # Vermont       - neighbor
    ],
    19: [                                          # Maryland
        (19, 0),   # Maryland      - exact match
        (7,  20),  # Delaware      - neighbor
        (45, 30),  # Virginia      - neighbor
        (37, 35),  # Pennsylvania  - neighbor
        (47, 40),  # West Virginia - neighbor
    ],
    20: [                                          # Massachusetts
        (20, 0),   # Massachusetts - exact match
        (6,  20),  # Connecticut   - neighbor
        (28, 25),  # New Hampshire - neighbor
        (31, 35),  # New York      - neighbor
        (38, 20),  # Rhode Island  - neighbor
        (44, 25),  # Vermont       - neighbor
    ],
    21: [                                          # Michigan
        (21, 0),   # Michigan      - exact match
        (13, 30),  # Indiana       - neighbor
        (34, 30),  # Ohio          - neighbor
    ],
    22: [                                          # Minnesota
        (22, 0),   # Minnesota     - exact match
        (14, 30),  # Iowa          - neighbor
        (33, 40),  # North Dakota  - neighbor
        (40, 40),  # South Dakota  - neighbor
        (48, 30),  # Wisconsin     - neighbor
    ],
    23: [                                          # Mississippi
        (23, 0),   # Mississippi   - exact match
        (0,  30),  # Alabama       - neighbor
        (3,  30),  # Arkansas      - neighbor
        (17, 30),  # Louisiana     - neighbor
        (41, 40),  # Tennessee     - neighbor
    ],
    24: [                                          # Missouri
        (24, 0),   # Missouri      - exact match
        (3,  30),  # Arkansas      - neighbor
        (15, 30),  # Kansas        - neighbor
        (12, 30),  # Illinois      - neighbor
        (14, 30),  # Iowa          - neighbor
        (26, 40),  # Nebraska      - neighbor
        (35, 40),  # Oklahoma      - neighbor
        (16, 40),  # Kentucky      - neighbor
        (41, 45),  # Tennessee     - neighbor
    ],
    25: [                                          # Montana
        (25, 0),   # Montana       - exact match
        (11, 30),  # Idaho         - neighbor
        (33, 40),  # North Dakota  - neighbor
        (40, 40),  # South Dakota  - neighbor
        (49, 30),  # Wyoming       - neighbor
    ],
    26: [                                          # Nebraska
        (26, 0),   # Nebraska      - exact match
        (5,  30),  # Colorado      - neighbor
        (15, 30),  # Kansas        - neighbor
        (14, 30),  # Iowa          - neighbor
        (24, 30),  # Missouri      - neighbor
        (40, 35),  # South Dakota  - neighbor
        (49, 40),  # Wyoming       - neighbor
    ],
    27: [                                          # Nevada
        (27, 0),   # Nevada        - exact match
        (4,  30),  # California    - neighbor
        (43, 30),  # Utah          - neighbor
        (2,  30),  # Arizona       - neighbor
        (11, 40),  # Idaho         - neighbor
        (36, 40),  # Oregon        - neighbor
    ],
    28: [                                          # New Hampshire
        (28, 0),   # New Hampshire - exact match
        (18, 30),  # Maine         - neighbor
        (44, 20),  # Vermont       - neighbor
        (20, 20),  # Massachusetts - neighbor
        (6,  30),  # Connecticut   - neighbor
        (38, 30),  # Rhode Island  - neighbor
    ],
    29: [                                          # New Jersey
        (29, 0),   # New Jersey    - exact match
        (7,  20),  # Delaware      - neighbor
        (37, 30),  # Pennsylvania  - neighbor
        (31, 30),  # New York      - neighbor
        (19, 30),  # Maryland      - neighbor
    ],
    30: [                                          # New Mexico
        (30, 0),   # New Mexico    - exact match
        (2,  30),  # Arizona       - neighbor
        (5,  30),  # Colorado      - neighbor
        (43, 40),  # Utah          - neighbor
        (42, 40),  # Texas         - neighbor
    ],
    31: [                                          # New York
        (31, 0),   # New York      - exact match
        (29, 30),  # New Jersey    - neighbor
        (37, 30),  # Pennsylvania  - neighbor
        (20, 30),  # Massachusetts - neighbor
        (6,  30),  # Connecticut   - neighbor
        (44, 30),  # Vermont       - neighbor
    ],
    32: [                                          # North Carolina
        (32, 0),   # North Carolina- exact match
        (39, 30),  # South Carolina- neighbor
        (45, 30),  # Virginia      - neighbor
        (41, 35),  # Tennessee     - neighbor
    ],
    33: [                                          # North Dakota
        (33, 0),   # North Dakota  - exact match
        (40, 30),  # South Dakota  - neighbor
        (25, 40),  # Montana       - neighbor
        (22, 40),  # Minnesota     - neighbor
    ],
    34: [                                          # Ohio
        (34, 0),   # Ohio          - exact match
        (13, 30),  # Indiana       - neighbor
        (21, 30),  # Michigan      - neighbor
        (16, 40),  # Kentucky      - neighbor
        (37, 35),  # Pennsylvania  - neighbor
        (47, 40),  # West Virginia - neighbor
    ],
    35: [                                          # Oklahoma
        (35, 0),   # Oklahoma      - exact match
        (3,  30),  # Arkansas      - neighbor
        (15, 20),  # Kansas        - neighbor
        (24, 40),  # Missouri      - neighbor
        (42, 30),  # Texas         - neighbor
        (5,  50),  # Colorado      - neighbor
    ],
    36: [                                          # Oregon
        (36, 0),   # Oregon        - exact match
        (11, 40),  # Idaho         - neighbor
        (4,  40),  # California    - neighbor
        (27, 40),  # Nevada        - neighbor
        (46, 40),  # Washington    - neighbor
    ],
    37: [                                          # Pennsylvania
        (37, 0),   # Pennsylvania  - exact match
        (7,  30),  # Delaware      - neighbor
        (19, 20),  # Maryland      - neighbor
        (29, 30),  # New Jersey    - neighbor
        (31, 30),  # New York      - neighbor
        (34, 30),  # Ohio          - neighbor
        (47, 30),  # West Virginia - neighbor
    ],
    38: [                                          # Rhode Island
        (38, 0),   # Rhode Island  - exact match
        (20, 20),  # Massachusetts - neighbor
        (6,  10),  # Connecticut   - neighbor
    ],
    39: [                                          # South Carolina
        (39, 0),   # South Carolina- exact match
        (32, 30),  # North Carolina- neighbor
        (9,  30),  # Georgia       - neighbor
    ],
    40: [                                          # South Dakota
        (40, 0),   # South Dakota  - exact match
        (33, 30),  # North Dakota  - neighbor
        (14, 40),  # Iowa          - neighbor
        (25, 40),  # Montana       - neighbor
        (26, 40),  # Nebraska      - neighbor
        (48, 40),  # Wisconsin     - neighbor
        (49, 40),  # Wyoming       - neighbor
    ],
    41: [                                          # Tennessee
        (41, 0),   # Tennessee     - exact match
        (3,  30),  # Arkansas      - neighbor
        (23, 30),  # Mississippi   - neighbor
        (0,  30),  # Alabama       - neighbor
        (9,  35),  # Georgia       - neighbor
        (32, 40),  # North Carolina- neighbor
        (45, 45),  # Virginia      - neighbor
        (16, 20),  # Kentucky      - neighbor
        (24, 40),  # Missouri      - neighbor
    ],
    42: [                                          # Texas
        (42, 0),   # Texas         - exact match
        (30, 40),  # New Mexico    - neighbor
        (35, 30),  # Oklahoma      - neighbor
        (17, 30),  # Louisiana     - neighbor
        (3,  40),  # Arkansas      - neighbor
    ],
    43: [                                          # Utah
        (43, 0),   # Utah          - exact match
        (2,  40),  # Arizona       - neighbor
        (5,  30),  # Colorado      - neighbor
        (27, 30),  # Nevada        - neighbor
        (11, 40),  # Idaho         - neighbor
        (49, 40),  # Wyoming       - neighbor
        (30, 45),  # New Mexico    - neighbor
    ],
    44: [                                          # Vermont
        (44, 0),   # Vermont       - exact match
        (31, 30),  # New York      - neighbor
        (28, 20),  # New Hampshire - neighbor
        (20, 20),  # Massachusetts - neighbor
    ],
    45: [                                          # Virginia
        (45, 0),   # Virginia      - exact match
        (19, 20),  # Maryland      - neighbor
        (47, 30),  # West Virginia - neighbor
        (32, 30),  # North Carolina- neighbor
        (41, 40),  # Tennessee     - neighbor
        (16, 40),  # Kentucky      - neighbor
    ],
    46: [                                          # Washington
        (46, 0),   # Washington    - exact match
        (36, 30),  # Oregon        - neighbor
        (11, 40),  # Idaho         - neighbor
    ],
    47: [                                          # West Virginia
        (47, 0),   # West Virginia - exact match
        (45, 30),  # Virginia      - neighbor
        (34, 30),  # Ohio          - neighbor
        (37, 30),  # Pennsylvania  - neighbor
        (16, 40),  # Kentucky      - neighbor
    ],
    48: [                                          # Wisconsin
        (48, 0),   # Wisconsin     - exact match
        (22, 30),  # Minnesota     - neighbor
        (14, 30),  # Iowa          - neighbor
        (12, 30),  # Illinois      - neighbor
    ],
    49: [                                          # Wyoming
        (49, 0),   # Wyoming       - exact match
        (43, 30),  # Utah          - neighbor
        (5,  30),  # Colorado      - neighbor
        (11, 30),  # Idaho         - neighbor
        (26, 30),  # Nebraska      - neighbor
        (25, 30),  # Montana       - neighbor
        (40, 40),  # South Dakota  - neighbor
    ],
}


# -----------------------------------------------
# NEIGHBOR CITY RATINGS
# Ported from us_neighbor_city_rating_list[] in demo
#
# Structure:
#   city_index -> list of (neighbor_city_index, penalty)
#
# penalty = 0  means it IS that city (exact match)
# penalty > 0  means it is a neighbor with that deduction
# Dummy cities are not included (they have no real neighbors)
# -----------------------------------------------
NEIGHBOR_CITY_RATINGS = {
    0:  [                                          # Albuquerque
        (0,   0),  # Albuquerque   - exact match
        (39,  40), # El Paso       - neighbor
        (90,  50), # Phoenix       - neighbor
        (109, 30), # Santa Fe      - neighbor
    ],
    1:  [                                          # Alexandria
        (1,   0),  # Alexandria    - exact match
        (126, 5),  # Washington DC - neighbor
        (7,   15), # Baltimore     - neighbor
        (96,  20), # Richmond      - neighbor
    ],
    2:  [                                          # Allentown
        (2,   0),  # Allentown     - exact match
        (43,  20), # Harrisburg    - neighbor
        (89,  10), # Philadelphia  - neighbor
        (128, 30), # Wilmington    - neighbor
        (7,   40), # Baltimore     - neighbor
    ],
    3:  [                                          # Anchorage
        (3,   0),  # Anchorage     - exact match
    ],
    4:  [                                          # Atlanta
        (4,   0),  # Atlanta       - exact match
        (72,  40), # Mobile        - neighbor
        (30,  40), # Columbia SC   - neighbor
    ],
    5:  [                                          # Augusta
        (5,   0),  # Augusta       - exact match
        (32,  40), # Concord       - neighbor
    ],
    6:  [                                          # Austin
        (6,   0),  # Austin        - exact match
        (34,  35), # Dallas        - neighbor
        (99,  20), # San Antonio   - neighbor
        (53,  30), # Houston       - neighbor
    ],
    7:  [                                          # Baltimore
        (7,   0),  # Baltimore     - exact match
        (1,   15), # Alexandria    - neighbor
        (43,  40), # Harrisburg    - neighbor
        (125, 10), # Washington    - neighbor
        (89,  40), # Philadelphia  - neighbor
        (128, 40), # Wilmington    - neighbor
    ],
    8:  [                                          # Boise
        (8,   0),  # Boise         - exact match
        (98,  40), # Salt Lake City- neighbor
        (92,  40), # Portland      - neighbor
    ],
    9:  [                                          # Boston
        (9,   0),  # Boston        - exact match
        (32,  30), # Concord       - neighbor
        (44,  30), # Hartford      - neighbor
        (93,  30), # Providence    - neighbor
    ],
    16: [                                          # Buffalo
        (16,  0),  # Buffalo       - exact match
        (115, 40), # Syracuse      - neighbor
        (91,  40), # Pittsburgh    - neighbor
    ],
    17: [                                          # Burlington
        (17,  0),  # Burlington    - exact match
    ],
    18: [                                          # Charleston SC
        (18,  0),  # Charleston SC - exact match
        (30,  30), # Columbia SC   - neighbor
    ],
    19: [                                          # Charleston WV
        (19,  0),  # Charleston WV - exact match
        (57,  40), # Lexington     - neighbor
        (31,  40), # Columbus      - neighbor
    ],
    20: [                                          # Charlotte
        (20,  0),  # Charlotte     - exact match
        (94,  30), # Raleigh       - neighbor
        (30,  30), # Columbia SC   - neighbor
    ],
    21: [                                          # Chicago
        (21,  0),  # Chicago       - exact match
        (70,  40), # Milwaukee     - neighbor
        (54,  40), # Indianapolis  - neighbor
    ],
    22: [                                          # Cincinnati
        (22,  0),  # Cincinnati    - exact match
        (35,  10), # Dayton        - neighbor
        (31,  30), # Columbus      - neighbor
        (57,  35), # Lexington     - neighbor
        (54,  35), # Indianapolis  - neighbor
        (61,  35), # Louisville    - neighbor
    ],
    23: [                                          # Cleveland
        (23,  0),  # Cleveland     - exact match
        (122, 30), # Toledo        - neighbor
        (31,  30), # Columbus      - neighbor
        (91,  40), # Pittsburgh    - neighbor
    ],
    24: [                                          # Colorado Springs
        (24,  0),  # Colorado Spgs - exact match
        (36,  20), # Denver        - neighbor
    ],
    30: [                                          # Columbia SC
        (30,  0),  # Columbia SC   - exact match
        (18,  30), # Charleston SC - neighbor
    ],
    31: [                                          # Columbus
        (31,  0),  # Columbus      - exact match
        (35,  20), # Dayton        - neighbor
        (22,  30), # Cincinnati    - neighbor
        (23,  30), # Cleveland     - neighbor
        (54,  35), # Indianapolis  - neighbor
        (122, 40), # Toledo        - neighbor
    ],
    32: [                                          # Concord
        (32,  0),  # Concord       - exact match
        (9,   30), # Boston        - neighbor
        (44,  30), # Hartford      - neighbor
        (93,  30), # Providence    - neighbor
        (5,   40), # Augusta       - neighbor
    ],
    33: [                                          # Cupertino
        (33,  0),  # Cupertino     - exact match
        (41,  3),  # Fremont       - neighbor
        (108, 2),  # San Jose      - neighbor
        (114, 1),  # Sunnyvale     - neighbor
        (74,  2),  # Mountain View - neighbor
        (110, 1),  # Santa Clara   - neighbor
        (83,  2),  # Palo Alto     - neighbor
        (69,  2),  # Milpitas      - neighbor
        (45,  4),  # Haywood       - neighbor
        (79,  8),  # Oakland       - neighbor
        (107, 8),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    34: [                                          # Dallas
        (34,  0),  # Dallas        - exact match
        (40,  10), # Fort Worth    - neighbor
        (6,   35), # Austin        - neighbor
        (53,  35), # Houston       - neighbor
    ],
    35: [                                          # Dayton
        (35,  0),  # Dayton        - exact match
        (22,  10), # Cincinnati    - neighbor
        (31,  20), # Columbus      - neighbor
        (54,  30), # Indianapolis  - neighbor
        (122, 40), # Toledo        - neighbor
    ],
    36: [                                          # Denver
        (36,  0),  # Denver        - exact match
        (24,  20), # Colorado Spgs - neighbor
    ],
    37: [                                          # Des Moines
        (37,  0),  # Des Moines    - exact match
        (55,  40), # Kansas City   - neighbor
    ],
    38: [                                          # Detroit
        (38,  0),  # Detroit       - exact match
        (122, 20), # Toledo        - neighbor
    ],
    39: [                                          # El Paso
        (39,  0),  # El Paso       - exact match
        (0,   40), # Albuquerque   - neighbor
    ],
    40: [                                          # Fort Worth
        (40,  0),  # Fort Worth    - exact match
        (34,  10), # Dallas        - neighbor
        (6,   30), # Austin        - neighbor
        (53,  35), # Houston       - neighbor
    ],
    41: [                                          # Fremont
        (41,  0),  # Fremont       - exact match
        (33,  3),  # Cupertino     - neighbor
        (108, 3),  # San Jose      - neighbor
        (114, 3),  # Sunnyvale     - neighbor
        (74,  3),  # Mountain View - neighbor
        (110, 3),  # Santa Clara   - neighbor
        (83,  3),  # Palo Alto     - neighbor
        (69,  3),  # Milpitas      - neighbor
        (45,  2),  # Haywood       - neighbor
        (79,  6),  # Oakland       - neighbor
        (107, 6),  # San Francisco - neighbor
        (97,  14), # Sacramento    - neighbor
    ],
    42: [                                          # Green Bay
        (42,  0),  # Green Bay     - exact match
        (70,  20), # Milwaukee     - neighbor
        (21,  30), # Chicago       - neighbor
    ],
    43: [                                          # Harrisburg
        (43,  0),  # Harrisburg    - exact match
        (2,   20), # Allentown     - neighbor
        (7,   20), # Baltimore     - neighbor
        (125, 30), # Washington    - neighbor
        (89,  30), # Philadelphia  - neighbor
        (91,  35), # Pittsburgh    - neighbor
        (128, 30), # Wilmington    - neighbor
    ],
    44: [                                          # Hartford
        (44,  0),  # Hartford      - exact match
        (93,  10), # Providence    - neighbor
        (9,   20), # Boston        - neighbor
        (32,  30), # Concord       - neighbor
    ],
    45: [                                          # Haywood
        (45,  0),  # Haywood       - exact match
        (33,  4),  # Cupertino     - neighbor
        (108, 4),  # San Jose      - neighbor
        (114, 4),  # Sunnyvale     - neighbor
        (74,  4),  # Mountain View - neighbor
        (110, 4),  # Santa Clara   - neighbor
        (83,  3),  # Palo Alto     - neighbor
        (69,  3),  # Milpitas      - neighbor
        (41,  2),  # Fremont       - neighbor
        (79,  5),  # Oakland       - neighbor
        (107, 5),  # San Francisco - neighbor
        (97,  13), # Sacramento    - neighbor
    ],
    46: [                                          # Hillsboro
        (46,  0),  # Hillsboro     - exact match
        (92,  5),  # Portland      - neighbor
        (112, 35), # Seattle       - neighbor
    ],
    47: [                                          # Honolulu
        (47,  0),  # Honolulu      - exact match
    ],
    53: [                                          # Houston
        (53,  0),  # Houston       - exact match
        (6,   30), # Austin        - neighbor
        (34,  35), # Dallas        - neighbor
        (40,  35), # Fort Worth    - neighbor
        (113, 35), # Shreveport    - neighbor
        (99,  30), # San Antonio   - neighbor
    ],
    54: [                                          # Indianapolis
        (54,  0),  # Indianapolis  - exact match
        (61,  30), # Louisville    - neighbor
        (22,  30), # Cincinnati    - neighbor
        (57,  35), # Lexington     - neighbor
        (35,  30), # Dayton        - neighbor
    ],
    55: [                                          # Kansas City
        (55,  0),  # Kansas City   - exact match
        (111, 30), # St Louis      - neighbor
        (127, 40), # Wichita       - neighbor
        (81,  45), # Omaha         - neighbor
        (58,  45), # Lincoln       - neighbor
    ],
    56: [                                          # Las Vegas
        (56,  0),  # Las Vegas     - exact match
        (60,  40), # Los Angeles   - neighbor
    ],
    57: [                                          # Lexington
        (57,  0),  # Lexington     - exact match
        (61,  10), # Louisville    - neighbor
        (22,  30), # Cincinnati    - neighbor
        (75,  35), # Nashville     - neighbor
        (62,  40), # Memphis       - neighbor
        (19,  40), # Charleston WV - neighbor
    ],
    58: [                                          # Lincoln
        (58,  0),  # Lincoln       - exact match
        (81,  10), # Omaha         - neighbor
        (37,  40), # Des Moines    - neighbor
        (55,  40), # Kansas City   - neighbor
    ],
    59: [                                          # Little Rock
        (59,  0),  # Little Rock   - exact match
        (62,  30), # Memphis       - neighbor
        (113, 30), # Shreveport    - neighbor
    ],
    60: [                                          # Los Angeles
        (60,  0),  # Los Angeles   - exact match
        (100, 20), # San Diego     - neighbor
    ],
    61: [                                          # Louisville
        (61,  0),  # Louisville    - exact match
        (57,  10), # Lexington     - neighbor
        (22,  30), # Cincinnati    - neighbor
        (54,  40), # Indianapolis  - neighbor
    ],
    62: [                                          # Memphis
        (62,  0),  # Memphis       - exact match
        (75,  30), # Nashville     - neighbor
        (59,  30), # Little Rock   - neighbor
    ],
    63: [                                          # Miami
        (63,  0),  # Miami         - exact match
        (82,  30), # Orlando       - neighbor
        (120, 30), # Tampa Bay     - neighbor
    ],
    69: [                                          # Milpitas
        (69,  0),  # Milpitas      - exact match
        (33,  3),  # Cupertino     - neighbor
        (108, 1),  # San Jose      - neighbor
        (114, 2),  # Sunnyvale     - neighbor
        (74,  3),  # Mountain View - neighbor
        (110, 2),  # Santa Clara   - neighbor
        (83,  3),  # Palo Alto     - neighbor
        (45,  4),  # Haywood       - neighbor
        (41,  3),  # Fremont       - neighbor
        (79,  5),  # Oakland       - neighbor
        (107, 7),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    70: [                                          # Milwaukee
        (70,  0),  # Milwaukee     - exact match
        (42,  30), # Green Bay     - neighbor
        (21,  30), # Chicago       - neighbor
    ],
    71: [                                          # Minneapolis
        (71,  0),  # Minneapolis   - exact match
    ],
    72: [                                          # Mobile
        (72,  0),  # Mobile        - exact match
        (76,  30), # New Orleans   - neighbor
    ],
    73: [                                          # Morristown
        (73,  0),  # Morristown    - exact match
        (77,  10), # New York      - neighbor
        (78,  10), # Newark        - neighbor
        (89,  30), # Philadelphia  - neighbor
        (2,   30), # Allentown     - neighbor
        (128, 30), # Wilmington    - neighbor
    ],
    74: [                                          # Mountain View
        (74,  0),  # Mountain View - exact match
        (33,  2),  # Cupertino     - neighbor
        (108, 2),  # San Jose      - neighbor
        (114, 1),  # Sunnyvale     - neighbor
        (69,  2),  # Milpitas      - neighbor
        (110, 1),  # Santa Clara   - neighbor
        (83,  1),  # Palo Alto     - neighbor
        (45,  5),  # Haywood       - neighbor
        (41,  4),  # Fremont       - neighbor
        (79,  6),  # Oakland       - neighbor
        (107, 7),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    75: [                                          # Nashville
        (75,  0),  # Nashville     - exact match
        (62,  30), # Memphis       - neighbor
        (61,  40), # Louisville    - neighbor
    ],
    76: [                                          # New Orleans
        (76,  0),  # New Orleans   - exact match
        (72,  30), # Mobile        - neighbor
        (53,  40), # Houston       - neighbor
    ],
    77: [                                          # New York
        (77,  0),  # New York      - exact match
        (78,  10), # Newark        - neighbor
        (73,  10), # Morristown    - neighbor
        (89,  30), # Philadelphia  - neighbor
        (2,   30), # Allentown     - neighbor
        (128, 30), # Wilmington    - neighbor
    ],
    78: [                                          # Newark
        (78,  0),  # Newark        - exact match
        (77,  10), # New York      - neighbor
        (73,  10), # Morristown    - neighbor
        (89,  25), # Philadelphia  - neighbor
        (2,   25), # Allentown     - neighbor
        (128, 25), # Wilmington    - neighbor
    ],
    79: [                                          # Oakland
        (79,  0),  # Oakland       - exact match
        (33,  8),  # Cupertino     - neighbor
        (108, 8),  # San Jose      - neighbor
        (114, 8),  # Sunnyvale     - neighbor
        (69,  8),  # Milpitas      - neighbor
        (110, 8),  # Santa Clara   - neighbor
        (83,  6),  # Palo Alto     - neighbor
        (45,  4),  # Haywood       - neighbor
        (41,  5),  # Fremont       - neighbor
        (74,  6),  # Mountain View - neighbor
        (107, 3),  # San Francisco - neighbor
        (97,  10), # Sacramento    - neighbor
    ],
    80: [                                          # Oklahoma City
        (80,  0),  # Oklahoma City - exact match
        (124, 30), # Tulsa         - neighbor
        (127, 40), # Wichita       - neighbor
    ],
    81: [                                          # Omaha
        (81,  0),  # Omaha         - exact match
        (58,  10), # Lincoln       - neighbor
        (37,  30), # Des Moines    - neighbor
        (55,  40), # Kansas City   - neighbor
    ],
    82: [                                          # Orlando
        (82,  0),  # Orlando       - exact match
        (63,  30), # Miami         - neighbor
        (120, 20), # Tampa Bay     - neighbor
    ],
    83: [                                          # Palo Alto
        (83,  0),  # Palo Alto     - exact match
        (33,  2),  # Cupertino     - neighbor
        (108, 2),  # San Jose      - neighbor
        (114, 1),  # Sunnyvale     - neighbor
        (69,  2),  # Milpitas      - neighbor
        (110, 1),  # Santa Clara   - neighbor
        (74,  1),  # Mountain View - neighbor
        (45,  4),  # Haywood       - neighbor
        (41,  2),  # Fremont       - neighbor
        (79,  6),  # Oakland       - neighbor
        (107, 6),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    89: [                                          # Philadelphia
        (89,  0),  # Philadelphia  - exact match
        (2,   10), # Allentown     - neighbor
        (128, 10), # Wilmington    - neighbor
        (73,  30), # Morristown    - neighbor
        (77,  35), # New York      - neighbor
        (43,  40), # Harrisburg    - neighbor
        (7,   40), # Baltimore     - neighbor
    ],
    90: [                                          # Phoenix
        (90,  0),  # Phoenix       - exact match
        (121, 0),  # Tempe         - neighbor (same area)
        (123, 10), # Tucson        - neighbor
    ],
    91: [                                          # Pittsburgh
        (91,  0),  # Pittsburgh    - exact match
        (23,  30), # Cleveland     - neighbor
        (43,  40), # Harrisburg    - neighbor
    ],
    92: [                                          # Portland
        (92,  0),  # Portland      - exact match
        (46,  5),  # Hillsboro     - neighbor
        (112, 35), # Seattle       - neighbor
    ],
    93: [                                          # Providence
        (93,  0),  # Providence    - exact match
        (44,  5),  # Hartford      - neighbor
        (9,   20), # Boston        - neighbor
        (32,  30), # Concord       - neighbor
    ],
    94: [                                          # Raleigh
        (94,  0),  # Raleigh       - exact match
        (20,  25), # Charlotte     - neighbor
        (30,  25), # Columbia SC   - neighbor
    ],
    95: [                                          # Reno
        (95,  0),  # Reno          - exact match
        (97,  35), # Sacramento    - neighbor
    ],
    96: [                                          # Richmond
        (96,  0),  # Richmond      - exact match
        (1,   20), # Alexandria    - neighbor
        (126, 25), # Washington DC - neighbor
        (94,  30), # Raleigh       - neighbor
    ],
    97: [                                          # Sacramento
        (97,  0),  # Sacramento    - exact match
        (95,  35), # Reno          - neighbor
        (79,  10), # Oakland       - neighbor
        (108, 15), # San Jose      - neighbor
        (107, 13), # San Francisco - neighbor
        (110, 15), # Santa Clara   - neighbor
        (83,  15), # Palo Alto     - neighbor
        (69,  15), # Milpitas      - neighbor
        (33,  15), # Cupertino     - neighbor
        (114, 15), # Sunnyvale     - neighbor
        (45,  13), # Haywood       - neighbor
        (41,  14), # Fremont       - neighbor
        (74,  15), # Mountain View - neighbor
    ],
    98: [                                          # Salt Lake City
        (98,  0),  # Salt Lake City- exact match
    ],
    99: [                                          # San Antonio
        (99,  0),  # San Antonio   - exact match
        (6,   10), # Austin        - neighbor
        (53,  30), # Houston       - neighbor
    ],
    100:[                                          # San Diego
        (100, 0),  # San Diego     - exact match
        (60,  24), # Los Angeles   - neighbor
    ],
    106:[                                          # Saint Louis
        (106, 0),  # Saint Louis   - exact match
        (55,  35), # Kansas City   - neighbor
    ],
    107:[                                          # San Francisco
        (107, 0),  # San Francisco - exact match
        (33,  8),  # Cupertino     - neighbor
        (108, 8),  # San Jose      - neighbor
        (114, 8),  # Sunnyvale     - neighbor
        (69,  8),  # Milpitas      - neighbor
        (110, 8),  # Santa Clara   - neighbor
        (83,  6),  # Palo Alto     - neighbor
        (45,  4),  # Haywood       - neighbor
        (41,  5),  # Fremont       - neighbor
        (74,  6),  # Mountain View - neighbor
        (79,  3),  # Oakland       - neighbor
        (97,  13), # Sacramento    - neighbor
    ],
    108:[                                          # San Jose
        (108, 0),  # San Jose      - exact match
        (33,  1),  # Cupertino     - neighbor
        (74,  2),  # Mountain View - neighbor
        (114, 1),  # Sunnyvale     - neighbor
        (69,  1),  # Milpitas      - neighbor
        (110, 1),  # Santa Clara   - neighbor
        (83,  1),  # Palo Alto     - neighbor
        (45,  4),  # Haywood       - neighbor
        (41,  3),  # Fremont       - neighbor
        (79,  6),  # Oakland       - neighbor
        (107, 7),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    109:[                                          # Santa Fe
        (109, 0),  # Santa Fe      - exact match
        (0,   30), # Albuquerque   - neighbor
    ],
    110:[                                          # Santa Clara
        (110, 0),  # Santa Clara   - exact match
        (33,  1),  # Cupertino     - neighbor
        (74,  1),  # Mountain View - neighbor
        (114, 1),  # Sunnyvale     - neighbor
        (69,  1),  # Milpitas      - neighbor
        (108, 1),  # San Jose      - neighbor
        (83,  2),  # Palo Alto     - neighbor
        (45,  4),  # Haywood       - neighbor
        (41,  3),  # Fremont       - neighbor
        (79,  6),  # Oakland       - neighbor
        (107, 7),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    111:[                                          # St Louis
        (111, 0),  # St Louis      - exact match
        (55,  35), # Kansas City   - neighbor
    ],
    112:[                                          # Seattle
        (112, 0),  # Seattle       - exact match
        (46,  35), # Hillsboro     - neighbor
        (92,  35), # Portland      - neighbor
    ],
    113:[                                          # Shreveport
        (113, 0),  # Shreveport    - exact match
        (34,  40), # Dallas        - neighbor
        (59,  40), # Little Rock   - neighbor
    ],
    114:[                                          # Sunnyvale
        (114, 0),  # Sunnyvale     - exact match
        (74,  1),  # Mountain View - neighbor
        (33,  2),  # Cupertino     - neighbor
        (108, 2),  # San Jose      - neighbor
        (69,  2),  # Milpitas      - neighbor
        (110, 1),  # Santa Clara   - neighbor
        (83,  1),  # Palo Alto     - neighbor
        (45,  5),  # Haywood       - neighbor
        (41,  4),  # Fremont       - neighbor
        (79,  6),  # Oakland       - neighbor
        (107, 7),  # San Francisco - neighbor
        (97,  15), # Sacramento    - neighbor
    ],
    115:[                                          # Syracuse
        (115, 0),  # Syracuse      - exact match
        (16,  40), # Buffalo       - neighbor
    ],
    120:[                                          # Tampa Bay
        (120, 0),  # Tampa Bay     - exact match
        (82,  20), # Orlando       - neighbor
        (63,  30), # Miami         - neighbor
    ],
    121:[                                          # Tempe
        (121, 0),  # Tempe         - exact match
        (90,  0),  # Phoenix       - neighbor (same area)
        (123, 10), # Tucson        - neighbor
    ],
    122:[                                          # Toledo
        (122, 0),  # Toledo        - exact match
        (38,  30), # Detroit       - neighbor
        (31,  30), # Columbus      - neighbor
        (23,  35), # Cleveland     - neighbor
        (35,  35), # Dayton        - neighbor
    ],
    123:[                                          # Tucson
        (123, 0),  # Tucson        - exact match
        (121, 0),  # Tempe         - neighbor (same area)
        (90,  0),  # Phoenix       - neighbor (same area)
    ],
    124:[                                          # Tulsa
        (124, 0),  # Tulsa         - exact match
        (80,  30), # Oklahoma City - neighbor
        (55,  20), # Kansas City   - neighbor
        (127, 40), # Wichita       - neighbor
    ],
    125:[                                          # Washington
        (125, 0),  # Washington    - exact match
        (1,   5),  # Alexandria    - neighbor
        (7,   10), # Baltimore     - neighbor
        (43,  30), # Harrisburg    - neighbor
        (89,  30), # Philadelphia  - neighbor
        (128, 30), # Wilmington    - neighbor
        (2,   40), # Allentown     - neighbor
    ],
    126:[                                          # Washington DC
        (126, 0),  # Washington DC - exact match
        (1,   5),  # Alexandria    - neighbor
        (7,   10), # Baltimore     - neighbor
        (43,  30), # Harrisburg    - neighbor
        (89,  30), # Philadelphia  - neighbor
        (128, 30), # Wilmington    - neighbor
        (2,   40), # Allentown     - neighbor
    ],
    127:[                                          # Wichita
        (127, 0),  # Wichita       - exact match
        (80,  40), # Oklahoma City - neighbor
        (55,  40), # Kansas City   - neighbor
        (124, 40), # Tulsa         - neighbor
    ],
    128:[                                          # Wilmington
        (128, 0),  # Wilmington    - exact match
        (89,  10), # Philadelphia  - neighbor
        (2,   20), # Allentown     - neighbor
        (43,  40), # Harrisburg    - neighbor
        (7,   40), # Baltimore     - neighbor
        (77,  50), # New York      - neighbor
    ],
}


# -----------------------------------------------
# HELPER FUNCTIONS
# Used by rating.py to look up indexes by name
# -----------------------------------------------

def find_region_index(name):
    """
    Return the index of a region by name.
    Input is lowercased before lookup to match demo behavior.
    Returns -1 if region not found.
    """
    name_lower = name.lower().strip()
    if name_lower in REGION_INDEX:
        return REGION_INDEX[name_lower]
    return -1


def find_state_index(name):
    """
    Return the index of a state by name.
    Input is lowercased before lookup to match demo behavior.
    Returns -1 if state not found.
    """
    name_lower = name.lower().strip()
    if name_lower in STATE_INDEX:
        return STATE_INDEX[name_lower]
    return -1


def find_city_index(name):
    """
    Return the index of a city by name.
    Input is lowercased before lookup to match demo behavior.
    Returns -1 if city not found.
    """
    name_lower = name.lower().strip()
    if name_lower in CITY_INDEX:
        return CITY_INDEX[name_lower]
    return -1


def state_is_in_region(state_idx, region_idx):
    """
    Return True if the given state index is in the given region index.
    Ported from the_state_is_in_the_region() in demo.
    """
    states = STATES_IN_REGIONS.get(region_idx, [])
    if state_idx in states:
        return True
    return False

# -----------------------------------------------
# CITY TO STATE MAPPING
# Ported from us_cities_in_states[] in demo
# Maps city_index -> state_index
# Moved here from rating.py so city_is_in_state()
# can use it directly in this same file
# -----------------------------------------------
CITY_TO_STATE = {
    72:  0,   # Mobile           -> Alabama
    3:   1,   # Anchorage        -> Alaska
    90:  2,   # Phoenix          -> Arizona
    121: 2,   # Tempe            -> Arizona
    123: 2,   # Tucson           -> Arizona
    59:  3,   # Little Rock      -> Arkansas
    33:  4,   # Cupertino        -> California
    41:  4,   # Fremont          -> California
    45:  4,   # Haywood          -> California
    60:  4,   # Los Angeles      -> California
    69:  4,   # Milpitas         -> California
    74:  4,   # Mountain View    -> California
    79:  4,   # Oakland          -> California
    83:  4,   # Palo Alto        -> California
    97:  4,   # Sacramento       -> California
    100: 4,   # San Diego        -> California
    107: 4,   # San Francisco    -> California
    108: 4,   # San Jose         -> California
    110: 4,   # Santa Clara      -> California
    114: 4,   # Sunnyvale        -> California
    24:  5,   # Colorado Springs -> Colorado
    36:  5,   # Denver           -> Colorado
    44:  6,   # Hartford         -> Connecticut
    128: 7,   # Wilmington       -> Delaware
    63:  8,   # Miami            -> Florida
    82:  8,   # Orlando          -> Florida
    120: 8,   # Tampa Bay        -> Florida
    4:   9,   # Atlanta          -> Georgia
    47:  10,  # Honolulu         -> Hawaii
    8:   11,  # Boise            -> Idaho
    21:  12,  # Chicago          -> Illinois
    54:  13,  # Indianapolis     -> Indiana
    37:  14,  # Des Moines       -> Iowa
    127: 15,  # Wichita          -> Kansas
    57:  16,  # Lexington        -> Kentucky
    61:  16,  # Louisville       -> Kentucky
    76:  17,  # New Orleans      -> Louisiana
    5:   18,  # Augusta          -> Maine
    7:   19,  # Baltimore        -> Maryland
    9:   20,  # Boston           -> Massachusetts
    38:  21,  # Detroit          -> Michigan
    71:  22,  # Minneapolis      -> Minnesota
    55:  24,  # Kansas City      -> Missouri
    111: 24,  # St Louis         -> Missouri
    58:  26,  # Lincoln          -> Nebraska
    81:  26,  # Omaha            -> Nebraska
    56:  27,  # Las Vegas        -> Nevada
    95:  27,  # Reno             -> Nevada
    32:  28,  # Concord          -> New Hampshire
    73:  29,  # Morristown       -> New Jersey
    78:  29,  # Newark           -> New Jersey
    0:   30,  # Albuquerque      -> New Mexico
    109: 30,  # Santa Fe         -> New Mexico
    16:  31,  # Buffalo          -> New York
    77:  31,  # New York City    -> New York
    115: 31,  # Syracuse         -> New York
    20:  32,  # Charlotte        -> North Carolina
    94:  32,  # Raleigh          -> North Carolina
    22:  34,  # Cincinnati       -> Ohio
    23:  34,  # Cleveland        -> Ohio
    31:  34,  # Columbus         -> Ohio
    35:  34,  # Dayton           -> Ohio
    122: 34,  # Toledo           -> Ohio
    80:  35,  # Oklahoma City    -> Oklahoma
    124: 35,  # Tulsa            -> Oklahoma
    46:  36,  # Hillsboro        -> Oregon
    92:  36,  # Portland         -> Oregon
    2:   37,  # Allentown        -> Pennsylvania
    43:  37,  # Harrisburg       -> Pennsylvania
    91:  37,  # Pittsburgh       -> Pennsylvania
    89:  37,  # Philadelphia     -> Pennsylvania
    93:  38,  # Providence       -> Rhode Island
    18:  39,  # Charleston SC    -> South Carolina
    30:  39,  # Columbia SC      -> South Carolina
    62:  41,  # Memphis          -> Tennessee
    75:  41,  # Nashville        -> Tennessee
    6:   42,  # Austin           -> Texas
    34:  42,  # Dallas           -> Texas
    40:  42,  # Fort Worth       -> Texas
    53:  42,  # Houston          -> Texas
    99:  42,  # San Antonio      -> Texas
    98:  43,  # Salt Lake City   -> Utah
    17:  44,  # Burlington       -> Vermont
    1:   45,  # Alexandria       -> Virginia
    96:  45,  # Richmond         -> Virginia
    112: 46,  # Seattle          -> Washington
    19:  47,  # Charleston WV    -> West Virginia
    42:  48,  # Green Bay        -> Wisconsin
    70:  48,  # Milwaukee        -> Wisconsin
}


def city_is_in_state(city_idx, state_idx):
    """
    Return True if the given city index is in the given state index.
    Ported from the_city_is_in_the_state() in demo's ematch_class.cxx.

    Uses the CITY_TO_STATE dictionary which maps each city index
    to its state index. This is the Python equivalent of the demo's
    us_cities_in_states[] array lookup.

    Parameters:
        city_idx  -- index of the city to check
        state_idx -- index of the state to check against

    Returns:
        True  if the city belongs to that state
        False if the city does not belong to that state
              or if the city is not found in CITY_TO_STATE
    """
    city_state = CITY_TO_STATE.get(city_idx, -1)

    if city_state == state_idx:
        return True

    return False

# -----------------------------------------------
# ONLY runs when you do: python3 location_data.py
# IGNORED when another file imports this
# -----------------------------------------------
if __name__ == "__main__":
    print(f"Regions : {len(US_REGIONS)}")
    print(f"States  : {len(US_STATES)}")
    print(f"Cities  : {len(US_CITIES)}")

    print("\n--- Region lookup ---")
    print("'california' state index :", find_state_index("california"))
    print("'texas' state index       :", find_state_index("texas"))
    print("'west' region index       :", find_region_index("west"))
    print("'san jose' city index     :", find_city_index("san jose"))

    print("\n--- Neighbor states of Texas (index 42) ---")
    for state_idx, penalty in NEIGHBOR_STATE_RATINGS[42]:
        print(f"  {US_STATES[state_idx]:20s} penalty={penalty}")

    print("\n--- Neighbor cities of San Jose (index 108) ---")
    for city_idx, penalty in NEIGHBOR_CITY_RATINGS[108]:
        print(f"  {US_CITIES[city_idx]:20s} penalty={penalty}")

    print("\n--- States in West region (index 16) ---")
    for si in STATES_IN_REGIONS[16]:
        print(f"  {US_STATES[si]}")

    print("\n--- Is California in West region? ---")
    print( state_is_in_region(find_state_index("california"), find_region_index("west")) )