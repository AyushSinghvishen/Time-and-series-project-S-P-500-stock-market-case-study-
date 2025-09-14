# ====== Imports ======
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ====== File Paths ======

company_list = [
    "individual_stock_5years/AAPL_data.csv",
    "individual_stock_5years/AMZN_data.csv",
    "individual_stock_5years/GOOG_data.csv",
    "individual_stock_5years/MSFT_data.csv"
]

# ====== Load & Combine Data ======
all_data = pd.DataFrame()
for file in company_list:
    current_df = pd.read_csv(file)
    all_data = pd.concat([all_data, current_df], ignore_index=True)

# Convert date to datetime
all_data["date"] = pd.to_datetime(all_data["date"])

# ====== Streamlit Page Setup ======
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
st.title("📈 Tech Stocks Analysis Dashboard")

# ====== Sidebar ======
tech_list = all_data["Name"].unique()
st.sidebar.title("Choose a Company")
selected_company = st.sidebar.selectbox("Select a stock", tech_list)

# Filter data for selected company
company_df = all_data[all_data["Name"] == selected_company].copy()
company_df.sort_values("date", inplace=True)

# ====== 1. Closing Price Over Time ======
st.subheader(f"1. Closing Price of {selected_company} Over Time")
fig1 = px.line(company_df, x="date", y="close",
               title=f"{selected_company} Closing Prices Over Time")
st.plotly_chart(fig1, use_container_width=True)

# ====== 2. Moving Averages ======
st.subheader("2. Moving Averages (10, 20, 50 days)")
ma_days = [10, 20, 50]
for ma in ma_days:
    company_df[f"close_{ma}"] = company_df["close"].rolling(ma).mean()

fig2 = px.line(company_df, x="date",
               y=["close", "close_10", "close_20", "close_50"],
               title=f"{selected_company} Closing Price with Moving Averages")
st.plotly_chart(fig2, use_container_width=True)

# ====== 3. Daily Returns ======
st.subheader(f"3. Daily Returns for {selected_company}")
company_df["daily_return_%"] = company_df["close"].pct_change() * 100

fig3 = px.line(company_df, x="date", y="daily_return_%",
               title=f"{selected_company} Daily Returns (%)")
st.plotly_chart(fig3, use_container_width=True)

# ====== 4. Resampled Closing Price ======
st.subheader("4. Resampled Closing Price (Monthly / Quarterly / Yearly)")
company_df.set_index("date", inplace=True)

resample_option = st.radio("Select Resample Frequency", ["Monthly", "Quarterly", "Yearly"])
if resample_option == "Monthly":
    resampled = company_df["close"].resample("M").mean()
elif resample_option == "Quarterly":
    resampled = company_df["close"].resample("Q").mean()
elif resample_option == "Yearly":
    resampled = company_df["close"].resample("Y").mean()

fig4 = px.line(resampled, x=resampled.index, y=resampled.values,
               title=f"{selected_company} Resampled Closing Price ({resample_option})")
st.plotly_chart(fig4, use_container_width=True)

# ====== 5. Correlation Heatmap of All Companies ======
st.subheader("5. Correlation Between Tech Stocks")

appl = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
goog = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame({
    "apple_close": appl["close"],
    "amzn_close": amzn["close"],
    "goog_close": goog["close"],
    "msft_close": msft["close"]
})

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(closing_price.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# ====== Notes ======
st.markdown("---")
st.markdown("*Note:* This dashboard provides basic technical analysis of major tech stocks using Streamlit, Pandas, Plotly, and Seaborn.")
