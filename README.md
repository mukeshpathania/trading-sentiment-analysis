# 📊 Trading Behavior vs Market Sentiment Analysis

## 📌 Project Overview
This project analyzes how trader performance and behavior change based on market sentiment (Fear vs Greed).

We combine:
- Historical trading data  
- Fear & Greed Index data  

to uncover insights about:
- Profitability  
- Risk behavior  
- Trading patterns  

---

## 📁 Dataset
1. **Historical Data**
   - Trade-level data (PnL, trade size, account, etc.)

2. **Fear & Greed Index**
   - Daily sentiment classification (Fear, Greed, Neutral)

---

## ⚙️ Methodology

### 1. Data Preparation
- Loaded both datasets using pandas  
- Converted timestamps to datetime  
- Aligned both datasets using daily date  
- Merged datasets on date  

### 2. Feature Engineering
Created key metrics:
- Daily PnL (Closed PnL)  
- Win rate (PnL > 0)  
- Loss (drawdown proxy)  
- Trade size  
- Trade frequency  
- Leverage  

### 3. Segmentation
- Frequent vs Infrequent traders (based on median trades)  
- Leverage-based behavior analysis  

---

## 📊 Analysis

### ✔ Performance by Sentiment
- Compared average PnL and win rate across:
  - Fear  
  - Greed  

### ✔ Behavior Changes
- Trade frequency  
- Average trade size  
- Leverage usage  

### ✔ Trader Segments
- Frequent vs Infrequent traders  
- Performance comparison  

---

## 📈 Charts

The following charts are generated:
- PnL by Sentiment  
- Win Rate by Sentiment  
- Trade Frequency  
- Trade Size  
- Leverage Distribution  
- Segment Performance  

📂 Saved in:
outputs/

---

## 🔍 Key Insights
- Trader performance differs between Fear and Greed market conditions  
- Trading activity changes with sentiment  
- Frequent traders behave differently than infrequent traders  

---

## 💡 Strategy Recommendations

- During Fear markets:
  - Reduce leverage  
  - Avoid overtrading  

- During Greed markets:
  - Control position size  
  - Avoid excessive risk exposure  

---

## ▶️ How to Run

1. Install required libraries:
   pip install pandas matplotlib

2. Run the script:
   python analysis.py  

---

## 📂 Output

All results are saved in:
outputs/

Includes:
- CSV files (processed data)  
- Performance summary  
- Charts (PNG images)  
