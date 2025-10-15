"""
Data Transformation Module for Historical Figures Explorer

This module handles the ETL (Extract, Transform, Load) process for
Wikipedia data, cleaning and structuring it for display and future
database storage.
"""

import re
from typing import Dict, Optional, List
from datetime import datetime


class DataTransformer:
    """
    Handles transformation and cleaning of Wikipedia API data.
    
    This class provides methods to clean, validate, and structure
    biographical data extracted from Wikipedia into a consistent
    format suitable for web display and future database storage.
    """
    
    def __init__(self):
        """Initialize the data transformer."""
        self.date_patterns = [
            r'(\d{1,2})\s+(January|February|March|April|May|June|'
            r'July|August|September|October|November|December)\s+(\d{4})',
            r'(\d{4})',  # Just year
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # MM/DD/YYYY
            r'(\d{4})-(\d{1,2})-(\d{1,2})'   # YYYY-MM-DD
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove Wikipedia markup
        text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)
        text = re.sub(r'\[([^\]]+)\]', '', text)
        text = re.sub(r'\'\'\'([^\']+)\'\'\'', r'\1', text)
        text = re.sub(r'\'\'([^\']+)\'\'', r'\1', text)
        
        # Clean up common Wikipedia artifacts
        text = re.sub(r'\s+\(born\s+[^)]+\)', '', text)
        text = re.sub(r'\s+\(died\s+[^)]+\)', '', text)
        
        return text.strip()
    
    def parse_date(self, date_string: str) -> Optional[Dict]:
        """
        Parse and standardize date information.
        
        Args:
            date_string (str): Raw date string from Wikipedia
            
        Returns:
            Dict: Parsed date information or None
        """
        if not date_string:
            return None
        
        # Clean the date string
        date_string = self.clean_text(date_string)
        
        # Try different date patterns
        for pattern in self.date_patterns:
            match = re.search(pattern, date_string, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                if len(groups) == 3 and groups[1].isalpha():  # Day Month Year
                    try:
                        day, month, year = int(groups[0]), groups[1], int(groups[2])
                        return {
                            'day': day,
                            'month': month,
                            'year': year,
                            'formatted': f"{day} {month} {year}",
                            'raw': date_string
                        }
                    except ValueError:
                        continue
                
                elif len(groups) == 1 and groups[0].isdigit():  # Just year
                    year = int(groups[0])
                    if 1000 <= year <= 2100:  # Reasonable year range
                        return {
                            'year': year,
                            'formatted': str(year),
                            'raw': date_string
                        }
                
                elif len(groups) == 3 and all(g.isdigit() for g in groups):  # Numeric dates
                    try:
                        if '/' in date_string:  # MM/DD/YYYY
                            month, day, year = int(groups[0]), int(groups[1]), int(groups[2])
                        else:  # YYYY-MM-DD
                            year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                        
                        return {
                            'day': day,
                            'month': month,
                            'year': year,
                            'formatted': f"{year}-{month:02d}-{day:02d}",
                            'raw': date_string
                        }
                    except ValueError:
                        continue
        
        # If no pattern matches, return raw date
        return {
            'formatted': date_string,
            'raw': date_string
        }
    
    def extract_categories(self, text: str) -> List[str]:
        """
        Extract relevant categories from biographical text.
        
        Args:
            text (str): Biographical text to analyze
            
        Returns:
            List[str]: List of relevant categories
        """
        if not text:
            return []
        
        categories = []
        text_lower = text.lower()
        
        # Define category keywords
        category_keywords = {
            'Politician': ['politician', 'president', 'prime minister', 'minister', 'governor', 'mayor'],
            'Scientist': ['scientist', 'physicist', 'chemist', 'biologist', 'mathematician', 'researcher'],
            'Artist': ['artist', 'painter', 'sculptor', 'musician', 'composer', 'writer', 'poet', 'novelist'],
            'Explorer': ['explorer', 'navigator', 'adventurer', 'discoverer'],
            'Military': ['general', 'admiral', 'soldier', 'commander', 'military'],
            'Philosopher': ['philosopher', 'thinker', 'philosophy'],
            'Inventor': ['inventor', 'invention', 'patent', 'engineer'],
            'Religious': ['priest', 'bishop', 'pope', 'monk', 'religious', 'saint'],
            'Royalty': ['king', 'queen', 'emperor', 'empress', 'prince', 'princess', 'royal']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        return categories
    
    def transform_figure_data(self, raw_data: Dict) -> Dict:
        """
        Transform raw Wikipedia data into structured format.
        
        Args:
            raw_data (Dict): Raw data from Wikipedia API
            
        Returns:
            Dict: Transformed and cleaned biographical data
        """
        if not raw_data:
            return {}
        
        # Clean basic information
        name = self.clean_text(raw_data.get('name', ''))
        summary = self.clean_text(raw_data.get('summary', ''))
        description = self.clean_text(raw_data.get('description', ''))
        
        # Parse dates
        birth_date = self.parse_date(raw_data.get('birth_date', ''))
        death_date = self.parse_date(raw_data.get('death_date', ''))
        
        # Clean locations
        birth_place = self.clean_text(raw_data.get('birth_place', ''))
        death_place = self.clean_text(raw_data.get('death_place', ''))
        
        # Clean occupation and nationality
        occupation = self.clean_text(raw_data.get('occupation', ''))
        nationality = self.clean_text(raw_data.get('nationality', ''))
        
        # Extract categories from summary
        categories = self.extract_categories(summary)
        
        # Calculate age if both birth and death dates are available
        age = None
        if birth_date and death_date and 'year' in birth_date and 'year' in death_date:
            age = death_date['year'] - birth_date['year']
        
        # Determine historical period
        historical_period = self._determine_historical_period(birth_date, death_date)
        
        # Structure the transformed data
        transformed_data = {
            # Basic information
            'name': name,
            'summary': summary,
            'description': description,
            
            # Dates and life information
            'birth_date': birth_date,
            'death_date': death_date,
            'age': age,
            'historical_period': historical_period,
            
            # Location information
            'birth_place': birth_place,
            'death_place': death_place,
            
            # Professional information
            'occupation': occupation,
            'nationality': nationality,
            'categories': categories,
            
            # Media and links
            'image_url': raw_data.get('image_url', ''),
            'wikipedia_url': raw_data.get('wikipedia_url', ''),
            'coordinates': raw_data.get('coordinates', {}),
            
            # Metadata
            'type': raw_data.get('type', ''),
            'last_updated': datetime.now().isoformat()
        }
        
        return transformed_data
    
    def _determine_historical_period(self, birth_date: Optional[Dict], 
                                   death_date: Optional[Dict]) -> str:
        """
        Determine the historical period based on birth/death dates.
        
        Args:
            birth_date (Optional[Dict]): Birth date information
            death_date (Optional[Dict]): Death date information
            
        Returns:
            str: Historical period name
        """
        # Use death date if available, otherwise birth date
        date_info = death_date or birth_date
        
        if not date_info or 'year' not in date_info:
            return 'Unknown'
        
        year = date_info['year']
        
        if year < 500:
            return 'Ancient History'
        elif year < 1000:
            return 'Early Middle Ages'
        elif year < 1300:
            return 'High Middle Ages'
        elif year < 1500:
            return 'Late Middle Ages'
        elif year < 1800:
            return 'Early Modern Period'
        elif year < 1900:
            return 'Modern Period'
        else:
            return 'Contemporary Period'
    
    def validate_data(self, data: Dict) -> Dict:
        """
        Validate and ensure data quality.
        
        Args:
            data (Dict): Data to validate
            
        Returns:
            Dict: Validated data with quality indicators
        """
        if not data:
            return {'error': 'No data provided'}
        
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = ['name', 'summary']
        for field in required_fields:
            if not data.get(field):
                validation_results['errors'].append(f'Missing required field: {field}')
                validation_results['is_valid'] = False
        
        # Check data quality
        if data.get('summary') and len(data['summary']) < 50:
            validation_results['warnings'].append('Summary is very short')
        
        if not data.get('birth_date') and not data.get('death_date'):
            validation_results['warnings'].append('No date information available')
        
        if not data.get('occupation'):
            validation_results['warnings'].append('No occupation information')
        
        return {
            **data,
            'validation': validation_results
        }

