import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="伝送換算 (990bit-FD0bit)", layout="centered")

# --- 見た目の設定 (CSS) ---
st.markdown("""
<style>
.stNumberInput label { font-size: 18px !important; font-weight: 800 !important; color: #4169E1 !important; }
.stSelectbox label { font-size: 18px !important; font-weight: 800 !important; color: #FF4B4B !important; }
.result-box {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #4169E1;
    margin-top: 20px;
}
.credit {
    text-align: right;
    font-size: 14px;
    color: #666;
    margin-bottom: -20px;
}
</style>
""", unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title('📱 伝送換算 (990h-FD0h)(HEX)')

# --- 1. 基本情報設定 ---
with st.expander("⚙️ 基本情報設定 (990h-FD0h基準)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        s_min = st.number_input("スケール下限 (0%)", value=0.00)
    with col2:
        s_max = st.number_input("スケール上限 (100%)", value=100.00)
    
    col3, col4 = st.columns(2)
    with col3:
        a_min = st.number_input("電流下限 (mA)", value=4.00, format="%.2f")
    with col4:
        a_max = st.number_input("電流上限 (mA)", value=20.00, format="%.2f")

    resistance = st.selectbox("入力抵抗を選択 (Ω)", [250, 500, 50], index=0)
    
    # 電圧自動計算（表示用）
    v_min_base = (a_min / 1000.0) * resistance
    v_max_base = (a_max / 1000.0) * resistance

    st.caption(f"💡 現在の設定: {resistance}Ω により、{a_min}mA→{v_min_base:.3f}V / {a_max}mA→{v_max_base:.3f}V")

    t_min = float(int("990", 16))
    t_max = float(int("FD0", 16))

st.markdown("---")

# --- 2. 入力セクション ---
mode = st.radio("項目を選択して入力", ["伝送値(HEX)", "指示値", "割合(%)", "電流(mA)", "電圧(V)"], horizontal=True)

percent = 0.0
if mode == "伝送値(HEX)":
    hex_input = st.text_input("現在の伝送値(HEX)を入力", value="990").upper()
    try:
        val_dec = int(hex_input, 16)
        percent = (float(val_dec) - t_min) / (t_max - t_min)
    except:
        st.error("有効な16進数を入力してください")
elif mode == "指示値":
    val = st.number_input("指示値", value=s_min)
    percent = (val - s_min) / (s_max - s_min) if (s_max - s_min) != 0 else 0
elif mode == "割合(%)":
    val = st.number_input("％値", value=0.0)
    percent = val / 100.0
elif mode == "電流(mA)":
    val = st.number_input("電流値", value=a_min, format="%.2f")
    percent = (val - a_min) / (a_max - a_min) if (a_max - a_min) != 0 else 0
elif mode == "電圧(V)":
    # --- 修正箇所：format="%.3f" を追加 ---
    val = st.number_input("電圧値 (V)", value=v_min_base, format="%.3f", step=0.001)
    percent = (val - v_min_base) / (v_max_base - v_min_base) if (v_max_base - v_min_base) != 0 else
