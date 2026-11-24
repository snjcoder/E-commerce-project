# 📊 E-Commerce Analytics Dashboard: Amazon vs. Alibaba vs. eBay
I built this interactive dashboard to compare the performance of three e-commerce giants—Amazon, Alibaba, and eBay—over an 11-year span (2010–2020). Instead of just looking at raw spreadsheets, I wanted a clean, visual way to explore sales trends, customer scales, and profitability metrics.

This is a purely descriptive analytics project. It's designed to show what the data looks like, without making assumptions about why things happened (remember: correlation doesn't equal causation!).

# 📁 Dataset
The dataset used is "E-Commerce Giants Comparison (2010-2020)", sourced from Kaggle. It contains 12,054 daily records detailing total sales, active users, market share, gross margin, operating income, average order value, and mobile transaction share.

# 📈 Live Interaction Dashboard
Interactive Filters: Filter the entire dashboard by Company, Year (2010–2020), and Top Region.

**[open the live Dashboard](#)**

📓 Jupyter Notebook

**[View the Data Analysis notebook](#)**

# 🔍 Key Analysis
One of the most interesting things I discovered while building this is that the three companies look surprisingly similar in this dataset.

1. Nearly identical averages: eBay has the highest average sales ($251.9B), followed by Amazon ($249.7B) and Alibaba ($249.2B)—a gap of only about 1%.

2. No major trends: Annual sales fluctuate around $250B, with 2017 being the strongest year and 2020 the weakest.

3. Balanced regions: Europe, North America, and Asia are almost exactly tied for the top-sales region.

4. A skewed new metric: I created a custom "Sales per Active User" metric. While eBay leads on average, the data is heavily skewed by a few records with very low user counts, so rankings here need to be taken with a grain of salt.

5. Dynamic KPI Cards: Get instant averages for Sales, Active Users, Market Share, Gross Margin, and Sales per Active User.

6. Interactive Charts:
- Average Total Sales by Company
- Annual Sales Trend
- Sales by Top Region
- Market Share vs. Gross Margin
- Order Value vs. Mobile Transactions
- Sales per Active User Trend


# 🛠️ Technologies
Python - Core programming language

Pandas - Data cleaning and manipulation

Plotly - Interactive data visualizations

Dash - Web framework for the dashboard

HTML/CSS - Dashboard layout and styling

# 💡Outcomes
Building this taught me a lot about the end-to-end data workflow, from cleaning raw CSVs with Pandas to wiring up a complex Dash callback.

Because the data is spread so evenly and the companies look so alike, it's highly likely this specific Kaggle dataset is simulated. Therefore, the insights here are great for practicing data visualization and monitoring mock performance, but they shouldn't be used to draw real-world conclusions about Amazon, Alibaba, or eBay.
