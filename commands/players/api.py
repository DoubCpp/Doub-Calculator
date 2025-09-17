import aiohttp
import re
from typing import Optional, List, Dict, Any


class RucoyAPI:
    """API wrapper for data from the Rucoy Online website"""
    
    BASE_URL = "https://www.rucoyonline.com"
    
    @staticmethod
    async def fetch_page(session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """
        Fetch a web page and return its text content
        
        Args:
            session: aiohttp session
            url: URL to fetch
            
        Returns:
            str: Page content or None on error
        """
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    @staticmethod
    def parse_character_data(html_content: str) -> Optional[Dict[str, Any]]:
        """
        Parse character data from HTML
        
        Args:
            html_content: HTML content of the page
            
        Returns:
            dict: Character data or None if not found
        """
        if not html_content:
            return None
            
        character_data = {}
        
        # Character name
        name_match = re.search(r'<h3>([^<]+?)(?:\s*<span|</h3>)', html_content)
        if name_match:
            character_data['name'] = name_match.group(1).strip()
        
        # Level
        level_match = re.search(r'<td>Level</td>\s*<td>(\d+)</td>', html_content)
        if level_match:
            character_data['level'] = int(level_match.group(1))
        
        # Guild
        guild_match = re.search(r'<td>Guild</td>\s*<td><a[^>]*>([^<]+)</a></td>', html_content)
        if guild_match:
            character_data['guild'] = guild_match.group(1).strip()
        else:
            guild_no_link = re.search(r'<td>Guild</td>\s*<td>([^<]+)</td>', html_content)
            if guild_no_link:
                character_data['guild'] = guild_no_link.group(1).strip()
            else:
                character_data['guild'] = "No Guild"
        
        # Title
        title_match = re.search(r'<td>Title</td>\s*<td>\s*([^<\n\r]+)', html_content)
        if title_match:
            character_data['title'] = title_match.group(1).strip()
        
        # Online status
        online_match = re.search(r'<td>Last online</td>\s*<td>\s*([^<\n\r]+)', html_content)
        if online_match:
            last_online = online_match.group(1).strip()
            character_data['last_online'] = last_online
            
            # Detailed detection of online status
            last_online_lower = last_online.lower()
            if any(word in last_online_lower for word in ['online', 'now', 'currently']):
                character_data['online'] = True
                character_data['offline_time'] = "Currently online"
            elif 'minute' in last_online_lower or 'second' in last_online_lower:
                character_data['online'] = True
                character_data['offline_time'] = f"Last seen {last_online}"
            else:
                character_data['online'] = False
                character_data['offline_time'] = f"Last seen {last_online}"
        else:
            character_data['online'] = False
            character_data['offline_time'] = "Unknown"
        
        # Born date
        born_match = re.search(r'<td>Born</td>\s*<td>\s*([^<\n\r]+)', html_content)
        if born_match:
            character_data['born'] = born_match.group(1).strip()
        
        # Check if supporter
        character_data['supporter'] = 'Supporter' in html_content
            
        return character_data if character_data else None
    
    @staticmethod
    def parse_pvp_logs(html_content: str, player_name: str) -> List[Dict[str, Any]]:
        """
        Parse PvP logs from the character page
        
        Args:
            html_content: HTML content
            player_name: Player name
            
        Returns:
            list: List of PvP logs
        """
        if not html_content:
            return []
        
        pvp_logs = []
        
        # Find the PvP logs table
        pvp_table_pattern = r'<table class="character-table[^"]*"[^>]*>.*?<thead[^>]*>.*?<td>Recent character kills and deaths</td>.*?</thead>.*?<tbody>(.*?)</tbody>'
        pvp_table_match = re.search(pvp_table_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        if pvp_table_match:
            tbody_content = pvp_table_match.group(1)
            
            # Extract each entry
            row_pattern = r'<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*</tr>'
            rows = re.findall(row_pattern, tbody_content, re.DOTALL)
            
            for row in rows:
                log_entry = {}
                row = row.strip()
                
                # Check if it's a kill or a death
                if f"{player_name}" in row and "killed" in row and row.index(player_name) < row.index("killed"):
                    # The player killed someone
                    log_entry['type'] = 'kill'
                    log_entry['actor'] = player_name
                    
                    # Extract the victim's name
                    victim_pattern = r'killed\s*<a[^>]*>([^<]+)</a>'
                    victim_match = re.search(victim_pattern, row)
                    if victim_match:
                        log_entry['victim'] = victim_match.group(1).strip()
                    
                    log_entry['killers'] = []
                    
                else:
                    # The player was killed
                    log_entry['type'] = 'death'
                    log_entry['victim'] = player_name
                    log_entry['killers'] = []
                    
                    # Extract killers
                    killed_index = row.find('killed')
                    if killed_index > 0:
                        before_killed = row[:killed_index]
                        killer_pattern = r'<a[^>]*>([^<]+)</a>'
                        killer_matches = re.findall(killer_pattern, before_killed)
                        
                        seen_killers = set()
                        for killer in killer_matches:
                            killer_name = killer.strip()
                            if killer_name not in seen_killers:
                                seen_killers.add(killer_name)
                                log_entry['killers'].append(killer_name)
                
                # Extract time
                time_pattern = r'-\s*([^<]+)$'
                time_match = re.search(time_pattern, row)
                if time_match:
                    log_entry['time_ago'] = time_match.group(1).strip()
                else:
                    log_entry['time_ago'] = 'Unknown'
                
                # Add only valid entries
                if log_entry.get('type') and (log_entry.get('victim') or log_entry.get('killers')):
                    pvp_logs.append(log_entry)
        
        return pvp_logs
    
    @staticmethod
    def parse_leaderboard_data(html_content: str, stat_type: str) -> List[Dict[str, Any]]:
        """
        Parse leaderboard data from HTML
        
        Args:
            html_content: HTML content
            stat_type: Stat type
            
        Returns:
            list: Leaderboard data
        """
        if not html_content:
            return []
            
        leaderboard_data = []
        
    # Find rows in the highscores table
        tbody_pattern = r'<tbody>(.*?)</tbody>'
        tbody_match = re.search(tbody_pattern, html_content, re.DOTALL)
        
        if tbody_match:
            tbody_content = tbody_match.group(1)
            row_pattern = r'<tr[^>]*>(.*?)</tr>'
            rows = re.findall(row_pattern, tbody_content, re.DOTALL)
            
            for row in rows:
                # Extract rank
                rank_match = re.search(r'<td>(\d+)</td>', row)
                if not rank_match:
                    continue
                rank = int(rank_match.group(1))
                
                # Extract player name
                name_match = re.search(r'<a href="/characters/[^"]*">([^<]+)</a>', row)
                if not name_match:
                    continue
                player_name = name_match.group(1).strip()
                
                # Extract the level/stat value
                td_numbers = re.findall(r'<td>(\d+)</td>', row)
                if len(td_numbers) >= 2:
                    level = int(td_numbers[-1])
                    
                    # Check if the player is online
                    online = "Online" in row
                    
                    leaderboard_data.append({
                        'rank': rank,
                        'name': player_name,
                        'level': level,
                        'online': online
                    })
        
        return leaderboard_data[:100]  # Return up to 100 entries

    @staticmethod
    def parse_guild_data(html_content: str) -> Optional[Dict[str, Any]]:
        """
        Parse guild data from HTML
        
        Args:
            html_content: HTML content
            
        Returns:
            dict: Guild data or None
        """
        if not html_content:
            return None
            
        guild_data = {}
        
        # Guild name
        name_match = re.search(r'<h3>([^<]+)</h3>', html_content)
        if name_match:
            guild_data['name'] = name_match.group(1).strip()
        
        # Guild description
        desc_pattern = r'</h3>\s*</div>\s*</div>\s*<p>(.*?)</p>'
        desc_match = re.search(desc_pattern, html_content, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
            description = re.sub(r'\s+', ' ', description)
            guild_data['description'] = description
        
        # Founded date
        founded_match = re.search(r'<i>Founded on ([^<]+)</i>', html_content)
        if founded_match:
            guild_data['founded'] = founded_match.group(1).strip()
        
        # Parse members
        members = []
        tbody_pattern = r'<tbody[^>]*>(.*?)</tbody>'
        tbody_match = re.search(tbody_pattern, html_content, re.DOTALL)
        
        if tbody_match:
            tbody_content = tbody_match.group(1)
            row_pattern = r'<tr[^>]*>(.*?)</tr>'
            rows = re.findall(row_pattern, tbody_content, re.DOTALL)
            
            for row in rows:
                # Extract member name
                name_match = re.search(r'<a href="/characters/[^"]*">([^<]+)</a>', row)
                if not name_match:
                    continue
                member_name = name_match.group(1).strip()
                
                # Check statuses
                is_leader = "(Leader)" in row
                is_supporter = "Supporter" in row
                is_online = "Online" in row
                
                # Extract level
                td_pattern = r'<td>([^<]+)</td>'
                tds = re.findall(td_pattern, row)
                
                level = None
                join_date = None
                
                # Look for level (number)
                for td in tds:
                    if td.strip().isdigit():
                        level = int(td.strip())
                        break
                
                # Look for the join date
                for td in tds:
                    td_clean = td.strip()
                    if any(month in td_clean for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) or \
                       re.match(r'\d{1,2}/\d{1,2}/\d{4}', td_clean) or \
                       re.match(r'\w+ \d{1,2}, \d{4}', td_clean):
                        join_date = td_clean
                        break
                
                members.append({
                    'name': member_name,
                    'level': level or 0,
                    'join_date': join_date or 'Unknown',
                    'is_leader': is_leader,
                    'is_supporter': is_supporter,
                    'is_online': is_online
                })
        
        guild_data['members'] = members
        guild_data['member_count'] = len(members)
        
        return guild_data if guild_data else None