# Alberta Grant Distribution Analysis

A comprehensive Streamlit dashboard analyzing Alberta's grant distribution patterns from 2014-2024. This portfolio project demonstrates data analysis, visualization, and interactive dashboard development skills using open government data.

## Features

- **Interactive Visualizations**: Treemaps, bar charts, and time-series analysis using Plotly
- **Dynamic Filtering**: Filter by ministry, fiscal year, and program
- **Non-Profit Analysis**: Deep dive into how grants flow through active non-profit organizations
- **Economic Context**: Compare grant trends with Alberta's economic activity and employment rates
- **Responsive Design**: Optimized for desktop and mobile viewing
- **Production-Ready**: Deployed on Streamlit Community Cloud with professional configuration

## Live Demo

🚀 **[View Live Dashboard](https://albertagrantsdashboard-da9bbqn8mzh66kpxeqtm6b.streamlit.app/)**

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .python-version          # Python version for deployment
├── streamlit_app.py         # Entry point for Streamlit Cloud
├── packages.txt             # System packages (if needed)
├── smoke_test.py
├── Dockerfile
├── .gitignore
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── src/
    ├── __init__.py
    ├── app.py               # Main application logic
    ├── components/
    │   ├── __init__.py
    │   ├── chart.py         # Chart components
    │   └── kpi.py           # KPI components
    └── data/
        ├── __init__.py
        ├── loader.py        # Data loading utilities
        ├── employment_rate.csv
        ├── grant_disclosure_combined.csv
        └── README.md
```

## Local Development

### Prerequisites

- Python 3.11+ (specified in `.python-version`)
- Git

### Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd AlbertaShowCase
```

2. **Create and activate virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run the application**

```bash
streamlit run streamlit_app.py
# Or alternatively:
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`


## Data Sources

- **Grant Payments**: Alberta Government Grant Payments Disclosure
- **Non-Profit Registry**: Alberta Corporate Registry
- **Economic Indicators**: Alberta Activity Index & Employment Statistics

## Technologies Used

- **Frontend**: Streamlit 1.37.1
- **Data Processing**: Pandas 2.2.2
- **Visualizations**: Plotly 5.24.1
- **Configuration**: python-dotenv 1.0.1

## Project Highlights

### Data Scale

- 1.2M+ grant payment records
- $330B+ in total grant distribution
- 27,634 active non-profit organizations tracked
- 10-year analysis period (2014-2024)

### Key Insights Provided

- Ministry-level funding distribution
- Program effectiveness tracking
- Non-profit sector analysis
- Economic context and correlation
- Employment trend analysis


## License

This project is open source and available for educational and portfolio purposes.