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

🚀 **[View Live Dashboard](YOUR_STREAMLIT_CLOUD_URL_HERE)**

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

4. **Run smoke test (optional)**

```bash
python smoke_test.py
```

5. **Run the application**

```bash
streamlit run streamlit_app.py
# Or alternatively:
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Community Cloud

### Quick Deploy Steps

1. **Push to GitHub**

   - Ensure all files are committed and pushed to your GitHub repository
   - Make sure `.gitignore` excludes `.venv/`, `__pycache__/`, and `.streamlit/secrets.toml`

2. **Connect to Streamlit Cloud**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `<username>/AlbertaShowCase`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configuration** (Optional)
   - Streamlit Cloud will automatically detect:
     - Python version from `.python-version`
     - Dependencies from `requirements.txt`
     - Configuration from `.streamlit/config.toml`
     - System packages from `packages.txt` (if any)

### Environment Variables

If you need environment variables (e.g., API keys), add them in Streamlit Cloud:

- Go to your app settings
- Navigate to "Secrets"
- Add secrets in TOML format:
  ```toml
  APP_TITLE = "Your Custom Title"
  PAGE_ICON = "📊"
  ```

### Custom Domain (Optional)

Once deployed, you can configure a custom domain:

1. Go to app settings
2. Navigate to "General"
3. Set up custom domain under "App URL"

## Docker Deployment (Alternative)

If you prefer Docker deployment:

## Docker Deployment (Alternative)

If you prefer Docker deployment:

```bash
# Build the image
docker build -t alberta-showcase .

# Run the container
docker run -p 8501:8501 alberta-showcase
```

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

## Contributing

This is a portfolio project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

This project is open source and available for educational and portfolio purposes.

## Contact

**Yevhenii Borysenko**

- Email: borisenko1315@gmail.com
- GitHub: [Your GitHub Profile]
- LinkedIn: [Your LinkedIn Profile]

## Acknowledgments

- Alberta Government for providing open data
- Streamlit community for excellent documentation
- Open data advocates supporting government transparency

---

_Built with ❤️ using Streamlit_

4. Start the app:

```bash
streamlit run src/app.py
```

Open http://localhost:8501 if your browser doesn’t open automatically.

## Provide your data

- Click "Upload CSV" in the sidebar, or
- Replace `src/data/sample.csv` with your data file and update `src/data/loader.py` to match your schema.

Expected columns (or map to these names):

- `date` (parsable as a date)
- `category`
- `region`
- `value` (numeric)

## Easy deployment

### Option A: Streamlit Community Cloud (fastest)

1. Push this folder to a Git repository (GitHub preferred).
2. Go to https://share.streamlit.io and link the repo.
3. Set the main file to `src/app.py`.
4. Deploy. That’s it.

### Option B: Docker (works anywhere)

Build and run locally:

```bash
docker build -t open-data-insights .
docker run --rm -p 8501:8501 open-data-insights
```

Deploy this image to any container platform (Fly.io, Railway, Render, GCP Cloud Run, Azure Container Apps, etc.).

## Customization

- App title/icon: set `APP_TITLE`/`PAGE_ICON` in a `.env` file (load via `python-dotenv`).
- Theme: tweak `.streamlit/config.toml`.
- Charts/KPIs: edit `src/components/*.py`.

## Notes

- This is a demo template; security is intentionally minimal. Don’t store secrets in the repo. For Streamlit Cloud, use `secrets.toml`.
- For a private share, consider using an expiring, unlisted Streamlit Cloud app URL or share only with the target email.
