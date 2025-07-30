"""
Data processing utilities for the organizational website.
This module provides functions for data fetching, processing, and visualization.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple

class DataProcessor:
    """Main class for handling data operations."""
    
    def __init__(self):
        self.cache_dir = "data/cache"
        self.ensure_cache_dir()
    
    def ensure_cache_dir(self):
        """Ensure cache directory exists."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def generate_sample_metrics(self, days: int = 365) -> pd.DataFrame:
        """Generate sample metrics data for demonstrations."""
        np.random.seed(42)  # For reproducible results
        
        start_date = datetime.now() - timedelta(days=days)
        dates = pd.date_range(start=start_date, periods=days, freq='D')
        
        # Generate realistic-looking data with trends and seasonality
        trend = np.linspace(1000, 1500, days)
        seasonality = 200 * np.sin(2 * np.pi * np.arange(days) / 365)
        noise = np.random.normal(0, 50, days)
        daily_users = trend + seasonality + noise
        
        # Revenue with some correlation to users
        revenue_base = daily_users * np.random.uniform(2, 5, days)
        revenue = revenue_base + np.random.normal(0, 500, days)
        
        # Other metrics
        satisfaction = np.random.beta(8, 2, days) * 4 + 1  # Skewed towards higher satisfaction
        support_tickets = np.random.poisson(30, days) + (daily_users / 50).astype(int)
        conversion_rate = np.random.beta(2, 8, days) * 10  # Realistic conversion rates
        
        return pd.DataFrame({
            'date': dates,
            'daily_active_users': daily_users.astype(int),
            'revenue': revenue.clip(min=0),
            'customer_satisfaction': satisfaction.clip(1, 5),
            'support_tickets': support_tickets,
            'conversion_rate': conversion_rate
        })
    
    def generate_geographic_data(self) -> pd.DataFrame:
        """Generate sample geographic distribution data."""
        countries = [
            'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
            'Australia', 'Japan', 'Brazil', 'India', 'China', 'Netherlands',
            'Sweden', 'Spain', 'Italy', 'South Korea'
        ]
        
        # Generate realistic user distribution (some countries have more users)
        weights = [0.35, 0.08, 0.12, 0.08, 0.07, 0.05, 0.06, 0.04, 0.08, 0.05, 0.02]
        
        total_users = 50000
        users = np.random.multinomial(total_users, weights + [0.01] * (len(countries) - len(weights)))
        
        # Revenue roughly proportional to users but with some variation
        revenue = users * np.random.uniform(25, 45, len(countries))
        
        return pd.DataFrame({
            'country': countries,
            'users': users,
            'revenue': revenue.astype(int)
        })
    
    def create_performance_dashboard(self, data: pd.DataFrame) -> go.Figure:
        """Create a comprehensive performance dashboard."""
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Daily Active Users', 'Revenue Trends', 
                          'Customer Satisfaction', 'Support Metrics'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": True}]],
            vertical_spacing=0.12
        )
        
        # Daily Active Users
        fig.add_trace(
            go.Scatter(
                x=data['date'], 
                y=data['daily_active_users'],
                mode='lines',
                name='Daily Users',
                line=dict(color='#2563eb', width=2)
            ),
            row=1, col=1
        )
        
        # Revenue
        fig.add_trace(
            go.Scatter(
                x=data['date'], 
                y=data['revenue'],
                mode='lines',
                name='Daily Revenue',
                line=dict(color='#059669', width=2)
            ),
            row=1, col=2
        )
        
        # Customer Satisfaction
        fig.add_trace(
            go.Scatter(
                x=data['date'], 
                y=data['customer_satisfaction'],
                mode='lines',
                name='Satisfaction',
                line=dict(color='#dc2626', width=2)
            ),
            row=2, col=1
        )
        
        # Support Tickets (primary y-axis)
        fig.add_trace(
            go.Scatter(
                x=data['date'], 
                y=data['support_tickets'],
                mode='lines',
                name='Support Tickets',
                line=dict(color='#7c3aed', width=2)
            ),
            row=2, col=2
        )
        
        # Conversion Rate (secondary y-axis)
        fig.add_trace(
            go.Scatter(
                x=data['date'], 
                y=data['conversion_rate'],
                mode='lines',
                name='Conversion Rate %',
                line=dict(color='#ea580c', width=2, dash='dash')
            ),
            row=2, col=2, secondary_y=True
        )
        
        fig.update_layout(
            height=600,
            showlegend=True,
            title_text="Performance Dashboard Overview",
            title_x=0.5
        )
        
        # Update y-axis labels
        fig.update_yaxes(title_text="Users", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
        fig.update_yaxes(title_text="Rating (1-5)", row=2, col=1)
        fig.update_yaxes(title_text="Tickets", row=2, col=2)
        fig.update_yaxes(title_text="Conversion %", row=2, col=2, secondary_y=True)
        
        return fig
    
    def create_geographic_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create an interactive geographic distribution chart."""
        fig = px.choropleth(
            data,
            locations='country',
            locationmode='country names',
            color='users',
            hover_name='country',
            hover_data={
                'users': ':,',
                'revenue': ':$,.0f'
            },
            color_continuous_scale='Blues',
            title='Global User Distribution'
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
    
    def calculate_kpis(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate key performance indicators from the data."""
        latest = data.iloc[-1]
        previous = data.iloc[-30]  # 30 days ago
        
        return {
            'current_users': latest['daily_active_users'],
            'users_growth': ((latest['daily_active_users'] - previous['daily_active_users']) 
                           / previous['daily_active_users'] * 100),
            'current_revenue': latest['revenue'],
            'revenue_growth': ((latest['revenue'] - previous['revenue']) 
                             / previous['revenue'] * 100),
            'avg_satisfaction': data['customer_satisfaction'].tail(30).mean(),
            'avg_support_tickets': data['support_tickets'].tail(30).mean(),
            'avg_conversion_rate': data['conversion_rate'].tail(30).mean()
        }
    
    def export_data_summary(self, data: pd.DataFrame, filename: str = None) -> str:
        """Export a summary of the data to markdown format."""
        if filename is None:
            filename = f"data_summary_{datetime.now().strftime('%Y%m%d')}.md"
        
        kpis = self.calculate_kpis(data)
        
        summary = f"""# Data Summary Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Performance Indicators

- **Current Daily Users**: {kpis['current_users']:,.0f} ({kpis['users_growth']:+.1f}%)
- **Current Daily Revenue**: ${kpis['current_revenue']:,.0f} ({kpis['revenue_growth']:+.1f}%)
- **Average Satisfaction**: {kpis['avg_satisfaction']:.2f}/5.0
- **Average Support Tickets**: {kpis['avg_support_tickets']:.0f}/day
- **Average Conversion Rate**: {kpis['avg_conversion_rate']:.2f}%

## Data Quality
- **Total Records**: {len(data):,}
- **Date Range**: {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}
- **Missing Values**: {data.isnull().sum().sum()}

## Statistical Summary
{data.describe().round(2).to_markdown()}
"""
        
        filepath = os.path.join(self.cache_dir, filename)
        with open(filepath, 'w') as f:
            f.write(summary)
        
        return filepath

def load_external_data(source: str, **kwargs) -> pd.DataFrame:
    """Load data from external sources (API, database, etc.)."""
    if source == "api":
        # Example API call (replace with actual API)
        # This would be used during build time
        import requests
        try:
            response = requests.get(kwargs.get('url', ''))
            return pd.DataFrame(response.json())
        except:
            # Return sample data if API fails
            return DataProcessor().generate_sample_metrics()
    
    elif source == "database":
        # Example database connection
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=kwargs.get('host', os.environ.get('DB_HOST')),
                database=kwargs.get('database', os.environ.get('DB_NAME')),
                user=kwargs.get('user', os.environ.get('DB_USER')),
                password=kwargs.get('password', os.environ.get('DB_PASSWORD'))
            )
            return pd.read_sql(kwargs.get('query', 'SELECT 1'), conn)
        except:
            # Return sample data if database connection fails
            return DataProcessor().generate_sample_metrics()
    
    else:
        # Default to sample data
        return DataProcessor().generate_sample_metrics()

# Utility functions for common operations
def format_currency(value: float) -> str:
    """Format a number as currency."""
    return f"${value:,.0f}"

def format_percentage(value: float) -> str:
    """Format a number as percentage."""
    return f"{value:.1f}%"

def format_large_number(value: float) -> str:
    """Format large numbers with appropriate suffixes."""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"