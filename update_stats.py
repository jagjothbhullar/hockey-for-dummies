#!/usr/bin/env python3
"""Update sharks_edge_data.json with fresh stats from NHL API."""

import json
import os
import requests
from datetime import datetime

EDGE_FILE = os.path.join(os.path.dirname(__file__), 'sharks_edge_data.json')

def main():
    # Load existing EDGE data to preserve tracking stats
    with open(EDGE_FILE, 'r') as f:
        existing = json.load(f)
    existing_players = existing.get('players', {})

    # Fetch current Sharks roster
    print("Fetching Sharks roster...")
    resp = requests.get("https://api-web.nhle.com/v1/roster/SJS/current", timeout=15)
    resp.raise_for_status()
    roster_data = resp.json()

    all_players = []
    for group in ['forwards', 'defensemen', 'goalies']:
        for p in roster_data.get(group, []):
            pid = p.get('id')
            first = p.get('firstName', {}).get('default', '')
            last = p.get('lastName', {}).get('default', '')
            pos = p.get('positionCode', '')
            all_players.append({'id': pid, 'name': f"{first} {last}", 'pos': pos})

    print(f"Found {len(all_players)} players on roster")

    updated_players = {}

    for player in all_players:
        pid = str(player['id'])
        name = player['name']
        pos = player['pos']

        print(f"  Fetching stats for {name} ({pid})...")
        try:
            resp = requests.get(f"https://api-web.nhle.com/v1/player/{pid}/landing", timeout=10)
            if resp.status_code != 200:
                print(f"    Skipped (HTTP {resp.status_code})")
                continue
            data = resp.json()
        except Exception as e:
            print(f"    Error: {e}")
            continue

        # Extract current season stats
        featured = data.get('featuredStats', {})
        season = featured.get('regularSeason', {}).get('subSeason', {})

        # Build player entry - start with existing EDGE data if available
        entry = {}
        if pid in existing_players:
            entry = dict(existing_players[pid])

        entry['name'] = name
        entry['position'] = pos

        # Update shooting stats from live data
        games = season.get('gamesPlayed', 0)
        if pos == 'G':
            entry['goalie_stats'] = {
                'games': games,
                'wins': season.get('wins', 0),
                'losses': season.get('losses', 0),
                'ot_losses': season.get('otLosses', 0),
                'gaa': season.get('goalsAgainstAvg', 0),
                'save_pct': season.get('savePctg', 0),
                'shutouts': season.get('shutouts', 0),
            }
        else:
            goals = season.get('goals', 0)
            shots = season.get('shots', 0)
            shooting_pct = round((goals / shots * 100), 1) if shots > 0 else 0

            # Update shooting block
            if 'shooting' not in entry:
                entry['shooting'] = {}
            entry['shooting']['shots'] = shots
            entry['shooting']['goals'] = goals
            entry['shooting']['shooting_pct'] = shooting_pct

            # Also store points/assists for reference
            entry['season_stats'] = {
                'games': games,
                'goals': goals,
                'assists': season.get('assists', 0),
                'points': season.get('points', 0),
                'plus_minus': season.get('plusMinus', 0),
                'pim': season.get('penaltyMinutes', 0),
            }

        updated_players[pid] = entry

    # Build final output
    output = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'players': updated_players
    }

    with open(EDGE_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nUpdated {len(updated_players)} players. Saved to {EDGE_FILE}")

if __name__ == '__main__':
    main()
