# Setup Guide: Oura Real Data Analysis

## 🔑 Getting Your Oura Personal Access Token

1. **Go to Oura Cloud**: https://cloud.ouraring.com/personal-access-tokens
2. **Sign in** with your Oura account
3. **Create a new token**:
   - Click "Create Token"
   - Give it a name (e.g., "Data Science Project")
   - Copy the token (you'll only see it once!)

## ⚙️ Configuration

### Option 1: Environment Variable (Recommended)

```bash
export OURA_PERSONAL_ACCESS_TOKEN='your_token_here'
```

### Option 2: .env File

Create a `.env` file in the project root:

```bash
OURA_PERSONAL_ACCESS_TOKEN=your_token_here
```

The `.env` file is already in `.gitignore` - your token will never be committed!

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install oura-ring specifically
pip install oura-ring
```

## 🚀 Quick Start

### 1. Fetch Real Data

```bash
python src/data_fetcher.py
```

This will:
- Connect to Oura API
- Fetch last 90 days of data
- Save to `data/raw/` as JSON and CSV

### 2. Process Data

```bash
python src/data_processor.py
```

### 3. Run Analytics

```bash
python src/advanced_analytics.py
```

## 📊 Data Available

Once you have a token, you can fetch:

- **Sleep Data**: Scores, stages, efficiency, latency
- **Activity Data**: Steps, calories, METs, activity scores
- **Readiness Data**: Readiness scores, HRV, temperature
- **Heart Rate**: Real-time heart rate data

## ⚠️ Without Oura Ring?

If you don't have an Oura Ring yet, you can:

1. **Study the API structure** from the code
2. **Use the synthetic data project** (`oura_readiness_prediction`)
3. **Wait until you get your Oura Ring** (they mentioned providing one!)

## 🔒 Security Notes

- **Never commit your token** to git
- `.env` file is in `.gitignore`
- Token gives access to your personal data - keep it secure!

## 📚 API Documentation

Full Oura API v2 documentation: https://cloud.ouraring.com/v2/docs

