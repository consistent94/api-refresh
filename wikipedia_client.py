"""
Wikipedia API Client for Historical Figures Explorer

This module handles all interactions with Wikipedia's REST API to extract
biographical data about historical figures.
"""

import requests
import time
from typing import Dict, List, Optional


class WikipediaClient:
    """
    Client for interacting with Wikipedia's REST API.
    
    Provides methods to search for historical figures and extract
    their biographical information including summaries, infobox data,
    and basic metadata.
    """
    
    def __init__(self):
        """Initialize the Wikipedia client with base API URL."""
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self.search_url = "https://en.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HistoricalFiguresExplorer/1.0 (Educational Project)'
        })
    
    def search_figure(self, name: str, limit: int = 5) -> List[Dict]:
        """
        Search for a historical figure by name.
        
        Args:
            name (str): Name of the historical figure to search for
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of search results with titles and snippets
        """
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': name,
                'srlimit': limit,
                'srprop': 'snippet|timestamp'
            }
            
            response = self.session.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'query' in data and 'search' in data['query']:
                for item in data['query']['search']:
                    results.append({
                        'title': item['title'],
                        'snippet': item.get('snippet', ''),
                        'timestamp': item.get('timestamp', '')
                    })
            
            return results
            
        except requests.RequestException as e:
            print(f"Error searching for {name}: {e}")
            return []
    
    def get_page_content(self, title: str) -> Optional[Dict]:
        """
        Get the full content of a Wikipedia page.
        
        Args:
            title (str): Title of the Wikipedia page
            
        Returns:
            Dict: Page content including summary, infobox, and metadata
        """
        try:
            # Get page summary
            summary_url = f"{self.base_url}/page/summary/{title}"
            summary_response = self.session.get(summary_url, timeout=10)
            
            if summary_response.status_code != 200:
                return None
                
            summary_data = summary_response.json()
            
            # Get full page content for infobox extraction
            content_url = f"{self.base_url}/page/html/{title}"
            content_response = self.session.get(content_url, timeout=10)
            
            # Rate limiting - be respectful to Wikipedia's servers
            time.sleep(0.1)
            
            return {
                'title': summary_data.get('title', title),
                'extract': summary_data.get('extract', ''),
                'description': summary_data.get('description', ''),
                'thumbnail': summary_data.get('thumbnail', {}).get('source', ''),
                'page_url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'coordinates': summary_data.get('coordinates', {}),
                'type': summary_data.get('type', ''),
                'full_html': content_response.text if content_response.status_code == 200 else ''
            }
            
        except requests.RequestException as e:
            print(f"Error fetching page content for {title}: {e}")
            return None
    
    def get_infobox_data(self, title: str) -> Dict:
        """
        Extract structured data from Wikipedia infobox.
        
        Args:
            title (str): Title of the Wikipedia page
            
        Returns:
            Dict: Structured infobox data
        """
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'revisions',
                'rvprop': 'content',
                'rvsection': '0'  # Only get the lead section
            }
            
            response = self.session.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract infobox data from wikitext
            infobox_data = {}
            
            if 'query' in data and 'pages' in data['query']:
                for page_id, page_data in data['query']['pages'].items():
                    if 'revisions' in page_data:
                        content = page_data['revisions'][0]['*']
                        infobox_data = self._parse_infobox(content)
            
            return infobox_data
            
        except requests.RequestException as e:
            print(f"Error fetching infobox for {title}: {e}")
            return {}
    
    def _parse_infobox(self, content: str) -> Dict:
        """
        Parse infobox data from Wikipedia wikitext.
        
        Args:
            content (str): Raw wikitext content
            
        Returns:
            Dict: Parsed infobox fields
        """
        import re
        
        infobox_data = {}
        
        # Extract birth/death information
        birth_match = re.search(r'\|\s*birth_date\s*=\s*([^\n|]*)', content, re.IGNORECASE)
        if birth_match:
            infobox_data['birth_date'] = birth_match.group(1).strip()
        
        death_match = re.search(r'\|\s*death_date\s*=\s*([^\n|]*)', content, re.IGNORECASE)
        if death_match:
            infobox_data['death_date'] = death_match.group(1).strip()
        
        # Extract birth/death place
        birth_place_match = re.search(r'\|\s*birth_place\s*=\s*([^\n|]*)', content, re.IGNORECASE)
        if birth_place_match:
            infobox_data['birth_place'] = birth_place_match.group(1).strip()
        
        death_place_match = re.search(r'\|\s*death_place\s*=\s*([^\n|]*)', content, re.IGNORECASE)
        if death_place_match:
            infobox_data['death_place'] = death_place_match.group(1).strip()
        
        # Extract occupation
        occupation_match = re.search(r'\|\s*occupation\s*=\s*([^\n|]*)', content, re.IGNORECASE)
        if occupation_match:
            infobox_data['occupation'] = occupation_match.group(1).strip()
        
        # Extract nationality
        nationality_match = re.search(r'\|\s*nationality\s*=\s*([^\n|]*)', content, re.IGNORECASE)
        if nationality_match:
            infobox_data['nationality'] = nationality_match.group(1).strip()
        
        return infobox_data
    
    def get_figure_data(self, name: str) -> Optional[Dict]:
        """
        Get comprehensive data about a historical figure.
        
        Args:
            name (str): Name of the historical figure
            
        Returns:
            Dict: Complete biographical data or None if not found
        """
        # First, search for the figure
        search_results = self.search_figure(name, limit=1)
        
        if not search_results:
            return None
        
        # Get the best match
        best_match = search_results[0]
        title = best_match['title']
        
        # Get page content and infobox data
        page_data = self.get_page_content(title)
        infobox_data = self.get_infobox_data(title)
        
        if not page_data:
            return None
        
        # Combine all data
        figure_data = {
            'name': page_data['title'],
            'summary': page_data['extract'],
            'description': page_data['description'],
            'image_url': page_data['thumbnail'],
            'wikipedia_url': page_data['page_url'],
            'coordinates': page_data['coordinates'],
            'type': page_data['type'],
            **infobox_data  # Merge infobox data
        }
        
        return figure_data

