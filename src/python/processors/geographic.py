"""
Geographic processor for handling location-based data and visualizations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go


class GeographicProcessor:
    """Process and visualize geographic distribution data."""
    
    def __init__(self):
        """Initialize the geographic processor."""
        self.supported_locations = [
            'country names', 'country', 'ISO-3', 'USA-states'
        ]
    
    def generate_geographic_data(self, num_countries: int = 15) -> pd.DataFrame:
        """
        Generate sample geographic distribution data.
        
        Args:
            num_countries: Number of countries to generate data for
            
        Returns:
            DataFrame with geographic data
        """
        countries = [
            'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
            'Australia', 'Japan', 'Brazil', 'India', 'China', 'Netherlands',
            'Sweden', 'Spain', 'Italy', 'South Korea'
        ][:num_countries]
        
        # Realistic user distribution
        weights = [0.35, 0.08, 0.12, 0.08, 0.07, 0.05, 0.06, 0.04, 0.08, 0.05, 0.02, 0.01, 0.01, 0.01, 0.01]
        weights = weights[:num_countries]
        
        total_users = 50000
        users = np.random.multinomial(total_users, weights)
        
        # Revenue with variation per country
        revenue = users * np.random.uniform(25, 45, len(countries))
        
        return pd.DataFrame({
            'country': countries,
            'users': users,
            'revenue': revenue.astype(int)
        })
    
    def aggregate_by_region(self, data: pd.DataFrame, region_mapping: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Aggregate geographic data by region.
        
        Args:
            data: DataFrame with geographic data
            region_mapping: Dictionary mapping regions to countries
            
        Returns:
            DataFrame aggregated by region
        """
        # Create region column
        data_copy = data.copy()
        data_copy['region'] = data_copy['country'].map(
            lambda x: next((region for region, countries in region_mapping.items() 
                          if x in countries), 'Other')
        )
        
        # Aggregate
        return data_copy.groupby('region').agg({
            'users': 'sum',
            'revenue': 'sum'
        }).reset_index()
    
    def calculate_geographic_metrics(self, data: pd.DataFrame) -> Dict[str, any]:
        """
        Calculate metrics for geographic data.
        
        Args:
            data: DataFrame with geographic data
            
        Returns:
            Dictionary with geographic metrics
        """
        return {
            'total_countries': len(data),
            'total_users': int(data['users'].sum()),
            'total_revenue': int(data['revenue'].sum()),
            'avg_users_per_country': float(data['users'].mean()),
            'avg_revenue_per_country': float(data['revenue'].mean()),
            'top_country_users': data.loc[data['users'].idxmax(), 'country'],
            'top_country_revenue': data.loc[data['revenue'].idxmax(), 'country'],
            'users_concentration': float(data['users'].max() / data['users'].sum() * 100)
        }
    
    def create_choropleth(self, data: pd.DataFrame, metric: str = 'users') -> go.Figure:
        """
        Create a choropleth map visualization.
        
        Args:
            data: DataFrame with geographic data (must have 'country' column)
            metric: Metric to visualize ('users' or 'revenue')
            
        Returns:
            Plotly Figure object
        """
        fig = px.choropleth(
            data,
            locations='country',
            locationmode='country names',
            color=metric,
            hover_name='country',
            hover_data={
                'users': ':,',
                'revenue': ':$,.0f'
            },
            color_continuous_scale='Blues',
            title=f'Global {metric.title()} Distribution'
        )
        
        fig.update_layout(
            height=500,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        return fig
    
    def create_geographic_bar_chart(self, data: pd.DataFrame, metric: str = 'users',
                                   top_n: int = 10) -> go.Figure:
        """
        Create a bar chart showing top countries by metric.
        
        Args:
            data: DataFrame with geographic data
            metric: Metric to visualize
            top_n: Number of top countries to show
            
        Returns:
            Plotly Figure object
        """
        top_data = data.nlargest(top_n, metric)
        
        fig = px.bar(
            top_data,
            x=metric,
            y='country',
            orientation='h',
            title=f'Top {top_n} Countries by {metric.title()}',
            labels={'country': 'Country', metric: metric.title()}
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title=metric.title(),
            yaxis_title='Country'
        )
        
        return fig
    
    def create_geographic_scatter(self, data: pd.DataFrame) -> go.Figure:
        """
        Create a scatter plot of users vs revenue by country.
        
        Args:
            data: DataFrame with geographic data
            
        Returns:
            Plotly Figure object
        """
        fig = px.scatter(
            data,
            x='users',
            y='revenue',
            size='users',
            hover_name='country',
            hover_data={'users': ':', 'revenue': ':$,.0f'},
            title='Users vs Revenue by Country',
            labels={'users': 'Active Users', 'revenue': 'Revenue ($)'}
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def get_country_data(self, data: pd.DataFrame, country: str) -> Optional[Dict]:
        """
        Get detailed data for a specific country.
        
        Args:
            data: DataFrame with geographic data
            country: Country name
            
        Returns:
            Dictionary with country data or None if not found
        """
        country_data = data[data['country'] == country]
        
        if country_data.empty:
            return None
        
        row = country_data.iloc[0]
        return {
            'country': country,
            'users': int(row['users']),
            'revenue': int(row['revenue']),
            'revenue_per_user': float(row['revenue'] / row['users']) if row['users'] > 0 else 0
        }