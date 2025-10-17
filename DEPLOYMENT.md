# Streamlit Community Cloud Deployment Guide

This guide walks you through deploying the Alberta Grant Distribution Analysis dashboard to Streamlit Community Cloud.

## Prerequisites

- [ ] GitHub account
- [ ] Git installed locally
- [ ] Project code ready to deploy
- [ ] All dependencies specified in `requirements.txt`

## Pre-Deployment Checklist

### 1. Verify Project Structure

Ensure your project has these key files in the root directory:

```
✅ streamlit_app.py       # Entry point for Streamlit Cloud
✅ requirements.txt       # Python dependencies
✅ .python-version        # Python version (3.11)
✅ .streamlit/config.toml # Streamlit configuration
✅ .gitignore             # Git ignore rules
✅ packages.txt           # System packages (optional, can be empty)
✅ README.md              # Project documentation
```

### 2. Check File Naming Conventions

Streamlit Community Cloud looks for specific file names:

- **Main app**: `streamlit_app.py` (preferred) or `app.py`
- **Requirements**: `requirements.txt` (must be exact name)
- **Python version**: `.python-version` or `runtime.txt`
- **Config**: `.streamlit/config.toml`
- **System packages**: `packages.txt`

### 3. Verify Requirements

Open `requirements.txt` and ensure:

- All dependencies are listed
- Versions are specified (recommended for stability)
- No local/development-only packages

Current requirements:

```
streamlit==1.37.1
pandas==2.2.2
plotly==5.24.1
python-dotenv==1.0.1
```

### 4. Test Locally

Before deploying, test your app locally:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the app
streamlit run streamlit_app.py

# Verify:
# - App loads without errors
# - All visualizations render
# - Filters work correctly
# - No missing dependencies
```

### 5. Prepare Git Repository

#### Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: Prepare for Streamlit deployment"
```

#### Push to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/AlbertaShowCase.git
git branch -M main
git push -u origin main
```

#### Verify on GitHub

- Check that all files are present
- Verify `.gitignore` is working (no `.venv/`, `__pycache__/`, etc.)
- Ensure data files are included (check file sizes < 100MB)

## Deployment Steps

### Step 1: Sign in to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** or **"Sign in"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub account

### Step 2: Create New App

1. Click **"New app"** button (top right)
2. Fill in the deployment form:

   **Repository:**

   - Select your GitHub repository: `YOUR_USERNAME/AlbertaShowCase`

   **Branch:**

   - Select `main` (or your default branch)

   **Main file path:**

   - Enter: `streamlit_app.py`

   **App URL (optional):**

   - Custom subdomain: `alberta-showcase` (or your choice)
   - Full URL will be: `https://alberta-showcase.streamlit.app`

3. Click **"Advanced settings"** (optional):

   - **Python version**: Auto-detected from `.python-version` (3.11)
   - **Secrets**: Add if you have environment variables (see below)

4. Click **"Deploy!"**

### Step 3: Monitor Deployment

Streamlit Cloud will:

1. ✅ Clone your repository
2. ✅ Install Python 3.11
3. ✅ Install dependencies from `requirements.txt`
4. ✅ Install system packages from `packages.txt` (if any)
5. ✅ Apply configuration from `.streamlit/config.toml`
6. ✅ Start your app

**Deployment typically takes 2-5 minutes.**

Watch the logs in real-time to catch any errors.

### Step 4: Verify Deployment

Once deployed:

- [ ] Visit your app URL: `https://your-app.streamlit.app`
- [ ] Test all features:
  - [ ] Filters work
  - [ ] Charts render correctly
  - [ ] KPIs display properly
  - [ ] Data loads successfully
  - [ ] No console errors

## Managing Your Deployed App

### Accessing App Settings

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find your app in the dashboard
3. Click the **⋮** (three dots) menu
4. Select **"Settings"**

### Managing Secrets (Environment Variables)

If you need to add secrets:

1. Go to app settings
2. Navigate to **"Secrets"** section
3. Add secrets in TOML format:

```toml
# Example secrets
APP_TITLE = "Alberta Grant Analysis"
PAGE_ICON = "📊"
API_KEY = "your-secret-key"
```

4. Click **"Save"**
5. App will automatically restart

**Important**: Never commit secrets to GitHub!

### Viewing Logs

To debug issues:

1. Click on your app in the dashboard
2. View real-time logs at the bottom
3. Look for errors or warnings

### Restarting App

If your app needs a restart:

1. Go to app settings
2. Click **"Reboot app"**

Or trigger a restart by pushing to GitHub (auto-deploys).

### Updating the App

Streamlit Cloud auto-deploys on every push:

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push origin main

# Streamlit Cloud will automatically:
# - Detect the push
# - Rebuild the app
# - Deploy the new version
```

**Note**: Changes appear within 1-2 minutes of pushing.

## Troubleshooting

### Common Issues

#### 1. **ModuleNotFoundError**

**Problem**: Missing dependency

**Solution**:

- Add the package to `requirements.txt`
- Push changes to GitHub
- Wait for auto-redeploy

```bash
echo "package-name==version" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

#### 2. **App Won't Start**

**Problem**: Error in `streamlit_app.py` or `src/app.py`

**Solution**:

- Check logs in Streamlit Cloud dashboard
- Test locally first: `streamlit run streamlit_app.py`
- Fix errors and push again

#### 3. **Data Files Missing**

**Problem**: CSV files not loading

**Solution**:

- Verify files are committed to GitHub
- Check `.gitignore` isn't excluding them
- Ensure file paths are correct (use relative paths)

#### 4. **File Too Large**

**Problem**: GitHub limits files to 100MB

**Solution**:

- Use Git LFS for large files
- Host data externally (S3, Google Drive) and load via URL
- Compress CSV files

#### 5. **Python Version Mismatch**

**Problem**: Wrong Python version used

**Solution**:

- Verify `.python-version` file exists and contains: `3.11`
- Or create `runtime.txt` with: `python-3.11`

#### 6. **Custom Configuration Not Applied**

**Problem**: `.streamlit/config.toml` not working

**Solution**:

- Verify directory name is exactly `.streamlit/`
- Verify file name is exactly `config.toml`
- Check TOML syntax is valid

### Getting Help

- **Streamlit Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues**: Report bugs in your repository

## Resource Limits

Streamlit Community Cloud (free tier) has limits:

- **Resources**: 1 CPU, 800MB RAM, 800MB storage
- **Apps**: 1 private app, unlimited public apps
- **Usage**: Unlimited (but fair use policy applies)

**Optimization tips**:

- Cache data loading with `@st.cache_data`
- Minimize data size
- Optimize queries
- Use efficient data structures

## Best Practices

### 1. Keep Secrets Secret

- Never commit API keys or passwords
- Use Streamlit secrets management
- Add `.streamlit/secrets.toml` to `.gitignore`

### 2. Optimize Performance

```python
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
```

### 3. Version Pin Dependencies

```
# Good: Specific versions
streamlit==1.37.1
pandas==2.2.2

# Avoid: Unpinned versions
streamlit
pandas
```

### 4. Test Before Deploying

```bash
# Always test locally first
streamlit run streamlit_app.py
```

### 5. Monitor After Deployment

- Check logs regularly
- Test all features after each update
- Monitor for errors or warnings

## Next Steps

After successful deployment:

1. **Share Your App**

   - Add the live URL to your README
   - Share on LinkedIn/Twitter
   - Add to your portfolio

2. **Monitor Usage**

   - Check analytics in Streamlit Cloud dashboard
   - Review user feedback

3. **Iterate**

   - Add new features
   - Fix bugs
   - Improve performance

4. **Upgrade (Optional)**
   - Consider Streamlit Cloud Pro for:
     - Private apps
     - More resources
     - Custom authentication
     - Priority support

## Summary

✅ **Pre-deployment**:

- Project structure correct
- Files named properly
- Tested locally
- Pushed to GitHub

✅ **Deployment**:

- Signed in to Streamlit Cloud
- Created new app
- Configured settings
- Deployed successfully

✅ **Post-deployment**:

- Verified app works
- Updated README with live URL
- Monitoring for issues
- Ready to share!

---

**Your app is now live and ready to showcase! 🎉**

**Live URL**: `https://your-app.streamlit.app`

Share it with the world!
