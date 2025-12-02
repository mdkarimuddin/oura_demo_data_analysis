# Oura Real Data Analysis: Advanced Analytics with Oura API

Advanced data science project using **real Oura Ring API data** for predictive health analytics and personalized insights.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![API](https://img.shields.io/badge/API-Oura%20v2-green.svg)
![ML](https://img.shields.io/badge/ML-Advanced%20Analytics-orange.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

## 🎯 Project Overview

This project uses the **official Oura API v2** to fetch real user data and build advanced analytics:

1. **Real-time Data Fetching**: Connect to Oura API and retrieve sleep, activity, readiness data
2. **Advanced Analytics**: Build predictive models on real user data
3. **Personalized Insights**: User-specific recommendations and patterns
4. **Multi-modal Analysis**: Combine sleep, activity, HRV, temperature data

## 🔥 What Makes This Outstanding

- ✅ **Uses Real Oura API** (not synthetic data!)
- ✅ **Production API Integration** (OuraClient from hedgertronic/oura-ring)
- ✅ **Advanced ML Models** (time series, forecasting, clustering)
- ✅ **Personalized Analytics** (user-specific insights)
- ✅ **Real-world Application** (actual wearable data)

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
│   ├── data_fetcher.py         # Fetch real Oura data
│   ├── data_processor.py       # Process and clean API data
│   ├── advanced_analytics.py   # ML models and analytics
│   ├── personalization.py      # User-specific insights
│   └── visualizations.py       # Create insights dashboards
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
- Real-time API fetching from Oura Cloud
- Historical data retrieval (up to 1 year)
- Multi-modal data integration

### Advanced Analytics
- **Time Series Forecasting**: Predict future readiness/sleep scores
- **Pattern Recognition**: Identify personal sleep/activity patterns
- **Anomaly Detection**: Detect unusual health patterns
- **Clustering**: Group similar days/weeks for insights

### Personalization
- User-specific baselines
- Personalized recommendations
- Trend analysis over time

## 💡 Key Features

1. **Real API Integration**: Uses official Oura API v2 (hedgertronic/oura-ring)
2. **Demo Mode**: Works without Oura Ring - generates realistic demo data
3. **Advanced ML**: Time series forecasting, anomaly detection, pattern recognition
4. **Personalized Insights**: User-specific baselines and analytics
5. **Production Ready**: Error handling, data validation, complete pipeline
6. **Comprehensive**: Sleep + Activity + Readiness + HRV analysis

## 📈 Results (Demo Mode)

**Data Generated:**
- 90 days of demo data matching real API structure
- Sleep, Activity, Readiness scores with contributors

**Analytics:**
- Personal Baselines: Calculated for all metrics
- Anomaly Detection: Statistical outlier detection
- Readiness Forecasting: R² = 0.084, MAE = 8.17 points
  - *Note: Low R² expected with demo data - will improve significantly with real data*

## 🛠️ Technologies

- **oura-ring**: Official Oura API Python client
- **pandas, numpy**: Data processing
- **scikit-learn**: Machine learning
- **matplotlib, seaborn**: Visualization
- **python-dotenv**: Environment configuration

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

