# ==============================================================================
# Import libraries
# ==============================================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ==============================================================================
# Load cleaned dataset
# ==============================================================================
df = pd.read_csv("e_commerce_cleaned_data.csv")

# ==============================================================================
# Initialize Dash app
# ==============================================================================
app = Dash(__name__)
app.title = "E-Commerce Performance Dashboard"

# ==============================================================================
# Filter values
# ==============================================================================
companies = sorted(df['Company'].dropna().unique())
years = sorted(df['Year'].dropna().unique())
regions = sorted(df['Region_with_Highest_Sales'].dropna().unique())

# ==============================================================================
# Reusable styles
# ==============================================================================
CARD = {
    'padding': '14px 18px',
    'border': '1px solid #dddddd',
    'borderRadius': '10px',
    'width': '180px',
    'textAlign': 'center',
    'backgroundColor': '#ffffff',
    'boxShadow': '0 2px 5px rgba(0,0,0,0.05)'
}

CHART_CARD = {
    'backgroundColor': '#ffffff',
    'padding': '15px',
    'borderRadius': '10px',
    'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
    'marginBottom': '20px'
}

# ==============================================================================
# App Layout
# ==============================================================================
app.layout = html.Div([
    
    # Title
    html.H1("E-Commerce Performance Dashboard (2010-2020)", 
            style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif', 'color': '#333'}),
    html.P("Comparing Amazon, Alibaba, and eBay — Descriptive Analytics", 
           style={'textAlign': 'center', 'color': '#666', 'marginBottom': '30px'}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Company"),
            dcc.Dropdown(id='company-filter', options=[{'label': c, 'value': c} for c in companies], 
                         value=companies, multi=True)
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Year"),
            dcc.Dropdown(id='year-filter', options=[{'label': str(y), 'value': y} for y in years], 
                         value=years, multi=True)
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Region"),
            dcc.Dropdown(id='region-filter', options=[{'label': r, 'value': r} for r in regions], 
                         value=regions, multi=True)
        ], style={'width': '30%', 'display': 'inline-block'}),
    ], style={'marginBottom': '30px', 'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px'}),

    # KPI Cards
    html.Div([
        html.Div([html.H4("Avg Total Sales", style={'margin': '0', 'color': '#666', 'fontSize': '14px'}),
                  html.H2(id='kpi-sales', style={'margin': '10px 0 0 0', 'color': '#111'})], style=CARD),
        html.Div([html.H4("Avg Active Users", style={'margin': '0', 'color': '#666', 'fontSize': '14px'}),
                  html.H2(id='kpi-users', style={'margin': '10px 0 0 0', 'color': '#111'})], style=CARD),
        html.Div([html.H4("Avg Market Share", style={'margin': '0', 'color': '#666', 'fontSize': '14px'}),
                  html.H2(id='kpi-share', style={'margin': '10px 0 0 0', 'color': '#111'})], style=CARD),
        html.Div([html.H4("Avg Gross Margin", style={'margin': '0', 'color': '#666', 'fontSize': '14px'}),
                  html.H2(id='kpi-margin', style={'margin': '10px 0 0 0', 'color': '#111'})], style=CARD),
        html.Div([html.H4("Avg Sales / User", style={'margin': '0', 'color': '#666', 'fontSize': '14px'}),
                  html.H2(id='kpi-spau', style={'margin': '10px 0 0 0', 'color': '#111'})], style=CARD),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),

    # Charts Grid (2 columns)
    html.Div([
        html.Div(dcc.Graph(id='fig-avg-sales'), style=CHART_CARD),
        html.Div(dcc.Graph(id='fig-annual-trend'), style=CHART_CARD),
        html.Div(dcc.Graph(id='fig-regional'), style=CHART_CARD),
        html.Div(dcc.Graph(id='fig-share-margin'), style=CHART_CARD),
        html.Div(dcc.Graph(id='fig-order-mobile'), style=CHART_CARD),
        html.Div(dcc.Graph(id='fig-spau-trend'), style=CHART_CARD),
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}),
    
    # Footer
    html.Footer("Data Source: Kaggle E-Commerce Giants Comparison. Note: Correlation does not imply causation.", 
                style={'textAlign': 'center', 'color': '#888', 'marginTop': '40px', 'fontSize': '12px'})

], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px', 'backgroundColor': '#f4f7f6', 'minHeight': '100vh'})

# ==============================================================================
# Callback to update KPIs and Charts
# ==============================================================================
@app.callback(
    [Output('kpi-sales', 'children'),
     Output('kpi-users', 'children'),
     Output('kpi-share', 'children'),
     Output('kpi-margin', 'children'),
     Output('kpi-spau', 'children'),
     Output('fig-avg-sales', 'figure'),
     Output('fig-annual-trend', 'figure'),
     Output('fig-regional', 'figure'),
     Output('fig-share-margin', 'figure'),
     Output('fig-order-mobile', 'figure'),
     Output('fig-spau-trend', 'figure')],
    [Input('company-filter', 'value'),
     Input('year-filter', 'value'),
     Input('region-filter', 'value')]
)
def update_dashboard(selected_companies, selected_years, selected_regions):
    
    # Handle empty filter selections
    if not selected_companies: selected_companies = companies
    if not selected_years: selected_years = years
    if not selected_regions: selected_regions = regions

    # Filter data
    dff = df[
        (df['Company'].isin(selected_companies)) & 
        (df['Year'].isin(selected_years)) & 
        (df['Region_with_Highest_Sales'].isin(selected_regions))
    ]

    # Handle empty dataframe
    if dff.empty:
        empty_fig = px.scatter(title="No data available for current filters")
        empty_fig.update_layout(template="plotly_white")
        return "0", "0", "0%", "0%", "$0", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # --- KPIs ---
    avg_sales = f"${dff['Total_Sales (USD Billion)'].mean():,.1f}B"
    avg_users = f"{dff['Active_Users (Million)'].mean():,.0f}M"
    avg_share = f"{dff['Market_Share (%)'].mean():,.1f}%"
    avg_margin = f"{dff['Gross_Margin (%)'].mean():,.1f}%"
    avg_spau = f"${dff['Sales_per_Active_User_USD'].mean():,.0f}"

    # --- Chart 1: Avg Sales ---
    fig1 = px.bar(dff.groupby('Company')['Total_Sales (USD Billion)'].mean().reset_index(),
                  x='Company', y='Total_Sales (USD Billion)', color='Company',
                  title="Average Total Sales by Company", text_auto='.1f')
    fig1.update_layout(template="plotly_white", showlegend=False)

    # --- Chart 2: Annual Trend ---
    fig2 = px.line(dff.groupby(['Year', 'Company'])['Total_Sales (USD Billion)'].mean().reset_index(),
                   x='Year', y='Total_Sales (USD Billion)', color='Company', markers=True,
                   title="Annual Average Sales Trend")
    fig2.update_layout(template="plotly_white")

    # --- Chart 3: Regional Sales ---
    fig3 = px.bar(dff.groupby(['Region_with_Highest_Sales', 'Company'])['Total_Sales (USD Billion)'].mean().reset_index(),
                  x='Region_with_Highest_Sales', y='Total_Sales (USD Billion)', color='Company', barmode='group',
                  title="Sales by Top Region")
    fig3.update_layout(template="plotly_white", xaxis_title="Region")

    # --- Chart 4: Share vs Margin ---
    share_margin = dff.groupby('Company')[['Market_Share (%)', 'Gross_Margin (%)']].mean().reset_index()
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=share_margin['Company'], y=share_margin['Market_Share (%)'], name='Market Share', marker_color='#4C78A8'))
    fig4.add_trace(go.Bar(x=share_margin['Company'], y=share_margin['Gross_Margin (%)'], name='Gross Margin', marker_color='#F58518'))
    fig4.update_layout(barmode='group', title="Market Share vs Gross Margin", template="plotly_white")

    # --- Chart 5: Order Value vs Mobile ---
    order_mobile = dff.groupby('Company')[['Average_Order_Value (USD)', 'Mobile_Transactions (%)']].mean().reset_index()
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=order_mobile['Company'], y=order_mobile['Average_Order_Value (USD)'], name='Avg Order Value (USD)', marker_color='#54A24B'))
    fig5.add_trace(go.Scatter(x=order_mobile['Company'], y=order_mobile['Mobile_Transactions (%)'], name='Mobile Trans (%)', mode='lines+markers', yaxis='y2', marker=dict(color='#E45756', size=10)))
    fig5.update_layout(title="Order Value vs Mobile Transactions", template="plotly_white",
                       yaxis=dict(title='AOV (USD)'),
                       yaxis2=dict(title='Mobile Share (%)', overlaying='y', side='right'))

    # --- Chart 6: SPAU Trend ---
    fig6 = px.line(dff.groupby(['Year', 'Company'])['Sales_per_Active_User_USD'].mean().reset_index(),
                   x='Year', y='Sales_per_Active_User_USD', color='Company', markers=True,
                   title="Sales per Active User Trend")
    fig6.update_layout(template="plotly_white", yaxis_title="USD per User")

    return avg_sales, avg_users, avg_share, avg_margin, avg_spau, fig1, fig2, fig3, fig4, fig5, fig6

# ==============================================================================
# Run App
# ==============================================================================
server = app.server  # Expose the server variable for deployment

if __name__ == '__main__':
    app.run(debug=True)