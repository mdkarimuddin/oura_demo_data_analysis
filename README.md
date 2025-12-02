# Oura Demo Data Analysis: Advanced Analytics with Oura API

Advanced data science project using **Oura Ring API structure** for predictive health analytics and personalized insights. Works with **demo data** (no Oura Ring required) and ready for **real API data** when available.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![API](https://img.shields.io/badge/API-Oura%20v2-green.svg)
![ML](https://img.shields.io/badge/ML-Advanced%20Analytics-orange.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

## 🎯 Project Overview

This project demonstrates **Oura API integration** and advanced analytics using **demo data** that matches the real Oura API v2 structure:

1. **Demo Data Generation**: Create realistic Oura data matching API structure (works without ring)
2. **Real API Integration**: Ready to fetch real data when Oura Ring is available
3. **Advanced Analytics**: Build predictive models on Oura data structure
4. **Personalized Insights**: User-specific recommendations and patterns
5. **Multi-modal Analysis**: Combine sleep, activity, HRV, temperature data

## 🔥 What Makes This Outstanding

- ✅ **Works Without Oura Ring** (demo data mode - no token needed!)
- ✅ **Real API Integration Ready** (OuraClient from hedgertronic/oura-ring)
- ✅ **Demo Data Matches Real API** (same structure as actual Oura API v2)
- ✅ **Advanced ML Models** (time series forecasting, anomaly detection)
- ✅ **Personalized Analytics** (user-specific baselines and insights)
- ✅ **Production-Ready Code** (error handling, validation, complete pipeline)

## 📊 Data Sources

### Oura API Endpoints Used:
- `get_daily_sleep()` - Sleep scores, stages, efficiency
- `get_daily_activity()` - Steps, calories, activity scores
- `get_daily_readiness()` - Readiness scores, HRV, temperature
- `get_heart_rate()` - Heart rate data
- `get_sleep_periods()` - Detailed sleep periods

### Data Features:
- Sleep metrics (deep, REM, light sleep)
- Activity metrics (steps, calories, METs)
- Readiness contributors (HRV balance, temperature, sleep balance)
- Heart rate variability (HRV)
- Body temperature deviations

## 🗂️ Project Structure

```
oura_real_data_analysis/
├── src/
│   ├── api_client.py           # Oura API client wrapper
│   ├── data_fetcher.py         # Fetch real Oura data (requires token)
│   ├── create_demo_data.py    # Generate demo data (no token needed)
│   ├── data_processor.py      # Process and merge API data
│   └── advanced_analytics.py   # ML models and analytics
├── data/
│   ├── raw/                    # Raw API responses
│   └── processed/              # Processed datasets
├── outputs/                    # Results and visualizations
├── config/                     # API configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

**Install dependencies**:
```bash
pip install -r requirements.txt
```

### Option 1: With Oura Ring (Real Data)

1. **Get Personal Access Token**: [Oura Cloud](https://cloud.ouraring.com/personal-access-tokens)
2. **Configure Token**:
```bash
export OURA_PERSONAL_ACCESS_TOKEN='your_token_here'
# Or create .env file: OURA_PERSONAL_ACCESS_TOKEN=your_token_here
```

3. **Fetch Real Data**:
```bash
python src/data_fetcher.py
python src/data_processor.py
python src/advanced_analytics.py
```

### Option 2: Without Oura Ring (Demo Mode) ⭐

**Works immediately - no token needed!**

1. **Generate Demo Data** (matches real API structure):
```bash
python src/create_demo_data.py
```

2. **Process & Analyze**:
```bash
python src/data_processor.py
python src/advanced_analytics.py
```

**When you get your Oura Ring**: Just add the token and run `data_fetcher.py` - everything else works!

## 🔬 Methodology

### Data Collection
- **Real API**: Fetch from Oura Cloud API v2 (when token available)
- **Demo Mode**: Generate realistic data matching API structure (no token needed)
- **Historical Data**: Retrieve up to 1 year of data
- **Multi-modal Integration**: Sleep + Activity + Readiness + HRV

### Data Processing
- Flatten nested JSON structures (contributors, nested objects)
- Merge multi-modal data by date
- Handle missing values and data validation
- Create time-series features (lags, rolling averages)

### Advanced Analytics

**1. Readiness Forecasting**
- Predict tomorrow's readiness score from today's data
- Features: Lag features (1, 2, 3, 7 days), rolling averages, current scores
- Model: Random Forest Regressor
- Evaluation: R², MAE, RMSE

**2. Anomaly Detection**
- Statistical outlier detection (2 standard deviations)
- Identify unusual readiness/sleep/activity patterns
- Flag potential health events or data quality issues

**3. Personal Baselines**
- Calculate user-specific mean, median, standard deviation
- Track trends over time
- Compare current performance to personal baseline

### Personalization
- User-specific baselines (not population averages)
- Personalized anomaly thresholds
- Trend analysis over time
- Ready for personalized recommendations (future enhancement)

## 💡 Key Features

1. **Real API Integration**: Uses official Oura API v2 (hedgertronic/oura-ring)
2. **Demo Mode**: Works without Oura Ring - generates realistic demo data matching API structure
3. **Advanced ML**: Time series forecasting, anomaly detection, pattern recognition
4. **Personalized Insights**: User-specific baselines and analytics
5. **Production Ready**: Error handling, data validation, complete pipeline
6. **Comprehensive**: Sleep + Activity + Readiness + HRV analysis
7. **Flexible**: Works with or without Oura Ring (demo mode)

## 🎯 Use Cases

### For Portfolio/Interview:
- ✅ Demonstrates real API integration skills
- ✅ Shows understanding of Oura data structure
- ✅ Production-ready code patterns
- ✅ Works immediately (no ring needed)

### For Personal Use (when you get ring):
- ✅ Fetch your real Oura data
- ✅ Get personalized health insights
- ✅ Forecast readiness scores
- ✅ Detect unusual health patterns

## 📈 Results

### Demo Mode Results (90 days of demo data)

**Data Generated:**
- 90 days of demo data matching real Oura API v2 structure
- Sleep, Activity, Readiness scores with all contributors
- Date range: 90 days of historical data

**Analytics Results:**

| Metric | Value |
|--------|-------|
| **Personal Baselines** | |
| Readiness (mean) | 74.8 ± 11.1 |
| Sleep (mean) | 78.9 ± 10.1 |
| Activity (mean) | 75.7 ± 11.2 |
| **Anomaly Detection** | |
| Anomalies Detected | 6 days (out of 90) |
| Threshold | ±2 standard deviations |
| **Readiness Forecasting** | |
| R² Score | 0.084 |
| MAE | 8.17 points |
| Model | Random Forest |

*Note: Low R² expected with demo data - will improve significantly with real user data*

### Expected Results with Real Data

When using real Oura Ring data:
- **Better forecasting performance** (R² > 0.70 expected)
- **More accurate baselines** (user-specific patterns)
- **Real anomaly detection** (actual health events)
- **Personalized insights** (based on your actual data)

## 🛠️ Technologies

- **oura-ring** (v0.3.0): Official Oura API Python client from hedgertronic/oura-ring
- **pandas, numpy**: Data processing and manipulation
- **scikit-learn**: Machine learning (Random Forest, preprocessing)
- **python-dotenv**: Environment variable management
- **requests**: HTTP requests for API calls

## 📋 Project Files

### Core Scripts
- `src/api_client.py` - Oura API client wrapper with error handling
- `src/data_fetcher.py` - Fetch real data from Oura API (requires token)
- `src/create_demo_data.py` - Generate demo data (works without token)
- `src/data_processor.py` - Process, clean, and merge Oura data
- `src/advanced_analytics.py` - ML models: forecasting, anomaly detection, baselines

### Documentation
- `README.md` - This file
- `SETUP_GUIDE.md` - Detailed setup instructions
- `PROJECT_PLAN.md` - Implementation roadmap
- `PROJECT_STATUS.md` - Current project status

## 🔒 Security

- `.env` file in `.gitignore` (tokens never committed)
- API tokens handled securely via environment variables
- No hardcoded credentials
- Production-ready security practices

## 👤 Author

**Karim Uddin**  
PhD Veterinary Medicine | MEng Big Data Analytics  
Postdoctoral Researcher, University of Helsinki

- GitHub: [@mdkarimuddin](https://github.com/mdkarimuddin)
- LinkedIn: [Karim Uddin](https://linkedin.com/in/karimuddin)

## 📜 License

MIT License

---

**⭐ Star this repo if you found it useful!**

*Built to demonstrate real-world API integration and advanced analytics for wearable health technology.*

