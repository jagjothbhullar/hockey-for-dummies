#!/usr/bin/env python3
"""
Hockey For Dummies - Learn Hockey Through Sports You Know
An interactive tool that explains hockey concepts using analogies from
Soccer (Premier League), NBA, NFL, and MLB.
"""

from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

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
# HELPER FUNCTIONS
# =============================================================================

def get_all_concepts():
    """Return list of all concept names"""
    return list(HOCKEY_CONCEPTS.keys())

def get_all_players():
    """Return list of all player names"""
    return list(PLAYER_COMPARISONS.keys())

def search_concept(query):
    """Search for a concept by keyword"""
    query = query.lower()
    matches = []
    for concept, data in HOCKEY_CONCEPTS.items():
        if query in concept or query in data['definition'].lower():
            matches.append(concept)
    return matches

def search_player(query):
    """Search for a player by name"""
    query = query.lower()
    matches = []
    for player, data in PLAYER_COMPARISONS.items():
        if query in player:
            matches.append(player)
    return matches

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
        'concepts': get_all_concepts()
    })

@app.route('/api/players')
def list_players():
    """Return list of all players"""
    return jsonify({
        'players': get_all_players()
    })

@app.route('/api/explain/<concept>')
def explain_concept(concept):
    """Explain a hockey concept with sport analogies"""
    concept = concept.lower().replace('-', ' ').replace('_', ' ')

    # Direct match
    if concept in HOCKEY_CONCEPTS:
        data = HOCKEY_CONCEPTS[concept]
        return jsonify({
            'found': True,
            'concept': concept,
            'data': data
        })

    # Fuzzy search
    matches = search_concept(concept)
    if matches:
        return jsonify({
            'found': True,
            'concept': matches[0],
            'data': HOCKEY_CONCEPTS[matches[0]],
            'did_you_mean': matches if len(matches) > 1 else None
        })

    return jsonify({
        'found': False,
        'message': f"Couldn't find '{concept}'. Try: {', '.join(list(HOCKEY_CONCEPTS.keys())[:5])}..."
    })

@app.route('/api/compare/<player>')
def compare_player(player):
    """Compare a hockey player to players in other sports"""
    player = player.lower()

    # Direct match
    if player in PLAYER_COMPARISONS:
        data = PLAYER_COMPARISONS[player]
        return jsonify({
            'found': True,
            'player': player.title(),
            'data': data
        })

    # Fuzzy search
    matches = search_player(player)
    if matches:
        return jsonify({
            'found': True,
            'player': matches[0].title(),
            'data': PLAYER_COMPARISONS[matches[0]],
            'did_you_mean': [m.title() for m in matches] if len(matches) > 1 else None
        })

    return jsonify({
        'found': False,
        'message': f"Player not found. Try: {', '.join([p.title() for p in list(PLAYER_COMPARISONS.keys())[:5]])}..."
    })

@app.route('/api/random')
def random_fact():
    """Return a random concept or comparison"""
    choice = random.choice(['concept', 'player'])
    if choice == 'concept':
        concept = random.choice(list(HOCKEY_CONCEPTS.keys()))
        return jsonify({
            'type': 'concept',
            'name': concept,
            'data': HOCKEY_CONCEPTS[concept]
        })
    else:
        player = random.choice(list(PLAYER_COMPARISONS.keys()))
        return jsonify({
            'type': 'player',
            'name': player.title(),
            'data': PLAYER_COMPARISONS[player]
        })

if __name__ == '__main__':
    app.run(debug=True, port=5051)
