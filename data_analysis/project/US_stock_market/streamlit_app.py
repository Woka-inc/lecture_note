import streamlit as st

from dataloader import TickerLoader
from model import Model

import os

st.session_state["ticker"] = False

st.write("# 📈Nasdaq Stock Market DashBoard")
latest_day = "-".join(os.listdir("./data")[0].split("_")[1:]).split(".")[0]
st.write(f"""
- **Period: first_day - {latest_day}**
         """)
st.write("---")

st.write(f"### Data load")

tl = TickerLoader()
data = tl.get_data(min_days=2500, streamlit_tqdm=True)

st.session_state["ticker"] = st.text_input("ticker input", "NVDA")

if st.session_state["ticker"]:
    chart_data = data.query(f"ticker == '{st.session_state["ticker"]}'")
    st.write("---")
    st.write("### Indicator")
    indi_cols = ["SMA_20", "SMA_200", "RSI_14", "MACD", "MACD_signal"]
    cols = st.columns(5)
    last_rows = chart_data.tail(2)[indi_cols]
    for i in range(len(indi_cols)):
        with cols[i]:
            name = indi_cols[i]
            now_value = round(last_rows.iloc[-1][indi_cols[i]], 4)
            diff_value = round(last_rows.iloc[-2][indi_cols[i]] - now_value, 4)
            cols[i].metric(
                name,
                now_value,
                diff_value
                )
    st.write("---")
    st.write("### Chart")
    st.line_chart(chart_data[["High", "Low", "SMA_20", "SMA_100"]].iloc[-126:])

    st.write("---")
    st.write("### Insight")
    with st.spinner("Thinking... plz wait"):
        insight = Model(chart_data).get_insight()
        st.write(insight)