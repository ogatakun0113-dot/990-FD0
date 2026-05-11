import streamlit as st

st.set_page_config(page_title="伝送値換算 (990-FD0)", layout="centered")

st.markdown("""
<style>
.stNumberInput label { font-size: 18px !important; font-weight: 800 !important; color: #4169E1 !important; }
.result-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4169E1; margin-top: 20px; }
.credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title('📱 伝送値換算 (990-FD0)(HEX)')

with st.expander("⚙️ 基本情報設定 (990h-FD0h基準)", expanded=True):
    col1, col2 = st.columns(2)
    s_min = col1.number_input("スケール下限 (0%)", value=0.00)
    s_max = col2.number_input("スケール上限 (100%)", value=100.00)
    
    col3, col4 = st.columns(2)
    a_min = col3.number_input("電流 4mA", value=4.00, format="%.2f")
    a_max = col4.number_input("電流 20mA", value=20.00, format="%.2f")

    resistance = st.selectbox("入力抵抗を選択 (Ω)", [250, 500, 50], index=0)
    
    v_min = (a_min / 1000.0) * resistance
    v_max = (a_max / 1000.0) * resistance
    st.caption(f"💡 設定: {resistance}Ω により {a_min}mA→{v_min:.3f}V / {a_max}mA→{v_max:.3f}V")

    t_min = float(int("990", 16))
    t_max = float(int("FD0", 16))

st.markdown("---")
mode = st.radio("項目を選択して入力", ["伝送値(HEX)", "指示値", "割合(%)", "電流(mA)", "電圧(V)"], horizontal=True)

percent = 0.0
try:
    if mode == "伝送値(HEX)":
        h_in = st.text_input("HEX入力", value="990").upper()
        percent = (float(int(h_in, 16)) - t_min) / (t_max - t_min)
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
        # 電圧入力を小数点3桁に変更
        val = st.number_input("電圧値", value=v_min, format="%.3f")
        percent = (val - v_min) / (v_max - v_min) if (v_max - v_min) != 0 else 0
except:
    st.error("有効な値を入力してください")

res_scale = s_min + (s_max - s_min) * percent
res_ma = a_min + (a_max - a_min) * percent
res_v = v_min + (v_max - v_min) * percent
res_hex = hex(int(round(t_min + (t_max - t_min) * percent))).replace('0x', '').upper()

st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 換算結果")
c1, c2, c3 = st.columns(3)
c1.metric("指示値", f"{res_scale:.2f}")
c2.metric("電流", f"{res_ma:.2f} mA")
c3.metric("電圧", f"{res_v:.3f} V") # 結果も3桁
st.metric("伝送値 (HEX)", f"{res_hex} h")
st.markdown('</div>', unsafe_allow_html=True)
# --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://7fjndw39dicdzckugyepb2.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
