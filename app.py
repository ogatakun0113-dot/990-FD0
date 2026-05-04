import streamlit as st

# --- 見た目の設定 ---
st.markdown("""
    <style>
    .stNumberInput label { font-size: 18px !important; font-weight: 800 !important; color: #4169E1 !important; }
    .stSelectbox label { font-size: 18px !important; font-weight: 800 !important; color: #FF4B4B !important; }
    </style>
    """, unsafe_allow_html=True)

st.title('📱 伝送換算アシスト(990h-FD0h)')

# --- 1. 基本情報設定 ---
with st.expander("⚙️ 基本情報設定", expanded=True):
    # スケール設定
    col1, col2 = st.columns(2)
    with col1:
        s_min = st.number_input("スケール下限 (0%)", value=0.00)
    with col2:
        s_max = st.number_input("スケール上限 (100%)", value=100.00)
    
    # 電流設定
    col3, col4 = st.columns(2)
    with col3:
        a_min = st.number_input("電流下限 (mA)", value=4.00, format="%.2f")
    with col4:
        a_max = st.number_input("電流上限 (mA)", value=20.00, format="%.2f")

    # 入力抵抗の選択（ここを追加）
    resistance = st.selectbox("入力抵抗を選択 (Ω)", [250, 500, 50], index=0)
    
    # 選択された抵抗値に基づいて電圧を自動計算 (V = I * R)
    # mAをAに直すため 1000 で割っています
    v_min_calc = (a_min / 1000.0) * resistance
    v_max_calc = (a_max / 1000.0) * resistance

    # 電圧表示（自動計算結果を表示し、微調整も可能に）
    col5, col6 = st.columns(2)
    with col5:
        v_min = st.number_input("電圧下限 (V) ※自動計算", value=v_min_calc, format="%.3f")
    with col6:
        v_max = st.number_input("電圧上限 (V) ※自動計算", value=v_max_calc, format="%.3f")

    st.caption(f"💡 現在の設定: {resistance}Ω の抵抗により、{a_min}mA→{v_min:.3f}V / {a_max}mA→{v_max:.3f}V となっています。")

    # 伝送値幅（990h-FD0h固定）
    t_min = float(int("990", 16))
    t_max = float(int("FD0", 16))

st.markdown("---")

# --- 以降の計算ロジック（前回の内容を維持） ---
mode = st.radio("項目を選択して入力", ["伝送値(HEX)", "指示値", "割合(%)", "電流(mA)", "電圧(V)"], horizontal=True)

percent = 0.0
if mode == "伝送値(HEX)":
    hex_input = st.text_input("現在の伝送値(HEX)を入力", value="990")
    try:
        val_dec = int(hex_input, 16)
        percent = (float(val_dec) - t_min) / (t_max - t_min)
    except: st.error("16進数を入れてください")
elif mode == "指示値":
    val = st.number_input("指示値", value=s_min)
    percent = (val - s_min) / (s_max - s_min)
elif mode == "割合(%)":
    val = st.number_input("％値", value=0.0)
    percent = val / 100.0
elif mode == "電流(mA)":
    val = st.number_input("電流値", value=a_min)
    percent = (val - a_min) / (a_max - a_min)
elif mode == "電圧(V)":
    val = st.number_input("電圧値", value=v_min)
    percent = (val - v_min) / (v_max - v_min)

# 結果計算
res_scale = s_min + (s_max - s_min) * percent
res_ma = a_min + (a_max - a_min) * percent
res_v = v_min + (v_max - v_min) * percent
res_hex = hex(int(round(t_min + (t_max - t_min) * percent))).replace('0x','').upper()

st.subheader("📊 換算結果")
c_r1, c_r2, c_r3 = st.columns(3)
c_r1.metric("指示値", f"{res_scale:.2f}")
c_r2.metric("電流", f"{res_ma:.2f} mA")
c_r3.metric("電圧", f"{res_v:.3f} V")
st.metric("伝送値 (HEX)", res_hex)
