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
