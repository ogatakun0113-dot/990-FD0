import streamlit as st

# --- 見た目の設定（CSS） ---
st.markdown("""
    <style>
    .stNumberInput label, .stTextInput label {
        font-size: 20px !important;
        color: #4169E1 !important;
        font-weight: 800 !important;
    }
    .main-input div[data-baseweb="input"], .main-input div[data-baseweb="base-input"] {
        height: 65px !important;
        font-size: 28px !important;
        border: 3px solid #4169E1 !important;
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] {
        font-size: 38px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('📱 伝送換算アシスト (990-FD0版)')

# --- 1. 基本情報設定 ---
with st.expander("⚙️ 基本情報設定 (990-FD0基準)", expanded=False):
    st.info("計器の上下限値を設定してください。伝送値は990-4048(FD0)固定です。")
    col1, col2 = st.columns(2)
    with col1:
        s_min = st.number_input("スケール下限 (0%)", value=0.00)
        a_min = st.number_input("電流下限 (mA)", value=4.00)
        v_min = st.number_input("電圧下限 (V)", value=1.000)
    with col2:
        s_max = st.number_input("スケール上限 (100%)", value=100.00)
        a_max = st.number_input("電流上限 (mA)", value=20.00)
        v_max = st.number_input("電圧上限 (V)", value=5.000)
    
    # 基準となる伝送値の設定
    t_min = 990.0   # 10進数の990 (HEX: 3DE)
    t_max = 4048.0  # 10進数の4048 (HEX: FD0)

st.markdown("---")

# --- 2. メイン：入力切替 ---
mode = st.radio(
    "項目を選択して入力",
    ["伝送値(HEX)", "指示値", "割合(%)", "電流(mA)", "電圧(V)"],
    horizontal=True
)

percent = 0.0
error_msg = ""

st.markdown('<div class="main-input">', unsafe_allow_html=True)
if mode == "伝送値(HEX)":
    # 16進数を文字列として入力。初期値を 990 の HEX である "3DE" に設定。
    hex_input = st.text_input("現在の伝送値(HEX)を入力", value="3DE")
    try:
        # 入力された16進数を10進数に変換して計算
        val_dec = int(hex_input, 16)
        percent = (float(val_dec) - t_min) / (t_max - t_min)
        st.caption(f"内部換算: {val_dec} bit")
    except ValueError:
        error_msg = "正しい16進数（0-9, A-F）を入力してください。"
elif mode == "指示値":
    val = st.number_input("現在の指示値を入力", value=0.000)
    percent = (val - s_min) / (s_max - s_min)
elif mode == "割合(%)":
    val = st.number_input("％値を入力", value=0.0)
    percent = val / 100.0
elif mode == "電流(mA)":
    val = st.number_input("電流値を入力", value=4.00)
    percent = (val - a_min) / (a_max - a_min)
elif mode == "電圧(V)":
    val = st.number_input("電圧値を入力", value=1.000)
    percent = (val - v_min) / (v_max - v_min)
st.markdown('</div>', unsafe_allow_html=True)

if error_msg:
    st.error(error_msg)

# --- 3. 計算処理 ---
res_bit = t_min + (t_max - t_min) * percent
res_scale = s_min + (s_max - s_min) * percent
res_ma = a_min + (a_max - a_min) * percent
res_v = v_min + (v_max - v_min) * percent

# 伝送値の表示（10進数と16進数の両方）
display_bit_dec = int(res_bit)
display_bit_hex = hex(display_bit_dec).split('x')[-1].upper()

# --- 4. 表示エリア ---
st.subheader("📊 換算結果")
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric("伝送値(10進)", f"{display_bit_dec} bit")
with col_res2:
    st.metric("伝送値(HEX)", f"{display_bit_hex}")

st.metric("スケール換算値", f"{res_scale:,.3f}")
st.metric("電流値", f"{res_ma:,.2f} mA")
st.metric("電圧値", f"{res_v:,.3f} V")

st.markdown("---")
st.caption(f"現在の計算ベース: {percent*100:.2f} % (0%基準: 3DE / 100%基準: FD0)")
