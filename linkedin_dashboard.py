import dash
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# CSV path
path = "./"

# Read CSVs with correct file names
company_job_type = pd.read_csv(path + "company_job_type_counts.csv")
location_job_type = pd.read_csv(path + "location_job_type_counts.csv")
top_job_titles = pd.read_csv(path + "top_job_titles.csv")
top_skills = pd.read_csv(path + "top_skills.csv")
job_type_dist = pd.read_csv(path + "job_type_distribution.csv")
monthly_trends = pd.read_csv(path + "monthly_postings.csv")
top_locations = pd.read_csv(path + "top_locations.csv")
top_companies = pd.read_csv(path + "top_companies.csv")
top_paying_jobs = pd.read_csv(path + "top_paying_jobs.csv")
experience_salary = pd.read_csv(path + "experience_salary.csv")
top_industries = pd.read_csv(path + "top_industries.csv")
top_jobs = pd.read_csv(path + "top_jobs.csv")
full_data = pd.read_csv(path + "linkedin_full_dataset.csv", low_memory=False)

print("✅ All CSV files loaded successfully!")

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Job Search Analytics</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .sidebar {
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                width: 280px;
                padding: 2rem 1rem;
                background: linear-gradient(180deg, #1e3a5f 0%, #2c5282 100%);
                overflow-y: auto;
                box-shadow: 4px 0 10px rgba(0,0,0,0.5);
                z-index: 1000;
            }
            .sidebar h2 {
                color: #fff;
                font-weight: 700;
                margin-bottom: 1.5rem;
                font-size: 1.6rem;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .sidebar hr {
                border-color: rgba(255,255,255,0.3);
                margin: 1.5rem 0;
            }
            .nav-button {
                display: block;
                padding: 1rem 1.2rem;
                color: #e2e8f0;
                text-decoration: none;
                border-radius: 0.75rem;
                margin-bottom: 0.75rem;
                transition: all 0.3s ease;
                font-weight: 500;
                font-size: 1.05rem;
                border: 2px solid transparent;
                background: transparent;
                cursor: pointer;
                text-align: left;
                width: 100%;
            }
            .nav-button:hover {
                background: rgba(255,255,255,0.15);
                color: #fff;
                transform: translateX(8px);
                border-color: rgba(255,255,255,0.3);
            }
            .content {
                margin-left: 300px;
                padding: 2.5rem;
                min-height: 100vh;
            }
            .chart-container {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 1.5rem;
                padding: 2rem;
                box-shadow: 0 8px 16px rgba(0,0,0,0.4);
                margin-bottom: 2.5rem;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .page-header {
                color: white;
                margin-bottom: 1.5rem;
                font-size: 2.5rem;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .page-description {
                color: #94a3b8;
                margin-bottom: 2rem;
                font-size: 1.1rem;
                line-height: 1.6;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2.5rem;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 1.2rem;
                padding: 1.5rem;
                color: white;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                text-align: center;
                transition: transform 0.3s ease;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            }
            .stat-value {
                font-size: 2.5rem;
                font-weight: 800;
                margin: 0.5rem 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .stat-label {
                font-size: 0.9rem;
                opacity: 0.95;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
            }
            .search-container {
                background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
                border-radius: 1.5rem;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            }
            .filter-label {
                color: #e2e8f0;
                font-weight: 600;
                margin-bottom: 0.5rem;
                font-size: 1rem;
            }
            .job-card {
                background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-left: 4px solid #667eea;
                transition: all 0.3s ease;
            }
            .job-card:hover {
                transform: translateX(10px);
                box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
            }
            .skill-badge {
                display: inline-block;
                background: rgba(102, 126, 234, 0.2);
                color: #a5b4fc;
                padding: 0.3rem 0.8rem;
                border-radius: 1rem;
                margin: 0.2rem;
                font-size: 0.85rem;
                border: 1px solid rgba(102, 126, 234, 0.3);
            }
            .skill-gap-badge {
                display: inline-block;
                background: rgba(251, 113, 133, 0.2);
                color: #fca5a5;
                padding: 0.3rem 0.8rem;
                border-radius: 1rem;
                margin: 0.2rem;
                font-size: 0.85rem;
                border: 1px solid rgba(251, 113, 133, 0.3);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App Layout
app.layout = html.Div([
    dcc.Store(id='current-page', data='search'),
    dcc.Store(id='selected-jobs-compare', data=[]),
    
    # Sidebar
    html.Div([
        html.H2("💼 Job Analytics"),
        html.Hr(),
        html.Button("🔍 Job Search", id="link-search", className="nav-button"),
        html.Button("🆚 Compare Jobs", id="link-compare", className="nav-button"),
        html.Button("🎯 Skill Gap Analysis", id="link-skillgap", className="nav-button"),
        html.Button("🌟 Sunburst Views", id="link-sunburst", className="nav-button"),
        html.Button("📊 Market Overview", id="link-overview", className="nav-button"),
        html.Button("💰 Salary Insights", id="link-salary", className="nav-button"),
        html.Button("🏢 Top Companies", id="link-companies", className="nav-button"),
        html.Button("📍 Location Analysis", id="link-locations", className="nav-button"),
        html.Button("📈 Hiring Trends", id="link-trends", className="nav-button"),
    ], className="sidebar"),
    
    # Content
    html.Div(id="page-content", className="content")
])

# JOB SEARCH PAGE WITH CARDS
def create_job_search_page():
    job_titles = ['All']
    companies = ['All']
    locations = ['All']
    job_types = ['All']
    
    if 'title' in full_data.columns:
       job_titles += sorted([str(x) for x in full_data['title'].dropna().unique()[:200]])
    if 'company_name' in full_data.columns:
        companies += sorted([str(x) for x in full_data['company_name'].dropna().unique()[:200]])
    if 'location' in full_data.columns:
        locations += sorted([str(x) for x in full_data['location'].dropna().unique()[:200]])
    if 'formatted_work_type' in full_data.columns:
        job_types += sorted([str(x) for x in full_data['formatted_work_type'].dropna().unique()])
    
    return html.Div([
        html.H1("🔍 Find Your Dream Job", className="page-header"),
        html.P("Search for jobs and see detailed cards with company, location, skills, and salary information.", 
               className="page-description"),
        
        html.Div([
            html.H3("🎯 Job Search Filters", style={'color': 'white', 'marginBottom': '1.5rem'}),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Search Job Title", className="filter-label"),
                    dcc.Dropdown(
                        id='job-title-dropdown',
                        options=[{'label': i, 'value': i} for i in job_titles],
                        value='All',
                        placeholder="Type to search job title...",
                        style={'marginBottom': '1rem'}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Company", className="filter-label"),
                    dcc.Dropdown(
                        id='company-dropdown',
                        options=[{'label': i, 'value': i} for i in companies],
                        value='All',
                        placeholder="Select Company",
                        style={'marginBottom': '1rem'}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Location", className="filter-label"),
                    dcc.Dropdown(
                        id='location-dropdown',
                        options=[{'label': i, 'value': i} for i in locations],
                        value='All',
                        placeholder="Select Location",
                        style={'marginBottom': '1rem'}
                    ),
                ], width=3),
                
                dbc.Col([
                    html.Label("Job Type", className="filter-label"),
                    dcc.Dropdown(
                        id='jobtype-dropdown',
                        options=[{'label': i, 'value': i} for i in job_types],
                        value='All',
                        placeholder="Select Job Type",
                        style={'marginBottom': '1rem'}
                    ),
                ], width=3),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Salary Range (if available)", className="filter-label"),
                    dcc.RangeSlider(
                        id='salary-slider',
                        min=0,
                        max=300000,
                        step=10000,
                        value=[0, 300000],
                        marks={0: '$0', 100000: '$100k', 200000: '$200k', 300000: '$300k+'},
                        tooltip={"placement": "bottom", "always_visible": False}
                    ),
                ], width=12),
            ], style={'marginTop': '1rem'}),
            
            html.Div([
                dbc.Button("🔍 Search Jobs", id="search-button", color="primary", size="lg", 
                          style={'marginTop': '1.5rem', 'width': '200px', 'fontWeight': 'bold'}, n_clicks=0)
            ], style={'textAlign': 'center'}),
            
        ], className="search-container"),
        
        html.Div(id='search-results', children=[
            html.Div([
                html.H3("👆 Select filters and click Search", 
                       style={'color': '#94a3b8', 'textAlign': 'center', 'padding': '3rem'})
            ], className="chart-container")
        ])
    ])

# Create search results with job cards
def create_search_results(job_title, company, location, job_type, salary_range):
    filtered_df = full_data.copy()
    
    if job_title != 'All' and 'title' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['title'] == job_title]
    if company != 'All' and 'company_name' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['company_name'] == company]
    if location != 'All' and 'location' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['location'] == location]
    if job_type != 'All' and 'formatted_work_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['formatted_work_type'] == job_type]
    
    # Salary filter
    if 'median_salary' in filtered_df.columns and salary_range:
        filtered_df = filtered_df[
            (filtered_df['median_salary'].isna()) | 
            ((filtered_df['median_salary'] >= salary_range[0]) & (filtered_df['median_salary'] <= salary_range[1]))
        ]
    
    total_jobs = len(filtered_df)
    
    if total_jobs == 0:
        return html.Div([
            html.H3("❌ No jobs found", style={'color': '#f87171', 'textAlign': 'center', 'padding': '2rem'}),
            html.P("Try different filters", style={'color': '#94a3b8', 'textAlign': 'center'})
        ], className="chart-container")
    
    # Stats
    total_companies = filtered_df['company_name'].nunique() if 'company_name' in filtered_df.columns else 0
    total_locations = filtered_df['location'].nunique() if 'location' in filtered_df.columns else 0
    avg_salary = filtered_df['median_salary'].dropna().median() if 'median_salary' in filtered_df.columns else None
    
    # Create job cards (first 20)
    job_cards = []
    for idx, row in filtered_df.head(20).iterrows():
        card_title = row.get('title', 'N/A')
        card_company = row.get('company_name', 'N/A')
        card_location = row.get('location', 'N/A')
        card_type = row.get('formatted_work_type', 'N/A')
        card_salary = f"${row.get('median_salary', 0):,.0f}" if pd.notna(row.get('median_salary')) else "N/A"
        card_skills = row.get('skills_desc', 'N/A')
        
        job_cards.append(
            html.Div([
                html.Div([
                    html.H4(card_title, style={'color': '#667eea', 'marginBottom': '0.5rem', 'fontSize': '1.3rem'}),
                    html.P([
                        html.Span("🏢 ", style={'marginRight': '0.5rem'}),
                        html.Span(card_company, style={'color': '#e2e8f0', 'fontWeight': '600'})
                    ], style={'marginBottom': '0.3rem'}),
                    html.P([
                        html.Span("📍 ", style={'marginRight': '0.5rem'}),
                        html.Span(card_location, style={'color': '#94a3b8'})
                    ], style={'marginBottom': '0.3rem'}),
                    html.P([
                        html.Span("💼 ", style={'marginRight': '0.5rem'}),
                        html.Span(card_type, style={'color': '#94a3b8'}),
                        html.Span(" | ", style={'margin': '0 0.5rem', 'color': '#475569'}),
                        html.Span("💰 ", style={'marginRight': '0.5rem'}),
                        html.Span(card_salary, style={'color': '#34d399', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '0.8rem'}),
                    html.Div([
                        html.Span("🎯 Skills: ", style={'color': '#94a3b8', 'marginRight': '0.5rem'}),
                        html.Span(card_skills, className='skill-badge')
                    ]) if pd.notna(card_skills) and card_skills != 'N/A' else html.Div()
                ])
            ], className="job-card")
        )
    
    # Charts
    top_companies_hiring = pd.DataFrame()
    fig_companies = go.Figure()
    if 'company_name' in filtered_df.columns:
        top_companies_hiring = filtered_df['company_name'].value_counts().head(15).reset_index()
        top_companies_hiring.columns = ['Company', 'Jobs']
        fig_companies = px.bar(top_companies_hiring, x='Jobs', y='Company', 
                               orientation='h', title="🏢 Top Companies Hiring",
                               template="plotly_dark", color='Jobs',
                               color_continuous_scale='Blues')
        fig_companies.update_layout(height=500, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    top_locations_hiring = pd.DataFrame()
    fig_locations = go.Figure()
    if 'location' in filtered_df.columns:
        top_locations_hiring = filtered_df['location'].value_counts().head(15).reset_index()
        top_locations_hiring.columns = ['Location', 'Jobs']
        fig_locations = px.bar(top_locations_hiring, x='Jobs', y='Location',
                               orientation='h', title="📍 Top Hiring Locations",
                               template="plotly_dark", color='Jobs',
                               color_continuous_scale='Greens')
        fig_locations.update_layout(height=500, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    skills_data = pd.DataFrame()
    fig_skills = go.Figure()
    if 'skills_desc' in filtered_df.columns:
        skills_data = filtered_df['skills_desc'].dropna().value_counts().head(20).reset_index()
        skills_data.columns = ['Skill', 'Count']
        fig_skills = px.bar(skills_data, x='Count', y='Skill',
                           orientation='h', title="🎯 Most Required Skills",
                           template="plotly_dark", color='Count',
                           color_continuous_scale='Purples')
        fig_skills.update_layout(height=600, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    return html.Div([
        # Stats
        html.Div([
            html.Div([html.Div("Jobs Found", className="stat-label"), html.Div(f"{total_jobs:,}", className="stat-value")], className="stat-card"),
            html.Div([html.Div("Companies", className="stat-label"), html.Div(f"{total_companies:,}", className="stat-value")], className="stat-card"),
            html.Div([html.Div("Locations", className="stat-label"), html.Div(f"{total_locations:,}", className="stat-value")], className="stat-card"),
            html.Div([html.Div("Median Salary", className="stat-label"), html.Div(f"${avg_salary:,.0f}" if avg_salary else "N/A", className="stat-value")], className="stat-card"),
        ], className="stats-grid"),
        
        # Job Cards Section
        html.Div([
            html.H3("💼 Available Positions (Top 20)", style={'color': 'white', 'marginBottom': '1.5rem'}),
            html.Div(job_cards)
        ], className="chart-container"),
        
        # Charts
        dbc.Row([
            dbc.Col([html.Div([dcc.Graph(figure=fig_companies, config={'displayModeBar': False})], className="chart-container")], width=6),
            dbc.Col([html.Div([dcc.Graph(figure=fig_locations, config={'displayModeBar': False})], className="chart-container")], width=6),
        ]),
        
        dbc.Row([
            dbc.Col([html.Div([dcc.Graph(figure=fig_skills, config={'displayModeBar': False})], className="chart-container")], width=12),
        ]),
    ])

# COMPARE JOBS PAGE
def create_compare_page():
    job_titles = sorted([str(x) for x in full_data['title'].dropna().unique()[:100]]) if 'title' in full_data.columns else []
    
    return html.Div([
        html.H1("🆚 Compare Job Roles", className="page-header"),
        html.P("Select two job titles to compare their skills, salaries, demand, and companies hiring.", className="page-description"),
        
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("Job Title 1", className="filter-label"),
                    dcc.Dropdown(id='compare-job1', options=[{'label': i, 'value': i} for i in job_titles], 
                                placeholder="Select first job", style={'marginBottom': '1rem'}),
                ], width=5),
                dbc.Col([
                    html.H2("VS", style={'color': '#667eea', 'textAlign': 'center', 'marginTop': '1.5rem'}),
                ], width=2),
                dbc.Col([
                    html.Label("Job Title 2", className="filter-label"),
                    dcc.Dropdown(id='compare-job2', options=[{'label': i, 'value': i} for i in job_titles],
                                placeholder="Select second job", style={'marginBottom': '1rem'}),
                ], width=5),
            ]),
            html.Div([
                dbc.Button("🔍 Compare", id="compare-button", color="success", size="lg",
                          style={'marginTop': '1rem', 'width': '200px', 'fontWeight': 'bold'}, n_clicks=0)
            ], style={'textAlign': 'center'}),
        ], className="search-container"),
        
        html.Div(id='compare-results')
    ])

# SKILL GAP ANALYSIS PAGE
def create_skillgap_page():
    job_titles = sorted([str(x) for x in full_data['title'].dropna().unique()[:100]]) if 'title' in full_data.columns else []
    all_skills = sorted([str(x) for x in full_data['skills_desc'].dropna().unique()[:200]]) if 'skills_desc' in full_data.columns else []
    
    return html.Div([
        html.H1("🎯 Skill Gap Analysis", className="page-header"),
        html.P("Select your target job and your current skills. We'll show you what skills you need to learn!", className="page-description"),
        
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("Target Job Title", className="filter-label"),
                    dcc.Dropdown(id='target-job', options=[{'label': i, 'value': i} for i in job_titles],
                                placeholder="Select target job", style={'marginBottom': '1rem'}),
                ], width=6),
                dbc.Col([
                    html.Label("Your Current Skills", className="filter-label"),
                    dcc.Dropdown(id='current-skills', options=[{'label': i, 'value': i} for i in all_skills],
                                multi=True, placeholder="Select your skills", style={'marginBottom': '1rem'}),
                ], width=6),
            ]),
            html.Div([
                dbc.Button("🎯 Analyze Gap", id="skillgap-button", color="warning", size="lg",
                          style={'marginTop': '1rem', 'width': '200px', 'fontWeight': 'bold'}, n_clicks=0)
            ], style={'textAlign': 'center'}),
        ], className="search-container"),
        
        html.Div(id='skillgap-results')
    ])

# SUNBURST PAGE
def create_sunburst_page():
    # Create sunbursts
    fig1 = create_skills_sunburst()
    fig2 = create_company_sunburst()
    fig3 = create_location_sunburst()
    fig4 = create_jobtype_sunburst()
    
    return html.Div([
        html.H1("🌟 Hierarchical Sunburst Visualizations", className="page-header"),
        html.P("Explore relationships between skills, companies, locations, and job types through interactive sunburst charts.", 
               className="page-description"),
        
        dbc.Row([
            dbc.Col([html.Div([
                html.H4("🎯 Skills → Job Type → Company", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '1rem'}),
                dcc.Graph(figure=fig1, config={'displayModeBar': False})
            ], className="chart-container")], width=6),
            dbc.Col([html.Div([
                html.H4("🏢 Company → Location → Job Type", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '1rem'}),
                dcc.Graph(figure=fig2, config={'displayModeBar': False})
            ], className="chart-container")], width=6),
        ]),
        
        dbc.Row([
            dbc.Col([html.Div([
                html.H4("📍 Location → Job Type → Skills", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '1rem'}),
                dcc.Graph(figure=fig3, config={'displayModeBar': False})
            ], className="chart-container")], width=6),
            dbc.Col([html.Div([
                html.H4("💼 Job Type → Company → Location", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '1rem'}),
                dcc.Graph(figure=fig4, config={'displayModeBar': False})
            ], className="chart-container")], width=6),
        ]),
    ])

# Sunburst helper functions
def create_skills_sunburst():
    df = full_data.dropna(subset=['skills_desc', 'formatted_work_type', 'company_name']).copy()
    top_skills_list = df['skills_desc'].value_counts().head(10).index.tolist()
    top_job_types = df['formatted_work_type'].value_counts().head(5).index.tolist()
    top_companies_list = df['company_name'].value_counts().head(20).index.tolist()
    
    df_filtered = df[(df['skills_desc'].isin(top_skills_list)) & (df['formatted_work_type'].isin(top_job_types)) & (df['company_name'].isin(top_companies_list))]
    df_grouped = df_filtered.groupby(['skills_desc', 'formatted_work_type', 'company_name']).size().reset_index(name='count')
    
    fig = px.sunburst(df_grouped, path=['skills_desc', 'formatted_work_type', 'company_name'], values='count',
                     template="plotly_dark", color='count', color_continuous_scale='Viridis')
    fig.update_layout(height=600)
    fig.update_traces(textinfo="label+percent parent")
    return fig

def create_company_sunburst():
    df = full_data.dropna(subset=['company_name', 'location', 'formatted_work_type']).copy()
    top_companies_list = df['company_name'].value_counts().head(15).index.tolist()
    top_locations_list = df['location'].value_counts().head(20).index.tolist()
    top_job_types = df['formatted_work_type'].value_counts().head(5).index.tolist()
    
    df_filtered = df[(df['company_name'].isin(top_companies_list)) & (df['location'].isin(top_locations_list)) & (df['formatted_work_type'].isin(top_job_types))]
    df_grouped = df_filtered.groupby(['company_name', 'location', 'formatted_work_type']).size().reset_index(name='count')
    
    fig = px.sunburst(df_grouped, path=['company_name', 'location', 'formatted_work_type'], values='count',
                     template="plotly_dark", color='count', color_continuous_scale='Blues')
    fig.update_layout(height=600)
    fig.update_traces(textinfo="label+percent parent")
    return fig

def create_location_sunburst():
    df = full_data.dropna(subset=['location', 'formatted_work_type', 'skills_desc']).copy()
    top_locations_list = df['location'].value_counts().head(15).index.tolist()
    top_job_types = df['formatted_work_type'].value_counts().head(5).index.tolist()
    top_skills_list = df['skills_desc'].value_counts().head(20).index.tolist()
    
    df_filtered = df[(df['location'].isin(top_locations_list)) & (df['formatted_work_type'].isin(top_job_types)) & (df['skills_desc'].isin(top_skills_list))]
    df_grouped = df_filtered.groupby(['location', 'formatted_work_type', 'skills_desc']).size().reset_index(name='count')
    
    fig = px.sunburst(df_grouped, path=['location', 'formatted_work_type', 'skills_desc'], values='count',
                     template="plotly_dark", color='count', color_continuous_scale='Greens')
    fig.update_layout(height=600)
    fig.update_traces(textinfo="label+percent parent")
    return fig

def create_jobtype_sunburst():
    df = full_data.dropna(subset=['formatted_work_type', 'company_name', 'location']).copy()
    top_job_types = df['formatted_work_type'].value_counts().head(5).index.tolist()
    top_companies_list = df['company_name'].value_counts().head(20).index.tolist()
    top_locations_list = df['location'].value_counts().head(15).index.tolist()
    
    df_filtered = df[(df['formatted_work_type'].isin(top_job_types)) & (df['company_name'].isin(top_companies_list)) & (df['location'].isin(top_locations_list))]
    df_grouped = df_filtered.groupby(['formatted_work_type', 'company_name', 'location']).size().reset_index(name='count')
    
    fig = px.sunburst(df_grouped, path=['formatted_work_type', 'company_name', 'location'], values='count',
                     template="plotly_dark", color='count', color_continuous_scale='Purples')
    fig.update_layout(height=600)
    fig.update_traces(textinfo="label+percent parent")
    return fig

# Other page functions
def create_overview_page():
    total_jobs = len(full_data)
    total_companies = full_data['company_name'].nunique() if 'company_name' in full_data.columns else 0
    total_locations = full_data['location'].nunique() if 'location' in full_data.columns else 0
    
    fig_trends = px.line(monthly_trends, x=monthly_trends.columns[0], y=monthly_trends.columns[1],
                        title="📈 Monthly Job Posting Trends", template="plotly_dark", markers=True)
    fig_trends.update_layout(height=500)
    fig_trends.update_traces(line_color='#667eea', line_width=3, marker_size=8)
    
    fig_jobtype = px.pie(job_type_dist, values=job_type_dist.columns[1], names=job_type_dist.columns[0],
                        title="💼 Job Type Distribution", template="plotly_dark", hole=0.4)
    fig_jobtype.update_layout(height=500)
    
    fig_industries = px.bar(top_industries.head(15), x=top_industries.columns[1], y=top_industries.columns[0],
                           orientation='h', title="🏭 Top Industries Hiring", template="plotly_dark", 
                           color=top_industries.columns[1], color_continuous_scale='Teal')
    fig_industries.update_layout(height=500, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    return html.Div([
        html.H1("📊 Job Market Overview", className="page-header"),
        html.P("Complete snapshot of the job market landscape.", className="page-description"),
        
        html.Div([
            html.Div([html.Div("Total Jobs", className="stat-label"), html.Div(f"{total_jobs:,}", className="stat-value")], className="stat-card"),
            html.Div([html.Div("Companies", className="stat-label"), html.Div(f"{total_companies:,}", className="stat-value")], className="stat-card"),
            html.Div([html.Div("Locations", className="stat-label"), html.Div(f"{total_locations:,}", className="stat-value")], className="stat-card"),
        ], className="stats-grid"),
        
        dbc.Row([
            dbc.Col([html.Div([dcc.Graph(figure=fig_trends)], className="chart-container")], width=8),
            dbc.Col([html.Div([dcc.Graph(figure=fig_jobtype)], className="chart-container")], width=4),
        ]),
        dbc.Row([
            dbc.Col([html.Div([dcc.Graph(figure=fig_industries)], className="chart-container")], width=12),
        ]),
    ])

def create_salary_page():
    fig1 = px.bar(top_paying_jobs.head(20), x=top_paying_jobs.columns[1], y=top_paying_jobs.columns[0],
                 orientation='h', title="💰 Top Paying Job Titles", template="plotly_dark", 
                 color=top_paying_jobs.columns[1], color_continuous_scale='Viridis')
    fig1.update_layout(height=500, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    fig2 = px.bar(experience_salary, x=experience_salary.columns[1], y=experience_salary.columns[0],
                 title="💼 Salary by Experience Level", template="plotly_dark", 
                 color=experience_salary.columns[1], color_continuous_scale='Blues')
    fig2.update_layout(height=400, showlegend=False)
    
    return html.Div([
        html.H1("💰 Salary Insights", className="page-header"),
        html.P("Understand salary ranges for different roles and experience levels.", className="page-description"),
        dbc.Row([
            dbc.Col([html.Div([dcc.Graph(figure=fig1)], className="chart-container")], width=7),
            dbc.Col([html.Div([dcc.Graph(figure=fig2)], className="chart-container")], width=5),
        ]),
    ])

def create_companies_page():
    fig = px.bar(top_companies.head(25), x=top_companies.columns[1], y=top_companies.columns[0],
                orientation='h', title="🏢 Top Hiring Companies", template="plotly_dark", 
                color=top_companies.columns[1], color_continuous_scale='Blues')
    fig.update_layout(height=800, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    return html.Div([
        html.H1("🏢 Top Companies", className="page-header"),
        html.P("See which companies are actively hiring.", className="page-description"),
        html.Div([dcc.Graph(figure=fig)], className="chart-container"),
    ])

def create_locations_page():
    fig = px.bar(top_locations.head(25), x=top_locations.columns[1], y=top_locations.columns[0],
                orientation='h', title="📍 Top Job Locations", template="plotly_dark", 
                color=top_locations.columns[1], color_continuous_scale='Greens')
    fig.update_layout(height=800, showlegend=False, yaxis={'categoryorder':'total ascending'})
    
    return html.Div([
        html.H1("📍 Location Insights", className="page-header"),
        html.P("Discover where jobs are concentrated.", className="page-description"),
        html.Div([dcc.Graph(figure=fig)], className="chart-container"),
    ])

def create_trends_page():
    fig = px.line(monthly_trends, x=monthly_trends.columns[0], y=monthly_trends.columns[1],
                title="📈 Hiring Trends Over Time", template="plotly_dark", markers=True)
    fig.update_layout(height=600)
    fig.update_traces(line_color='#667eea', line_width=4, marker_size=10)
    
    return html.Div([
        html.H1("📈 Hiring Trends", className="page-header"),
        html.P("Track how job postings change over time.", className="page-description"),
        html.Div([dcc.Graph(figure=fig)], className="chart-container"),
    ])

# Callbacks
@app.callback(
    [Output("page-content", "children"), Output("current-page", "data")],
    [Input("link-search", "n_clicks"), Input("link-compare", "n_clicks"),
     Input("link-skillgap", "n_clicks"), Input("link-sunburst", "n_clicks"),
     Input("link-overview", "n_clicks"), Input("link-salary", "n_clicks"),
     Input("link-companies", "n_clicks"), Input("link-locations", "n_clicks"),
     Input("link-trends", "n_clicks")],
    [State("current-page", "data")]
)
def update_page(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return create_job_search_page(), 'search'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    pages = {
        "link-search": (create_job_search_page(), 'search'),
        "link-compare": (create_compare_page(), 'compare'),
        "link-skillgap": (create_skillgap_page(), 'skillgap'),
        "link-sunburst": (create_sunburst_page(), 'sunburst'),
        "link-overview": (create_overview_page(), 'overview'),
        "link-salary": (create_salary_page(), 'salary'),
        "link-companies": (create_companies_page(), 'companies'),
        "link-locations": (create_locations_page(), 'locations'),
        "link-trends": (create_trends_page(), 'trends')
    }
    return pages.get(button_id, (create_job_search_page(), 'search'))

@app.callback(
    Output('search-results', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('job-title-dropdown', 'value'), State('company-dropdown', 'value'),
     State('location-dropdown', 'value'), State('jobtype-dropdown', 'value'),
     State('salary-slider', 'value')],
    prevent_initial_call=False
)
def update_search_results(n_clicks, job_title, company, location, job_type, salary_range):
    if n_clicks == 0:
        return html.Div([
            html.H3("👆 Select filters and click Search", 
                   style={'color': '#94a3b8', 'textAlign': 'center', 'padding': '3rem'})
        ], className="chart-container")
    return create_search_results(job_title, company, location, job_type, salary_range)

@app.callback(
    Output('compare-results', 'children'),
    [Input('compare-button', 'n_clicks')],
    [State('compare-job1', 'value'), State('compare-job2', 'value')],
    prevent_initial_call=True
)
def update_compare_results(n_clicks, job1, job2):
    if not job1 or not job2:
        return html.Div([
            html.H3("⚠️ Please select both job titles to compare", 
                   style={'color': '#fbbf24', 'textAlign': 'center', 'padding': '2rem'})
        ], className="chart-container")
    
    # Filter data for both jobs
    df1 = full_data[full_data['title'] == job1] if 'title' in full_data.columns else pd.DataFrame()
    df2 = full_data[full_data['title'] == job2] if 'title' in full_data.columns else pd.DataFrame()
    
    # Stats comparison
    job1_count = len(df1)
    job2_count = len(df2)
    job1_salary = df1['median_salary'].median() if 'median_salary' in df1.columns else None
    job2_salary = df2['median_salary'].median() if 'median_salary' in df2.columns else None
    job1_companies = df1['company_name'].nunique() if 'company_name' in df1.columns else 0
    job2_companies = df2['company_name'].nunique() if 'company_name' in df2.columns else 0
    
    # Top skills comparison
    job1_skills = df1['skills_desc'].value_counts().head(10) if 'skills_desc' in df1.columns else pd.Series()
    job2_skills = df2['skills_desc'].value_counts().head(10) if 'skills_desc' in df2.columns else pd.Series()
    
    # Create comparison chart
    comparison_data = pd.DataFrame({
        'Metric': ['Job Postings', 'Companies Hiring', 'Median Salary'],
        job1: [job1_count, job1_companies, job1_salary if job1_salary else 0],
        job2: [job2_count, job2_companies, job2_salary if job2_salary else 0]
    })
    
    fig_comparison = go.Figure()
    fig_comparison.add_trace(go.Bar(name=job1, x=comparison_data['Metric'], y=comparison_data[job1], marker_color='#667eea'))
    fig_comparison.add_trace(go.Bar(name=job2, x=comparison_data['Metric'], y=comparison_data[job2], marker_color='#764ba2'))
    fig_comparison.update_layout(barmode='group', template='plotly_dark', title='📊 Side-by-Side Comparison', height=400)
    
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H3(job1, style={'color': '#667eea', 'textAlign': 'center'}),
                    html.Div([html.Div(f"{job1_count:,}", className="stat-value"), html.Div("Jobs", className="stat-label")], className="stat-card"),
                    html.Div([html.Div(f"${job1_salary:,.0f}" if job1_salary else "N/A", className="stat-value"), html.Div("Salary", className="stat-label")], className="stat-card"),
                    html.Div([html.Div(f"{job1_companies:,}", className="stat-value"), html.Div("Companies", className="stat-label")], className="stat-card"),
                ], width=5),
                dbc.Col([html.H2("VS", style={'color': 'white', 'textAlign': 'center', 'fontSize': '3rem', 'marginTop': '3rem'})], width=2),
                dbc.Col([
                    html.H3(job2, style={'color': '#764ba2', 'textAlign': 'center'}),
                    html.Div([html.Div(f"{job2_count:,}", className="stat-value"), html.Div("Jobs", className="stat-label")], className="stat-card"),
                    html.Div([html.Div(f"${job2_salary:,.0f}" if job2_salary else "N/A", className="stat-value"), html.Div("Salary", className="stat-label")], className="stat-card"),
                    html.Div([html.Div(f"{job2_companies:,}", className="stat-value"), html.Div("Companies", className="stat-label")], className="stat-card"),
                ], width=5),
            ])
        ], className="chart-container"),
        
        html.Div([dcc.Graph(figure=fig_comparison)], className="chart-container"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4(f"🎯 Top Skills for {job1}", style={'color': 'white', 'marginBottom': '1rem'}),
                    html.Div([html.Span(skill, className='skill-badge') for skill in job1_skills.index[:10]])
                ], className="chart-container")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H4(f"🎯 Top Skills for {job2}", style={'color': 'white', 'marginBottom': '1rem'}),
                    html.Div([html.Span(skill, className='skill-badge') for skill in job2_skills.index[:10]])
                ], className="chart-container")
            ], width=6),
        ]),
    ])

@app.callback(
    Output('skillgap-results', 'children'),
    [Input('skillgap-button', 'n_clicks')],
    [State('target-job', 'value'), State('current-skills', 'value')],
    prevent_initial_call=True
)
def update_skillgap_results(n_clicks, target_job, current_skills):
    if not target_job:
        return html.Div([
            html.H3("⚠️ Please select a target job", 
                   style={'color': '#fbbf24', 'textAlign': 'center', 'padding': '2rem'})
        ], className="chart-container")
    
    current_skills = current_skills or []
    
    # Get required skills for target job
    df_target = full_data[full_data['title'] == target_job] if 'title' in full_data.columns else pd.DataFrame()
    required_skills = df_target['skills_desc'].value_counts().head(15) if 'skills_desc' in df_target.columns else pd.Series()
    
    # Calculate skill gap
    missing_skills = [skill for skill in required_skills.index if skill not in current_skills]
    matching_skills = [skill for skill in required_skills.index if skill in current_skills]
    
    match_percentage = (len(matching_skills) / len(required_skills) * 100) if len(required_skills) > 0 else 0
    
    return html.Div([
        html.Div([
            html.H3(f"🎯 Skill Analysis for {target_job}", style={'color': 'white', 'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Div([
                    html.Div(f"{match_percentage:.0f}%", className="stat-value"),
                    html.Div("Skills Match", className="stat-label")
                ], className="stat-card"),
                html.Div([
                    html.Div(f"{len(matching_skills)}", className="stat-value"),
                    html.Div("Skills You Have", className="stat-label")
                ], className="stat-card"),
                html.Div([
                    html.Div(f"{len(missing_skills)}", className="stat-value"),
                    html.Div("Skills to Learn", className="stat-label")
                ], className="stat-card"),
            ], className="stats-grid"),
        ], className="chart-container"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("✅ Skills You Have", style={'color': '#34d399', 'marginBottom': '1rem'}),
                    html.Div([html.Span(skill, className='skill-badge') for skill in matching_skills]) if matching_skills else html.P("No matching skills", style={'color': '#94a3b8'})
                ], className="chart-container")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H4("🎓 Skills to Learn", style={'color': '#fb7185', 'marginBottom': '1rem'}),
                    html.Div([html.Span(skill, className='skill-gap-badge') for skill in missing_skills]) if missing_skills else html.P("You have all required skills!", style={'color': '#34d399'})
                ], className="chart-container")
            ], width=6),
        ]),
        
        html.Div([
            html.H4("💡 Recommendations", style={'color': 'white', 'marginBottom': '1rem'}),
            html.Ul([
                html.Li(f"Focus on learning: {', '.join(missing_skills[:3])}", style={'color': '#94a3b8', 'marginBottom': '0.5rem'}) if len(missing_skills) >= 3 else html.Li("Great! You have most required skills", style={'color': '#34d399'}),
                html.Li(f"Your strongest skills: {', '.join(matching_skills[:3])}", style={'color': '#94a3b8', 'marginBottom': '0.5rem'}) if matching_skills else None,
                html.Li(f"Consider taking online courses for the missing skills", style={'color': '#94a3b8', 'marginBottom': '0.5rem'}),
            ])
        ], className="chart-container")
    ])

if __name__ == "__main__":
    app.run(debug=True, port=8050)