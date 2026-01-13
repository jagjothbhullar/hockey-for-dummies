#!/usr/bin/env python3
"""
Hockey For Dummies - Learn Hockey Through Sports You Know
An interactive tool that explains hockey concepts using analogies from
Soccer (Premier League), NBA, NFL, and MLB.
"""

from flask import Flask, render_template, jsonify, request
import random
import requests
from difflib import SequenceMatcher

app = Flask(__name__)

# NHL API Base URL
NHL_API_BASE = "https://api-web.nhle.com/v1"

# Path to cached roster file
import os
ROSTER_FILE = os.path.join(os.path.dirname(__file__), 'nhl_rosters.json')

# =============================================================================
# NHL ROSTER CACHE - Load from JSON file for instant startup
# =============================================================================

NHL_ROSTER_CACHE = []
NHL_ROSTER_LOADED = False

def load_rosters_from_file():
    """Load rosters from JSON file (instant)"""
    global NHL_ROSTER_CACHE, NHL_ROSTER_LOADED

    try:
        import json
        with open(ROSTER_FILE, 'r') as f:
            NHL_ROSTER_CACHE = json.load(f)
        NHL_ROSTER_LOADED = True
        print(f"Loaded {len(NHL_ROSTER_CACHE)} players from cache file")
        return True
    except Exception as e:
        print(f"Could not load from file: {e}")
        return False

def save_rosters_to_file():
    """Save current roster cache to JSON file"""
    try:
        import json
        with open(ROSTER_FILE, 'w') as f:
            json.dump(NHL_ROSTER_CACHE, f)
        print(f"Saved {len(NHL_ROSTER_CACHE)} players to cache file")
        return True
    except Exception as e:
        print(f"Could not save to file: {e}")
        return False

def load_all_nhl_rosters():
    """Load all NHL rosters - from file first, then API as fallback"""
    global NHL_ROSTER_CACHE, NHL_ROSTER_LOADED

    if NHL_ROSTER_LOADED:
        return

    # Try loading from file first (instant)
    if load_rosters_from_file():
        return

    # Fallback: load from API (slower, but ensures data exists)
    print("Loading NHL rosters from API...")

    # All 32 NHL team abbreviations
    teams = [
        'ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ',
        'DAL', 'DET', 'EDM', 'FLA', 'LAK', 'MIN', 'MTL', 'NSH',
        'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SJS', 'SEA',
        'STL', 'TBL', 'TOR', 'UTA', 'VAN', 'VGK', 'WSH', 'WPG'
    ]

    all_players = []

    for team in teams:
        try:
            response = requests.get(f"{NHL_API_BASE}/roster/{team}/current", timeout=10)
            if response.status_code == 200:
                data = response.json()
                for pos in ['forwards', 'defensemen', 'goalies']:
                    for player in data.get(pos, []):
                        all_players.append({
                            'id': player.get('id'),
                            'name': f"{player.get('firstName', {}).get('default', '')} {player.get('lastName', {}).get('default', '')}",
                            'first_name': player.get('firstName', {}).get('default', ''),
                            'last_name': player.get('lastName', {}).get('default', ''),
                            'position': player.get('positionCode', ''),
                            'number': player.get('sweaterNumber', ''),
                            'team': team
                        })
        except Exception as e:
            print(f"Error loading {team}: {e}")

    NHL_ROSTER_CACHE = all_players
    NHL_ROSTER_LOADED = True
    print(f"Loaded {len(all_players)} NHL players from API")

    # Save to file for next time
    save_rosters_to_file()

def refresh_rosters_from_api():
    """Force refresh rosters from NHL API and update cache file"""
    global NHL_ROSTER_CACHE, NHL_ROSTER_LOADED

    print("Refreshing NHL rosters from API...")
    NHL_ROSTER_LOADED = False
    NHL_ROSTER_CACHE = []

    teams = [
        'ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ',
        'DAL', 'DET', 'EDM', 'FLA', 'LAK', 'MIN', 'MTL', 'NSH',
        'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SJS', 'SEA',
        'STL', 'TBL', 'TOR', 'UTA', 'VAN', 'VGK', 'WSH', 'WPG'
    ]

    all_players = []

    for team in teams:
        try:
            response = requests.get(f"{NHL_API_BASE}/roster/{team}/current", timeout=10)
            if response.status_code == 200:
                data = response.json()
                for pos in ['forwards', 'defensemen', 'goalies']:
                    for player in data.get(pos, []):
                        all_players.append({
                            'id': player.get('id'),
                            'name': f"{player.get('firstName', {}).get('default', '')} {player.get('lastName', {}).get('default', '')}",
                            'first_name': player.get('firstName', {}).get('default', ''),
                            'last_name': player.get('lastName', {}).get('default', ''),
                            'position': player.get('positionCode', ''),
                            'number': player.get('sweaterNumber', ''),
                            'team': team
                        })
        except Exception as e:
            print(f"Error loading {team}: {e}")

    NHL_ROSTER_CACHE = all_players
    NHL_ROSTER_LOADED = True
    save_rosters_to_file()
    return len(all_players)

# =============================================================================
# MEET THE SHARKS - San Jose Sharks Roster with Roles & Comparisons
# =============================================================================

SHARKS_ROSTER = {
    "macklin celebrini": {
        "number": 71,
        "position": "Center",
        "age": 18,
        "from": "Vancouver, BC",
        "draft": "#1 Overall, 2024",
        "role": "Franchise Cornerstone",
        "role_description": "The future of the franchise. Celebrini is expected to be the offensive catalyst and face of the Sharks for the next decade+. Think of him as the new foundation everything is being built around.",
        "play_style": "Elite skating, incredible hockey IQ, can score and set up teammates equally well. Already showing NHL-level compete despite his age.",
        "fun_fact": "First #1 pick in Sharks history. Won the Hobey Baker Award (college hockey's Heisman) as a freshman.",
        "soccer_comp": {"player": "Jude Bellingham", "why": "Teenage phenom who immediately became a franchise cornerstone"},
        "nba_comp": {"player": "Victor Wembanyama", "why": "Generational #1 pick expected to transform a struggling franchise"},
        "nfl_comp": {"player": "Caleb Williams", "why": "Top pick brought in to be the new face of the franchise"},
        "mlb_comp": {"player": "Jackson Holliday", "why": "Top prospect with elite bloodlines and expectations"}
    },
    "william eklund": {
        "number": 72,
        "position": "Left Wing",
        "age": 22,
        "from": "Stockholm, Sweden",
        "draft": "#7 Overall, 2021",
        "role": "Top-6 Playmaker",
        "role_description": "Skilled Swedish winger who creates offense with vision and puck skills. Part of the young core being built around Celebrini.",
        "play_style": "Excellent passer, smart positional player, sees plays develop before they happen. Still developing his shot and physical game.",
        "fun_fact": "One of the top Swedish prospects of his generation. Made the team out of camp as an 18-year-old.",
        "soccer_comp": {"player": "Florian Wirtz", "why": "Young creative talent from a country known for producing skilled players"},
        "nba_comp": {"player": "Tyrese Maxey", "why": "Young guard developing into a star alongside other young talent"},
        "nfl_comp": {"player": "Garrett Wilson", "why": "Young receiver still growing into his potential"},
        "mlb_comp": {"player": "Corbin Carroll", "why": "Young talent with speed and skill, still maturing"}
    },
    "will smith": {
        "number": 2,
        "position": "Center",
        "age": 19,
        "from": "Lexington, MA",
        "draft": "#4 Overall, 2023",
        "role": "Future Top-Line Center",
        "role_description": "Another blue-chip prospect in the Sharks' rebuild. Will center one of the top lines alongside Celebrini in the future.",
        "play_style": "Excellent offensive instincts, great vision, skilled playmaker. Smart two-way player who can be trusted defensively.",
        "fun_fact": "Played at Boston College. His dad was also a hockey player at BC.",
        "soccer_comp": {"player": "Kobbie Mainoo", "why": "Young midfielder breaking through, expected to be a star"},
        "nba_comp": {"player": "Chet Holmgren", "why": "High draft pick with unique skills, part of a rebuild"},
        "nfl_comp": {"player": "Drake Maye", "why": "Top-5 pick expected to be a franchise building block"},
        "mlb_comp": {"player": "Paul Skenes", "why": "Top draft pick making an immediate impact"}
    },
    "mikael granlund": {
        "number": 64,
        "position": "Center/Wing",
        "age": 32,
        "from": "Oulu, Finland",
        "draft": "#9 Overall, 2010",
        "role": "Veteran Leader",
        "role_description": "Experienced Finnish forward who provides leadership and playoff experience. Mentors the young players while still producing offensively.",
        "play_style": "Crafty playmaker with excellent hands. Smart positional player, good on the power play. Responsible defensively.",
        "fun_fact": "Famous for scoring a lacrosse-style goal in international competition. Has played in two Olympics for Finland.",
        "soccer_comp": {"player": "Luka Modric", "why": "Veteran playmaker who leads by example"},
        "nba_comp": {"player": "Chris Paul", "why": "Veteran floor general mentoring young talent"},
        "nfl_comp": {"player": "Aaron Rodgers", "why": "Experienced QB leading a young team"},
        "mlb_comp": {"player": "Justin Verlander", "why": "Veteran presence guiding a rebuilding roster"}
    },
    "tyler toffoli": {
        "number": 73,
        "position": "Right Wing",
        "age": 31,
        "from": "Scarborough, ON",
        "draft": "#47 Overall, 2010",
        "role": "Top-Line Scorer",
        "role_description": "Proven goal scorer who provides offensive punch. Stanley Cup champion who brings winning experience to a young team.",
        "play_style": "Pure goal scorer with a lethal shot. Finds soft spots in the defense, excellent around the net. Good on the power play.",
        "fun_fact": "Won the Stanley Cup with LA Kings in 2014. Has scored 30+ goals in a season.",
        "soccer_comp": {"player": "Jamie Vardy", "why": "Proven goal scorer who's been there and done that"},
        "nba_comp": {"player": "Klay Thompson", "why": "Championship-winning scorer who can still fill it up"},
        "nfl_comp": {"player": "Davante Adams", "why": "Veteran receiver with championship experience"},
        "mlb_comp": {"player": "Teoscar Hernandez", "why": "Veteran bat who provides pop in the lineup"}
    },
    "fabian zetterlund": {
        "number": 20,
        "position": "Right Wing",
        "age": 25,
        "from": "Stockholm, Sweden",
        "draft": "#63 Overall, 2018",
        "role": "Middle-Six Scorer",
        "role_description": "Solid two-way winger who can chip in offensively while playing a responsible game. Brings energy every shift.",
        "play_style": "Good shot, plays physical for his size, responsible in his own zone. Can play up and down the lineup.",
        "fun_fact": "Originally drafted by New Jersey, acquired by Sharks in 2022. Fellow Swede with Eklund.",
        "soccer_comp": {"player": "Jarrod Bowen", "why": "Hard-working winger who contributes on both ends"},
        "nba_comp": {"player": "Donte DiVincenzo", "why": "Energy player who does a bit of everything"},
        "nfl_comp": {"player": "Jaylen Waddle", "why": "Dynamic player who makes plays when given opportunities"},
        "mlb_comp": {"player": "Bryan Reynolds", "why": "Solid all-around player, does everything well"}
    },
    "logan couture": {
        "number": 39,
        "position": "Center",
        "age": 35,
        "from": "Guelph, ON",
        "draft": "#9 Overall, 2007",
        "role": "Captain / Veteran Mentor",
        "role_description": "Team captain and franchise icon. While his playing time has decreased due to injuries, he remains the heart and soul of the locker room.",
        "play_style": "Elite two-way center in his prime. Known for clutch playoff performances and leadership. One of the best Sharks ever.",
        "fun_fact": "Sharks all-time playoff leader in goals and points. Has been captain since 2019.",
        "soccer_comp": {"player": "Jordan Henderson", "why": "Long-time captain, the heartbeat of the team"},
        "nba_comp": {"player": "Udonis Haslem", "why": "Franchise lifer, more valuable as a leader now"},
        "nfl_comp": {"player": "Eli Manning", "why": "Franchise legend, beloved by fans and teammates"},
        "mlb_comp": {"player": "Buster Posey", "why": "Franchise icon who led through example"}
    },
    "mario ferraro": {
        "number": 38,
        "position": "Defenseman",
        "age": 26,
        "from": "Toronto, ON",
        "draft": "#49 Overall, 2017",
        "role": "Top Pair Defenseman",
        "role_description": "The Sharks' best all-around defenseman. Plays tough minutes against the other team's best players.",
        "play_style": "Mobile, competitive, plays with an edge. Good skater who can move the puck and defend physically.",
        "fun_fact": "Wore an 'A' as alternate captain. Fan favorite for his compete level.",
        "soccer_comp": {"player": "William Saliba", "why": "Young defender who's become the defensive anchor"},
        "nba_comp": {"player": "Herb Jones", "why": "Defensive specialist who guards the toughest assignments"},
        "nfl_comp": {"player": "Sauce Gardner", "why": "Lockdown defender who takes on the best"},
        "mlb_comp": {"player": "Matt Chapman", "why": "Elite defender at a premium position"}
    },
    "cody ceci": {
        "number": 4,
        "position": "Defenseman",
        "age": 30,
        "from": "Ottawa, ON",
        "draft": "#15 Overall, 2012",
        "role": "Top-4 Defenseman",
        "role_description": "Veteran defenseman who provides stability on the blue line. Plays a steady, reliable game.",
        "play_style": "Right-shot defenseman, good size, moves the puck efficiently. Reliable if not spectacular.",
        "fun_fact": "Has played for 5 NHL teams. Son of former OHL coach.",
        "soccer_comp": {"player": "Gary Cahill", "why": "Experienced, steady defender"},
        "nba_comp": {"player": "Al Horford", "why": "Veteran presence, does his job consistently"},
        "nfl_comp": {"player": "James Bradberry", "why": "Reliable veteran corner"},
        "mlb_comp": {"player": "Paul DeJong", "why": "Veteran middle infielder providing depth"}
    },
    "jake walman": {
        "number": 96,
        "position": "Defenseman",
        "age": 28,
        "from": "Toronto, ON",
        "draft": "#82 Overall, 2014",
        "role": "Offensive Defenseman",
        "role_description": "Puck-moving defenseman who adds offense from the blue line. Can quarterback a power play.",
        "play_style": "Good skater with offensive instincts. Has a good shot from the point. Still developing his defensive consistency.",
        "fun_fact": "Broke out with Detroit before being traded to San Jose.",
        "soccer_comp": {"player": "Trent Alexander-Arnold", "why": "Attack-minded defender who creates offense"},
        "nba_comp": {"player": "Draymond Green", "why": "Defender who can run the offense"},
        "nfl_comp": {"player": "Micah Parsons", "why": "Dynamic defender with playmaking ability"},
        "mlb_comp": {"player": "Gunnar Henderson", "why": "Defender with offensive pop"}
    },
    "mackenzie blackwood": {
        "number": 29,
        "position": "Goaltender",
        "age": 27,
        "from": "Thunder Bay, ON",
        "draft": "#42 Overall, 2015",
        "role": "Starting Goaltender",
        "role_description": "The Sharks' number one netminder. A talented goalie who can steal games when he's on his game.",
        "play_style": "Athletic, good size (6'4\"), tracks the puck well. Can be streaky but capable of elite performances.",
        "fun_fact": "Acquired from New Jersey. Named after former NHL goalie Kirk McLean (his parents were fans).",
        "soccer_comp": {"player": "David Raya", "why": "Athletic goalkeeper who can make spectacular saves"},
        "nba_comp": {"player": "Brook Lopez", "why": "Solid presence protecting the paint"},
        "nfl_comp": {"player": "Geno Smith", "why": "Veteran who's found a home and playing well"},
        "mlb_comp": {"player": "Sonny Gray", "why": "Talented arm who can dominate when locked in"}
    },
    "vitek vanecek": {
        "number": 41,
        "position": "Goaltender",
        "age": 28,
        "from": "Havlickuv Brod, Czech Republic",
        "draft": "#39 Overall, 2014",
        "role": "Backup Goaltender",
        "role_description": "Experienced backup who provides rest for Blackwood and can win games when called upon.",
        "play_style": "Positionally sound, good athleticism. Has starting experience in the league.",
        "fun_fact": "Has played for Washington and New Jersey before San Jose. Czech international.",
        "soccer_comp": {"player": "Aaron Ramsdale", "why": "Quality backup pushing for playing time"},
        "nba_comp": {"player": "Daniel Theis", "why": "Reliable backup center who can start if needed"},
        "nfl_comp": {"player": "Cooper Rush", "why": "Quality backup who's proven he can win games"},
        "mlb_comp": {"player": "Ross Stripling", "why": "Swing pitcher who can start or relieve"}
    },
    "timothy liljegren": {
        "number": 37,
        "position": "Defenseman",
        "age": 25,
        "from": "Kristianstad, Sweden",
        "draft": "#17 Overall, 2017",
        "role": "Depth Defenseman",
        "role_description": "Skilled puck-moving defenseman. Former first-round pick still trying to reach his potential.",
        "play_style": "Good skater, can move the puck. Working on defensive consistency and physicality.",
        "fun_fact": "Traded from Toronto. Swedish national team member.",
        "soccer_comp": {"player": "Josko Gvardiol", "why": "Skilled young defender with high pedigree"},
        "nba_comp": {"player": "Patrick Williams", "why": "Former lottery pick developing his game"},
        "nfl_comp": {"player": "Trevon Diggs", "why": "Talented but can be inconsistent"},
        "mlb_comp": {"player": "Spencer Torkelson", "why": "High draft pick still finding his footing"}
    },
    "ty dellandrea": {
        "number": 10,
        "position": "Center",
        "age": 24,
        "from": "Toronto, ON",
        "draft": "#13 Overall, 2018",
        "role": "Bottom-Six Forward",
        "role_description": "Energy center who brings compete level every night. Plays a responsible two-way game.",
        "play_style": "Hard worker, good penalty killer, responsible defensively. Chips in some offense.",
        "fun_fact": "Former first-round pick of Dallas. Captain of Canada's World Junior team.",
        "soccer_comp": {"player": "Conor Gallagher", "why": "High-energy midfielder who never stops running"},
        "nba_comp": {"player": "Alex Caruso", "why": "Hustle player who does the little things"},
        "nfl_comp": {"player": "Rex Burkhead", "why": "Versatile player who does whatever's needed"},
        "mlb_comp": {"player": "Nick Ahmed", "why": "Glue guy who plays solid defense"}
    },
    "luke kunin": {
        "number": 11,
        "position": "Right Wing",
        "age": 27,
        "from": "Chesterfield, MO",
        "draft": "#15 Overall, 2016",
        "role": "Bottom-Six Forward",
        "role_description": "Physical forward who brings energy and can chip in offense. Good penalty killer.",
        "play_style": "Plays with an edge, willing to go to the hard areas. Can score but primarily a grinder.",
        "fun_fact": "American-born, played at University of Wisconsin. Former first-round pick.",
        "soccer_comp": {"player": "Adam Lallana", "why": "Works hard, brings energy, occasional goals"},
        "nba_comp": {"player": "P.J. Tucker", "why": "Hustle player who does the dirty work"},
        "nfl_comp": {"player": "Taysom Hill", "why": "Versatile player who brings energy"},
        "mlb_comp": {"player": "Kiké Hernandez", "why": "Utility player who fills in where needed"}
    },
    "carl grundstrom": {
        "number": 91,
        "position": "Left Wing",
        "age": 27,
        "from": "Stockholm, Sweden",
        "draft": "#57 Overall, 2016",
        "role": "Bottom-Six Forward",
        "role_description": "Physical forward who brings sandpaper to the lineup. Plays a heavy game.",
        "play_style": "Physical, hits everything that moves. Forechecks hard. Limited offensive upside but valuable role player.",
        "fun_fact": "Originally drafted by Toronto, won a Calder Cup (AHL championship) with Ontario Reign.",
        "soccer_comp": {"player": "James Milner", "why": "Does the dirty work, never complains"},
        "nba_comp": {"player": "Patrick Beverley", "why": "Pest who opponents hate to play against"},
        "nfl_comp": {"player": "Cordarrelle Patterson", "why": "Does multiple jobs, special teams ace"},
        "mlb_comp": {"player": "Tommy Edman", "why": "Role player who does whatever's asked"}
    },
    "barclay goodrow": {
        "number": 23,
        "position": "Center/Wing",
        "age": 31,
        "from": "Toronto, ON",
        "draft": "Undrafted",
        "role": "Veteran Role Player",
        "role_description": "Two-time Stanley Cup champion who brings winning experience. Versatile forward who can play any situation.",
        "play_style": "Intelligent player, excellent penalty killer, does all the little things right. True professional.",
        "fun_fact": "Won back-to-back Cups with Tampa Bay. Fan favorite who returned to San Jose where he started.",
        "soccer_comp": {"player": "Olivier Giroud", "why": "Veteran winner who does the intangibles"},
        "nba_comp": {"player": "Andre Iguodala", "why": "Championship DNA, knows how to win"},
        "nfl_comp": {"player": "Julian Edelman", "why": "Clutch veteran with rings"},
        "mlb_comp": {"player": "David Ross", "why": "Veteran presence with championship experience"}
    },
    "alexander wennberg": {
        "number": 21,
        "position": "Center",
        "age": 30,
        "from": "Stockholm, Sweden",
        "draft": "#14 Overall, 2013",
        "role": "Veteran Center",
        "role_description": "Experienced Swedish center who provides depth and leadership. Smart two-way player who can be trusted in all situations.",
        "play_style": "Smart positional player, excellent penalty killer, good on faceoffs. Steady and reliable.",
        "fun_fact": "Won the Stanley Cup with Florida Panthers in 2024. Has represented Sweden in multiple World Championships.",
        "soccer_comp": {"player": "N'Golo Kante", "why": "Tireless worker who covers the entire pitch"},
        "nba_comp": {"player": "Jrue Holiday", "why": "Veteran two-way player who does everything right"},
        "nfl_comp": {"player": "Zach Wilson", "why": "Former high pick finding his role"},
        "mlb_comp": {"player": "Tommy Edman", "why": "Versatile veteran who fills any role needed"}
    },
    "nico sturm": {
        "number": 7,
        "position": "Center",
        "age": 29,
        "from": "Augsburg, Germany",
        "draft": "Undrafted",
        "role": "Fourth-Line Center",
        "role_description": "Physical German center who brings energy and grit. Excellent penalty killer and faceoff specialist.",
        "play_style": "Physical presence, wins battles along the boards, strong on faceoffs. Plays a heavy, grinding style.",
        "fun_fact": "One of only a few German players in the NHL. Played college hockey at Clarkson University.",
        "soccer_comp": {"player": "Joshua Kimmich", "why": "German workhorse who does the dirty work"},
        "nba_comp": {"player": "Marcus Smart", "why": "Defensive-minded player who brings toughness"},
        "nfl_comp": {"player": "Zach Line", "why": "Fullback type - does the grunt work"},
        "mlb_comp": {"player": "Max Stassi", "why": "Defense-first player who contributes intangibles"}
    },
    "klim kostin": {
        "number": 21,
        "position": "Right Wing",
        "age": 25,
        "from": "Penza, Russia",
        "draft": "#31 Overall, 2017",
        "role": "Power Forward",
        "role_description": "Big-bodied Russian winger with skill. Uses his size to protect the puck and create offense.",
        "play_style": "Physical player with soft hands. Protects the puck well, crashes the net, has a good shot.",
        "fun_fact": "Former first-round pick by St. Louis. Played in the KHL before coming to North America.",
        "soccer_comp": {"player": "Romelu Lukaku", "why": "Big, physical forward who uses his body"},
        "nba_comp": {"player": "Zion Williamson", "why": "Power player who overwhelms with physicality"},
        "nfl_comp": {"player": "Derrick Henry", "why": "Power runner who punishes defenders"},
        "mlb_comp": {"player": "Yordan Alvarez", "why": "Big bat who drives in runs"}
    },
    "marc-edouard vlasic": {
        "number": 44,
        "position": "Defenseman",
        "age": 37,
        "from": "Montreal, QC",
        "draft": "#35 Overall, 2005",
        "role": "Veteran Defenseman",
        "role_description": "Long-time Sharks defenseman and franchise icon. While no longer the shutdown force he once was, brings experience and leadership.",
        "play_style": "In his prime was one of the best shutdown defensemen in the NHL. Smart positioning, excellent stick work.",
        "fun_fact": "Three-time Olympic gold medalist for Canada. One of the longest-tenured Sharks ever.",
        "soccer_comp": {"player": "Thiago Silva", "why": "Veteran defender who's been a cornerstone for years"},
        "nba_comp": {"player": "Al Horford", "why": "Veteran big man still contributing"},
        "nfl_comp": {"player": "Andrew Whitworth", "why": "Veteran tackle winding down a great career"},
        "mlb_comp": {"player": "Yadier Molina", "why": "Franchise legend in the twilight years"}
    },
    "henry thrun": {
        "number": 3,
        "position": "Defenseman",
        "age": 24,
        "from": "Southborough, MA",
        "draft": "#101 Overall, 2019",
        "role": "Young Defenseman",
        "role_description": "Left-shot defenseman developing his NHL game. Mobile skater who moves the puck well.",
        "play_style": "Good skating defenseman, moves the puck efficiently. Still learning to defend at the NHL level.",
        "fun_fact": "Played at Harvard University before turning pro. Massachusetts native.",
        "soccer_comp": {"player": "Marc Cucurella", "why": "Left-footed defender with good mobility"},
        "nba_comp": {"player": "Ayo Dosunmu", "why": "Young player carving out his role"},
        "nfl_comp": {"player": "Aidan Hutchinson", "why": "Young defender learning at the pro level"},
        "mlb_comp": {"player": "Brendan Rodgers", "why": "Young infielder developing his game"}
    },
    "shakir mukhamadullin": {
        "number": 54,
        "position": "Defenseman",
        "age": 23,
        "from": "Nizhnekamsk, Russia",
        "draft": "#20 Overall, 2020",
        "role": "Prospect Defenseman",
        "role_description": "Big Russian defenseman with offensive upside. First-round pick developing his North American game.",
        "play_style": "Large (6'4\"), skating defenseman with a good shot. Offense-first mindset, still learning defensive responsibilities.",
        "fun_fact": "Spent several years in the KHL before coming to North America. Represented Russia internationally.",
        "soccer_comp": {"player": "Clement Lenglet", "why": "Big defender with room to grow"},
        "nba_comp": {"player": "Jalen Smith", "why": "First-round pick still developing"},
        "nfl_comp": {"player": "Travon Walker", "why": "High draft pick with high ceiling"},
        "mlb_comp": {"player": "Oneil Cruz", "why": "Raw talent with enormous potential"}
    },
    "yaroslav askarov": {
        "number": 30,
        "position": "Goaltender",
        "age": 22,
        "from": "Omsk, Russia",
        "draft": "#11 Overall, 2020",
        "role": "Goalie Prospect",
        "role_description": "Highly touted Russian goaltending prospect. One of the best goalie prospects in hockey, expected to be a future franchise netminder.",
        "play_style": "Athletic, aggressive goaltending style. Quick reflexes, good positioning, competitive fire.",
        "fun_fact": "Considered one of the best goalie prospects of his generation. Acquired from Nashville.",
        "soccer_comp": {"player": "Gianluigi Donnarumma", "why": "Young superstar goalkeeper with elite potential"},
        "nba_comp": {"player": "Victor Wembanyama", "why": "Generational prospect at his position"},
        "nfl_comp": {"player": "Bryce Young", "why": "Top prospect expected to be a franchise player"},
        "mlb_comp": {"player": "Jackson Holliday", "why": "Elite prospect with superstar upside"}
    },
    "jan rutta": {
        "number": 18,
        "position": "Defenseman",
        "age": 34,
        "from": "Pisek, Czech Republic",
        "draft": "Undrafted",
        "role": "Depth Defenseman",
        "role_description": "Veteran Czech defenseman who provides stability and experience. Physical, stay-at-home defender.",
        "play_style": "Physical, shot-blocking defenseman. Plays a simple, effective game. Good penalty killer.",
        "fun_fact": "Two-time Stanley Cup champion with Tampa Bay. Late bloomer who didn't reach NHL until age 27.",
        "soccer_comp": {"player": "Petr Cech", "why": "Czech veteran who's won championships"},
        "nba_comp": {"player": "Jeff Green", "why": "Veteran journeyman who knows how to win"},
        "nfl_comp": {"player": "Mike Hilton", "why": "Physical defender with championship pedigree"},
        "mlb_comp": {"player": "Chris Taylor", "why": "Veteran role player with playoff experience"}
    },
    "jeff skinner": {
        "number": 53,
        "position": "Left Wing",
        "age": 32,
        "from": "Markham, ON",
        "draft": "#7 Overall, 2010",
        "role": "Veteran Scorer",
        "role_description": "Experienced goal scorer who provides offensive punch. Former Calder Trophy winner who knows how to find the net.",
        "play_style": "Elite skating, quick hands, excellent shot. Pure goal scorer who lives around the crease.",
        "fun_fact": "Won the Calder Trophy as NHL Rookie of the Year in 2011. Was a competitive figure skater as a child.",
        "soccer_comp": {"player": "Raheem Sterling", "why": "Skilled, speedy winger who can score in bunches"},
        "nba_comp": {"player": "Zach LaVine", "why": "Explosive scorer with great athleticism"},
        "nfl_comp": {"player": "Stefon Diggs", "why": "Proven receiver who can still produce"},
        "mlb_comp": {"player": "Anthony Santander", "why": "Veteran bat who provides consistent offense"}
    },
    "ryan reaves": {
        "number": 75,
        "position": "Right Wing",
        "age": 38,
        "from": "Winnipeg, MB",
        "draft": "#156 Overall, 2005",
        "role": "Enforcer / Energy",
        "role_description": "Physical presence who protects teammates and brings energy. One of the most feared fighters in NHL history.",
        "play_style": "Physical, intimidating, willing to drop the gloves. Brings energy and protects the young stars.",
        "fun_fact": "Stanley Cup champion with Vegas. Has over 100 NHL fights. Known for his infectious personality.",
        "soccer_comp": {"player": "Diego Costa", "why": "Physical intimidator who gets under opponents' skin"},
        "nba_comp": {"player": "Patrick Beverley", "why": "Tough guy who protects his teammates"},
        "nfl_comp": {"player": "Vontaze Burfict", "why": "Intimidating physical presence"},
        "mlb_comp": {"player": "AJ Pierzynski", "why": "Tough veteran who opponents hate to face"}
    },
    "dmitry orlov": {
        "number": 9,
        "position": "Defenseman",
        "age": 33,
        "from": "Novokuznetsk, Russia",
        "draft": "#55 Overall, 2009",
        "role": "Top-4 Defenseman",
        "role_description": "Veteran Russian defenseman with Stanley Cup experience. Provides stability and puck-moving ability.",
        "play_style": "Mobile defender, good puck mover, strong on the power play. Smart positional player.",
        "fun_fact": "Won the Stanley Cup with Washington in 2018. Has represented Russia internationally.",
        "soccer_comp": {"player": "David Alaba", "why": "Experienced defender who can play multiple positions"},
        "nba_comp": {"player": "Brook Lopez", "why": "Veteran who's reinvented his game"},
        "nfl_comp": {"player": "Stephon Gilmore", "why": "Veteran corner with championship pedigree"},
        "mlb_comp": {"player": "Andrelton Simmons", "why": "Veteran defender with a championship ring"}
    },
    "john klingberg": {
        "number": 3,
        "position": "Defenseman",
        "age": 32,
        "from": "Gothenburg, Sweden",
        "draft": "#131 Overall, 2010",
        "role": "Offensive Defenseman",
        "role_description": "Swedish defenseman known for his offensive abilities. Former All-Star who quarterbacks the power play.",
        "play_style": "Elite puck mover, great vision, excellent shot from the point. Offense-first defenseman.",
        "fun_fact": "Was a late-round steal by Dallas. Led all NHL defensemen in assists during 2020-21 season.",
        "soccer_comp": {"player": "Trent Alexander-Arnold", "why": "Attack-minded defender known for creating offense"},
        "nba_comp": {"player": "Draymond Green", "why": "Playmaking defender who runs the offense"},
        "nfl_comp": {"player": "Quenton Nelson", "why": "Elite at creating opportunities"},
        "mlb_comp": {"player": "Xander Bogaerts", "why": "Shortstop with an offensive edge"}
    },
    "nick leddy": {
        "number": 4,
        "position": "Defenseman",
        "age": 33,
        "from": "Eden Prairie, MN",
        "draft": "#16 Overall, 2009",
        "role": "Veteran Defenseman",
        "role_description": "Experienced skating defenseman. Stanley Cup champion who brings poise and mobility.",
        "play_style": "Elite skater, good puck mover. Uses speed to break up plays and start rushes.",
        "fun_fact": "Won the Stanley Cup with Chicago in 2013 and 2015. American Olympian.",
        "soccer_comp": {"player": "Jordi Alba", "why": "Speedy defender known for getting forward"},
        "nba_comp": {"player": "Nic Claxton", "why": "Athletic defender who covers ground"},
        "nfl_comp": {"player": "Taron Johnson", "why": "Quick, athletic defender"},
        "mlb_comp": {"player": "Jose Iglesias", "why": "Veteran with great range in the field"}
    },
    "alex nedeljkovic": {
        "number": 33,
        "position": "Goaltender",
        "age": 29,
        "from": "Parma, OH",
        "draft": "#37 Overall, 2014",
        "role": "Goaltender",
        "role_description": "Experienced American goaltender. Former Calder Trophy finalist who can steal games.",
        "play_style": "Athletic, competitive goaltender. Active puck handler, battles hard.",
        "fun_fact": "Finished 2nd in Calder Trophy voting in 2021. American World Junior gold medalist.",
        "soccer_comp": {"player": "Matt Turner", "why": "American keeper with big-game experience"},
        "nba_comp": {"player": "Spencer Dinwiddie", "why": "Solid veteran who can step up"},
        "nfl_comp": {"player": "Geno Smith", "why": "Veteran finding success after a journey"},
        "mlb_comp": {"player": "Jordan Montgomery", "why": "Solid arm who can compete"}
    },
    "sam dickinson": {
        "number": 6,
        "position": "Defenseman",
        "age": 19,
        "from": "Toronto, ON",
        "draft": "#11 Overall, 2024",
        "role": "Top Prospect",
        "role_description": "High-end defensive prospect from the 2024 draft class. Part of the rebuild's young core on defense.",
        "play_style": "Mobile, puck-moving defenseman. Good size, excellent skating, offensive upside.",
        "fun_fact": "Drafted 11th overall in 2024. Played for the London Knights in the OHL.",
        "soccer_comp": {"player": "Levi Colwill", "why": "Young defender with high ceiling"},
        "nba_comp": {"player": "Ausar Thompson", "why": "Athletic young prospect"},
        "nfl_comp": {"player": "Derek Stingley Jr.", "why": "High draft pick with elite tools"},
        "mlb_comp": {"player": "Elly De La Cruz", "why": "Athletic young prospect with star potential"}
    },
    "philipp kurashev": {
        "number": 96,
        "position": "Center",
        "age": 25,
        "from": "Bern, Switzerland",
        "draft": "#120 Overall, 2018",
        "role": "Middle-Six Forward",
        "role_description": "Swiss forward who brings skill and versatility. Can play center or wing.",
        "play_style": "Skilled playmaker, good hands, smart positional player. Contributes on the power play.",
        "fun_fact": "Swiss international, has represented Switzerland at World Championships.",
        "soccer_comp": {"player": "Granit Xhaka", "why": "Swiss player with technical skills"},
        "nba_comp": {"player": "Tyus Jones", "why": "Smart player who does a bit of everything"},
        "nfl_comp": {"player": "Tyler Lockett", "why": "Skilled player who makes the most of opportunities"},
        "mlb_comp": {"player": "Nico Hoerner", "why": "Versatile player who contributes everywhere"}
    },
    "vincent desharnais": {
        "number": 5,
        "position": "Defenseman",
        "age": 28,
        "from": "Laurier-Station, QC",
        "draft": "Undrafted",
        "role": "Physical Defenseman",
        "role_description": "Big, physical defenseman who plays a simple, effective game. Uses his size to his advantage.",
        "play_style": "Large (6'7\"), physical defender. Clears the crease, blocks shots, plays a stay-at-home style.",
        "fun_fact": "Undrafted player who worked his way up through the minor leagues. Towering presence on the blue line.",
        "soccer_comp": {"player": "Wout Weghorst", "why": "Towering physical presence"},
        "nba_comp": {"player": "Bol Bol", "why": "Uses height as an advantage"},
        "nfl_comp": {"player": "Jordan Mailata", "why": "Massive player who uses size effectively"},
        "mlb_comp": {"player": "Aaron Judge", "why": "Imposing physical presence"}
    },
    "adam gaudette": {
        "number": 81,
        "position": "Center",
        "age": 28,
        "from": "Braintree, MA",
        "draft": "#149 Overall, 2015",
        "role": "Depth Forward",
        "role_description": "Skilled forward who can fill in anywhere in the lineup. Won the Hobey Baker Award in college.",
        "play_style": "Smart player with good offensive instincts. Can contribute on the power play.",
        "fun_fact": "Won the Hobey Baker Award at Northeastern in 2018 as college hockey's best player.",
        "soccer_comp": {"player": "Adam Lallana", "why": "Skilled veteran who can contribute when called upon"},
        "nba_comp": {"player": "Malik Beasley", "why": "Offensive spark off the bench"},
        "nfl_comp": {"player": "Randall Cobb", "why": "Veteran who knows his role"},
        "mlb_comp": {"player": "Whit Merrifield", "why": "Versatile veteran who can play anywhere"}
    },
    "zack ostapchuk": {
        "number": 63,
        "position": "Center",
        "age": 21,
        "from": "St. Albert, AB",
        "draft": "#39 Overall, 2021",
        "role": "Young Forward",
        "role_description": "Physical young center developing his NHL game. Brings size and energy.",
        "play_style": "Big-bodied center, plays physical, developing offensive game. Works hard every shift.",
        "fun_fact": "Former second-round pick. Played in the WHL for the Vancouver Giants.",
        "soccer_comp": {"player": "Evan Ferguson", "why": "Young forward still developing"},
        "nba_comp": {"player": "Jaime Jaquez Jr.", "why": "Hardworking young player"},
        "nfl_comp": {"player": "Tank Dell", "why": "Young player making an impression"},
        "mlb_comp": {"player": "Jordan Lawlar", "why": "Promising young talent"}
    },
    "michael misa": {
        "number": 77,
        "position": "Center",
        "age": 18,
        "from": "Oakville, ON",
        "draft": "#9 Overall, 2025",
        "role": "Elite Prospect",
        "role_description": "Exceptional young talent, one of the top prospects in hockey. Future offensive star.",
        "play_style": "Elite offensive skills, incredible hockey sense, natural goal scorer. Special talent.",
        "fun_fact": "Granted exceptional status to play in the OHL a year early. One of the most highly-touted prospects in years.",
        "soccer_comp": {"player": "Lamine Yamal", "why": "Teenage phenom with exceptional talent"},
        "nba_comp": {"player": "Cooper Flagg", "why": "Generational prospect everyone is excited about"},
        "nfl_comp": {"player": "Arch Manning", "why": "Elite prospect with unlimited ceiling"},
        "mlb_comp": {"player": "Travis Bazzana", "why": "Top prospect with elite tools"}
    }
}

# =============================================================================
# STATS GLOSSARY - Hockey Statistics Explained with Analogies
# =============================================================================

STATS_GLOSSARY = {
    "goals": {
        "abbrev": "G",
        "definition": "The number of times a player has put the puck in the net. The most straightforward stat in hockey.",
        "good_number": "30+ goals in a season is excellent. 50+ is elite.",
        "soccer": "Same as goals in soccer - the ultimate measure of a scorer.",
        "nba": "Like points, but each goal is equally weighted (no 2s vs 3s).",
        "nfl": "Like touchdowns - the most celebrated offensive achievement.",
        "mlb": "Like home runs - the stat everyone notices."
    },
    "assists": {
        "abbrev": "A",
        "definition": "The pass(es) that led directly to a goal. Up to TWO assists are awarded per goal (primary and secondary).",
        "good_number": "50+ assists is excellent for a playmaker.",
        "soccer": "Same concept, but hockey gives two assists per goal instead of one.",
        "nba": "Same concept - the pass before the score.",
        "nfl": "Like getting credit for the pass AND the block that sprung a TD.",
        "mlb": "Like RBI credits, but for the setup instead of the finish."
    },
    "points": {
        "abbrev": "P / PTS",
        "definition": "Goals + Assists combined. The primary measure of offensive production.",
        "good_number": "70+ points is very good. 100+ is elite (point-per-game pace).",
        "soccer": "Like 'goal contributions' (G+A) but with two assists possible per goal.",
        "nba": "Different meaning - hockey points measure production, not scoring.",
        "nfl": "Would be like combining TDs + TD passes for a QB.",
        "mlb": "Like combining runs + RBIs into one number."
    },
    "plus_minus": {
        "abbrev": "+/-",
        "definition": "The goal differential when a player is on the ice at even strength. +1 if your team scores, -1 if they allow.",
        "good_number": "+20 or better is excellent. Negative means more goals against.",
        "soccer": "Like tracking goal difference only when a specific player is on the pitch.",
        "nba": "NBA uses this exact same stat - hockey invented it!",
        "nfl": "Like point differential when a specific player is on the field.",
        "mlb": "No direct equivalent - baseball doesn't track this way."
    },
    "pim": {
        "abbrev": "PIM",
        "definition": "Penalty Infraction Minutes - total time spent in the penalty box. Can indicate physical play or discipline issues.",
        "good_number": "Context matters. Enforcers have 100+, skilled players aim for under 30.",
        "soccer": "Like counting yellow and red cards, but measured in minutes.",
        "nba": "Like tracking personal fouls, but with actual time penalties.",
        "nfl": "Like penalty yards, but assigned to individual players.",
        "mlb": "Like HBP (hit by pitch) - sometimes it's strategic aggression."
    },
    "shots": {
        "abbrev": "SOG / S",
        "definition": "Shots on goal - shots that would go in if not stopped by the goalie. Doesn't count misses or blocked shots.",
        "good_number": "200+ shots per season shows someone who shoots a lot.",
        "soccer": "Same concept - shots that require a save.",
        "nba": "Like field goal attempts - how often you're shooting.",
        "nfl": "Like pass attempts - volume of offensive action.",
        "mlb": "Like at-bats - opportunities to produce."
    },
    "shooting_percentage": {
        "abbrev": "S% / SH%",
        "definition": "Goals divided by shots. How often your shots go in.",
        "good_number": "10-12% is average. 15%+ is excellent (or unsustainable). Under 8% is cold.",
        "soccer": "Same as conversion rate - goals per shot on target.",
        "nba": "Like field goal percentage - your efficiency at scoring.",
        "nfl": "Like completion percentage - how often your attempts succeed.",
        "mlb": "Like batting average - how often you get a hit when you try."
    },
    "toi": {
        "abbrev": "TOI",
        "definition": "Time on Ice - how many minutes a player plays per game. Shows coach's trust and player's stamina.",
        "good_number": "Top forwards: 18-22 min. Top D: 22-27 min. Stars play more.",
        "soccer": "Like tracking actual minutes played (not just appearances).",
        "nba": "Same concept - minutes per game shows importance to team.",
        "nfl": "Like snap counts - how much you're actually on the field.",
        "mlb": "Like plate appearances - how much action you see."
    },
    "faceoff_percentage": {
        "abbrev": "FO%",
        "definition": "Percentage of faceoffs won. Only centers take faceoffs regularly.",
        "good_number": "50% is break-even. 55%+ is excellent. Below 45% is poor.",
        "soccer": "No equivalent - soccer doesn't have this type of set play.",
        "nba": "Like tip-off win rate, but it happens 50+ times per game.",
        "nfl": "Like a long snapper's accuracy - specialized skill.",
        "mlb": "Like a catcher's framing rate - specialized but important."
    },
    "corsi": {
        "abbrev": "CF / CF%",
        "definition": "All shot attempts (goals, saves, misses, blocks) for vs against when a player is on ice. Measures puck possession.",
        "good_number": "55%+ CF% means your team dominates possession with you on ice.",
        "soccer": "Like expected goals (xG) - advanced metric for possession/chances.",
        "nba": "Like tracking all field goal attempts for/against when on court.",
        "nfl": "Like EPA (Expected Points Added) - advanced efficiency metric.",
        "mlb": "Like OPS+ or wRC+ - advanced metric beyond basic stats."
    },
    "fenwick": {
        "abbrev": "FF / FF%",
        "definition": "Like Corsi but excludes blocked shots. Some prefer it as blocked shots can be strategy.",
        "good_number": "Similar to Corsi - 55%+ is excellent.",
        "soccer": "A variation on xG that excludes certain shot types.",
        "nba": "Like Corsi but filtering out certain play types.",
        "nfl": "Like a modified EPA - slightly different calculation.",
        "mlb": "Like different versions of WAR - same concept, different calc."
    },
    "pdo": {
        "abbrev": "PDO",
        "definition": "Team shooting % + team save % when on ice. Measures luck. 1000 is average, tends to regress to mean.",
        "good_number": "1000 is average. Much higher/lower usually regresses over time.",
        "soccer": "Like tracking if you're 'overperforming' your xG - luck indicator.",
        "nba": "Like looking at clutch shooting % - often regresses to mean.",
        "nfl": "Like fumble recovery rate - tends to even out over time.",
        "mlb": "Like BABIP - measures luck on balls in play."
    },
    "save_percentage": {
        "abbrev": "SV%",
        "definition": "For goalies - percentage of shots stopped. The primary goalie stat.",
        "good_number": ".915+ is good. .920+ is excellent. .930+ is elite.",
        "soccer": "Like save percentage for goalkeepers.",
        "nba": "Like defensive field goal percentage allowed.",
        "nfl": "Like passer rating allowed for a cornerback.",
        "mlb": "Like ERA but inverted - lower ERA = higher save %."
    },
    "gaa": {
        "abbrev": "GAA",
        "definition": "Goals Against Average - average goals allowed per 60 minutes for goalies.",
        "good_number": "Under 2.50 is good. Under 2.20 is excellent.",
        "soccer": "Like goals conceded per 90 minutes.",
        "nba": "Like defensive rating - points allowed per possession.",
        "nfl": "Like points allowed per game for a defense.",
        "mlb": "Exactly like ERA - runs/goals allowed per standard time period."
    },
    "wins": {
        "abbrev": "W",
        "definition": "For goalies - games won while playing. Goalie of record when team wins.",
        "good_number": "30+ wins is excellent (but depends on team quality).",
        "soccer": "Like clean sheets, but any win counts.",
        "nba": "No individual win stat - team wins only.",
        "nfl": "Like QB wins - credited to the goalie but very team-dependent.",
        "mlb": "Like pitcher wins - individual credit for team achievement."
    },
    "shutouts": {
        "abbrev": "SO",
        "definition": "Games where the goalie allows zero goals for the entire game.",
        "good_number": "5+ shutouts in a season is excellent.",
        "soccer": "Same as clean sheets - no goals allowed.",
        "nba": "No equivalent - impossible to hold a team scoreless.",
        "nfl": "Same concept - shutout means zero points allowed.",
        "mlb": "Like a complete game shutout for a pitcher."
    },
    "pp_points": {
        "abbrev": "PPP / PPG / PPA",
        "definition": "Points/Goals/Assists scored on the power play (when opponent is short-handed).",
        "good_number": "20+ PPP shows a power play specialist.",
        "soccer": "Like goals/assists from set pieces only.",
        "nba": "Like free throw production - easier scoring chances.",
        "nfl": "Like red zone touchdowns - scoring in advantageous situations.",
        "mlb": "Like RBIs with runners in scoring position - key situations."
    },
    "sh_points": {
        "abbrev": "SHP / SHG / SHA",
        "definition": "Points/Goals/Assists while YOUR team is short-handed (killing a penalty).",
        "good_number": "Any is impressive! 5+ SHP is rare and valuable.",
        "soccer": "Like scoring while down a man - extremely difficult.",
        "nba": "Like scoring while in foul trouble - against the odds.",
        "nfl": "Like a pick-six - scoring when you're supposed to be defending.",
        "mlb": "Like a pitcher getting an RBI - not their job but valuable."
    },
    "blocks": {
        "abbrev": "BLK / BKS",
        "definition": "Shots blocked by a skater (not goalie). Shows willingness to sacrifice body.",
        "good_number": "100+ blocks per season shows a shot-blocking defender.",
        "soccer": "Like blocked shots by outfield players.",
        "nba": "Same stat - shots blocked (though usually by big men).",
        "nfl": "Like batted passes - disrupting the opponent's attack.",
        "mlb": "No equivalent - can't block anything in baseball."
    },
    "hits": {
        "abbrev": "HIT",
        "definition": "Legal body checks delivered. Shows physical play.",
        "good_number": "200+ hits per season is very physical.",
        "soccer": "Like successful tackles - winning physical battles.",
        "nba": "Like screens set - physical plays that help the team.",
        "nfl": "Like tackles - making contact to stop the opponent.",
        "mlb": "No equivalent - not a contact sport."
    },
    "giveaways": {
        "abbrev": "GV",
        "definition": "Turnovers caused by your own mistake (bad pass, lost puck battle).",
        "good_number": "Lower is better, but top players handle the puck more so may have more.",
        "soccer": "Like losing possession through your own error.",
        "nba": "Same as turnovers.",
        "nfl": "Like fumbles or interceptions - giving the puck away.",
        "mlb": "Like errors - mistakes that hurt your team."
    },
    "takeaways": {
        "abbrev": "TK",
        "definition": "Turnovers forced by stealing the puck from opponents.",
        "good_number": "50+ takeaways shows good defensive reads.",
        "soccer": "Like interceptions or winning the ball back.",
        "nba": "Same as steals.",
        "nfl": "Like forced fumbles or interceptions.",
        "mlb": "Like a catcher throwing out a runner - proactive defense."
    }
}

# =============================================================================
# RINK ZONES - Interactive Rink Map Data
# =============================================================================

RINK_ZONES = {
    "center_ice": {
        "name": "Center Ice",
        "description": "The middle of the rink where the game begins. The center face-off dot and circle are here.",
        "purpose": "Every period and game starts with a face-off at center ice. After every goal, play restarts here.",
        "fun_fact": "The center ice logo is usually the home team's logo - for the Sharks, it's the iconic Shark biting a hockey stick.",
        "soccer": "Like the center circle kickoff spot - where play begins and restarts after goals.",
        "nba": "Like the tip-off circle at half court.",
        "nfl": "Like the 50-yard line - neutral territory where play begins.",
        "mlb": "Like the pitcher's mound - the central point where action initiates."
    },
    "offensive_zone": {
        "name": "Offensive Zone",
        "description": "The area past the opponent's blue line where your team attacks. Contains the opposing goal.",
        "purpose": "This is where you score goals! Teams try to maintain possession here and create scoring chances.",
        "fun_fact": "Teams average about 20-25 minutes of offensive zone time per game. Elite teams push 30+.",
        "soccer": "Like the attacking third - the area closest to the opponent's goal.",
        "nba": "Like being in the paint/key area - prime scoring territory.",
        "nfl": "Like the red zone - inside the opponent's 20-yard line.",
        "mlb": "Like having runners in scoring position - you're threatening to score."
    },
    "defensive_zone": {
        "name": "Defensive Zone",
        "description": "The area behind your own blue line. Contains your goal that you must protect.",
        "purpose": "Keep the puck out of your net! Clear pucks, block shots, and get the puck to neutral ice.",
        "fun_fact": "Goalies face an average of 30 shots per game, with most coming from this zone.",
        "soccer": "Like your defensive third - protecting your own goal.",
        "nba": "Like protecting your own basket against an opposing fast break.",
        "nfl": "Like defending your own end zone.",
        "mlb": "Like your infield defense trying to prevent runs from scoring."
    },
    "neutral_zone": {
        "name": "Neutral Zone",
        "description": "The area between the two blue lines. Neither team's territory.",
        "purpose": "Transition area! Teams move the puck through here to enter the offensive zone. Turnovers here are dangerous.",
        "fun_fact": "The neutral zone trap is a defensive strategy where teams clog this area to prevent attacks.",
        "soccer": "Like the midfield - transitional space between attack and defense.",
        "nba": "Like the half-court area during transition.",
        "nfl": "Like the area between the 20-yard lines - moving territory.",
        "mlb": "Like the gap between infield and outfield."
    },
    "blue_line_offensive": {
        "name": "Blue Line (Offensive)",
        "description": "The line marking entry into the offensive zone. The puck must cross before any attacking player.",
        "purpose": "Determines offside! If an attacking player crosses before the puck, play stops.",
        "fun_fact": "Defensemen often position themselves 'at the point' just inside this line to keep plays alive and take slap shots.",
        "soccer": "Functions like the offside line - you can't be ahead of the puck entering the zone.",
        "nba": "Like the three-point line in reverse - a boundary that changes the rules.",
        "nfl": "Like the line of scrimmage - crossing early is a penalty.",
        "mlb": "Like the baseline - defines fair territory for scoring."
    },
    "blue_line_defensive": {
        "name": "Blue Line (Defensive)",
        "description": "The line marking your defensive zone. Once cleared past this line, you've relieved pressure.",
        "purpose": "Get the puck past this line to clear the zone! Dump-and-chase plays aim to get puck deep past it.",
        "fun_fact": "When a team ices the puck, it must cross both the center red line AND this blue line.",
        "soccer": "Like clearing out of your defensive third.",
        "nba": "Like crossing half court to escape backcourt pressure.",
        "nfl": "Like gaining positive yards past the line of scrimmage.",
        "mlb": "Like getting the ball out of the infield."
    },
    "red_line": {
        "name": "Red Line (Center Line)",
        "description": "The thick red line at center ice dividing the rink in half.",
        "purpose": "Key for icing calls! If you shoot from behind your side and it crosses the goal line untouched, it's icing.",
        "fun_fact": "Before 2005, two-line passes across the red line were illegal. Removing this rule sped up the game significantly.",
        "soccer": "Like the halfway line dividing the pitch.",
        "nba": "Like the half-court line - cross it and you can't go back (8-second rule).",
        "nfl": "Like the 50-yard line - true midfield.",
        "mlb": "Like the line between fair and foul - defines legal plays."
    },
    "goal_crease": {
        "name": "Goal Crease",
        "description": "The blue painted semicircle directly in front of the goal. The goalie's protected zone.",
        "purpose": "Goalies have special rights here. Attackers can't interfere with the goalie in the crease. Goals can be disallowed if there's crease violation.",
        "fun_fact": "The crease is 8 feet wide and extends 4.5 feet from the goal line. It was made larger in 1999 to protect goalies.",
        "soccer": "Like the 6-yard box - the goalkeeper's protected area.",
        "nba": "Like the restricted area under the basket - special rules apply.",
        "nfl": "Like the end zone - the most protected scoring area.",
        "mlb": "Like home plate area - where plays at the plate happen."
    },
    "faceoff_circle_center": {
        "name": "Center Face-off Circle",
        "description": "The large circle at center ice (30 feet diameter) with a face-off dot in the middle.",
        "purpose": "Only the two players taking the face-off can be inside until the puck drops. All other players must stay outside.",
        "fun_fact": "Face-off wins are tracked as a stat. Elite centers win 55%+ of their draws.",
        "soccer": "Like the center circle at kickoff - only one team's players inside initially.",
        "nba": "Like the tip-off circle - where the jump ball happens.",
        "nfl": "Like the coin toss spot - ceremonial start location.",
        "mlb": "Like home plate before the first pitch."
    },
    "faceoff_circle_end": {
        "name": "End Zone Face-off Circles",
        "description": "The two circles in each end zone (4 total), 30 feet in diameter. Face-offs here after icings, penalties, and stoppages in the zone.",
        "purpose": "Face-offs in your defensive zone are dangerous - the opponent has good scoring position. Face-offs in offensive zone are opportunities!",
        "fun_fact": "After an icing, the offending team cannot change lines, giving the opponent fresh legs for the face-off.",
        "soccer": "Like taking a corner kick vs defending one - position matters hugely.",
        "nba": "Like an inbound play under your own basket vs the opponent's.",
        "nfl": "Like starting a drive at your 5-yard line vs the opponent's 5.",
        "mlb": "Like batting with bases loaded vs pitching with bases loaded."
    },
    "goal_line": {
        "name": "Goal Line",
        "description": "The red line that runs across the width of the rink at each end, passing through the goal.",
        "purpose": "The puck must FULLY cross this line inside the goal posts for it to count as a goal. Also used for icing calls.",
        "fun_fact": "Modern NHL arenas have cameras in the goal posts and crossbar to help determine if the puck crossed the line.",
        "soccer": "Like the goal line in soccer - the puck must completely cross just like the ball.",
        "nba": "Like the baseline - out of bounds and scoring boundary.",
        "nfl": "Like the goal line - must break the plane to score.",
        "mlb": "Like home plate - cross it to score a run."
    },
    "trapezoid": {
        "name": "Trapezoid",
        "description": "The trapezoid-shaped area behind each goal where goalies ARE allowed to play the puck.",
        "purpose": "Goalies can only play the puck in the crease or in the trapezoid. Playing it elsewhere is a delay of game penalty.",
        "fun_fact": "Called the 'Martin Brodeur Rule' - added in 2005 to limit his puck-handling which was considered too dominant.",
        "soccer": "Goalies have the whole box - hockey restricts them to this zone plus the crease.",
        "nba": "No equivalent - hockey goalies have unique territorial restrictions.",
        "nfl": "Like a kicker/punter's operating zone - specialized player, specialized space.",
        "mlb": "Like the catcher's box - defined area for a specialized defensive player."
    },
    "boards": {
        "name": "Boards",
        "description": "The 42-inch high walls surrounding the ice. Made of fiberglass and topped with protective glass/netting.",
        "purpose": "Keep the puck (and players) in play. Players use boards strategically to bank passes and battle for pucks.",
        "fun_fact": "Board battles are a key part of hockey. Physical players who excel along the boards are called 'power forwards.'",
        "soccer": "No equivalent - soccer has touchlines where the ball goes out of play.",
        "nba": "Like the baseline/sidelines but you CAN'T go out - the wall keeps play alive.",
        "nfl": "Like if the sidelines were walls you could bounce off of.",
        "mlb": "Like the outfield wall - balls (pucks) play off it and stay live."
    },
    "bench": {
        "name": "Players' Bench",
        "description": "Where each team's players sit when not on the ice. Located on one side of the neutral zone.",
        "purpose": "Players substitute on-the-fly here during play! No stoppages needed. Usually 5 forwards and 4 defensemen waiting.",
        "fun_fact": "Line changes happen every 30-45 seconds. Getting caught on a 'long shift' is exhausting - shifts over 90 seconds are brutal.",
        "soccer": "Like the technical area but subs happen DURING play, not just at stoppages.",
        "nba": "Like the bench but subs happen freely during live action.",
        "nfl": "Like the sideline but imagine if you could sub during the play.",
        "mlb": "Like the dugout - where position players wait their turn."
    },
    "penalty_box": {
        "name": "Penalty Box",
        "description": "The area where players serve penalty time. Also called 'the sin bin.' Each team has one, across from their bench.",
        "purpose": "When you commit a penalty, you sit here for 2-5 minutes while your team plays short-handed (power play for opponents).",
        "fun_fact": "There's a penalty box attendant who opens and closes the door. Players have been known to chat with them during long penalties!",
        "soccer": "No equivalent - soccer uses cards and sends players off entirely.",
        "nba": "Like fouling out but it's temporary and you come back.",
        "nfl": "Like an ejection but just for a few minutes.",
        "mlb": "Like being in the dugout after an ejection - but you get to return."
    },
    "slot": {
        "name": "The Slot",
        "description": "The area directly in front of the goal, between the face-off circles. Prime scoring territory.",
        "purpose": "Most goals are scored from here! Teams fight hard to get the puck into the slot and fight hard to keep it out.",
        "fun_fact": "Goals scored from the slot have the highest percentage. Coaches always talk about 'getting to the dirty areas' - this is it.",
        "soccer": "Like the space right in front of goal - the danger zone.",
        "nba": "Like the paint/key area - highest percentage shots.",
        "nfl": "Like goal-line plays - high-percentage scoring territory.",
        "mlb": "Like having a hanging curveball - prime opportunity to score."
    },
    "point": {
        "name": "The Point",
        "description": "The area just inside the offensive blue line, usually manned by defensemen during offensive pressure.",
        "purpose": "Defensemen at the point take slap shots, keep pucks in the zone, and quarterback the power play.",
        "fun_fact": "Point shots often aim to get deflected or screened. A clean 'point shot' through traffic is a classic way to score.",
        "soccer": "Like a deep-lying playmaker position - controlling play from behind.",
        "nba": "Like the point guard position at the top of the key.",
        "nfl": "Like the quarterback position - orchestrating from behind the play.",
        "mlb": "Like a pitcher controlling the game from the mound."
    },
    "hash_marks": {
        "name": "Hash Marks",
        "description": "The small lines inside the face-off circles where players must line up for a face-off.",
        "purpose": "Players taking the face-off must have skates on or inside the hash marks. Everyone else must stay outside the circle.",
        "fun_fact": "Face-off violations (moving early) result in being kicked out. Another player must take the draw.",
        "soccer": "Like the penalty spot - precise location for a set piece.",
        "nba": "Like the free throw lane marks - defines where players can stand.",
        "nfl": "Like the hash marks on the field marking yard lines.",
        "mlb": "Like the batter's box lines - you must stay within them."
    }
}

# =============================================================================
# HOCKEY DICTIONARY - Comprehensive Term Definitions
# =============================================================================

HOCKEY_DICTIONARY = {
    # Game Structure
    "period": {
        "definition": "One of three 20-minute segments of a hockey game. Unlike soccer halves or basketball quarters, hockey has 3 periods.",
        "category": "game_structure"
    },
    "intermission": {
        "definition": "The 18-minute break between periods. Used to resurface the ice with a Zamboni.",
        "category": "game_structure"
    },
    "regulation": {
        "definition": "The standard 60 minutes of play (3 periods). If tied after regulation, the game goes to overtime.",
        "category": "game_structure"
    },
    "overtime": {
        "definition": "Extra period(s) played if tied after regulation. Regular season: 5-minute 3-on-3. Playoffs: 20-minute 5-on-5 until someone scores.",
        "category": "game_structure"
    },
    "shootout": {
        "definition": "If still tied after overtime in regular season, teams alternate penalty shots. Best of 3, then sudden death.",
        "category": "game_structure"
    },

    # Rink & Locations
    "rink": {
        "definition": "The ice surface where hockey is played. NHL rinks are 200 feet long by 85 feet wide.",
        "category": "rink"
    },
    "crease": {
        "definition": "The blue painted area directly in front of the goal. The goalie's protected zone.",
        "category": "rink"
    },
    "blue_line": {
        "definition": "The lines that divide the rink into three zones (defensive, neutral, offensive). Key for offside calls.",
        "category": "rink"
    },
    "red_line": {
        "definition": "The center line dividing the rink in half. Also called center ice.",
        "category": "rink"
    },
    "faceoff_circle": {
        "definition": "The circles where faceoffs take place. There are 9 total - 2 in each end zone, 4 in neutral zone, 1 at center.",
        "category": "rink"
    },
    "slot": {
        "definition": "The prime scoring area between the faceoff circles in front of the net. High-danger zone.",
        "category": "rink"
    },
    "point": {
        "definition": "The area just inside the blue line where defensemen position on offense. 'Point shot' comes from here.",
        "category": "rink"
    },
    "boards": {
        "definition": "The walls surrounding the ice. Players are frequently checked 'into the boards.'",
        "category": "rink"
    },
    "glass": {
        "definition": "The plexiglass panels above the boards that protect fans while allowing visibility.",
        "category": "rink"
    },
    "corner": {
        "definition": "The rounded areas where the boards meet behind the goals. Lots of puck battles happen here.",
        "category": "rink"
    },
    "trapezoid": {
        "definition": "The area behind the goal where goalies CAN play the puck. Outside it, they cannot (post-Brodeur rule).",
        "category": "rink"
    },

    # Player Positions
    "center": {
        "definition": "The middle forward who takes faceoffs and plays in the middle of the ice. Often the most complete forward.",
        "category": "positions"
    },
    "winger": {
        "definition": "The forwards who play on the left or right side. Usually responsible for their side of the ice.",
        "category": "positions"
    },
    "defenseman": {
        "definition": "The two players who primarily defend and start plays from the back. Also called 'D-men' or 'blueliners.'",
        "category": "positions"
    },
    "goaltender": {
        "definition": "The player who guards the net. Also called goalie, netminder, or keeper. Only one on ice at a time.",
        "category": "positions"
    },
    "forward": {
        "definition": "Collective term for centers and wingers - the offensive players. Three forwards on ice normally.",
        "category": "positions"
    },

    # Team Structure
    "line": {
        "definition": "A group of forwards who play together. Teams typically have 4 lines of 3 forwards each.",
        "category": "team"
    },
    "first_line": {
        "definition": "The top scoring line with the best offensive players. Gets the most ice time and key situations.",
        "category": "team"
    },
    "fourth_line": {
        "definition": "The checking/energy line. Usually physical players who forecheck hard and play limited minutes.",
        "category": "team"
    },
    "pairing": {
        "definition": "Two defensemen who play together. Teams have 3 defensive pairings.",
        "category": "team"
    },
    "top_pairing": {
        "definition": "The best two defensemen who play the most minutes and toughest matchups.",
        "category": "team"
    },
    "healthy_scratch": {
        "definition": "A player in the lineup but not playing that game. Teams dress 20 players but roster is 23.",
        "category": "team"
    },
    "taxi_squad": {
        "definition": "Reserve players who practice with the team but aren't on the active roster.",
        "category": "team"
    },

    # Gameplay Actions
    "faceoff": {
        "definition": "How play begins - the ref drops the puck between two opposing centers who try to win possession.",
        "category": "gameplay"
    },
    "line_change": {
        "definition": "Substituting players during play or stoppages. Hockey has unlimited subs that happen constantly.",
        "category": "gameplay"
    },
    "shift": {
        "definition": "One stint on the ice before changing. Usually 30-60 seconds due to the sport's intensity.",
        "category": "gameplay"
    },
    "forecheck": {
        "definition": "Pressuring the opponent in their defensive zone to force turnovers. Aggressive offensive tactic.",
        "category": "gameplay"
    },
    "backcheck": {
        "definition": "Forwards skating back to help defend after losing the puck. Shows work ethic.",
        "category": "gameplay"
    },
    "dump_and_chase": {
        "definition": "Shooting the puck into the offensive zone and chasing it, rather than carrying it in.",
        "category": "gameplay"
    },
    "cycling": {
        "definition": "Moving the puck along the boards in the offensive zone to maintain possession and create chances.",
        "category": "gameplay"
    },
    "zone_entry": {
        "definition": "How you get the puck into the offensive zone - carry it, pass it, or dump it.",
        "category": "gameplay"
    },
    "breakout": {
        "definition": "The play to move the puck out of your defensive zone and start offense.",
        "category": "gameplay"
    },
    "neutral_zone_trap": {
        "definition": "A defensive system that clogs the neutral zone to prevent zone entries. Boring but effective.",
        "category": "gameplay"
    },

    # Shots & Scoring
    "slap_shot": {
        "definition": "A powerful shot with a big wind-up. Can reach 100+ mph but takes time to execute.",
        "category": "shots"
    },
    "wrist_shot": {
        "definition": "A quick, accurate shot using wrist movement. Most common shot type.",
        "category": "shots"
    },
    "snap_shot": {
        "definition": "Between a slap shot and wrist shot - quicker than slap, harder than wrist.",
        "category": "shots"
    },
    "backhand": {
        "definition": "A shot or pass from the backhand side of the stick. Harder to control but deceptive.",
        "category": "shots"
    },
    "one_timer": {
        "definition": "Shooting directly from a pass without stopping the puck. Requires perfect timing.",
        "category": "shots"
    },
    "tip_in": {
        "definition": "Deflecting a shot with your stick to redirect it into the net.",
        "category": "shots"
    },
    "rebound": {
        "definition": "When the goalie stops a shot but can't control it, leaving the puck loose. Second chance opportunity.",
        "category": "shots"
    },
    "screen": {
        "definition": "Standing in front of the goalie to block their view of the shot. Legal if not in crease.",
        "category": "shots"
    },
    "five_hole": {
        "definition": "The space between the goalie's legs. One of the five 'holes' to shoot at.",
        "category": "shots"
    },
    "top_shelf": {
        "definition": "The upper part of the net, 'where grandma keeps the cookies.' Hard for goalies to reach.",
        "category": "shots"
    },
    "bar_down": {
        "definition": "A shot that hits the crossbar and goes down into the net. Considered a perfect shot.",
        "category": "shots"
    },

    # Moves & Skills
    "deke": {
        "definition": "A fake or move to deceive the defender or goalie. Short for 'decoy.'",
        "category": "skills"
    },
    "dangle": {
        "definition": "Fancy stickhandling to beat defenders. 'He dangled through three guys.'",
        "category": "skills"
    },
    "toe_drag": {
        "definition": "Pulling the puck back with the toe of the stick blade. Classic move to create space.",
        "category": "skills"
    },
    "sauce": {
        "definition": "A pass that goes airborne (saucer-like) over sticks or players. Also called a saucer pass.",
        "category": "skills"
    },
    "no_look_pass": {
        "definition": "Passing without looking at your target to deceive defenders.",
        "category": "skills"
    },
    "between_the_legs": {
        "definition": "Either a pass, shot, or deke that goes through your own legs. Showtime move.",
        "category": "skills"
    },
    "spin_o_rama": {
        "definition": "A full 360° spin move while controlling the puck. Highlight reel material.",
        "category": "skills"
    },
    "michigan": {
        "definition": "The lacrosse-style goal where you scoop the puck on your blade and score from behind the net.",
        "category": "skills"
    },

    # Checking & Physical Play
    "body_check": {
        "definition": "Using your body to legally hit an opponent who has the puck. Must not target head.",
        "category": "physical"
    },
    "hip_check": {
        "definition": "Lowering your body and hitting opponent with your hip. High risk, high reward.",
        "category": "physical"
    },
    "open_ice_hit": {
        "definition": "A body check in open ice rather than along the boards. Often the biggest hits.",
        "category": "physical"
    },
    "finishing_your_check": {
        "definition": "Completing your hit even after the player has passed the puck. Legal but annoying.",
        "category": "physical"
    },
    "boarding": {
        "definition": "An illegal hit that drives an opponent violently into the boards. 2-5 minute penalty.",
        "category": "physical"
    },
    "charging": {
        "definition": "Taking too many strides or jumping before delivering a check. Illegal.",
        "category": "physical"
    },
    "fighting": {
        "definition": "Dropping gloves and fighting an opponent. Results in 5-minute major penalty for both players.",
        "category": "physical"
    },
    "enforcer": {
        "definition": "A player whose role includes fighting and protecting teammates. Rare in modern NHL.",
        "category": "physical"
    },
    "goon": {
        "definition": "A player who primarily fights and plays physically. Sometimes derogatory term.",
        "category": "physical"
    },

    # Penalties
    "minor_penalty": {
        "definition": "A 2-minute penalty for infractions like tripping, hooking, slashing. Team plays short-handed.",
        "category": "penalties"
    },
    "major_penalty": {
        "definition": "A 5-minute penalty for serious infractions like fighting or intent to injure.",
        "category": "penalties"
    },
    "double_minor": {
        "definition": "A 4-minute penalty, usually for high-sticking that draws blood.",
        "category": "penalties"
    },
    "misconduct": {
        "definition": "A 10-minute penalty where player sits but team doesn't play short-handed.",
        "category": "penalties"
    },
    "game_misconduct": {
        "definition": "Player is ejected from the game. Team isn't necessarily short-handed.",
        "category": "penalties"
    },
    "match_penalty": {
        "definition": "Ejection plus potential suspension review. For deliberate attempt to injure.",
        "category": "penalties"
    },
    "tripping": {
        "definition": "Using stick, arm, or leg to knock an opponent down. 2-minute minor.",
        "category": "penalties"
    },
    "hooking": {
        "definition": "Using the stick blade to impede an opponent. 2-minute minor.",
        "category": "penalties"
    },
    "slashing": {
        "definition": "Swinging your stick at an opponent. 2-minute minor, or more if injury.",
        "category": "penalties"
    },
    "holding": {
        "definition": "Grabbing an opponent with hands or stick. 2-minute minor.",
        "category": "penalties"
    },
    "interference": {
        "definition": "Impeding a player who doesn't have the puck. 2-minute minor.",
        "category": "penalties"
    },
    "roughing": {
        "definition": "Punching or rough play that doesn't rise to fighting. 2-minute minor.",
        "category": "penalties"
    },
    "high_sticking": {
        "definition": "Hitting an opponent with your stick above the shoulders. 2 or 4 minutes.",
        "category": "penalties"
    },
    "cross_checking": {
        "definition": "Hitting opponent with the shaft of your stick while both hands are on it.",
        "category": "penalties"
    },
    "delay_of_game": {
        "definition": "Various infractions that delay play, like shooting puck over glass from defensive zone.",
        "category": "penalties"
    },
    "too_many_men": {
        "definition": "Having more than 6 players on the ice. Bench minor penalty.",
        "category": "penalties"
    },
    "embellishment": {
        "definition": "Exaggerating contact to draw a penalty. Can result in offsetting minors.",
        "category": "penalties"
    },

    # Special Teams
    "power_play": {
        "definition": "When your team has more players due to opponent's penalty. Usually 5-on-4.",
        "category": "special_teams"
    },
    "penalty_kill": {
        "definition": "Playing short-handed while a teammate serves a penalty. Defensive mode.",
        "category": "special_teams"
    },
    "man_advantage": {
        "definition": "Another term for power play - you have more men on the ice.",
        "category": "special_teams"
    },
    "five_on_four": {
        "definition": "Standard power play situation. Can also be 5-on-3 with two penalties.",
        "category": "special_teams"
    },
    "four_on_four": {
        "definition": "Both teams have a player in the box. More open ice, exciting hockey.",
        "category": "special_teams"
    },
    "pp_unit": {
        "definition": "The 5 players on the ice for power play. Teams have 2 units that rotate.",
        "category": "special_teams"
    },
    "pk_unit": {
        "definition": "The 4 players on ice during penalty kill. Usually defensive specialists.",
        "category": "special_teams"
    },
    "box": {
        "definition": "The penalty kill formation - 4 players form a box/diamond shape.",
        "category": "special_teams"
    },
    "umbrella": {
        "definition": "A power play formation with 3 players high and 2 low.",
        "category": "special_teams"
    },

    # Rules & Situations
    "offside": {
        "definition": "When an attacking player enters the offensive zone before the puck. Play is stopped.",
        "category": "rules"
    },
    "icing": {
        "definition": "Shooting the puck from your side past the opponent's goal line without anyone touching it.",
        "category": "rules"
    },
    "goalie_interference": {
        "definition": "Illegal contact with the goalie that prevents them from making a save.",
        "category": "rules"
    },
    "hand_pass": {
        "definition": "Passing the puck with your hand is only legal in the defensive zone.",
        "category": "rules"
    },
    "high_touch": {
        "definition": "Directing the puck with a stick above the crossbar. Goal disallowed.",
        "category": "rules"
    },
    "kicking": {
        "definition": "You can't kick the puck into the net. Distinct kicking motion = no goal.",
        "category": "rules"
    },
    "goalie_pulled": {
        "definition": "Removing the goalie for an extra attacker. Done when trailing late in games.",
        "category": "rules"
    },
    "delayed_penalty": {
        "definition": "When a penalty is called but the non-offending team has the puck. Play continues until they lose it.",
        "category": "rules"
    },
    "penalty_shot": {
        "definition": "A free breakaway awarded when a scoring chance is illegally taken away.",
        "category": "rules"
    },

    # Achievements
    "hat_trick": {
        "definition": "Scoring 3 goals in one game. Fans throw hats on the ice to celebrate.",
        "category": "achievements"
    },
    "gordie_howe_hat_trick": {
        "definition": "A goal, an assist, AND a fight in one game. Named after the legendary Red Wing.",
        "category": "achievements"
    },
    "natural_hat_trick": {
        "definition": "Three consecutive goals by the same player, no one else scoring in between.",
        "category": "achievements"
    },
    "shutout": {
        "definition": "When a goalie allows zero goals for the entire game.",
        "category": "achievements"
    },
    "empty_netter": {
        "definition": "A goal scored into an empty net after the opposing goalie is pulled.",
        "category": "achievements"
    },
    "game_winning_goal": {
        "definition": "The goal that gives your team one more than the opponent's final total.",
        "category": "achievements"
    },
    "overtime_winner": {
        "definition": "The goal that wins the game in overtime. Walk-off equivalent.",
        "category": "achievements"
    },
    "first_nhl_goal": {
        "definition": "A player's first career NHL goal. Teammates usually give them the puck.",
        "category": "achievements"
    },

    # Goalie-Specific
    "butterfly": {
        "definition": "Goalie drops to knees with pads flared out to cover low shots. Modern standard style.",
        "category": "goalie"
    },
    "glove_save": {
        "definition": "Catching the puck with the catching glove (worn on non-stick hand).",
        "category": "goalie"
    },
    "blocker": {
        "definition": "The rectangular pad on the goalie's stick hand. Used to deflect shots.",
        "category": "goalie"
    },
    "pad_save": {
        "definition": "Stopping the puck with the leg pads. Most common save type.",
        "category": "goalie"
    },
    "poke_check": {
        "definition": "Goalie lunges forward to knock the puck away from a shooter.",
        "category": "goalie"
    },
    "desperation_save": {
        "definition": "An athletic, scrambling save when out of position. Often highlight-reel worthy.",
        "category": "goalie"
    },
    "stacking_the_pads": {
        "definition": "Sliding across with pads stacked on top of each other. Old school move.",
        "category": "goalie"
    },
    "playing_the_puck": {
        "definition": "When the goalie leaves the crease to pass or clear the puck. Risky but helpful.",
        "category": "goalie"
    },

    # Slang & Culture
    "biscuit": {
        "definition": "Slang for the puck. 'Put the biscuit in the basket.'",
        "category": "slang"
    },
    "barn": {
        "definition": "Slang for the arena/rink. 'Nice barn you got here.'",
        "category": "slang"
    },
    "beauty": {
        "definition": "A great player or a great goal. 'What a beauty!'",
        "category": "slang"
    },
    "celly": {
        "definition": "Goal celebration. 'Sick celly, bro.'",
        "category": "slang"
    },
    "clapper": {
        "definition": "A slap shot. From the clapping sound of stick hitting ice.",
        "category": "slang"
    },
    "snipe": {
        "definition": "A perfectly placed shot, usually top corner. 'Absolute snipe.'",
        "category": "slang"
    },
    "twig": {
        "definition": "A hockey stick. 'Nice twig.'",
        "category": "slang"
    },
    "bucket": {
        "definition": "A helmet. 'Lost his bucket on that hit.'",
        "category": "slang"
    },
    "sweater": {
        "definition": "The hockey jersey. Traditional Canadian term.",
        "category": "slang"
    },
    "chirping": {
        "definition": "Trash talking opponents. 'He was chirping all game.'",
        "category": "slang"
    },
    "wheel": {
        "definition": "To skate fast. 'He can really wheel.'",
        "category": "slang"
    },
    "pigeon": {
        "definition": "A player who scores garbage goals or rides better players' coattails.",
        "category": "slang"
    },
    "plug": {
        "definition": "A bad player. AHL-caliber guy in the NHL.",
        "category": "slang"
    },
    "rocket": {
        "definition": "A very attractive person. 'His wife's a rocket.'",
        "category": "slang"
    },
    "tendy": {
        "definition": "Short for goaltender. 'Our tendy stood on his head.'",
        "category": "slang"
    },
    "silky": {
        "definition": "Smooth hands/skills. 'Silky mitts on that kid.'",
        "category": "slang"
    },
    "lettuce": {
        "definition": "Hair flowing out of the helmet. 'Nice lettuce, buddy.'",
        "category": "slang"
    },
    "flow": {
        "definition": "Same as lettuce - good hockey hair.",
        "category": "slang"
    }
}

# =============================================================================
# HOCKEY CONCEPTS KNOWLEDGE BASE
# =============================================================================

HOCKEY_CONCEPTS = {
    "power play": {
        "definition": "When one team has more players on the ice because the opponent committed a penalty. Typically 5 players vs 4 (or sometimes 5v3).",
        "duration": "Usually 2 minutes for minor penalties, 5 minutes for major penalties.",
        "soccer": {
            "analogy": "Red Card Advantage",
            "explanation": "It's like when the opponent gets a red card and plays with 10 men - except in hockey it's only temporary (2-5 minutes). Your team has a massive advantage to attack and score.",
            "key_difference": "In soccer a red card lasts the whole game. In hockey, penalties expire or end when you score."
        },
        "nba": {
            "analogy": "Opponent in Foul Trouble",
            "explanation": "Imagine if a team's best defender fouled out, but only for 2 minutes. You'd attack aggressively while they're short-handed. Teams run set plays specifically designed for power plays.",
            "key_difference": "In the NBA you lose the player permanently when they foul out. Hockey penalties are temporary."
        },
        "nfl": {
            "analogy": "Illegal Formation / Free Play",
            "explanation": "It's like when the defense jumps offsides and the QB gets a 'free play' - you have a major advantage to take a shot. Except this 'free play' lasts 2 minutes.",
            "key_difference": "NFL free plays are one snap. Hockey power plays can last several minutes of sustained pressure."
        },
        "mlb": {
            "analogy": "Bases Loaded, No Outs",
            "explanation": "That feeling of anticipation when your team has bases loaded with no outs - you SHOULD score here. Power plays are prime scoring opportunities that teams practice extensively.",
            "key_difference": "Bases loaded is situational luck. Power plays are earned by drawing penalties through aggressive play."
        },
        "diagram": "power_play.svg"
    },

    "penalty kill": {
        "definition": "When your team is SHORT-handed (has fewer players) due to a penalty. You're trying to survive without giving up a goal.",
        "duration": "2-5 minutes depending on the penalty.",
        "soccer": {
            "analogy": "Playing Down a Man",
            "explanation": "Like defending with 10 men after a red card - you pack your defense, limit chances, and try to survive. Some teams are so good at this they actually score 'short-handed goals'.",
            "key_difference": "It's temporary, and you can actually score while short-handed (called a 'shorty')."
        },
        "nba": {
            "analogy": "Zone Defense Under Pressure",
            "explanation": "Like running a 2-3 zone when you're outmatched - clog the lane, protect the paint, force tough outside shots. PK units are specialists at defensive positioning.",
            "key_difference": "You're literally missing a player, not just changing defensive scheme."
        },
        "nfl": {
            "analogy": "Prevent Defense",
            "explanation": "Similar mindset to prevent defense - bend but don't break. Give up some zone entries but protect the dangerous areas. Time is your friend.",
            "key_difference": "You're actually playing 4 vs 5, not just dropping into conservative coverage."
        },
        "mlb": {
            "analogy": "Infield In with Bases Loaded",
            "explanation": "That high-pressure defensive situation where you're trying to prevent a run. Everyone's in position, communication is critical, one mistake is costly.",
            "key_difference": "Baseball is one play at a time. Penalty kill is 2 minutes of sustained pressure."
        },
        "diagram": "penalty_kill.svg"
    },

    "icing": {
        "definition": "When a team shoots the puck from their side of center ice all the way past the opponent's goal line without anyone touching it. Results in a faceoff in the offending team's zone.",
        "soccer": {
            "analogy": "Deliberate Ball Out of Play",
            "explanation": "Like a goalkeeper punting the ball out of bounds under pressure - it relieves immediate pressure but gives possession back to the opponent in a dangerous area.",
            "key_difference": "Icing isn't really a foul, just a rule to prevent teams from mindlessly clearing the puck."
        },
        "nba": {
            "analogy": "Backcourt Violation Reset",
            "explanation": "Imagine if you could throw the ball to the other end of the court to relieve pressure, but then had to defend right in front of your basket. That's icing.",
            "key_difference": "Icing is legal but has consequences. Backcourt violation is a turnover."
        },
        "nfl": {
            "analogy": "Intentional Grounding",
            "explanation": "When a QB throws the ball away under pressure to avoid a sack - you avoided immediate danger but there's a penalty. Icing is similar but without the yardage loss.",
            "key_difference": "Icing is legal. You just lose the ability to change players and face-off in your zone."
        },
        "mlb": {
            "analogy": "Intentional Walk",
            "explanation": "A strategic choice to avoid a bad situation, but it puts runners in scoring position. You're trading one problem for another.",
            "key_difference": "Icing is usually desperation, not strategy."
        },
        "diagram": "icing.svg"
    },

    "offside": {
        "definition": "A player cannot enter the attacking zone (cross the blue line) before the puck does. The puck must always enter the zone first.",
        "soccer": {
            "analogy": "Offside Rule",
            "explanation": "Very similar concept! Except instead of being behind the last defender, you need to be behind an invisible line (the blue line). No 'offside trap' though - it's purely based on the blue line.",
            "key_difference": "Hockey offside is simpler - just one line to watch. Soccer offside depends on defender positions."
        },
        "nba": {
            "analogy": "Backcourt Violation (Reversed)",
            "explanation": "Like backcourt violation, but for the attacking zone. Once the puck is in the zone, players can move freely. If the puck leaves, everyone must exit before it re-enters.",
            "key_difference": "NBA backcourt is about going backwards. Hockey offside is about going forward too early."
        },
        "nfl": {
            "analogy": "False Start / Offsides",
            "explanation": "Like lining up offsides before the snap - you're in the wrong place at the wrong time. Play is whistled dead and resets.",
            "key_difference": "NFL offsides is about the line of scrimmage. Hockey has a permanent 'blue line' that never moves."
        },
        "mlb": {
            "analogy": "Leading Off Too Early",
            "explanation": "Like a runner leaving the base before the pitch in Little League - you're getting ahead of the play. Must wait for the puck to enter the zone.",
            "key_difference": "Baseball leads are about timing the pitch. Hockey offside is purely positional."
        },
        "diagram": "offside.svg"
    },

    "goalie pull": {
        "definition": "When a team removes their goaltender for an extra skater, usually when losing late in the game. Creates a 6-on-5 advantage but leaves an empty net.",
        "soccer": {
            "analogy": "Goalkeeper Joining Attack",
            "explanation": "Like when a goalkeeper comes up for a corner kick in stoppage time. You're desperate, you need a goal, so you add an extra attacker at huge risk. If you lose the puck, they can score on an empty net from anywhere.",
            "key_difference": "Soccer goalies only come up for set pieces. Hockey teams pull goalies for extended periods (1-2 minutes)."
        },
        "nba": {
            "analogy": "Intentional Fouling + Full Court Press",
            "explanation": "Similar desperation tactics when down late. You're taking a huge risk (giving free throws / empty net) for a chance to get back in the game.",
            "key_difference": "Fouling gives opponent free throws. Pulling goalie gives opponent an easy target."
        },
        "nfl": {
            "analogy": "Hail Mary / Onside Kick",
            "explanation": "Like going for an onside kick or Hail Mary - you're in desperation mode. The risk is enormous but you have no choice. Empty net goals are the equivalent of returning an onside kick for a TD.",
            "key_difference": "Hail Mary is one play. Pulled goalie situations can last several minutes."
        },
        "mlb": {
            "analogy": "Pinch Hitter for Pitcher",
            "explanation": "Trading defense for offense. You're giving up your best defensive player (goalie/pitcher) for extra offensive power when you absolutely need a run/goal.",
            "key_difference": "Pinch hitter is permanent. Pulled goalie can come back if you gain possession."
        },
        "diagram": "goalie_pull.svg"
    },

    "line change": {
        "definition": "Substituting players while play is ongoing. Hockey is the only major sport with unlimited, on-the-fly substitutions.",
        "soccer": {
            "analogy": "Rolling Substitutions",
            "explanation": "Imagine if soccer had unlimited subs AND you could swap players without stopping play. That's hockey. Players typically play 45-second 'shifts' before changing.",
            "key_difference": "Soccer has 3-5 permanent subs. Hockey has unlimited changes happening constantly."
        },
        "nba": {
            "analogy": "Constant Rotation",
            "explanation": "Like how NBA teams rotate players, but imagine if you could sub without a stoppage. 'Lines' are like 5-man units that play together. Fresh legs are crucial.",
            "key_difference": "NBA subs only during dead balls. Hockey subs happen live during play."
        },
        "nfl": {
            "analogy": "Special Teams Units",
            "explanation": "Think of how NFL has offense, defense, special teams. Hockey has multiple 'lines' (units) that rotate constantly. First line is your best, fourth line is energy/defense.",
            "key_difference": "NFL changes between plays. Hockey changes during live action."
        },
        "mlb": {
            "analogy": "Pitching Changes + Defensive Shifts",
            "explanation": "The strategic thinking is similar to bullpen management - fresh arms/legs are important. But in hockey, you're changing multiple players every 45 seconds.",
            "key_difference": "Baseball subs are permanent and rare. Hockey subs are temporary and constant."
        },
        "diagram": "line_change.svg"
    },

    "hat trick": {
        "definition": "When a player scores three goals in a single game. Fans traditionally throw hats onto the ice to celebrate.",
        "soccer": {
            "analogy": "Hat Trick",
            "explanation": "Exactly the same! Three goals by one player in one match. The term actually originated from cricket and is used in both sports identically.",
            "key_difference": "None - it's the same thing!"
        },
        "nba": {
            "analogy": "Triple Double",
            "explanation": "Similar level of individual achievement. A hat trick is as celebrated in hockey as a triple-double in basketball. Both show complete dominance.",
            "key_difference": "Triple-double is about versatility. Hat trick is pure scoring prowess."
        },
        "nfl": {
            "analogy": "3 Touchdown Game",
            "explanation": "When a receiver or running back scores 3 TDs in a game - it's a standout individual performance that often wins the game.",
            "key_difference": "3 TDs is impressive but not uncommon. Hat tricks are rarer and more celebrated."
        },
        "mlb": {
            "analogy": "Hitting for the Cycle",
            "explanation": "A rare individual achievement that fans remember. Hat tricks are celebrated with fans throwing hats on the ice - a unique tradition.",
            "key_difference": "Cycle is about variety of hits. Hat trick is three of the same thing (goals)."
        },
        "diagram": "hat_trick.svg"
    },

    "checking": {
        "definition": "Using your body to hit an opponent to separate them from the puck or disrupt their play. Legal hits must target the body (not head) and the player must have the puck.",
        "soccer": {
            "analogy": "Shoulder-to-Shoulder Challenge",
            "explanation": "Like an aggressive shoulder challenge, but way more intense. Imagine if soccer allowed you to fully body-check someone off the ball (when they have it). That's hockey.",
            "key_difference": "Soccer challenges are about getting the ball. Hockey checks are about physical dominance."
        },
        "nba": {
            "analogy": "Hard Foul / Flagrant",
            "explanation": "What would be a flagrant foul in basketball is often a legal, celebrated hit in hockey. 'Finishing your check' is considered good, tough hockey.",
            "key_difference": "NBA flagrants are punished. Hockey checks (when clean) are encouraged."
        },
        "nfl": {
            "analogy": "Open Field Tackle",
            "explanation": "Very similar to tackling! Except in hockey the player gets back up and the play continues. Defensemen are like linebackers - physical presence matters.",
            "key_difference": "NFL tackles end the play. Hockey checks happen and play continues."
        },
        "mlb": {
            "analogy": "Home Plate Collision (Old Rules)",
            "explanation": "Remember when catchers could block the plate and runners could truck catchers? Hockey has that level of contact on every play.",
            "key_difference": "Baseball removed most contact. Hockey embraces it."
        },
        "diagram": "checking.svg"
    },

    "face-off": {
        "definition": "How play begins - the referee drops the puck between two opposing players who try to gain possession. Happens at start of periods, after goals, and after stoppages.",
        "soccer": {
            "analogy": "Kickoff / Drop Ball",
            "explanation": "Like a kickoff or drop ball to restart play. Winning the face-off gives your team immediate possession - it's a specialized skill some players excel at.",
            "key_difference": "Face-offs happen 50+ times per game. Soccer restarts are less frequent."
        },
        "nba": {
            "analogy": "Jump Ball / Tip-Off",
            "explanation": "Very similar to a tip-off! Two players compete for initial possession. Some players are 'face-off specialists' like how some centers are great at winning tips.",
            "key_difference": "Hockey face-offs happen after every stoppage, not just to start periods."
        },
        "nfl": {
            "analogy": "Snap + Line of Scrimmage",
            "explanation": "The battle at the face-off dot is like the battle at the line of scrimmage. Winning it gives your team an advantage. Losing it puts you on defense immediately.",
            "key_difference": "NFL snap gives the ball to one team. Face-off is a 50/50 battle."
        },
        "mlb": {
            "analogy": "First Pitch",
            "explanation": "Sets the tone for the at-bat/play. A won face-off in the offensive zone is like getting ahead in the count - immediate advantage.",
            "key_difference": "First pitch is pitcher vs batter. Face-off is player vs player."
        },
        "diagram": "faceoff.svg"
    },

    "overtime": {
        "definition": "If the game is tied after regulation, teams play sudden-death overtime. Regular season OT is 5 minutes of 3-on-3, then a shootout if still tied. Playoffs are full 5-on-5 periods until someone scores.",
        "soccer": {
            "analogy": "Extra Time + Penalties",
            "explanation": "Very similar! Regular season is like going to penalties quickly. Playoffs are like Champions League knockout rounds - keep playing until there's a winner, no matter how long.",
            "key_difference": "Hockey playoff OT can go for multiple extra periods. Soccer extra time is capped at 30 min."
        },
        "nba": {
            "analogy": "Overtime Periods",
            "explanation": "Similar concept - extra time to determine a winner. But playoff hockey OT is sudden death, so one goal ends it. The tension is incredible.",
            "key_difference": "NBA OT is a full 5 minutes. Hockey playoff OT is sudden death - one goal wins."
        },
        "nfl": {
            "analogy": "NFL Overtime",
            "explanation": "Playoff hockey OT is like if NFL overtime was truly sudden death - first score wins, no matter what. Can last for hours in marathon games.",
            "key_difference": "NHL playoff OT is pure sudden death. NFL OT has touchdown rules."
        },
        "mlb": {
            "analogy": "Extra Innings",
            "explanation": "The closest comparison! Like extra innings, playoff hockey OT goes until someone wins. Games can be legendary marathons.",
            "key_difference": "Hockey OT is sudden death. Baseball extra innings are full innings."
        },
        "diagram": "overtime.svg"
    },

    "the crease": {
        "definition": "The blue painted area in front of the goal. The goalie's protected territory - interfering with a goalie in the crease can disallow a goal.",
        "soccer": {
            "analogy": "Six-Yard Box",
            "explanation": "Like the six-yard box is the goalkeeper's domain. In hockey, you cannot interfere with the goalie in the crease or your goal may be disallowed.",
            "key_difference": "Hockey crease rules are stricter about contact with the goalie."
        },
        "nba": {
            "analogy": "Restricted Area",
            "explanation": "Like the restricted area under the basket - special rules apply. The goalie has rights in the crease similar to a defender's rights outside the restricted arc.",
            "key_difference": "NBA restricted area is about charges. Hockey crease is about goalie protection."
        },
        "nfl": {
            "analogy": "Quarterback in the Pocket",
            "explanation": "The goalie in the crease has protection like a QB in the pocket. Hitting them inappropriately will result in penalties or disallowed goals.",
            "key_difference": "QB protection ends after the throw. Goalie protection is constant."
        },
        "mlb": {
            "analogy": "Batter's Box",
            "explanation": "A designated area with specific rules. Just as batters have rights in the box, goalies have protection in the crease.",
            "key_difference": "Batter's box is for offense. Crease is defensive territory."
        },
        "diagram": "crease.svg"
    },

    "fighting": {
        "definition": "Unlike other sports, fighting is technically allowed in hockey with a 5-minute penalty. Fights often occur to protect teammates, change momentum, or enforce unwritten rules.",
        "soccer": {
            "analogy": "Protecting Your Teammate (Extreme)",
            "explanation": "Remember when players get in each other's faces after a hard tackle? In hockey, that can escalate to actual fighting - and both players just get 5-minute penalties.",
            "key_difference": "Soccer fights = red cards and suspensions. Hockey fights = 5 minutes in the 'penalty box'."
        },
        "nba": {
            "analogy": "Malice at the Palace (Legal)",
            "explanation": "Imagine if the Pistons-Pacers brawl was just... allowed. With rules. Hockey has 'enforcers' whose job is to protect star players through intimidation and fighting.",
            "key_difference": "NBA fights = ejections, fines, suspensions. Hockey fights = 5 minute timeout."
        },
        "nfl": {
            "analogy": "Defensive Intimidation",
            "explanation": "Like how defensive players talk trash and try to intimidate receivers. But in hockey, you can actually throw punches to enforce respect. It's a unique cultural element.",
            "key_difference": "NFL fighting = ejection. Hockey fighting is part of the game."
        },
        "mlb": {
            "analogy": "Bench-Clearing Brawl (Allowed)",
            "explanation": "Like a controlled bench-clearing brawl where two guys square off, fight, then sit in timeout. There are unwritten rules about when fighting is 'appropriate.'",
            "key_difference": "MLB brawls clear benches and cause chaos. Hockey fights are 1-on-1 with referees watching."
        },
        "diagram": "fighting.svg"
    }
}

# =============================================================================
# PLAYER COMPARISONS DATABASE
# =============================================================================

PLAYER_COMPARISONS = {
    "macklin celebrini": {
        "position": "Center",
        "team": "San Jose Sharks",
        "age": 19,
        "style": "Elite offensive talent, high hockey IQ, franchise cornerstone",
        "accolades": "#1 Overall Pick 2024, NCAA scoring leader",
        "soccer": {
            "player": "Jude Bellingham",
            "team": "Real Madrid",
            "explanation": "Both are teenage phenoms who immediately became franchise cornerstones. Bellingham won La Liga in his first season at 20; Celebrini is expected to transform the Sharks similarly. Both have elite vision, can score and create, and carry massive expectations."
        },
        "nba": {
            "player": "Victor Wembanyama",
            "team": "San Antonio Spurs",
            "explanation": "Both were #1 picks expected to transform struggling franchises. Generational talents drafted into rebuild situations. Celebrini, like Wemby, is already showing flashes of superstar potential in his rookie year."
        },
        "nfl": {
            "player": "Caleb Williams",
            "team": "Chicago Bears",
            "explanation": "Both are #1 overall picks chosen to be franchise saviors for struggling teams. Young, hyped quarterbacks/centers who carry the weight of turning around their organizations. Both have exceptional playmaking ability."
        },
        "mlb": {
            "player": "Jackson Holliday",
            "team": "Baltimore Orioles",
            "explanation": "Both are #1 overall picks who rose through the ranks as the most hyped prospects in their sport. Expected to be the face of their franchise for the next decade."
        }
    },

    "connor mcdavid": {
        "position": "Center",
        "team": "Edmonton Oilers",
        "age": 27,
        "style": "Fastest skater in NHL, elite scorer, best player in the world",
        "accolades": "4x Hart Trophy (MVP), 4x Art Ross (scoring leader)",
        "soccer": {
            "player": "Erling Haaland",
            "team": "Manchester City",
            "explanation": "Both are the undisputed best at their position. McDavid's speed and finishing is like Haaland's - when they have the puck/ball, it's almost always a goal chance. Dominant forces who make everything look effortless."
        },
        "nba": {
            "player": "LeBron James (Prime)",
            "team": "N/A",
            "explanation": "Best player of their generation, can single-handedly take over games, elite in every offensive category. McDavid is hockey's LeBron - transcendent talent that comes once in a generation."
        },
        "nfl": {
            "player": "Patrick Mahomes",
            "team": "Kansas City Chiefs",
            "explanation": "Both are the consensus best players in their sport RIGHT NOW. Can make plays nobody else can. Have that 'it factor' that makes you watch every play. Game-breaking talent."
        },
        "mlb": {
            "player": "Shohei Ohtani",
            "team": "Los Angeles Dodgers",
            "explanation": "Both are once-in-a-generation talents who do things nobody else can do. McDavid's skating speed and hands are as unique as Ohtani's two-way abilities. Transcendent."
        }
    },

    "sidney crosby": {
        "position": "Center",
        "team": "Pittsburgh Penguins",
        "age": 37,
        "style": "Two-way excellence, leadership, clutch performer",
        "accolades": "3x Stanley Cup Champion, 2x Hart Trophy, 2x Conn Smythe",
        "soccer": {
            "player": "Lionel Messi",
            "team": "Inter Miami",
            "explanation": "The GOAT comparison. Both are widely considered the greatest of their generation. Elite in every phase, clutch in big moments, multiple championships. Crosby is hockey's Messi."
        },
        "nba": {
            "player": "Tim Duncan",
            "team": "San Antonio Spurs (Retired)",
            "explanation": "Both are quiet, humble superstars who just WIN. Multiple championships, consistent excellence over decades, ultimate teammates. The 'boring' greatness that's actually incredible."
        },
        "nfl": {
            "player": "Tom Brady",
            "team": "Retired",
            "explanation": "Winner's mentality, multiple championships, clutch in the biggest moments. Both defined their era and will be in the GOAT conversation forever."
        },
        "mlb": {
            "player": "Derek Jeter",
            "team": "New York Yankees (Retired)",
            "explanation": "Captain, leader, multiple championships, clutch performer. Both are synonymous with winning and leadership. Class acts who represent their sport well."
        }
    },

    "alex ovechkin": {
        "position": "Left Wing",
        "team": "Washington Capitals",
        "age": 39,
        "style": "Pure goal scorer, lethal one-timer, power forward",
        "accolades": "All-time goal scoring leader chase, Stanley Cup Champion",
        "soccer": {
            "player": "Cristiano Ronaldo",
            "team": "Al-Nassr",
            "explanation": "GOAL SCORERS. Both are obsessed with scoring, have legendary shots, and are chasing all-time records. Ovechkin's one-timer is like Ronaldo's free kicks - iconic. Both have the drive to play forever."
        },
        "nba": {
            "player": "Kevin Durant",
            "team": "Phoenix Suns",
            "explanation": "Pure scorers who make it look effortless. When they want to score, there's nothing you can do. Ovechkin's release from the left circle is as automatic as KD's pull-up jumper."
        },
        "nfl": {
            "player": "Derrick Henry",
            "team": "Tennessee Titans",
            "explanation": "Power and scoring. Both are physical specimens who punish defenders and seem to get better with age. Ovechkin's physicality combined with scoring touch is like Henry's bruising style."
        },
        "mlb": {
            "player": "Albert Pujols",
            "team": "St. Louis Cardinals (Retired)",
            "explanation": "Chasing historic milestones late in career. Both are all-time great power producers who've maintained excellence into their late 30s/40s."
        }
    },

    "cale makar": {
        "position": "Defenseman",
        "team": "Colorado Avalanche",
        "age": 25,
        "style": "Elite offensive defenseman, elite skater, game-changer",
        "accolades": "Norris Trophy (Best D), Conn Smythe (Playoff MVP), Stanley Cup",
        "soccer": {
            "player": "Trent Alexander-Arnold",
            "team": "Liverpool",
            "explanation": "Offensive defensemen who redefine their position. Both are elite passers from the back who create as much offense as forwards. Game-changers from the defensive position."
        },
        "nba": {
            "player": "Draymond Green (Offensive Version)",
            "team": "Golden State Warriors",
            "explanation": "Elite defensive player who also runs the offense. Makar is like if Draymond could also score 25 points a game. Quarterback of the defense with elite vision."
        },
        "nfl": {
            "player": "Micah Parsons",
            "team": "Dallas Cowboys",
            "explanation": "Young, dynamic, game-changing defenders. Both can do everything - rush, cover, make plays all over the field/ice. Best at their position in their early 20s."
        },
        "mlb": {
            "player": "Mookie Betts",
            "team": "Los Angeles Dodgers",
            "explanation": "Elite defenders who also hit for power. Complete players who do everything at an elite level. No weaknesses in their game."
        }
    },

    "auston matthews": {
        "position": "Center",
        "team": "Toronto Maple Leafs",
        "age": 26,
        "style": "Elite goal scorer, lethal wrist shot, two-way center",
        "accolades": "60+ goals in a season, Maurice Richard Trophy (goals leader)",
        "soccer": {
            "player": "Harry Kane",
            "team": "Bayern Munich",
            "explanation": "Elite finishers who score at historic rates but haven't won the big one yet. Both are clinical goal scorers who carry massive market pressure (Toronto/England)."
        },
        "nba": {
            "player": "Damian Lillard",
            "team": "Milwaukee Bucks",
            "explanation": "Superstar scorer who played for years on a team that couldn't get over the playoff hump. Elite offensive players who fans debate about due to lack of championship success."
        },
        "nfl": {
            "player": "Justin Herbert",
            "team": "Los Angeles Chargers",
            "explanation": "Elite talent, big market pressure, but playoff success has been elusive. Both are unquestionable stars who need to 'win the big one' to cement legacy."
        },
        "mlb": {
            "player": "Mike Trout",
            "team": "Los Angeles Angels",
            "explanation": "Best player at their position, incredible individual stats, but team success has been limited. Both carry the weight of their franchise."
        }
    },

    "connor bedard": {
        "position": "Center",
        "team": "Chicago Blackhawks",
        "age": 19,
        "style": "Generational playmaker, elite shot, rookie sensation",
        "accolades": "#1 Overall Pick 2023, Calder Trophy candidate",
        "soccer": {
            "player": "Lamine Yamal",
            "team": "Barcelona",
            "explanation": "Teenage prodigies who are already playing at an elite level. Both broke onto the scene as minors and are considered future faces of their sport. Generational talent."
        },
        "nba": {
            "player": "Paolo Banchero",
            "team": "Orlando Magic",
            "explanation": "#1 picks expected to lead franchise rebuilds. Both are already showing star potential in their second year and are cornerstone pieces."
        },
        "nfl": {
            "player": "C.J. Stroud",
            "team": "Houston Texans",
            "explanation": "Rookie phenoms who immediately played at an elite level. Both exceeded expectations and led their struggling teams to relevance in year one."
        },
        "mlb": {
            "player": "Gunnar Henderson",
            "team": "Baltimore Orioles",
            "explanation": "Young stars who are already elite. Both are leading the next wave of superstars in their sport with incredible skill and maturity."
        }
    },

    "leon draisaitl": {
        "position": "Center",
        "team": "Edmonton Oilers",
        "age": 28,
        "style": "Elite scorer and playmaker, physical, German star",
        "accolades": "Hart Trophy (MVP), Art Ross Trophy (scoring leader)",
        "soccer": {
            "player": "Florian Wirtz",
            "team": "Bayer Leverkusen",
            "explanation": "Elite German playmakers who combine scoring and creating. Both are among the best in the world at their position and carry their national team's hopes."
        },
        "nba": {
            "player": "Luka Dončić",
            "team": "Dallas Mavericks",
            "explanation": "European superstars who came to North America and dominated. Elite scorers and playmakers who can do everything offensively. Draisaitl and Luka share similar 'do it all' games."
        },
        "nfl": {
            "player": "Travis Kelce",
            "team": "Kansas City Chiefs",
            "explanation": "The 'other' superstar next to the MVP. Draisaitl plays with McDavid like Kelce plays with Mahomes - both are elite in their own right but sometimes overlooked."
        },
        "mlb": {
            "player": "Freddie Freeman",
            "team": "Los Angeles Dodgers",
            "explanation": "Elite players who do everything well. Both are complete players who can hit for power, average, and drive in runs/create plays consistently."
        }
    }
}

# =============================================================================
# CONCEPT SYNONYMS & KEYWORDS - For flexible matching
# =============================================================================

CONCEPT_SYNONYMS = {
    # Power play variations
    "power play": ["power play", "pp", "man advantage", "5 on 4", "5v4", "5-on-4", "extra man", "powerplay"],

    # Penalty kill variations
    "penalty kill": ["penalty kill", "pk", "shorthanded", "short handed", "killing a penalty", "4 on 5", "4v5", "man down", "penaltykill"],

    # Icing variations
    "icing": ["icing", "iced the puck", "ice the puck", "clearing the puck", "dump out"],

    # Offside variations
    "offside": ["offside", "offsides", "off-side", "off side", "blue line violation", "offside rule"],

    # Goalie pull variations
    "goalie pull": ["goalie pull", "pull the goalie", "pulled goalie", "extra attacker", "empty net", "6 on 5", "6v5", "empty netter"],

    # Line change variations
    "line change": ["line change", "change lines", "substitution", "shift change", "changing on the fly", "line changes"],

    # Hat trick variations
    "hat trick": ["hat trick", "hatrick", "hat-trick", "3 goals", "three goals", "hattrick"],

    # Checking variations
    "checking": ["checking", "body check", "hit", "hitting", "check", "body checking", "open ice hit", "hip check", "boarding", "charge"],

    # Face-off variations
    "face-off": ["face-off", "faceoff", "face off", "puck drop", "draw", "faceoffs"],

    # Overtime variations
    "overtime": ["overtime", "ot", "extra time", "sudden death", "shootout", "3 on 3", "3v3"],

    # Crease variations
    "the crease": ["crease", "the crease", "goal crease", "blue paint", "goalie crease", "in the crease"],

    # Fighting variations
    "fighting": ["fighting", "fight", "dropping gloves", "scrap", "tilt", "enforcers", "goon", "brawl", "throwing hands"]
}

# Additional hockey terms that map to explanations
ADDITIONAL_CONCEPTS = {
    "breakaway": {
        "definition": "When a player gets behind all defenders with just the goalie to beat. A high-percentage scoring chance.",
        "soccer": {
            "analogy": "Through Ball 1-on-1",
            "explanation": "Like when a striker gets played through on goal with just the keeper to beat. Pure speed vs positioning.",
            "key_difference": "Hockey breakaways happen faster - you have 2-3 seconds to shoot."
        },
        "nba": {
            "analogy": "Fast Break Dunk",
            "explanation": "Like a fast break with a clear path to the rim. It's you vs the last defender (goalie), and you're expected to score.",
            "key_difference": "NBA dunks are high percentage. Hockey breakaways are actually saved ~65% of the time."
        },
        "nfl": {
            "analogy": "Wide Open Receiver Deep",
            "explanation": "When a receiver beats his man and has nothing but green grass ahead. Pure execution required.",
            "key_difference": "NFL receivers catch and run. Hockey players have to beat a goalie."
        },
        "mlb": {
            "analogy": "Grand Slam Opportunity",
            "explanation": "A huge scoring opportunity that doesn't come often. When you get one, you need to capitalize.",
            "key_difference": "Grand slams are still only ~15% success. Breakaways are saved less often."
        }
    },
    "deke": {
        "definition": "A fake or feint move used to deceive the goalie or defender. Short for 'decoy.'",
        "soccer": {
            "analogy": "Skill Move / Stepover",
            "explanation": "Like Ronaldo's stepovers or Neymar's skills - moves to get past defenders and goalies.",
            "key_difference": "Hockey dekes happen at much higher speed on slippery ice."
        },
        "nba": {
            "analogy": "Crossover / Euro Step",
            "explanation": "Like AI's crossover or the euro step - moves designed to fake out the defender and create space.",
            "key_difference": "Hockey dekes often end with a shot attempt, not just beating your man."
        },
        "nfl": {
            "analogy": "Juke Move",
            "explanation": "Like a running back's juke to make a defender miss. Skill move to create space.",
            "key_difference": "Football jukes are to avoid tackles. Hockey dekes are to beat the goalie."
        },
        "mlb": {
            "analogy": "Fake Throw by Infielder",
            "explanation": "That fake throw that freezes the runner. A deceptive move to gain advantage.",
            "key_difference": "Baseball fakes are rare. Dekes are constant in hockey."
        }
    },
    "slap shot": {
        "definition": "A powerful shot where the player winds up and slaps the puck. Can reach 100+ mph.",
        "soccer": {
            "analogy": "Volley / Thunderbolt",
            "explanation": "Like a Roberto Carlos free kick or a full volley - maximum power, aiming for pure velocity.",
            "key_difference": "Slap shots are 100+ mph. Soccer shots max around 80 mph."
        },
        "nba": {
            "analogy": "Tomahawk Dunk",
            "explanation": "The power move - wind up and throw it down. Slap shots are the statement play of hockey.",
            "key_difference": "Dunks are close range. Slap shots work from distance."
        },
        "nfl": {
            "analogy": "Hail Mary Throw",
            "explanation": "A big wind-up, maximum power throw. When you see a player loading up for a slap shot, everyone tenses up.",
            "key_difference": "Hail Marys are deep throws. Slap shots can be from the blue line."
        },
        "mlb": {
            "analogy": "Full Power Swing",
            "explanation": "Like going for the fences with a full hack. Maximum power, less control.",
            "key_difference": "Baseball swings are horizontal. Slap shots are a downward swing that hits ice then puck."
        }
    },
    "wrist shot": {
        "definition": "A quicker, more accurate shot using wrist movement to snap the puck. Most common shot type.",
        "soccer": {
            "analogy": "Placed Shot / Finesse",
            "explanation": "Like a curling shot into the corner - technique over power. Most goals are scored this way.",
            "key_difference": "Wrist shots are still 70-90 mph, just more accurate than slap shots."
        },
        "nba": {
            "analogy": "Pull-Up Jumper",
            "explanation": "The go-to scoring move. Quick release, accurate, can be done on the move.",
            "key_difference": "Jump shots have arc. Wrist shots are more like line drives."
        },
        "nfl": {
            "analogy": "Quick Slant Pass",
            "explanation": "Quick release, accurate, effective. Not flashy but gets the job done.",
            "key_difference": "NFL passes are thrown. Wrist shots are snapped with stick flex."
        },
        "mlb": {
            "analogy": "Line Drive Hit",
            "explanation": "Contact-focused, going for the gaps. Effective and repeatable.",
            "key_difference": "Baseball is reaction-based. Wrist shots are player-initiated."
        }
    },
    "one-timer": {
        "definition": "Shooting the puck directly from a pass without stopping it first. Requires perfect timing.",
        "soccer": {
            "analogy": "First-Time Finish",
            "explanation": "Hitting it first time off a cross or pass. No touch to control - straight into a finish.",
            "key_difference": "Hockey one-timers are even harder because the puck is flat and fast."
        },
        "nba": {
            "analogy": "Catch and Shoot",
            "explanation": "Like Klay Thompson catch-and-shoot 3s. No dribble, just receive and fire.",
            "key_difference": "NBA shooters have more time. One-timers are instantaneous."
        },
        "nfl": {
            "analogy": "Screen Pass TD",
            "explanation": "Catch in stride and immediately score. All about timing with the passer.",
            "key_difference": "Screen passes are planned. One-timers require reading the play."
        },
        "mlb": {
            "analogy": "Swinging at First Pitch Fastball",
            "explanation": "Being ready to attack immediately. No waiting, just react and swing.",
            "key_difference": "First pitch swings are a choice. One-timers are the play design."
        }
    },
    "assist": {
        "definition": "A pass that leads directly to a goal. Up to two assists can be awarded per goal.",
        "soccer": {
            "analogy": "Assist",
            "explanation": "Exactly the same concept! The pass before the goal. Hockey awards two assists per goal (primary and secondary).",
            "key_difference": "Hockey gives two assists. Soccer gives one."
        },
        "nba": {
            "analogy": "Assist",
            "explanation": "Same thing - the pass that leads to a score. Elite playmakers rack up assists.",
            "key_difference": "Hockey awards two assists per goal. NBA just one."
        },
        "nfl": {
            "analogy": "QB Gets Credit for TD Pass",
            "explanation": "The pass that creates the score. Both the passer and receiver get recognition.",
            "key_difference": "NFL is one-to-one. Hockey has primary and secondary assists."
        },
        "mlb": {
            "analogy": "RBI Situation Setup",
            "explanation": "Getting on base so someone else can drive you in. Setting up the scorer.",
            "key_difference": "Baseball doesn't formally track 'assists' for runs."
        }
    },
    "plus minus": {
        "definition": "A stat tracking if you're on ice when your team scores (+1) or gets scored on (-1). Measures overall impact.",
        "soccer": {
            "analogy": "Goal Difference When Playing",
            "explanation": "Like tracking goal difference only for minutes a player is on the pitch. Good players are usually plus players.",
            "key_difference": "Soccer doesn't formally track this per-player."
        },
        "nba": {
            "analogy": "Plus/Minus",
            "explanation": "Exactly the same stat! Tracks point differential when you're on the court. Hockey invented it.",
            "key_difference": "None - NBA adopted this directly from hockey."
        },
        "nfl": {
            "analogy": "Points For/Against When Playing",
            "explanation": "Like tracking if your team outscores opponents when you're in the game.",
            "key_difference": "NFL doesn't track individual plus/minus."
        },
        "mlb": {
            "analogy": "Win Probability Added",
            "explanation": "A stat measuring if you helped your team win while you were playing.",
            "key_difference": "WPA is more complex. Plus/minus is simple count."
        }
    },
    "penalty box": {
        "definition": "Where players sit to serve their penalty time. Also called 'the sin bin.'",
        "soccer": {
            "analogy": "Sin Bin (Rugby)",
            "explanation": "Soccer doesn't have this, but rugby does. A timeout area for rule breakers.",
            "key_difference": "Soccer uses cards. Hockey uses timed exclusions."
        },
        "nba": {
            "analogy": "Fouled Out (Temporary)",
            "explanation": "Imagine if fouling out was just for 2-5 minutes instead of permanent.",
            "key_difference": "NBA fouls out permanently. Hockey penalty box is temporary."
        },
        "nfl": {
            "analogy": "Ejection (But Temporary)",
            "explanation": "Like getting ejected but you can come back after a few minutes.",
            "key_difference": "NFL ejections are permanent. Penalty box is timed."
        },
        "mlb": {
            "analogy": "Ejection (But Temporary)",
            "explanation": "Like if an ejection was just a timeout instead of removal from game.",
            "key_difference": "MLB ejections are game-long. Penalty box is minutes."
        }
    },
    "slapshot": {
        "definition": "A powerful shot where the player winds up and slaps the puck. Can reach 100+ mph.",
        "soccer": {
            "analogy": "Volley / Thunderbolt",
            "explanation": "Like a Roberto Carlos free kick or a full volley - maximum power, aiming for pure velocity.",
            "key_difference": "Slap shots are 100+ mph. Soccer shots max around 80 mph."
        },
        "nba": {
            "analogy": "Tomahawk Dunk",
            "explanation": "The power move - wind up and throw it down. Slap shots are the statement play of hockey.",
            "key_difference": "Dunks are close range. Slap shots work from distance."
        },
        "nfl": {
            "analogy": "Hail Mary Throw",
            "explanation": "A big wind-up, maximum power throw. When you see a player loading up for a slap shot, everyone tenses up.",
            "key_difference": "Hail Marys are deep throws. Slap shots can be from the blue line."
        },
        "mlb": {
            "analogy": "Full Power Swing",
            "explanation": "Like going for the fences with a full hack. Maximum power, less control.",
            "key_difference": "Baseball swings are horizontal. Slap shots are a downward swing that hits ice then puck."
        }
    },
    "goaltender": {
        "definition": "The player who guards the net. Also called goalie, netminder, or keeper. Only player allowed to use hands to stop puck.",
        "soccer": {
            "analogy": "Goalkeeper",
            "explanation": "Exactly the same role! Guards the net, can use hands/body to stop shots. The last line of defense.",
            "key_difference": "Hockey goalies wear massive pads and see 30-40 shots per game."
        },
        "nba": {
            "analogy": "Rim Protector",
            "explanation": "Like a Rudy Gobert who protects the basket. The last line of defense before scoring.",
            "key_difference": "Rim protectors block shots. Goalies stop 90%+ of them."
        },
        "nfl": {
            "analogy": "Safety (Last Line)",
            "explanation": "The last player back preventing touchdowns. When all else fails, they have to make the stop.",
            "key_difference": "Safeties tackle runners. Goalies stop pucks."
        },
        "mlb": {
            "analogy": "Catcher",
            "explanation": "Specialized defensive position requiring unique equipment. Quarterbacks the defense.",
            "key_difference": "Catchers receive pitches. Goalies stop shots."
        }
    },
    "zamboni": {
        "definition": "The ice resurfacing machine that cleans and smooths the ice between periods.",
        "soccer": {
            "analogy": "Groundskeeper",
            "explanation": "Like the grounds crew that maintains the pitch, but a specialized machine for ice.",
            "key_difference": "Grass grows naturally. Ice needs constant resurfacing."
        },
        "nba": {
            "analogy": "Court Sweepers",
            "explanation": "Like the people who mop sweat off the court, but a big machine for ice.",
            "key_difference": "Mopping is quick. Zamboni drives full laps for 15+ minutes."
        },
        "nfl": {
            "analogy": "Field Crew",
            "explanation": "Like the halftime field maintenance crew. Keeps the playing surface optimal.",
            "key_difference": "Field work is rare. Zamboni runs every intermission."
        },
        "mlb": {
            "analogy": "Infield Dragger",
            "explanation": "Like dragging the infield dirt between innings. Regular maintenance.",
            "key_difference": "Dirt dragging is quick. Zamboni is a 15-minute process."
        }
    },
    "shutout": {
        "definition": "When a goalie doesn't allow any goals for the entire game. A major achievement.",
        "soccer": {
            "analogy": "Clean Sheet",
            "explanation": "Exactly the same! No goals allowed. Goalies and defenders work toward this.",
            "key_difference": "None - same concept!"
        },
        "nba": {
            "analogy": "Holding to Under 80",
            "explanation": "No direct equivalent, but holding a team way below average is similar dominance.",
            "key_difference": "Basketball always has scoring. Shutouts happen in hockey."
        },
        "nfl": {
            "analogy": "Shutout",
            "explanation": "Same term! Holding the opponent scoreless is a shutout in both sports.",
            "key_difference": "None - same concept!"
        },
        "mlb": {
            "analogy": "Complete Game Shutout",
            "explanation": "Pitcher throwing a full game with no runs allowed. Same idea.",
            "key_difference": "Pitchers get sole credit. Hockey shutouts credit the whole team too."
        }
    },
    "blue line": {
        "definition": "The lines that divide the rink into three zones. Crossing it determines offside and zone entries.",
        "soccer": {
            "analogy": "Halfway Line",
            "explanation": "Like the halfway line but there are two (one each direction). Determines offside positioning.",
            "key_difference": "Soccer's offside is about defenders. Hockey's is about the blue line."
        },
        "nba": {
            "analogy": "Half Court Line",
            "explanation": "The line that divides the court. You can't go backwards over it in hockey's attacking zone.",
            "key_difference": "NBA line is midcourt. Hockey has two blue lines creating three zones."
        },
        "nfl": {
            "analogy": "Line of Scrimmage",
            "explanation": "A line that governs the game structure. But hockey's is fixed, not changing each play.",
            "key_difference": "NFL line moves. Hockey lines are permanent."
        },
        "mlb": {
            "analogy": "Bases/Basepaths",
            "explanation": "Markers that define territory and where you can be. Fixed positions on the field.",
            "key_difference": "Bases are points. Blue lines are full lines across the ice."
        }
    },
    "hockey stick": {
        "definition": "The main equipment - a long stick with a curved blade used to shoot and handle the puck.",
        "soccer": {
            "analogy": "No Equivalent (Feet/Head)",
            "explanation": "Soccer uses feet and head. Hockey uses a specialized stick. The curve on the blade affects shots like boot tech affects kicks.",
            "key_difference": "Soccer is natural body. Hockey requires the stick tool."
        },
        "nba": {
            "analogy": "No Equivalent (Hands)",
            "explanation": "Basketball is hands-only. The hockey stick is like if you could only use a bat to score.",
            "key_difference": "NBA is body contact with ball. Hockey is stick-to-puck."
        },
        "nfl": {
            "analogy": "No Equivalent",
            "explanation": "Football uses hands and feet. Hockey is entirely stick-dependent for offense.",
            "key_difference": "NFL is body contact. Hockey requires the stick."
        },
        "mlb": {
            "analogy": "Bat",
            "explanation": "The primary tool for offense. Different players prefer different stick curves like batters prefer bat weights.",
            "key_difference": "Bats just hit. Sticks pass, shoot, and handle."
        }
    },
    "puck": {
        "definition": "A hard rubber disc that players shoot, pass, and score with. About 3 inches in diameter.",
        "soccer": {
            "analogy": "Football/Ball",
            "explanation": "The thing you're trying to put in the net! But it's flat and slides on ice instead of rolling.",
            "key_difference": "Pucks slide flat. Soccer balls roll and bounce."
        },
        "nba": {
            "analogy": "Basketball",
            "explanation": "The scoring object. But pucks don't bounce - they slide and can be hidden by players.",
            "key_difference": "Basketballs are big and visible. Pucks are small and fast."
        },
        "nfl": {
            "analogy": "Football",
            "explanation": "The thing you move down the ice/field. Flat and faster than any football throw.",
            "key_difference": "Footballs are thrown. Pucks are shot at 100+ mph."
        },
        "mlb": {
            "analogy": "Baseball",
            "explanation": "Small, hard, and fast. Pucks go even faster than pitched baseballs.",
            "key_difference": "Baseballs are round. Pucks are flat discs."
        }
    },
    "stanley cup": {
        "definition": "The NHL championship trophy - the oldest professional sports trophy in North America (1893).",
        "soccer": {
            "analogy": "Champions League / FA Cup",
            "explanation": "The ultimate prize. The Stanley Cup has unique traditions - each player gets it for a day, names engraved on it.",
            "key_difference": "Stanley Cup is passed around. Soccer trophies stay with the club."
        },
        "nba": {
            "analogy": "Larry O'Brien Trophy",
            "explanation": "The championship trophy, but with way more history and tradition. Players get their names on it forever.",
            "key_difference": "Names are engraved on Stanley Cup. NBA trophy doesn't have names."
        },
        "nfl": {
            "analogy": "Lombardi Trophy",
            "explanation": "The championship prize. But teams get a new Lombardi each year - the Stanley Cup is THE same cup since 1893.",
            "key_difference": "Stanley Cup is one trophy forever. New Lombardi made each year."
        },
        "mlb": {
            "analogy": "Commissioner's Trophy",
            "explanation": "The championship prize. Stanley Cup tradition is unique - each player gets it for a day to celebrate.",
            "key_difference": "Stanley Cup has player names. Commissioner's Trophy doesn't."
        }
    },
    "center ice": {
        "definition": "The middle of the rink where face-offs start each period and after goals.",
        "soccer": {
            "analogy": "Center Circle",
            "explanation": "The middle of the pitch where kickoffs happen. Same concept for starting play.",
            "key_difference": "Soccer kickoffs are kicks. Hockey is face-off battles."
        },
        "nba": {
            "analogy": "Center Court",
            "explanation": "The middle where tip-offs happen. Iconic location for game starts.",
            "key_difference": "Tip-off happens once. Face-offs at center ice happen after every goal."
        },
        "nfl": {
            "analogy": "50-Yard Line",
            "explanation": "The middle of the field. Neutral territory before the action starts.",
            "key_difference": "50-yard line is territory. Center ice is for starting play."
        },
        "mlb": {
            "analogy": "Pitcher's Mound",
            "explanation": "The center of action where play begins. The focal point.",
            "key_difference": "Mound is for one player. Center ice is for face-off battles."
        }
    },
    "point": {
        "definition": "In hockey stats, 1 goal = 1 point, 1 assist = 1 point. Also refers to the defenseman position at the blue line on power plays.",
        "soccer": {
            "analogy": "Goal Contributions",
            "explanation": "Goals + assists combined. The total offensive impact stat.",
            "key_difference": "Hockey counts two assists per goal. Soccer just one."
        },
        "nba": {
            "analogy": "Points (Scoring)",
            "explanation": "Different meaning - NBA points are from baskets. Hockey points are goals + assists.",
            "key_difference": "NBA points = scoring. Hockey points = goals + assists."
        },
        "nfl": {
            "analogy": "Touchdowns + Assists",
            "explanation": "If you counted TDs and the passes that led to them equally.",
            "key_difference": "NFL doesn't track points this way."
        },
        "mlb": {
            "analogy": "Runs + RBIs",
            "explanation": "Production stats combined. Measures total offensive contribution.",
            "key_difference": "Baseball has separate stats. Hockey combines into points."
        }
    }
}

# =============================================================================
# PLAYER ARCHETYPES - Multiple options per archetype for variety
# =============================================================================

PLAYER_ARCHETYPES = {
    "elite_center": {
        "description": "Elite two-way center, franchise cornerstone",
        "soccer": [
            {"player": "Kevin De Bruyne", "team": "Manchester City", "style": "Elite playmaker who controls the game from the middle"},
            {"player": "Rodri", "team": "Manchester City", "style": "Midfield maestro, Ballon d'Or winner who dictates tempo"},
            {"player": "Jude Bellingham", "team": "Real Madrid", "style": "Complete midfielder who scores, creates, and defends"}
        ],
        "nba": [
            {"player": "Nikola Jokic", "team": "Denver Nuggets", "style": "Complete player who makes everyone around them better"},
            {"player": "Shai Gilgeous-Alexander", "team": "Oklahoma City Thunder", "style": "Two-way star who dominates on both ends"},
            {"player": "Jayson Tatum", "team": "Boston Celtics", "style": "Franchise cornerstone, championship-caliber player"}
        ],
        "nfl": [
            {"player": "Lamar Jackson", "team": "Baltimore Ravens", "style": "Dynamic playmaker who can do it all"},
            {"player": "Josh Allen", "team": "Buffalo Bills", "style": "Elite dual-threat who carries his team"},
            {"player": "Jalen Hurts", "team": "Philadelphia Eagles", "style": "Complete QB, runs the show on offense"}
        ],
        "mlb": [
            {"player": "Mookie Betts", "team": "LA Dodgers", "style": "Five-tool player, elite at everything"},
            {"player": "Corey Seager", "team": "Texas Rangers", "style": "Championship-proven, complete player"},
            {"player": "Marcus Semien", "team": "Texas Rangers", "style": "All-around excellence, durable star"}
        ]
    },
    "goal_scorer": {
        "description": "Pure goal scorer with lethal shot",
        "soccer": [
            {"player": "Erling Haaland", "team": "Manchester City", "style": "Elite finisher, born goal scorer"},
            {"player": "Kylian Mbappe", "team": "Real Madrid", "style": "Explosive scorer with devastating pace"},
            {"player": "Mohamed Salah", "team": "Liverpool", "style": "Clinical finisher, scores in every big game"},
            {"player": "Harry Kane", "team": "Bayern Munich", "style": "Complete striker, lethal from anywhere"}
        ],
        "nba": [
            {"player": "Kevin Durant", "team": "Phoenix Suns", "style": "Pure scorer, impossible to stop when hot"},
            {"player": "Devin Booker", "team": "Phoenix Suns", "style": "Bucket getter, scores at will"},
            {"player": "Donovan Mitchell", "team": "Cleveland Cavaliers", "style": "Dynamic scorer who can explode any night"},
            {"player": "Zach LaVine", "team": "Chicago Bulls", "style": "Athletic scorer with limitless range"}
        ],
        "nfl": [
            {"player": "Tyreek Hill", "team": "Miami Dolphins", "style": "Big play threat, scores from anywhere"},
            {"player": "Ja'Marr Chase", "team": "Cincinnati Bengals", "style": "Elite receiver who dominates in the red zone"},
            {"player": "Davante Adams", "team": "Las Vegas Raiders", "style": "Route-running master, touchdown machine"},
            {"player": "Justin Jefferson", "team": "Minnesota Vikings", "style": "Explosive playmaker, game-breaking talent"}
        ],
        "mlb": [
            {"player": "Aaron Judge", "team": "NY Yankees", "style": "Power hitter, home run threat every at-bat"},
            {"player": "Kyle Schwarber", "team": "Philadelphia Phillies", "style": "Power lefty who crushes the ball"},
            {"player": "Pete Alonso", "team": "NY Mets", "style": "Polar Bear power, dangerous slugger"},
            {"player": "Matt Olson", "team": "Atlanta Braves", "style": "Elite power bat, run producer"}
        ]
    },
    "playmaker": {
        "description": "Elite passer and setup man",
        "soccer": [
            {"player": "Martin Odegaard", "team": "Arsenal", "style": "Creative genius who sees passes others don't"},
            {"player": "Bruno Fernandes", "team": "Manchester United", "style": "Chance creator with elite vision"},
            {"player": "Bukayo Saka", "team": "Arsenal", "style": "Creative winger who makes things happen"},
            {"player": "Cole Palmer", "team": "Chelsea", "style": "Young creator with incredible technique"}
        ],
        "nba": [
            {"player": "Chris Paul", "team": "San Antonio Spurs", "style": "Point god, elite court vision and passing"},
            {"player": "Tyrese Haliburton", "team": "Indiana Pacers", "style": "Floor general with elite assist numbers"},
            {"player": "Trae Young", "team": "Atlanta Hawks", "style": "Elite passer who runs the offense"},
            {"player": "LaMelo Ball", "team": "Charlotte Hornets", "style": "Creative playmaker with flashy passing"}
        ],
        "nfl": [
            {"player": "Travis Kelce", "team": "Kansas City Chiefs", "style": "Security blanket who always finds the open space"},
            {"player": "George Kittle", "team": "San Francisco 49ers", "style": "Playmaking tight end, moves the chains"},
            {"player": "CeeDee Lamb", "team": "Dallas Cowboys", "style": "Route runner who creates separation"},
            {"player": "Amon-Ra St. Brown", "team": "Detroit Lions", "style": "Reliable target who moves the chains"}
        ],
        "mlb": [
            {"player": "Jose Altuve", "team": "Houston Astros", "style": "Table setter, always getting on base"},
            {"player": "Trea Turner", "team": "Philadelphia Phillies", "style": "Catalyst at the top of the order"},
            {"player": "Luis Arraez", "team": "San Diego Padres", "style": "Contact king, elite bat-to-ball skills"},
            {"player": "Steven Kwan", "team": "Cleveland Guardians", "style": "On-base machine, pesky hitter"}
        ]
    },
    "power_forward": {
        "description": "Physical, hard-nosed player who scores and hits",
        "soccer": [
            {"player": "Darwin Nunez", "team": "Liverpool", "style": "Physical striker who bullies defenders"},
            {"player": "Romelu Lukaku", "team": "Napoli", "style": "Powerful target man who holds up play"},
            {"player": "Alexander Isak", "team": "Newcastle", "style": "Physical presence with clinical finishing"},
            {"player": "Ivan Toney", "team": "Al-Ahli", "style": "Strong forward who wins aerial duels"}
        ],
        "nba": [
            {"player": "Giannis Antetokounmpo", "team": "Milwaukee Bucks", "style": "Physical freak who dominates through power"},
            {"player": "Zion Williamson", "team": "New Orleans Pelicans", "style": "Unstoppable force at the rim"},
            {"player": "Paolo Banchero", "team": "Orlando Magic", "style": "Physical scorer who bullies defenders"},
            {"player": "Julius Randle", "team": "New York Knicks", "style": "Power forward who creates his own shot"}
        ],
        "nfl": [
            {"player": "Derrick Henry", "team": "Baltimore Ravens", "style": "Bruising runner who punishes defenders"},
            {"player": "Josh Jacobs", "team": "Green Bay Packers", "style": "Physical back who wears down defenses"},
            {"player": "Saquon Barkley", "team": "Philadelphia Eagles", "style": "Power and speed combination"},
            {"player": "Nick Chubb", "team": "Cleveland Browns", "style": "Powerful runner who breaks tackles"}
        ],
        "mlb": [
            {"player": "Yordan Alvarez", "team": "Houston Astros", "style": "Power bat who crushes the ball"},
            {"player": "Giancarlo Stanton", "team": "NY Yankees", "style": "Raw power, tape-measure home runs"},
            {"player": "Marcell Ozuna", "team": "Atlanta Braves", "style": "Middle-of-the-order power threat"},
            {"player": "Rhys Hoskins", "team": "Milwaukee Brewers", "style": "Power-hitting first baseman"}
        ]
    },
    "defensive_forward": {
        "description": "Responsible two-way forward, shutdown role",
        "soccer": [
            {"player": "N'Golo Kante", "team": "Al-Ittihad", "style": "Tireless worker who wins the ball everywhere"},
            {"player": "Declan Rice", "team": "Arsenal", "style": "Defensive midfielder who breaks up play"},
            {"player": "Casemiro", "team": "Manchester United", "style": "Destroyer who protects the back line"},
            {"player": "Moises Caicedo", "team": "Chelsea", "style": "Ball-winner with endless energy"}
        ],
        "nba": [
            {"player": "Marcus Smart", "team": "Memphis Grizzlies", "style": "Defensive specialist who does the dirty work"},
            {"player": "Alex Caruso", "team": "Oklahoma City Thunder", "style": "Hustle player, elite perimeter defender"},
            {"player": "Herb Jones", "team": "New Orleans Pelicans", "style": "Lockdown defender who guards the best"},
            {"player": "Jrue Holiday", "team": "Boston Celtics", "style": "Two-way guard, championship defender"}
        ],
        "nfl": [
            {"player": "Nick Bosa", "team": "San Francisco 49ers", "style": "Disruptive defender who impacts every play"},
            {"player": "T.J. Watt", "team": "Pittsburgh Steelers", "style": "Dominant pass rusher, game-wrecker"},
            {"player": "Myles Garrett", "team": "Cleveland Browns", "style": "Elite edge rusher, sack machine"},
            {"player": "Maxx Crosby", "team": "Las Vegas Raiders", "style": "Relentless motor, high-effort player"}
        ],
        "mlb": [
            {"player": "Andrelton Simmons", "team": "Free Agent", "style": "Elite defender, Gold Glove caliber"},
            {"player": "Kevin Kiermaier", "team": "Toronto Blue Jays", "style": "Outfield wizard, highlight-reel catches"},
            {"player": "Harrison Bader", "team": "New York Mets", "style": "Elite center fielder, defensive specialist"},
            {"player": "Dansby Swanson", "team": "Chicago Cubs", "style": "Gold Glove shortstop, steady defender"}
        ]
    },
    "offensive_defenseman": {
        "description": "Defenseman who quarterbacks the offense",
        "soccer": [
            {"player": "Trent Alexander-Arnold", "team": "Liverpool", "style": "Attacking fullback who creates from deep"},
            {"player": "Josko Gvardiol", "team": "Manchester City", "style": "Ball-playing defender who joins attacks"},
            {"player": "Achraf Hakimi", "team": "PSG", "style": "Attacking wingback with pace and skill"},
            {"player": "Reece James", "team": "Chelsea", "style": "Complete fullback who contributes offensively"}
        ],
        "nba": [
            {"player": "Draymond Green", "team": "Golden State Warriors", "style": "Defensive anchor who runs the offense"},
            {"player": "Bam Adebayo", "team": "Miami Heat", "style": "Defensive big who facilitates offense"},
            {"player": "Evan Mobley", "team": "Cleveland Cavaliers", "style": "Two-way big with playmaking ability"},
            {"player": "Jaren Jackson Jr.", "team": "Memphis Grizzlies", "style": "Shot-blocking big who can shoot"}
        ],
        "nfl": [
            {"player": "Micah Parsons", "team": "Dallas Cowboys", "style": "Dynamic defender who makes plays everywhere"},
            {"player": "Fred Warner", "team": "San Francisco 49ers", "style": "Sideline-to-sideline linebacker"},
            {"player": "Roquan Smith", "team": "Baltimore Ravens", "style": "Playmaking linebacker, tackles machine"},
            {"player": "Bobby Wagner", "team": "Washington Commanders", "style": "Veteran playmaker, still elite"}
        ],
        "mlb": [
            {"player": "Francisco Lindor", "team": "NY Mets", "style": "Elite defender with offensive pop"},
            {"player": "Bo Bichette", "team": "Toronto Blue Jays", "style": "Shortstop with offensive upside"},
            {"player": "Xander Bogaerts", "team": "San Diego Padres", "style": "Complete shortstop, bat and glove"},
            {"player": "Willy Adames", "team": "Milwaukee Brewers", "style": "Power-hitting shortstop"}
        ]
    },
    "shutdown_defenseman": {
        "description": "Stay-at-home defenseman, defensive specialist",
        "soccer": [
            {"player": "Virgil van Dijk", "team": "Liverpool", "style": "Dominant defender who shuts down attackers"},
            {"player": "Ruben Dias", "team": "Manchester City", "style": "Rock-solid center back, defensive leader"},
            {"player": "William Saliba", "team": "Arsenal", "style": "Young but composed defender"},
            {"player": "Antonio Rudiger", "team": "Real Madrid", "style": "Aggressive defender, wins every duel"}
        ],
        "nba": [
            {"player": "Rudy Gobert", "team": "Minnesota Timberwolves", "style": "Defensive anchor, protects the paint"},
            {"player": "Giannis Antetokounmpo", "team": "Milwaukee Bucks", "style": "DPOY candidate, elite rim protector"},
            {"player": "Anthony Davis", "team": "Los Angeles Lakers", "style": "Elite shot-blocker, defensive anchor"},
            {"player": "Chet Holmgren", "team": "Oklahoma City Thunder", "style": "Length and timing, blocks everything"}
        ],
        "nfl": [
            {"player": "Aaron Donald", "team": "LA Rams (Retired)", "style": "Dominant force who disrupts everything"},
            {"player": "Chris Jones", "team": "Kansas City Chiefs", "style": "Interior dominance, pass-rush specialist"},
            {"player": "Quinnen Williams", "team": "New York Jets", "style": "Run-stuffer who collapses pockets"},
            {"player": "Dexter Lawrence", "team": "New York Giants", "style": "Massive presence, immovable object"}
        ],
        "mlb": [
            {"player": "Matt Chapman", "team": "San Francisco Giants", "style": "Elite defender, vacuum at the position"},
            {"player": "Nolan Arenado", "team": "St. Louis Cardinals", "style": "Gold Glove third baseman, defensive wizard"},
            {"player": "Ke'Bryan Hayes", "team": "Pittsburgh Pirates", "style": "Elite defender, smooth at third"},
            {"player": "Jose Iglesias", "team": "New York Mets", "style": "Defensive specialist, sure hands"}
        ]
    },
    "starting_goalie": {
        "description": "Starting goaltender, the last line of defense",
        "soccer": [
            {"player": "Alisson Becker", "team": "Liverpool", "style": "Elite shot-stopper, commands the box"},
            {"player": "Ederson", "team": "Manchester City", "style": "Sweeper-keeper with elite distribution"},
            {"player": "Thibaut Courtois", "team": "Real Madrid", "style": "Big-game goalkeeper, clutch saves"},
            {"player": "David Raya", "team": "Arsenal", "style": "Shot-stopper who plays with the ball"}
        ],
        "nba": [
            {"player": "Rudy Gobert", "team": "Minnesota Timberwolves", "style": "Rim protector, alters every shot"},
            {"player": "Brook Lopez", "team": "Milwaukee Bucks", "style": "Veteran rim protector, anchor"},
            {"player": "Walker Kessler", "team": "Utah Jazz", "style": "Young shot-blocker with elite timing"},
            {"player": "Mitchell Robinson", "team": "New York Knicks", "style": "Athletic rim protector, alley-oop threat"}
        ],
        "nfl": [
            {"player": "Minkah Fitzpatrick", "team": "Pittsburgh Steelers", "style": "Last line of defense, ball hawk"},
            {"player": "Jessie Bates III", "team": "Atlanta Falcons", "style": "Rangey safety, covers ground"},
            {"player": "Derwin James", "team": "Los Angeles Chargers", "style": "Versatile safety, does everything"},
            {"player": "Antoine Winfield Jr.", "team": "Tampa Bay Buccaneers", "style": "Playmaking safety, big-play threat"}
        ],
        "mlb": [
            {"player": "J.T. Realmuto", "team": "Philadelphia Phillies", "style": "Elite catcher, controls the game"},
            {"player": "Will Smith", "team": "Los Angeles Dodgers", "style": "Complete catcher, bat and glove"},
            {"player": "Adley Rutschman", "team": "Baltimore Orioles", "style": "Young franchise catcher, leader"},
            {"player": "Sean Murphy", "team": "Atlanta Braves", "style": "Elite defensive catcher with pop"}
        ]
    },
    "young_star": {
        "description": "Young phenom, rising star",
        "soccer": [
            {"player": "Lamine Yamal", "team": "Barcelona", "style": "Teenage sensation with unlimited potential"},
            {"player": "Florian Wirtz", "team": "Bayer Leverkusen", "style": "Young German playmaker, future superstar"},
            {"player": "Jamal Musiala", "team": "Bayern Munich", "style": "Skillful young star, dribbling wizard"},
            {"player": "Pedri", "team": "Barcelona", "style": "Young midfield maestro, beyond his years"},
            {"player": "Kobbie Mainoo", "team": "Manchester United", "style": "Breakthrough teenager, composed beyond his years"}
        ],
        "nba": [
            {"player": "Victor Wembanyama", "team": "San Antonio Spurs", "style": "Generational talent, franchise-changing"},
            {"player": "Chet Holmgren", "team": "Oklahoma City Thunder", "style": "Unicorn big man, does everything"},
            {"player": "Anthony Edwards", "team": "Minnesota Timberwolves", "style": "Young superstar, athletic freak"},
            {"player": "Tyrese Maxey", "team": "Philadelphia 76ers", "style": "Explosive young guard, rising star"},
            {"player": "Jalen Williams", "team": "Oklahoma City Thunder", "style": "Two-way young star, does it all"}
        ],
        "nfl": [
            {"player": "C.J. Stroud", "team": "Houston Texans", "style": "Young star performing beyond his years"},
            {"player": "Puka Nacua", "team": "Los Angeles Rams", "style": "Rookie sensation, record-breaker"},
            {"player": "Brock Bowers", "team": "Las Vegas Raiders", "style": "Young tight end, immediate impact"},
            {"player": "Jayden Daniels", "team": "Washington Commanders", "style": "Dual-threat rookie QB, electric"},
            {"player": "Malik Nabers", "team": "New York Giants", "style": "Young receiver, explosive playmaker"}
        ],
        "mlb": [
            {"player": "Elly De La Cruz", "team": "Cincinnati Reds", "style": "Electric young talent, game-changer"},
            {"player": "Gunnar Henderson", "team": "Baltimore Orioles", "style": "Young superstar, five-tool talent"},
            {"player": "Corbin Carroll", "team": "Arizona Diamondbacks", "style": "Speed and power, dynamic leadoff"},
            {"player": "Jackson Chourio", "team": "Milwaukee Brewers", "style": "Teenage phenom, exciting talent"},
            {"player": "Jackson Merrill", "team": "San Diego Padres", "style": "Rookie sensation, breakout star"}
        ]
    },
    "veteran_leader": {
        "description": "Experienced veteran, locker room leader",
        "soccer": [
            {"player": "Luka Modric", "team": "Real Madrid", "style": "Ageless leader who controls the game"},
            {"player": "Thiago Silva", "team": "Fluminense", "style": "Veteran leader, still performing at high level"},
            {"player": "James Milner", "team": "Brighton", "style": "Ultimate professional, leads by example"},
            {"player": "Olivier Giroud", "team": "AC Milan", "style": "Veteran striker, clutch performer"}
        ],
        "nba": [
            {"player": "LeBron James", "team": "Los Angeles Lakers", "style": "Veteran leader still performing at elite level"},
            {"player": "Stephen Curry", "team": "Golden State Warriors", "style": "All-time great, championship DNA"},
            {"player": "Chris Paul", "team": "San Antonio Spurs", "style": "Point God, mentor to young players"},
            {"player": "Kevin Durant", "team": "Phoenix Suns", "style": "Veteran scorer, still elite"}
        ],
        "nfl": [
            {"player": "Aaron Rodgers", "team": "New York Jets", "style": "Experienced leader, seen it all"},
            {"player": "Davante Adams", "team": "Las Vegas Raiders", "style": "Veteran receiver, route-running master"},
            {"player": "Travis Kelce", "team": "Kansas City Chiefs", "style": "Veteran playmaker, championship experience"},
            {"player": "Derrick Henry", "team": "Baltimore Ravens", "style": "Veteran workhorse, still dominant"}
        ],
        "mlb": [
            {"player": "Clayton Kershaw", "team": "Los Angeles Dodgers", "style": "Veteran ace, team leader"},
            {"player": "Justin Verlander", "team": "San Francisco Giants", "style": "Future Hall of Famer, still competing"},
            {"player": "Max Scherzer", "team": "Texas Rangers", "style": "Intense competitor, championship proven"},
            {"player": "Miguel Cabrera", "team": "Retired", "style": "Hall of Fame career, respected veteran"}
        ]
    },
    "grinder": {
        "description": "Energy player, hard worker, 4th line role",
        "soccer": [
            {"player": "James Milner", "team": "Brighton", "style": "Utility player, does everything asked"},
            {"player": "Mateo Kovacic", "team": "Manchester City", "style": "Engine room player, tireless worker"},
            {"player": "Conor Gallagher", "team": "Atletico Madrid", "style": "High-energy midfielder, never stops running"},
            {"player": "Pascal Gross", "team": "Brighton", "style": "Workmanlike player, reliable performer"}
        ],
        "nba": [
            {"player": "Patrick Beverley", "team": "Various", "style": "Energy guy, does the dirty work"},
            {"player": "P.J. Tucker", "team": "LA Clippers", "style": "Corner specialist, defensive hustle"},
            {"player": "Royce O'Neale", "team": "Phoenix Suns", "style": "3-and-D role player, does the little things"},
            {"player": "Torrey Craig", "team": "Chicago Bulls", "style": "Energy wing, hustle plays"}
        ],
        "nfl": [
            {"player": "Cordarrelle Patterson", "team": "Pittsburgh Steelers", "style": "Versatile role player, special teams ace"},
            {"player": "Taysom Hill", "team": "New Orleans Saints", "style": "Swiss Army knife, does everything"},
            {"player": "Rex Burkhead", "team": "Houston Texans", "style": "Versatile back, reliable veteran"},
            {"player": "C.J. Ham", "team": "Minnesota Vikings", "style": "Fullback, blocking specialist"}
        ],
        "mlb": [
            {"player": "Kiké Hernandez", "team": "LA Dodgers", "style": "Super utility, postseason hero"},
            {"player": "Tommy Edman", "team": "LA Dodgers", "style": "Versatile defender, plays everywhere"},
            {"player": "Isiah Kiner-Falefa", "team": "Toronto Blue Jays", "style": "Utility player, defensive versatility"},
            {"player": "David Fletcher", "team": "Atlanta Braves", "style": "Contact hitter, plays multiple positions"}
        ]
    },
    "enforcer": {
        "description": "Physical presence, protects teammates",
        "soccer": [
            {"player": "Roy Keane (Classic)", "team": "Retired", "style": "Intimidator who protected teammates"},
            {"player": "Sergio Ramos", "team": "Retired", "style": "Hard-nosed defender, feared competitor"},
            {"player": "Bruno Guimaraes", "team": "Newcastle", "style": "Tough midfielder who battles for everything"},
            {"player": "Rodri", "team": "Manchester City", "style": "Physical presence, wins every duel"}
        ],
        "nba": [
            {"player": "Draymond Green", "team": "Golden State Warriors", "style": "Physical, emotional leader, protector"},
            {"player": "Steven Adams", "team": "Houston Rockets", "style": "Enforcer, sets hard screens, protects teammates"},
            {"player": "Jusuf Nurkic", "team": "Phoenix Suns", "style": "Physical center, tough competitor"},
            {"player": "Montrezl Harrell", "team": "Various", "style": "Energy big, physical presence"}
        ],
        "nfl": [
            {"player": "Ray Lewis (Classic)", "team": "Retired", "style": "Intimidating presence, enforcer mentality"},
            {"player": "Cam Heyward", "team": "Pittsburgh Steelers", "style": "Veteran enforcer, physical leader"},
            {"player": "Budda Baker", "team": "Arizona Cardinals", "style": "Hard-hitting safety, enforcer"},
            {"player": "Zack Baun", "team": "Philadelphia Eagles", "style": "Physical linebacker, thumper"}
        ],
        "mlb": [
            {"player": "Chase Utley (Classic)", "team": "Retired", "style": "Hard-nosed, didn't back down"},
            {"player": "Pete Rose (Classic)", "team": "Retired", "style": "Charlie Hustle, played hard every play"},
            {"player": "Ty Cobb (Classic)", "team": "Retired", "style": "Aggressive, fiery competitor"},
            {"player": "Josh Donaldson", "team": "Retired", "style": "Intense competitor, fired up teammates"}
        ]
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_concepts():
    """Return list of all concept names including additional concepts"""
    return list(HOCKEY_CONCEPTS.keys()) + list(ADDITIONAL_CONCEPTS.keys())

def get_all_players():
    """Return list of all player names in our database"""
    return list(PLAYER_COMPARISONS.keys())

def similarity_score(a, b):
    """Calculate string similarity using SequenceMatcher"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_concept_match(query):
    """
    Find the best matching concept for a query using synonyms and fuzzy matching.
    Returns (concept_name, data_dict) or (None, None) if no match.
    """
    query = query.lower().strip()

    # 1. Check exact match in main concepts
    if query in HOCKEY_CONCEPTS:
        return query, HOCKEY_CONCEPTS[query]

    # 2. Check exact match in additional concepts
    if query in ADDITIONAL_CONCEPTS:
        return query, ADDITIONAL_CONCEPTS[query]

    # 3. Check synonym mappings
    for concept, synonyms in CONCEPT_SYNONYMS.items():
        if query in [s.lower() for s in synonyms]:
            if concept in HOCKEY_CONCEPTS:
                return concept, HOCKEY_CONCEPTS[concept]
            elif concept in ADDITIONAL_CONCEPTS:
                return concept, ADDITIONAL_CONCEPTS[concept]

    # 4. Fuzzy match against all concepts and their definitions
    best_match = None
    best_score = 0.0

    all_concepts = {**HOCKEY_CONCEPTS, **ADDITIONAL_CONCEPTS}

    for concept, data in all_concepts.items():
        # Check concept name similarity
        score = similarity_score(query, concept)
        if score > best_score:
            best_score = score
            best_match = (concept, data)

        # Check if query is in definition
        if query in data.get('definition', '').lower():
            if score < 0.5:  # Boost score if found in definition
                score = 0.6
                if score > best_score:
                    best_score = score
                    best_match = (concept, data)

    # 5. Check synonyms with fuzzy matching
    for concept, synonyms in CONCEPT_SYNONYMS.items():
        for synonym in synonyms:
            score = similarity_score(query, synonym)
            if score > best_score:
                best_score = score
                if concept in HOCKEY_CONCEPTS:
                    best_match = (concept, HOCKEY_CONCEPTS[concept])
                elif concept in ADDITIONAL_CONCEPTS:
                    best_match = (concept, ADDITIONAL_CONCEPTS[concept])

    # Return match if score is reasonable
    if best_score >= 0.5 and best_match:
        return best_match

    return None, None

def search_concept(query):
    """Search for concepts by keyword - returns list of matching concept names"""
    query = query.lower()
    matches = []

    all_concepts = {**HOCKEY_CONCEPTS, **ADDITIONAL_CONCEPTS}

    for concept, data in all_concepts.items():
        if query in concept or query in data.get('definition', '').lower():
            matches.append(concept)

    # Also check synonyms
    for concept, synonyms in CONCEPT_SYNONYMS.items():
        if any(query in s.lower() for s in synonyms):
            if concept not in matches:
                matches.append(concept)

    return matches

def search_player(query):
    """Search for a player in our curated database"""
    query = query.lower()
    matches = []
    for player, data in PLAYER_COMPARISONS.items():
        if query in player:
            matches.append(player)
    return matches

# =============================================================================
# NHL API FUNCTIONS - For dynamic player lookup
# =============================================================================

def fetch_nhl_teams():
    """Fetch all NHL teams from the API"""
    try:
        response = requests.get(f"{NHL_API_BASE}/standings/now", timeout=5)
        if response.status_code == 200:
            data = response.json()
            teams = []
            for standing in data.get('standings', []):
                teams.append({
                    'abbrev': standing.get('teamAbbrev', {}).get('default', ''),
                    'name': standing.get('teamName', {}).get('default', ''),
                    'commonName': standing.get('teamCommonName', {}).get('default', '')
                })
            return teams
    except:
        pass
    return []

def fetch_team_roster(team_abbrev):
    """Fetch roster for a specific team"""
    try:
        response = requests.get(f"{NHL_API_BASE}/roster/{team_abbrev}/current", timeout=5)
        if response.status_code == 200:
            data = response.json()
            players = []

            for pos in ['forwards', 'defensemen', 'goalies']:
                for player in data.get(pos, []):
                    players.append({
                        'id': player.get('id'),
                        'name': f"{player.get('firstName', {}).get('default', '')} {player.get('lastName', {}).get('default', '')}",
                        'position': player.get('positionCode', ''),
                        'number': player.get('sweaterNumber', ''),
                        'team': team_abbrev
                    })
            return players
    except:
        pass
    return []

def fetch_player_details(player_id):
    """Fetch detailed player info from NHL API"""
    try:
        response = requests.get(f"{NHL_API_BASE}/player/{player_id}/landing", timeout=5)
        if response.status_code == 200:
            data = response.json()

            # Extract key info
            first_name = data.get('firstName', {}).get('default', '')
            last_name = data.get('lastName', {}).get('default', '')
            position = data.get('position', 'F')
            team = data.get('currentTeamAbbrev', '')
            team_name = data.get('fullTeamName', {}).get('default', '')

            # Get age from birth date
            birth_date = data.get('birthDate', '')
            age = 0
            if birth_date:
                from datetime import datetime
                try:
                    birth = datetime.strptime(birth_date, '%Y-%m-%d')
                    age = (datetime.now() - birth).days // 365
                except:
                    age = 25  # Default

            # Get career stats
            career_stats = data.get('featuredStats', {}).get('regularSeason', {}).get('career', {})
            goals = career_stats.get('goals', 0)
            assists = career_stats.get('assists', 0)
            points = career_stats.get('points', 0)
            games = career_stats.get('gamesPlayed', 0)

            # Get draft info
            draft = data.get('draftDetails', {})
            draft_round = draft.get('round', 0)
            draft_pick = draft.get('pickInRound', 0)
            draft_year = draft.get('year', 0)
            draft_overall = draft.get('overallPick', 0)

            # Height/Weight
            height = data.get('heightInInches', 72)
            weight = data.get('weightInPounds', 200)

            return {
                'name': f"{first_name} {last_name}",
                'position': position,
                'team': team,
                'team_name': team_name,
                'age': age,
                'goals': goals,
                'assists': assists,
                'points': points,
                'games': games,
                'draft_year': draft_year,
                'draft_round': draft_round,
                'draft_pick': draft_pick,
                'draft_overall': draft_overall,
                'height': height,
                'weight': weight,
                'ppg': round(points / games, 2) if games > 0 else 0
            }
    except Exception as e:
        print(f"Error fetching player {player_id}: {e}")
    return None

def search_nhl_player(query):
    """Search for an NHL player using the cached roster data"""
    global NHL_ROSTER_CACHE, NHL_ROSTER_LOADED

    # Load cache if not already loaded
    if not NHL_ROSTER_LOADED:
        load_all_nhl_rosters()

    query = query.lower().strip()
    matches = []

    # Search the cache - much faster than 32 API calls!
    for player in NHL_ROSTER_CACHE:
        player_name = player.get('name', '').lower()
        first_name = player.get('first_name', '').lower()
        last_name = player.get('last_name', '').lower()

        # Check various matching strategies
        if query in player_name:
            matches.append(player)
        elif query == last_name:  # Exact last name match
            matches.append(player)
        elif query == first_name:  # Exact first name match
            matches.append(player)
        elif similarity_score(query, player_name) > 0.7:
            matches.append(player)
        elif similarity_score(query, last_name) > 0.8:
            matches.append(player)

    return matches

def determine_player_archetype(player_info):
    """Determine the best archetype for a player based on their stats and position"""
    position = player_info.get('position', 'C')
    age = player_info.get('age', 25)
    ppg = player_info.get('ppg', 0)
    games = player_info.get('games', 0)
    goals = player_info.get('goals', 0)
    assists = player_info.get('assists', 0)
    draft_overall = player_info.get('draft_overall', 100)

    # Goalie
    if position == 'G':
        return 'starting_goalie'

    # Defenseman
    if position == 'D':
        if ppg > 0.6:
            return 'offensive_defenseman'
        else:
            return 'shutdown_defenseman'

    # Forwards
    # Young star (under 23, high draft pick or high PPG)
    if age <= 23 and (draft_overall <= 10 or ppg > 0.8):
        return 'young_star'

    # Veteran leader (over 32, significant games)
    if age >= 32 and games > 500:
        return 'veteran_leader'

    # Elite center (high PPG, plays center)
    if position == 'C' and ppg > 0.9:
        return 'elite_center'

    # Goal scorer (goals > assists significantly)
    if goals > 0 and goals > assists * 1.2:
        return 'goal_scorer'

    # Playmaker (assists > goals significantly)
    if assists > 0 and assists > goals * 1.3:
        return 'playmaker'

    # Power forward (bigger player, moderate scoring)
    if player_info.get('weight', 200) > 210 and ppg > 0.3:
        return 'power_forward'

    # Defensive forward (low ppg, still gets ice time)
    if ppg < 0.4 and games > 100:
        return 'defensive_forward'

    # Grinder (4th line type)
    if ppg < 0.3:
        return 'grinder'

    # Default to goal scorer for forwards
    return 'goal_scorer'

def generate_player_comparison(player_info):
    """Generate cross-sport comparisons for any NHL player"""
    archetype = determine_player_archetype(player_info)
    arch_data = PLAYER_ARCHETYPES.get(archetype, PLAYER_ARCHETYPES['goal_scorer'])

    name = player_info.get('name', 'Unknown')
    team = player_info.get('team_name', player_info.get('team', ''))
    position = player_info.get('position', '')
    age = player_info.get('age', 0)
    ppg = player_info.get('ppg', 0)
    goals = player_info.get('goals', 0)
    assists = player_info.get('assists', 0)
    draft_overall = player_info.get('draft_overall', 0)

    # Randomly pick one comparison per sport from the options
    soccer_comp = random.choice(arch_data['soccer'])
    nba_comp = random.choice(arch_data['nba'])
    nfl_comp = random.choice(arch_data['nfl'])
    mlb_comp = random.choice(arch_data['mlb'])

    # Build position description
    pos_map = {'C': 'Center', 'L': 'Left Wing', 'R': 'Right Wing', 'D': 'Defenseman', 'G': 'Goaltender'}
    full_position = pos_map.get(position, position)

    # Build style description
    style_parts = []
    if draft_overall > 0 and draft_overall <= 5:
        style_parts.append(f"Top-5 pick (#{draft_overall} overall)")
    elif draft_overall > 0 and draft_overall <= 15:
        style_parts.append(f"First-round pick (#{draft_overall} overall)")

    if ppg > 1.0:
        style_parts.append("elite scorer")
    elif ppg > 0.7:
        style_parts.append("strong offensive player")
    elif ppg > 0.4:
        style_parts.append("solid contributor")
    else:
        style_parts.append("role player")

    style_parts.append(arch_data['description'])

    # Build accolades
    accolades_parts = []
    if goals > 0:
        accolades_parts.append(f"{goals} career goals")
    if assists > 0:
        accolades_parts.append(f"{assists} career assists")
    if player_info.get('games', 0) > 500:
        accolades_parts.append(f"{player_info.get('games')}+ games played")

    return {
        'position': full_position,
        'team': team,
        'age': age,
        'style': ', '.join(style_parts),
        'accolades': ', '.join(accolades_parts) if accolades_parts else "Current NHL player",
        'archetype': archetype,
        'soccer': {
            'player': soccer_comp['player'],
            'team': soccer_comp['team'],
            'explanation': f"{name} plays like {soccer_comp['player']} - {soccer_comp['style']}. Both are {arch_data['description'].lower()}s who impact the game in similar ways."
        },
        'nba': {
            'player': nba_comp['player'],
            'team': nba_comp['team'],
            'explanation': f"The NBA equivalent is {nba_comp['player']} - {nba_comp['style']}. Like {name}, they bring a {arch_data['description'].lower()} approach to their team."
        },
        'nfl': {
            'player': nfl_comp['player'],
            'team': nfl_comp['team'],
            'explanation': f"Think of {nfl_comp['player']} - {nfl_comp['style']}. {name} fills a similar role as a {arch_data['description'].lower()}."
        },
        'mlb': {
            'player': mlb_comp['player'],
            'team': mlb_comp['team'],
            'explanation': f"In baseball terms, {name} is like {mlb_comp['player']} - {mlb_comp['style']}. Both are {arch_data['description'].lower()}s."
        }
    }

# =============================================================================
# GENERAL HOCKEY Q&A - For questions that don't match specific concepts
# =============================================================================

GENERAL_HOCKEY_QA = {
    "periods": {
        "question_keywords": ["period", "periods", "how long", "quarters", "halves", "game length"],
        "answer": "Hockey has 3 periods of 20 minutes each (60 minutes total), with 18-minute intermissions between periods.",
        "soccer": "Unlike soccer's two 45-minute halves, hockey has three 20-minute periods. The intermissions allow for ice resurfacing.",
        "nba": "Similar to quarters in basketball, but hockey has 3 periods instead of 4. Each period is 20 minutes of game time.",
        "nfl": "Like football quarters but only 3 of them. The clock stops frequently for stoppages, so games last about 2.5 hours total.",
        "mlb": "Unlike baseball's 9 innings, hockey has 3 set periods. There's always a guaranteed 60 minutes of play (barring overtime)."
    },
    "roster": {
        "question_keywords": ["roster", "players", "how many", "team size", "lineup", "skaters"],
        "answer": "Teams dress 20 players for a game: 12 forwards (4 lines of 3), 6 defensemen (3 pairs), and 2 goalies. Only 6 players are on ice at once (5 skaters + 1 goalie).",
        "soccer": "Like soccer's 11 on the pitch, hockey has 6 on the ice. But hockey has unlimited substitutions happening constantly.",
        "nba": "Similar to 5 players on court, hockey has 5 skaters plus a goalie. Teams rotate lines every 45 seconds.",
        "nfl": "Like how NFL rotates offensive/defensive units, hockey rotates 'lines' - but the changes happen during live play.",
        "mlb": "Unlike baseball's 9 fixed positions, hockey players rotate in and out constantly. Same positions, different personnel."
    },
    "scoring": {
        "question_keywords": ["score", "scoring", "points", "goals per game", "high scoring", "low scoring"],
        "answer": "NHL games typically see 5-7 total goals. A 3-2 or 4-3 game is common. Shutouts (0 goals) happen but are notable achievements.",
        "soccer": "More goals than soccer on average. A typical NHL game has 5-6 total goals compared to soccer's 2-3.",
        "nba": "Much lower scoring than basketball. A hat trick (3 goals) by one player is celebrated; NBA players score 20+ routinely.",
        "nfl": "Similar scoring rhythm to football touchdowns. 3-4 goals per team is a solid offensive performance.",
        "mlb": "More consistent scoring than baseball. You rarely see 10-1 blowouts in hockey like you do in MLB."
    },
    "season": {
        "question_keywords": ["season", "games", "how many games", "schedule", "playoffs"],
        "answer": "The NHL regular season is 82 games (October-April). 16 teams make the playoffs, which run April-June with best-of-7 series.",
        "soccer": "Longer than Premier League's 38 games. NHL plays 82 games plus potentially 28 playoff games.",
        "nba": "Same 82-game regular season as NBA. Playoffs are also best-of-7, can go to 4 rounds.",
        "nfl": "Much longer than NFL's 17 games. Hockey players play almost daily at times during the season.",
        "mlb": "Shorter than MLB's 162 games but still a marathon. The Stanley Cup Playoffs are legendary for intensity."
    },
    "positions": {
        "question_keywords": ["position", "positions", "forward", "defense", "wing", "centre", "center"],
        "answer": "Hockey has 3 forwards (Left Wing, Center, Right Wing), 2 Defensemen, and 1 Goalie on the ice. Centers take faceoffs, wings play the sides, D-men protect the goal.",
        "soccer": "Think of it like: Wings = Wingers, Center = Midfielder, Defense = Center Backs, Goalie = Goalkeeper.",
        "nba": "Center is like a point guard (playmaker). Wings are like shooting guards. Defensemen are like power forwards protecting the paint.",
        "nfl": "Centers are like quarterbacks (run the offense). Wings are receivers. Defensemen are linebackers. Goalie is the last safety.",
        "mlb": "Different structure, but Center = shortstop (controls the middle), Wings = outfielders, Defense = corner infielders."
    },
    "equipment": {
        "question_keywords": ["equipment", "gear", "pads", "helmet", "skates", "what do they wear"],
        "answer": "Players wear: helmet with visor, shoulder pads, elbow pads, gloves, pants with hip/thigh pads, shin guards, and skates. Goalies wear even more protection.",
        "soccer": "Much more equipment than soccer. Hockey players are padded like NFL players but also on skates.",
        "nba": "Way more gear than basketball. The puck is hard rubber at 100mph, so protection is essential.",
        "nfl": "Similar padding philosophy to football. Helmet, shoulder pads, but also specialized skates and a stick.",
        "mlb": "Think of goalie equipment like catcher's gear but even more. Skaters wear pads like football players."
    },
    "rink": {
        "question_keywords": ["rink", "ice", "size", "arena", "how big", "dimensions"],
        "answer": "NHL rinks are 200 feet long by 85 feet wide. The ice is kept at 22°F (-5.5°C). Boards surround the ice with glass/plexiglas above.",
        "soccer": "Much smaller than a soccer pitch. Hockey rinks are enclosed by boards, so the puck never goes out of play (except over the glass).",
        "nba": "Slightly bigger than an NBA court. The boards create a unique enclosed playing surface.",
        "nfl": "About 1/5 the length of a football field. The compact space makes the game extremely fast.",
        "mlb": "Enclosed unlike a baseball diamond. No foul territory - everything is in play off the boards."
    },
    "rules": {
        "question_keywords": ["rules", "basic rules", "how to play", "objective", "goal of the game"],
        "answer": "Score more goals than the opponent in 60 minutes. Use sticks to pass/shoot the puck. Various rules prevent dangerous play. If tied, overtime and/or shootout.",
        "soccer": "Same basic objective as soccer - put the ball (puck) in the net more than the other team.",
        "nba": "Like basketball, it's about scoring more than the opponent. But goals are harder - average is 3 per team per game.",
        "nfl": "Like football's objective but continuous play. No downs or possessions - just flowing action with line changes.",
        "mlb": "Unlike baseball's turn-based play, hockey is continuous. Both teams attack and defend simultaneously."
    },
    "salary cap": {
        "question_keywords": ["salary", "cap", "money", "contracts", "how much", "paid"],
        "answer": "The NHL has a hard salary cap (around $83.5 million in 2024-25). All teams must stay under this limit, creating parity.",
        "soccer": "Unlike Premier League with no cap, NHL has strict spending limits. Every team operates on similar budgets.",
        "nba": "Similar to NBA's cap system but stricter. No luxury tax - you simply can't exceed the cap.",
        "nfl": "Very similar to NFL's hard cap. Teams must manage contracts carefully to build competitive rosters.",
        "mlb": "Unlike MLB's luxury tax system, NHL teams MUST stay under the cap. No buying championships."
    },
    "draft": {
        "question_keywords": ["draft", "drafted", "prospects", "lottery", "picks"],
        "answer": "The NHL Draft has 7 rounds. The Draft Lottery determines the top picks, with worse teams having better odds (but not guaranteed). Top prospects are usually 18 years old.",
        "soccer": "Unlike soccer's transfer system, NHL uses a draft like American sports. Teams select exclusive rights to young players.",
        "nba": "Very similar to NBA draft but 7 rounds instead of 2. Lottery system for bottom teams.",
        "nfl": "Similar to NFL draft but players come from junior hockey leagues, not college.",
        "mlb": "Like MLB draft but shorter. Players are usually NHL-ready within 1-3 years, not 3-5 like baseball."
    },
    "minor leagues": {
        "question_keywords": ["minor league", "ahl", "farm team", "development", "juniors"],
        "answer": "The AHL (American Hockey League) is the NHL's primary minor league. Teams also have players in the ECHL and junior leagues (OHL, WHL, QMJHL).",
        "soccer": "Like how Premier League clubs have academy systems and loan players out. The AHL is the equivalent of the Championship level.",
        "nba": "Similar to the G-League. Top prospects develop in the AHL before getting NHL roster spots.",
        "nfl": "Like practice squad players, but they play real games in the AHL. More development time than NFL.",
        "mlb": "Similar to baseball's minor league system (AAA, AA, etc.). The AHL is like Triple-A."
    },
    "trades": {
        "question_keywords": ["trade", "trades", "deadline", "traded", "deals"],
        "answer": "Teams can trade players and draft picks. The Trade Deadline is in early March. Trades can include cap retention and conditional picks.",
        "soccer": "Unlike soccer's transfer windows, NHL trades happen anytime until the deadline. No transfer fees - just player/pick swaps.",
        "nba": "Very similar to NBA trades. Salary matching is important due to the cap.",
        "nfl": "Like NFL trades but more common. Hockey teams frequently move players, especially at the deadline.",
        "mlb": "Similar deadline concept. Contenders load up for playoff runs by trading prospects for veterans."
    }
}

def find_general_answer(query):
    """Find a general hockey answer for common questions"""
    query = query.lower()

    for topic, qa_data in GENERAL_HOCKEY_QA.items():
        for keyword in qa_data['question_keywords']:
            if keyword in query:
                return {
                    'topic': topic,
                    'answer': qa_data['answer'],
                    'soccer': qa_data.get('soccer', ''),
                    'nba': qa_data.get('nba', ''),
                    'nfl': qa_data.get('nfl', ''),
                    'mlb': qa_data.get('mlb', '')
                }

    return None

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/concepts')
def list_concepts():
    """Return list of all concepts"""
    return jsonify({
        'concepts': get_all_concepts(),
        'categories': {
            'rules': ['offside', 'icing', 'the crease', 'blue line'],
            'gameplay': ['power play', 'penalty kill', 'face-off', 'line change', 'checking'],
            'scoring': ['hat trick', 'assist', 'one-timer', 'slap shot', 'wrist shot', 'breakaway', 'deke'],
            'situations': ['overtime', 'goalie pull', 'fighting', 'penalty box'],
            'basics': ['puck', 'hockey stick', 'goaltender', 'zamboni', 'stanley cup', 'shutout']
        }
    })

@app.route('/api/players')
def list_players():
    """Return list of curated players + note about API search"""
    return jsonify({
        'players': get_all_players(),
        'note': 'Search for any current NHL player by name'
    })

@app.route('/api/explain/<path:query>')
def explain_concept(query):
    """Explain a hockey concept with sport analogies - with intelligent matching"""
    query = query.lower().replace('-', ' ').replace('_', ' ').strip()

    # 1. Try general Q&A matching FIRST (for questions like "how many periods")
    general_answer = find_general_answer(query)
    if general_answer:
        return jsonify({
            'found': True,
            'concept': general_answer['topic'],
            'data': {
                'definition': general_answer['answer'],
                'soccer': {
                    'analogy': 'Soccer Comparison',
                    'explanation': general_answer['soccer'],
                    'key_difference': ''
                },
                'nba': {
                    'analogy': 'NBA Comparison',
                    'explanation': general_answer['nba'],
                    'key_difference': ''
                },
                'nfl': {
                    'analogy': 'NFL Comparison',
                    'explanation': general_answer['nfl'],
                    'key_difference': ''
                },
                'mlb': {
                    'analogy': 'MLB Comparison',
                    'explanation': general_answer['mlb'],
                    'key_difference': ''
                }
            },
            'match_type': 'general'
        })

    # 2. Try concept matching (exact + fuzzy)
    concept_name, concept_data = find_concept_match(query)
    if concept_name and concept_data:
        return jsonify({
            'found': True,
            'concept': concept_name,
            'data': concept_data,
            'match_type': 'concept'
        })

    # 3. Suggest related concepts
    related = search_concept(query)
    all_concepts = get_all_concepts()

    return jsonify({
        'found': False,
        'query': query,
        'suggestions': related[:5] if related else all_concepts[:8],
        'message': f"I don't have a specific entry for '{query}', but try these related topics or ask about: {', '.join(all_concepts[:6])}..."
    })

@app.route('/api/compare/<path:player>')
def compare_player(player):
    """Compare a hockey player to players in other sports - with NHL API fallback"""
    player_query = player.lower().strip()

    # 1. Check curated comparisons first (these have detailed, custom write-ups)
    if player_query in PLAYER_COMPARISONS:
        return jsonify({
            'found': True,
            'player': player_query.title(),
            'data': PLAYER_COMPARISONS[player_query],
            'source': 'curated'
        })

    # 2. Fuzzy search in curated database
    matches = search_player(player_query)
    if matches:
        best_match = matches[0]
        return jsonify({
            'found': True,
            'player': best_match.title(),
            'data': PLAYER_COMPARISONS[best_match],
            'source': 'curated',
            'did_you_mean': [m.title() for m in matches] if len(matches) > 1 else None
        })

    # 3. Search NHL API for any current player
    nhl_matches = search_nhl_player(player_query)
    if nhl_matches:
        # Get detailed info for the first match
        best_match = nhl_matches[0]
        player_details = fetch_player_details(best_match['id'])

        if player_details:
            comparison_data = generate_player_comparison(player_details)
            return jsonify({
                'found': True,
                'player': player_details['name'],
                'data': comparison_data,
                'source': 'nhl_api',
                'api_note': 'Comparison generated based on player stats and profile'
            })

    # 4. Not found - provide suggestions
    return jsonify({
        'found': False,
        'query': player,
        'suggestions': [p.title() for p in list(PLAYER_COMPARISONS.keys())[:8]],
        'message': f"Couldn't find '{player}'. Try searching by full name (first and last). Featured players: {', '.join([p.title() for p in list(PLAYER_COMPARISONS.keys())[:4]])}..."
    })

@app.route('/api/random')
def random_fact():
    """Return a random concept or comparison based on requested type"""
    # Get the requested type from query parameter (defaults to random choice)
    requested_type = request.args.get('type', None)

    all_concepts = {**HOCKEY_CONCEPTS, **ADDITIONAL_CONCEPTS}

    # If type specified, use it; otherwise pick randomly
    if requested_type == 'concepts':
        choice = 'concept'
    elif requested_type == 'players':
        choice = 'player'
    else:
        choice = random.choice(['concept', 'concept', 'player'])  # Weight towards concepts

    if choice == 'concept':
        concept = random.choice(list(all_concepts.keys()))
        return jsonify({
            'type': 'concept',
            'name': concept,
            'data': all_concepts[concept]
        })
    else:
        player = random.choice(list(PLAYER_COMPARISONS.keys()))
        return jsonify({
            'type': 'player',
            'name': player.title(),
            'data': PLAYER_COMPARISONS[player]
        })

@app.route('/api/search')
def search():
    """Universal search endpoint for concepts and players"""
    query = request.args.get('q', '').lower().strip()

    if not query:
        return jsonify({
            'concepts': get_all_concepts()[:10],
            'players': [p.title() for p in get_all_players()]
        })

    results = {
        'concepts': [],
        'players': [],
        'query': query
    }

    # Search concepts
    concept_name, concept_data = find_concept_match(query)
    if concept_name:
        results['concepts'].append({
            'name': concept_name,
            'preview': concept_data.get('definition', '')[:100] + '...'
        })

    # Also add partial matches
    for concept in search_concept(query):
        if concept != concept_name:
            all_concepts = {**HOCKEY_CONCEPTS, **ADDITIONAL_CONCEPTS}
            if concept in all_concepts:
                results['concepts'].append({
                    'name': concept,
                    'preview': all_concepts[concept].get('definition', '')[:100] + '...'
                })

    # Search curated players
    for player_name in PLAYER_COMPARISONS.keys():
        if query in player_name:
            results['players'].append({
                'name': player_name.title(),
                'team': PLAYER_COMPARISONS[player_name].get('team', ''),
                'source': 'curated'
            })

    return jsonify(results)

@app.route('/api/nhl/search/<path:query>')
def search_nhl_api(query):
    """Direct NHL API search for players"""
    matches = search_nhl_player(query)

    return jsonify({
        'found': len(matches) > 0,
        'players': [{'name': m['name'], 'team': m['team'], 'position': m['position']} for m in matches[:10]]
    })

@app.route('/api/admin/refresh-rosters')
def admin_refresh_rosters():
    """Refresh NHL rosters from API (use after trades/roster changes)"""
    try:
        count = refresh_rosters_from_api()
        return jsonify({
            'success': True,
            'message': f'Refreshed {count} players from NHL API',
            'player_count': count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/roster-status')
def admin_roster_status():
    """Check roster cache status"""
    return jsonify({
        'loaded': NHL_ROSTER_LOADED,
        'player_count': len(NHL_ROSTER_CACHE),
        'sample_players': [p['name'] for p in NHL_ROSTER_CACHE[:5]] if NHL_ROSTER_CACHE else []
    })

# =============================================================================
# MEET THE SHARKS ROUTES - Live Data from NHL API
# =============================================================================

# Cache for live Sharks data
SHARKS_LIVE_CACHE = {
    'roster': None,
    'stats': {},
    'last_updated': None
}

def fetch_live_sharks_roster():
    """Fetch current Sharks roster from NHL API with stats"""
    import requests
    from datetime import datetime

    # Check cache (refresh every 10 minutes)
    if SHARKS_LIVE_CACHE['roster'] and SHARKS_LIVE_CACHE['last_updated']:
        age = (datetime.now() - SHARKS_LIVE_CACHE['last_updated']).seconds
        if age < 600:  # 10 minutes
            return SHARKS_LIVE_CACHE['roster']

    try:
        # Fetch roster
        roster_url = "https://api-web.nhle.com/v1/roster/SJS/current"
        resp = requests.get(roster_url, timeout=10)
        if resp.status_code != 200:
            return None

        roster_data = resp.json()
        players = []

        # Process forwards, defensemen, goalies
        for position_group in ['forwards', 'defensemen', 'goalies']:
            for player in roster_data.get(position_group, []):
                player_id = player.get('id')
                first_name = player.get('firstName', {}).get('default', '')
                last_name = player.get('lastName', {}).get('default', '')
                full_name = f"{first_name} {last_name}"

                # Get headshot URL - use local static files for instant loading
                headshot = f"/static/headshots/{player_id}.png"

                # Position mapping
                pos_code = player.get('positionCode', '')
                position_map = {
                    'C': 'Center', 'L': 'Left Wing', 'R': 'Right Wing',
                    'D': 'Defenseman', 'G': 'Goalie'
                }
                position = position_map.get(pos_code, pos_code)

                players.append({
                    'id': player_id,
                    'name': full_name,
                    'number': player.get('sweaterNumber', 0),
                    'position': position,
                    'position_code': pos_code,
                    'headshot': headshot,
                    'height': player.get('heightInInches', 0),
                    'weight': player.get('weightInPounds', 0),
                    'birth_date': player.get('birthDate', ''),
                    'birth_city': player.get('birthCity', {}).get('default', ''),
                    'birth_country': player.get('birthCountry', ''),
                    'shoots_catches': player.get('shootsCatches', '')
                })

        # Sort by jersey number
        players.sort(key=lambda x: x['number'] if x['number'] else 99)

        SHARKS_LIVE_CACHE['roster'] = players
        SHARKS_LIVE_CACHE['last_updated'] = datetime.now()

        return players

    except Exception as e:
        print(f"Error fetching Sharks roster: {e}")
        return None

def fetch_player_stats(player_id):
    """Fetch current season stats for a player"""
    import requests

    # Check cache
    if player_id in SHARKS_LIVE_CACHE['stats']:
        return SHARKS_LIVE_CACHE['stats'][player_id]

    try:
        url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None

        data = resp.json()

        # Get current season stats
        featured_stats = data.get('featuredStats', {})
        current_season = featured_stats.get('regularSeason', {}).get('subSeason', {})
        career_stats = featured_stats.get('regularSeason', {}).get('career', {})

        # Get draft info
        draft_details = data.get('draftDetails', {})
        draft_info = None
        if draft_details:
            draft_info = f"Round {draft_details.get('round', '?')}, Pick {draft_details.get('pickInRound', '?')} ({draft_details.get('year', '?')})"

        stats = {
            'current_season': current_season,
            'career': career_stats,
            'draft': draft_info,
            'birth_date': data.get('birthDate', ''),
            'birth_city': data.get('birthCity', {}).get('default', ''),
            'birth_country': data.get('birthCountry', ''),
            'height_inches': data.get('heightInInches', 0),
            'weight_lbs': data.get('weightInPounds', 0),
            'position': data.get('position', '')
        }

        SHARKS_LIVE_CACHE['stats'][player_id] = stats
        return stats

    except Exception as e:
        print(f"Error fetching player stats: {e}")
        return None

def calculate_age(birth_date):
    """Calculate age from birth date string"""
    from datetime import datetime
    try:
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age
    except:
        return None

@app.route('/api/sharks')
def get_sharks_roster():
    """Get all Sharks players with live data from NHL API"""
    # Try to get live data first
    live_roster = fetch_live_sharks_roster()

    if live_roster:
        players = []
        for player in live_roster:
            # Get curated role if available
            name_lower = player['name'].lower()
            curated = SHARKS_ROSTER.get(name_lower, {})
            role = curated.get('role', 'Roster Player')

            age = calculate_age(player['birth_date'])

            players.append({
                'id': player['id'],
                'name': player['name'],
                'number': player['number'],
                'position': player['position'],
                'role': role,
                'age': age,
                'headshot': player['headshot']
            })

        return jsonify({
            'team': 'San Jose Sharks',
            'players': players,
            'count': len(players),
            'source': 'live'
        })

    # Fallback to curated data
    players = []
    for name, info in SHARKS_ROSTER.items():
        players.append({
            'name': name.title(),
            'number': info['number'],
            'position': info['position'],
            'role': info['role'],
            'age': info['age'],
            'headshot': None
        })
    players.sort(key=lambda x: x['number'])

    return jsonify({
        'team': 'San Jose Sharks',
        'players': players,
        'count': len(players),
        'source': 'curated'
    })

@app.route('/api/sharks/<path:player>')
def get_shark_player(player):
    """Get detailed info for a specific Sharks player with live stats"""
    from difflib import SequenceMatcher

    player_lower = player.lower().strip()

    # Try to find in live roster first
    live_roster = fetch_live_sharks_roster()
    matched_player = None

    if live_roster:
        # Try exact match
        for p in live_roster:
            if p['name'].lower() == player_lower:
                matched_player = p
                break

        # Try fuzzy match
        if not matched_player:
            best_score = 0
            for p in live_roster:
                score = SequenceMatcher(None, player_lower, p['name'].lower()).ratio()
                if score > best_score:
                    best_score = score
                    matched_player = p

            if best_score < 0.6:
                matched_player = None

    if matched_player:
        # Get live stats
        stats = fetch_player_stats(matched_player['id'])

        # Get curated info if available
        name_lower = matched_player['name'].lower()
        curated = SHARKS_ROSTER.get(name_lower, {})

        # Calculate age
        age = calculate_age(matched_player['birth_date'])

        # Format height
        height_in = matched_player.get('height', 0)
        height_str = f"{height_in // 12}'{height_in % 12}\"" if height_in else None

        # Build response
        response = {
            'found': True,
            'source': 'live',
            'id': matched_player['id'],
            'name': matched_player['name'],
            'number': matched_player['number'],
            'position': matched_player['position'],
            'headshot': matched_player['headshot'],
            'age': age,
            'height': height_str,
            'weight': f"{matched_player.get('weight', 0)} lbs" if matched_player.get('weight') else None,
            'birthplace': f"{matched_player.get('birth_city', '')}, {matched_player.get('birth_country', '')}".strip(', '),
            'shoots': matched_player.get('shoots_catches', '')
        }

        # Add live stats if available
        if stats:
            response['draft'] = stats.get('draft', curated.get('draft', 'Undrafted'))

            current = stats.get('current_season', {})
            if current:
                if matched_player['position'] == 'Goalie':
                    response['stats'] = {
                        'games': current.get('gamesPlayed', 0),
                        'wins': current.get('wins', 0),
                        'losses': current.get('losses', 0),
                        'gaa': round(current.get('goalsAgainstAvg', 0), 2),
                        'save_pct': round(current.get('savePctg', 0) * 100, 1) if current.get('savePctg') else 0,
                        'shutouts': current.get('shutouts', 0)
                    }
                else:
                    response['stats'] = {
                        'games': current.get('gamesPlayed', 0),
                        'goals': current.get('goals', 0),
                        'assists': current.get('assists', 0),
                        'points': current.get('points', 0),
                        'plus_minus': current.get('plusMinus', 0),
                        'pim': current.get('pim', 0)
                    }

            career = stats.get('career', {})
            if career:
                if matched_player['position'] == 'Goalie':
                    response['career_stats'] = {
                        'games': career.get('gamesPlayed', 0),
                        'wins': career.get('wins', 0),
                        'gaa': round(career.get('goalsAgainstAvg', 0), 2),
                        'save_pct': round(career.get('savePctg', 0) * 100, 1) if career.get('savePctg') else 0
                    }
                else:
                    response['career_stats'] = {
                        'games': career.get('gamesPlayed', 0),
                        'goals': career.get('goals', 0),
                        'assists': career.get('assists', 0),
                        'points': career.get('points', 0)
                    }

        # Add curated content if available
        if curated:
            response['role'] = curated.get('role', 'Roster Player')
            response['role_description'] = curated.get('role_description', '')
            response['play_style'] = curated.get('play_style', '')
            response['fun_fact'] = curated.get('fun_fact', '')
            response['comparisons'] = {
                'soccer': curated.get('soccer_comp', {}),
                'nba': curated.get('nba_comp', {}),
                'nfl': curated.get('nfl_comp', {}),
                'mlb': curated.get('mlb_comp', {})
            }
        else:
            response['role'] = 'Roster Player'
            response['role_description'] = f"A key member of the Sharks roster at {matched_player['position']}."
            response['play_style'] = ''
            response['fun_fact'] = ''
            response['comparisons'] = {}

        return jsonify(response)

    # Fallback to curated data only
    if player_lower in SHARKS_ROSTER:
        info = SHARKS_ROSTER[player_lower]
        return jsonify({
            'found': True,
            'source': 'curated',
            'name': player_lower.title(),
            'number': info['number'],
            'position': info['position'],
            'age': info['age'],
            'from': info['from'],
            'draft': info['draft'],
            'role': info['role'],
            'role_description': info['role_description'],
            'play_style': info['play_style'],
            'fun_fact': info['fun_fact'],
            'comparisons': {
                'soccer': info['soccer_comp'],
                'nba': info['nba_comp'],
                'nfl': info['nfl_comp'],
                'mlb': info['mlb_comp']
            }
        })

    # Try fuzzy match on curated
    best_match = None
    best_score = 0
    for name in SHARKS_ROSTER.keys():
        score = SequenceMatcher(None, player_lower, name).ratio()
        if score > best_score:
            best_score = score
            best_match = name

    if best_match and best_score > 0.6:
        info = SHARKS_ROSTER[best_match]
        return jsonify({
            'found': True,
            'source': 'curated',
            'name': best_match.title(),
            'number': info['number'],
            'position': info['position'],
            'age': info['age'],
            'from': info['from'],
            'draft': info['draft'],
            'role': info['role'],
            'role_description': info['role_description'],
            'play_style': info['play_style'],
            'fun_fact': info['fun_fact'],
            'comparisons': {
                'soccer': info['soccer_comp'],
                'nba': info['nba_comp'],
                'nfl': info['nfl_comp'],
                'mlb': info['mlb_comp']
            }
        })

    return jsonify({
        'found': False,
        'error': f"Player '{player}' not found in Sharks roster"
    })

# =============================================================================
# STATS GLOSSARY ROUTES
# =============================================================================

@app.route('/api/stats')
def get_stats_glossary():
    """Get all stats with basic info"""
    stats = []
    for stat_name, info in STATS_GLOSSARY.items():
        stats.append({
            'name': stat_name.replace('_', ' ').title(),
            'abbrev': info.get('abbrev', ''),
            'short_def': info['definition'][:100] + '...' if len(info['definition']) > 100 else info['definition']
        })
    return jsonify({
        'stats': stats,
        'count': len(stats)
    })

@app.route('/api/stats/<path:stat>')
def get_stat_detail(stat):
    """Get detailed explanation for a specific stat"""
    stat_lower = stat.lower().strip().replace(' ', '_').replace('-', '_')

    # Handle common variations
    stat_variations = {
        'plus_minus': 'plus_minus',
        'plus/minus': 'plus_minus',
        '+/-': 'plus_minus',
        'plusminus': 'plus_minus',
        'save_percentage': 'save_percentage',
        'save%': 'save_percentage',
        'sv%': 'save_percentage',
        'gaa': 'goals_against_average',
        'goals_against': 'goals_against_average',
        'pdo': 'pdo',
        'toi': 'time_on_ice'
    }

    if stat_lower in stat_variations:
        stat_lower = stat_variations[stat_lower]

    if stat_lower in STATS_GLOSSARY:
        info = STATS_GLOSSARY[stat_lower]
        return jsonify({
            'found': True,
            'name': stat_lower.replace('_', ' ').title(),
            'abbrev': info.get('abbrev', ''),
            'definition': info['definition'],
            'good_number': info.get('good_number', ''),
            'analogies': {
                'soccer': info.get('soccer', ''),
                'nba': info.get('nba', ''),
                'nfl': info.get('nfl', ''),
                'mlb': info.get('mlb', '')
            }
        })

    # Try fuzzy match
    from difflib import SequenceMatcher
    best_match = None
    best_score = 0

    for name in STATS_GLOSSARY.keys():
        score = SequenceMatcher(None, stat_lower, name).ratio()
        if score > best_score:
            best_score = score
            best_match = name

    if best_match and best_score > 0.5:
        info = STATS_GLOSSARY[best_match]
        return jsonify({
            'found': True,
            'name': best_match.replace('_', ' ').title(),
            'abbrev': info.get('abbrev', ''),
            'definition': info['definition'],
            'good_number': info.get('good_number', ''),
            'analogies': {
                'soccer': info.get('soccer', ''),
                'nba': info.get('nba', ''),
                'nfl': info.get('nfl', ''),
                'mlb': info.get('mlb', '')
            }
        })

    return jsonify({
        'found': False,
        'error': f"Stat '{stat}' not found",
        'available_stats': [name.replace('_', ' ').title() for name in STATS_GLOSSARY.keys()]
    })

# =============================================================================
# HOCKEY DICTIONARY ROUTES
# =============================================================================

@app.route('/api/dictionary')
def get_dictionary():
    """Get all dictionary terms grouped by category"""
    by_category = {}

    for term, info in HOCKEY_DICTIONARY.items():
        category = info.get('category', 'general')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append({
            'term': term.replace('_', ' ').title(),
            'short_def': info['definition'][:80] + '...' if len(info['definition']) > 80 else info['definition']
        })

    # Sort terms within each category
    for category in by_category:
        by_category[category].sort(key=lambda x: x['term'])

    return jsonify({
        'categories': by_category,
        'total_terms': len(HOCKEY_DICTIONARY)
    })

@app.route('/api/dictionary/<path:term>')
def get_dictionary_term(term):
    """Get definition for a specific term"""
    term_lower = term.lower().strip().replace(' ', '_').replace('-', '_')

    if term_lower in HOCKEY_DICTIONARY:
        info = HOCKEY_DICTIONARY[term_lower]
        has_analogies = 'soccer' in info

        result = {
            'found': True,
            'term': term_lower.replace('_', ' ').title(),
            'definition': info['definition'],
            'category': info.get('category', 'general')
        }

        if has_analogies:
            result['analogies'] = {
                'soccer': info.get('soccer', {}),
                'nba': info.get('nba', {}),
                'nfl': info.get('nfl', {}),
                'mlb': info.get('mlb', {})
            }

        return jsonify(result)

    # Try fuzzy match
    from difflib import SequenceMatcher
    best_match = None
    best_score = 0

    for name in HOCKEY_DICTIONARY.keys():
        score = SequenceMatcher(None, term_lower, name).ratio()
        if score > best_score:
            best_score = score
            best_match = name

    if best_match and best_score > 0.5:
        info = HOCKEY_DICTIONARY[best_match]
        has_analogies = 'soccer' in info

        result = {
            'found': True,
            'term': best_match.replace('_', ' ').title(),
            'definition': info['definition'],
            'category': info.get('category', 'general')
        }

        if has_analogies:
            result['analogies'] = {
                'soccer': info.get('soccer', {}),
                'nba': info.get('nba', {}),
                'nfl': info.get('nfl', {}),
                'mlb': info.get('mlb', {})
            }

        return jsonify(result)

    return jsonify({
        'found': False,
        'error': f"Term '{term}' not found",
        'suggestion': 'Try browsing by category at /api/dictionary'
    })

# =============================================================================
# RINK MAP ROUTES
# =============================================================================

@app.route('/api/rink')
def get_rink_zones():
    """Get all rink zones for the interactive map"""
    zones = []
    for zone_id, info in RINK_ZONES.items():
        zones.append({
            'id': zone_id,
            'name': info['name'],
            'description': info['description'][:100] + '...' if len(info['description']) > 100 else info['description']
        })
    return jsonify({
        'zones': zones,
        'count': len(zones)
    })

@app.route('/api/rink/<path:zone>')
def get_rink_zone(zone):
    """Get detailed info for a specific rink zone"""
    zone_lower = zone.lower().strip().replace(' ', '_').replace('-', '_')

    if zone_lower in RINK_ZONES:
        info = RINK_ZONES[zone_lower]
        return jsonify({
            'found': True,
            'id': zone_lower,
            'name': info['name'],
            'description': info['description'],
            'purpose': info['purpose'],
            'fun_fact': info['fun_fact'],
            'analogies': {
                'soccer': info.get('soccer', ''),
                'nba': info.get('nba', ''),
                'nfl': info.get('nfl', ''),
                'mlb': info.get('mlb', '')
            }
        })

    # Try fuzzy match
    from difflib import SequenceMatcher
    best_match = None
    best_score = 0

    for name in RINK_ZONES.keys():
        score = SequenceMatcher(None, zone_lower, name).ratio()
        if score > best_score:
            best_score = score
            best_match = name

    if best_match and best_score > 0.5:
        info = RINK_ZONES[best_match]
        return jsonify({
            'found': True,
            'id': best_match,
            'name': info['name'],
            'description': info['description'],
            'purpose': info['purpose'],
            'fun_fact': info['fun_fact'],
            'analogies': {
                'soccer': info.get('soccer', ''),
                'nba': info.get('nba', ''),
                'nfl': info.get('nfl', ''),
                'mlb': info.get('mlb', '')
            }
        })

    return jsonify({
        'found': False,
        'error': f"Zone '{zone}' not found",
        'available_zones': [name for name in RINK_ZONES.keys()]
    })

def initialize_app():
    """Pre-load NHL rosters at startup so searches are instant"""
    print("Initializing Hockey For Dummies...")
    load_all_nhl_rosters()
    print("Ready to go!")

# Load rosters when app starts (happens during deployment on Render)
with app.app_context():
    initialize_app()

if __name__ == '__main__':
    app.run(debug=True, port=5051)
