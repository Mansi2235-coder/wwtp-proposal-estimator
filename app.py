import streamlit as st
from mass_balance import (
    pollutant_load, removed_load, sludge_production,
    tank_volume, oxygen_demand, hrt, fm_ratio, check_fm,
)

st.title("Wastewater Treatment Plant Estimator")
st.write("Activated sludge, carbon (BOD) removal only. Based on textbook design values.")

flow = st.number_input("Design flow (m3/day)", min_value=1, value=10000)
bod_in = st.number_input("Influent BOD5 (mg/L)", min_value=1, value=250)
bod_out = st.number_input("Effluent BOD5 target (mg/L)", min_value=1, value=20)
srt = st.number_input("Sludge retention time, SRT (days)", min_value=1, value=10)

yield_y = 0.6
decay_kd = 0.08
mlvss = 2500
bod_ratio = 0.68

volume = tank_volume(flow, bod_in, bod_out, yield_y, decay_kd, srt, mlvss)
fm = fm_ratio(flow, bod_in, volume, mlvss)

st.subheader("Results")
st.metric("Influent BOD load (kg/day)", round(pollutant_load(flow, bod_in), 1))
st.metric("Sludge production (kg VSS/day)", round(sludge_production(flow, bod_in, bod_out, yield_y, decay_kd, srt), 1))
st.metric("Aeration tank volume (m3)", round(volume, 1))
st.metric("HRT (hours)", round(hrt(volume, flow), 1))
st.metric("F/M ratio", round(fm, 2))
st.metric("Oxygen demand (kg O2/day)", round(oxygen_demand(flow, bod_in, bod_out, yield_y, decay_kd, srt, bod_ratio), 1))

if check_fm(fm) == "F/M is OK":
    st.success(check_fm(fm))
else:
    st.warning(check_fm(fm))