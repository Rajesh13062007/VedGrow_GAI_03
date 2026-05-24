# Deployment Guide

## Deploy on Streamlit Community Cloud

### Step 1: Upload to GitHub

Create a public repository named:

```text
VedGrow_GAI_03
```

Upload these files:

```text
app.py
README.md
requirements.txt
.env.example
.gitignore
sample_questions.md
DEMO_VIDEO_SCRIPT.md
DEPLOYMENT.md
test_pdf_extract.py
```

### Step 2: Create New Streamlit App

1. Go to Streamlit Community Cloud.
2. Sign in with GitHub.
3. Click **New app**.
4. Select your repository.
5. Set the main file path as:

```text
app.py
```

6. Click **Deploy**.

### Step 3: Add Secrets

Open app settings and add these secrets:

```toml
GOOGLE_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-001"
```

### Step 4: Reboot the App

After saving secrets, reboot the app.

### Step 5: Submit

Submit:

1. GitHub repository link
2. Demo video link

If the app is live, you can also include the Streamlit app link.
