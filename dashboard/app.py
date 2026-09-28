import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from decision_engine.data import synthetic_prices,live_prices
from decision_engine.engine import run_engine

st.set_page_config(page_title="Portfolio Decision Engine",layout="wide")
st.title("Portfolio Decision Engine")
st.caption("Signals → expected returns → portfolio → execution → risk → attribution")

mode=st.sidebar.selectbox("Data",["synthetic","live"])
prices=synthetic_prices() if mode=="synthetic" else live_prices()
res=run_engine(prices)

st.dataframe(res["summary"],use_container_width=True)
st.subheader("Cumulative performance")
st.line_chart((1+res["returns"]).cumprod())

d=res["decision_log"]
c1,c2,c3=st.columns(3)
c1.metric("Rebalances",len(d))
c2.metric("Average turnover",f"{d.turnover.mean():.1%}")
c3.metric("Execution-cost drag",f"{d.execution_cost.sum():.2%}")

tabs=st.tabs(["Latest decision","Weights","Signals","Execution","Attribution"])
with tabs[0]:
    st.dataframe(d.tail(12),use_container_width=True)
with tabs[1]:
    w=res["weights"].pivot(index="return_date",columns="asset",values="weight")
    st.line_chart(w)
with tabs[2]:
    st.dataframe(res["signals"].tail(40),use_container_width=True)
with tabs[3]:
    st.dataframe(res["blotter"].tail(50),use_container_width=True)
with tabs[4]:
    st.dataframe(res["attribution"].tail(50),use_container_width=True)
