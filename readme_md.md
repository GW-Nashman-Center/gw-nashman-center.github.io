# Organizational Website

A modern, interactive organizational website built with Quarto, featuring data dashboards and dynamic content.

## Features

- 🎨 Modern, responsive design with custom styling
- 📊 Interactive data dashboards with Plotly
- 🚀 Automatic deployment to GitHub Pages
- 📱 Mobile-friendly layout
- 🔍 Built-in search functionality
- 📈 Real-time metrics simulation
- 🎯 SEO optimized

## Quick Start

### Prerequisites

- Python 3.8+ 
- Quarto CLI
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/your-org-website.git
   cd your-org-website
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Quarto**
   - Download from [https://quarto.org/docs/get-started/](https://quarto.org/docs/get-started/)
   - Or use conda: `conda install -c conda-forge quarto`

4. **Preview the site locally**
   ```bash
   quarto preview
   ```

5. **Build the site**
   ```bash
   quarto render
   ```

### GitHub Pages Deployment

1. **Enable GitHub Pages**
   - Go to your repository settings
   - Navigate to Pages section
   - Set source to "GitHub Actions"

2. **Push to main branch**
   ```bash
   git add .
   git commit -m "Initial site setup"
   git push origin main
   ```

3. **Automatic deployment**
   - The GitHub Action will automatically build and deploy your site
   - Check the Actions tab for build status
   - Your site will be available at `https://yourusername.github.io/your-repo-name`

## Project Structure

```
├── _quarto.yml           # Main configuration
├── index.qmd            # Home page
├── dashboard.qmd        # Data dashboard
├── about.qmd            # About page
├── services.qmd         # Services page
├── team.qmd             # Team page
├── contact.qmd          # Contact page
├── custom.scss          # Custom styling
├── requirements.txt     # Python dependencies
├── .github/
│   └── workflows/
│       └── quarto-publish.yml  # Deployment workflow
└── docs/               # Generated site (auto-created)
```

## Customization

### Styling
- Edit `custom.scss` for design changes
- Modify color variables in the SCSS defaults section
- Add custom CSS in individual `.qmd` files

### Content
- Update `_quarto.yml` for navigation and site settings
- Edit `.qmd` files for page content
- Add new pages by creating new `.qmd` files

### Data Integration
- Replace sample data in dashboard with your real data
- Connect to external APIs for live data
- Use the Python environment for data processing

## Adding Dynamic Features

### External Data Sources
Since GitHub Pages is static, for dynamic data you can:

1. **Client-side API calls**
   ```javascript
   // Fetch data from external API
   fetch('https://api.example.com/data')
     .then(response => response.json())
     .then(data => updateDashboard(data));
   ```

2. **Scheduled data updates**
   - Use GitHub Actions to fetch data periodically
   - Commit updated data files
   - Site rebuilds automatically

3. **External services**
   - Integrate with services like Airtable, Google Sheets
   - Use Netlify Functions or Vercel for serverless functions

### Database Integration
For PostgreSQL integration in a static