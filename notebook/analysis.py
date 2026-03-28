import pandas as pd
import matplotlib.pyplot as plt
import os

# load data
hist = pd.read_csv(r"D:\Projects\trading-sentiment-analysis\data\historical_data.csv")
fg = pd.read_csv(r"D:\Projects\trading-sentiment-analysis\data\fear_greed_index.csv")

# basic info
print("Historical shape:", hist.shape)
print("Fear & Greed shape:", fg.shape)

# convert timestamp
hist['Timestamp'] = pd.to_datetime(hist['Timestamp'], unit='ms', errors='coerce')
fg['date'] = pd.to_datetime(fg['date'], errors='coerce')

# IMPORTANT: use only DATE (no time)
hist['date'] = hist['Timestamp'].dt.date
fg['date'] = fg['date'].dt.date

# check date range
print("Hist date range:", hist['date'].min(), hist['date'].max())
print("FG date range:", fg['date'].min(), fg['date'].max())

# merge data
merged = pd.merge(hist, fg, on='date', how='left')

print("Before drop:", merged.shape)


# remove missing sentiment
merged = merged.dropna(subset=['classification'])

print("After drop:", merged.shape)

# stop if empty
if merged.empty:
    print("No data after merge")
    print("Merged shape:", merged.shape)
    exit()

# create metrics
merged['win'] = merged['Closed PnL'] > 0
merged['loss'] = merged['Closed PnL'].apply(lambda x: x if x < 0 else 0)

# performance
performance = merged.groupby('classification').agg({
    'Closed PnL': 'mean',
    'win': 'mean'
})

performance.rename(columns={
    'Closed PnL': 'avg_pnl',
    'win': 'win_rate'
}, inplace=True)

# behavior
behavior = merged.groupby('classification').agg({
    'Trade ID': 'count',
    'Size USD': 'mean'
})

behavior.rename(columns={
    'Trade ID': 'num_trades',
    'Size USD': 'avg_trade_size'
}, inplace=True)

# segmentation
trade_counts = merged.groupby('Account')['Trade ID'].count()
threshold = trade_counts.median()

merged['trader_type'] = merged['Account'].map(
    lambda x: 'Frequent' if trade_counts[x] > threshold else 'Infrequent'
)

segment_perf = merged.groupby('trader_type')['Closed PnL'].mean()

# leverage
if 'Leverage' not in merged.columns:
    merged['leverage'] = merged['Size USD'] / merged['Start Position']

# create output folder
output_path = r"D:\Projects\trading-sentiment-analysis\outputs"
os.makedirs(output_path, exist_ok=True)

# =========================
# CHARTS
# =========================

# 1. PnL
plt.figure()
plt.bar(performance.index, performance['avg_pnl'])
plt.title("PnL by Sentiment")
plt.savefig(output_path + "/pnl.png")
plt.close()

# 2. Win Rate
plt.figure()
plt.bar(performance.index, performance['win_rate'])
plt.title("Win Rate")
plt.savefig(output_path + "/winrate.png")
plt.close()

# 3. Trades
plt.figure()
plt.bar(behavior.index, behavior['num_trades'])
plt.title("Number of Trades")
plt.savefig(output_path + "/trades.png")
plt.close()

# 4. Trade Size
plt.figure()
plt.bar(behavior.index, behavior['avg_trade_size'])
plt.title("Trade Size")
plt.savefig(output_path + "/size.png")
plt.close()

# 5. Leverage
plt.figure()

if 'Leverage' in merged.columns:
    data = merged['Leverage']
else:
    data = merged['leverage']

data = data.replace([float('inf'), -float('inf')], None).dropna()

if not data.empty:
    plt.hist(data, bins=10)
    plt.title("Leverage Distribution")
    plt.savefig(output_path + "/leverage.png")
    plt.close()
else:
    print("No valid leverage data")

# 6. Segment
plt.figure()
plt.bar(segment_perf.index, segment_perf.values)
plt.title("Trader Segments")
plt.savefig(output_path + "/segment.png")
plt.close()

# save data
merged.to_csv(output_path + "/merged.csv", index=False)
performance.to_csv(output_path + "/performance.csv")

print("\n✅ Done. Check outputs folder.")
