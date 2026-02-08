"""
College Data Manager
Handles loading and filtering college data from external CSV dataset
"""

import pandas as pd
from typing import List, Dict, Optional
import os


class CollegeDataManager:
    """Manages college data from CSV dataset"""
    
    def __init__(self, data_source: str = "real_college_names_500_FULLY_LOGICAL.csv"):
        self.data_source = data_source
        self.colleges_df = None
        self.load_data()
    
    def load_data(self):
        """Load college data from CSV file"""
        if not os.path.exists(self.data_source):
            print(f"Warning: Data file not found at {self.data_source}")
            return
        
        try:
            self.colleges_df = pd.read_csv(self.data_source)
            print(f"✅ Successfully loaded {len(self.colleges_df)} colleges from dataset")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def get_colleges_by_stream(self, stream: str, tier: str = None, max_results: int = 10) -> List[Dict]:
        """
        Get colleges filtered by stream for 10th grade students
        
        Args:
            stream: Stream name (Science, Commerce, Arts)
            tier: Tier filter (Tier 1, Tier 2, Tier 3) - optional
            max_results: Maximum number of colleges to return
        
        Returns:
            List of college dictionaries
        """
        if self.colleges_df is None or self.colleges_df.empty:
            return []
        
        try:
            # Filter by stream
            filtered_df = self.colleges_df[
                self.colleges_df['Stream'].str.lower() == stream.lower()
            ].copy()
            
            # Filter by tier if specified
            if tier:
                filtered_df = filtered_df[filtered_df['Tier'] == tier]
            
            # Sort by NIRF Rank (lower is better) and Rating (higher is better)
            filtered_df = filtered_df.sort_values(
                by=['NIRF Rank', 'Rating'], 
                ascending=[True, False]
            )
            
            # Limit results
            filtered_df = filtered_df.head(max_results)
            
            # Convert to list of dictionaries
            colleges = []
            for _, row in filtered_df.iterrows():
                college = {
                    'name': row['College Name'],
                    'location': f"{row['City']}, {row['State']}",
                    'type': row['Area Type'],
                    'tier': row['Tier'],
                    'cutoff': f"{row['Cutoff (%)']}%",
                    'entrance_exam': row['Entrance Exam'],
                    'fees': f"₹{int(row['Fees (INR/year)']):,}/year",
                    'hostel_fees': f"₹{int(row['Hostel Fees (INR/year)']):,}/year" if pd.notna(row['Hostel Fees (INR/year)']) else 'N/A',
                    'naac_grade': row['NAAC Grade'],
                    'nirf_rank': int(row['NIRF Rank']) if pd.notna(row['NIRF Rank']) else 'N/A',
                    'rating': float(row['Rating']) if pd.notna(row['Rating']) else 0,
                    'placement': row['Placement Details'],
                    'facilities': row['Facilities'].split('|') if pd.notna(row['Facilities']) else [],
                    'campus_size': f"{int(row['Campus Size (acres)'])} acres" if pd.notna(row['Campus Size (acres)']) else 'N/A',
                    'scholarships': row['Scholarships'] if pd.notna(row['Scholarships']) else 'N/A',
                    'degree': row['Degree'],
                    'specialization': row['Specialization']
                }
                colleges.append(college)
            
            return colleges
            
        except Exception as e:
            print(f"Error filtering colleges by stream: {str(e)}")
            return []
    
    def get_colleges_by_field(self, field: str, degree: str = None, tier: str = None, max_results: int = 10) -> List[Dict]:
        """
        Get colleges filtered by field for 12th grade students
        
        Args:
            field: Field name (e.g., Computer Science, Medicine, Business Administration)
            degree: Degree filter (B.Tech, MBBS, MBA, etc.) - optional
            tier: Tier filter (Tier 1, Tier 2, Tier 3) - optional
            max_results: Maximum number of colleges to return
        
        Returns:
            List of college dictionaries
        """
        if self.colleges_df is None or self.colleges_df.empty:
            return []
        
        try:
            # Map common field names to dataset fields
            field_mapping = {
                'engineering': 'Engineering',
                'computer science': 'Computer Science',
                'electrical': 'Electrical',
                'mechanical': 'Mechanical',
                'medical': 'Medicine',
                'medicine': 'Medicine',
                'business': 'Business Administration',
                'management': 'Business Administration',
                'law': 'Law',
                'design': 'Design',
                'arts': 'Arts',
                'psychology': 'Psychology',
                'history': 'History',
                'political science': 'Political Science',
                'economics': 'Economics'
            }
            
            # Get the mapped field name
            search_field = field_mapping.get(field.lower(), field)
            
            # Filter by field
            filtered_df = self.colleges_df[
                self.colleges_df['Field'].str.contains(search_field, case=False, na=False)
            ].copy()
            
            # Filter by degree if specified
            if degree:
                filtered_df = filtered_df[
                    filtered_df['Degree'].str.contains(degree, case=False, na=False)
                ]
            
            # Filter by tier if specified
            if tier:
                filtered_df = filtered_df[filtered_df['Tier'] == tier]
            
            # Sort by NIRF Rank (lower is better) and Rating (higher is better)
            filtered_df = filtered_df.sort_values(
                by=['NIRF Rank', 'Rating'], 
                ascending=[True, False]
            )
            
            # Limit results
            filtered_df = filtered_df.head(max_results)
            
            # Convert to list of dictionaries
            colleges = []
            for _, row in filtered_df.iterrows():
                college = {
                    'name': row['College Name'],
                    'location': f"{row['City']}, {row['State']}",
                    'type': row['Area Type'],
                    'tier': row['Tier'],
                    'ranking': int(row['NIRF Rank']) if pd.notna(row['NIRF Rank']) else 'N/A',
                    'cutoff': f"{row['Cutoff (%)']}%",
                    'entrance_exam': row['Entrance Exam'],
                    'fees': f"₹{int(row['Fees (INR/year)']):,}/year",
                    'hostel_fees': f"₹{int(row['Hostel Fees (INR/year)']):,}/year" if pd.notna(row['Hostel Fees (INR/year)']) else 'N/A',
                    'naac_grade': row['NAAC Grade'],
                    'rating': float(row['Rating']) if pd.notna(row['Rating']) else 0,
                    'placement': row['Placement Details'],
                    'facilities': row['Facilities'].split('|') if pd.notna(row['Facilities']) else [],
                    'campus_size': f"{int(row['Campus Size (acres)'])} acres" if pd.notna(row['Campus Size (acres)']) else 'N/A',
                    'scholarships': row['Scholarships'] if pd.notna(row['Scholarships']) else 'N/A',
                    'degree': row['Degree'],
                    'field': row['Field'],
                    'specialization': row['Specialization'],
                    'stream': row['Stream']
                }
                colleges.append(college)
            
            return colleges
            
        except Exception as e:
            print(f"Error filtering colleges by field: {str(e)}")
            return []
    
    def get_top_colleges(self, max_results: int = 20) -> List[Dict]:
        """Get top colleges overall based on NIRF ranking"""
        if self.colleges_df is None or self.colleges_df.empty:
            return []
        
        try:
            # Sort by NIRF Rank and Rating
            sorted_df = self.colleges_df.sort_values(
                by=['NIRF Rank', 'Rating'], 
                ascending=[True, False]
            ).head(max_results)
            
            colleges = []
            for _, row in sorted_df.iterrows():
                college = {
                    'name': row['College Name'],
                    'stream': row['Stream'],
                    'field': row['Field'],
                    'location': f"{row['City']}, {row['State']}",
                    'nirf_rank': int(row['NIRF Rank']) if pd.notna(row['NIRF Rank']) else 'N/A',
                    'rating': float(row['Rating']) if pd.notna(row['Rating']) else 0,
                    'naac_grade': row['NAAC Grade'],
                    'tier': row['Tier']
                }
                colleges.append(college)
            
            return colleges
            
        except Exception as e:
            print(f"Error getting top colleges: {str(e)}")
            return []
    
    def get_colleges_by_city(self, city: str, max_results: int = 10) -> List[Dict]:
        """Get colleges in a specific city"""
        if self.colleges_df is None or self.colleges_df.empty:
            return []
        
        try:
            filtered_df = self.colleges_df[
                self.colleges_df['City'].str.lower() == city.lower()
            ].copy()
            
            filtered_df = filtered_df.sort_values(
                by=['NIRF Rank', 'Rating'], 
                ascending=[True, False]
            ).head(max_results)
            
            colleges = []
            for _, row in filtered_df.iterrows():
                college = {
                    'name': row['College Name'],
                    'stream': row['Stream'],
                    'field': row['Field'],
                    'degree': row['Degree'],
                    'nirf_rank': int(row['NIRF Rank']) if pd.notna(row['NIRF Rank']) else 'N/A',
                    'rating': float(row['Rating']) if pd.notna(row['Rating']) else 0
                }
                colleges.append(college)
            
            return colleges
            
        except Exception as e:
            print(f"Error filtering colleges by city: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get dataset statistics"""
        if self.colleges_df is None or self.colleges_df.empty:
            return {}
        
        return {
            'total_colleges': len(self.colleges_df),
            'streams': self.colleges_df['Stream'].unique().tolist(),
            'fields': self.colleges_df['Field'].unique().tolist(),
            'cities': self.colleges_df['City'].nunique(),
            'states': self.colleges_df['State'].unique().tolist(),
            'tiers': self.colleges_df['Tier'].unique().tolist(),
            'avg_rating': round(self.colleges_df['Rating'].mean(), 2)
        }
