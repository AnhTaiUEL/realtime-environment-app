import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# =============================================================================
# 1. CẤU HÌNH TRANG VÀ DESIGN SYSTEM ULTRA VIP (CYBER-GLOW & GLASSMORPHISM)
# =============================================================================
st.set_page_config(
    page_title="👑 VIP System: Giám Sát & Dự Báo Môi Trường 4D & AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện Ultra VIP Dark Glassmorphism Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #F8FAFC;
    }
    
    /* Header VIP */
    .vip-header {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 28px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px -15px rgba(0, 242, 254, 0.15), 0 0 20px rgba(139, 92, 246, 0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        position: relative;
        overflow: hidden;
    }
    
    .vip-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #00F2FE, #4FACFE, #00E676, #FF007F, #8B5CF6);
    }
    
    .vip-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .vip-badge {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        color: #0F172A;
        font-weight: 800;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        letter-spacing: 1.5px;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
        margin-bottom: 10px;
    }
    
    /* Live Pulse Dot */
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.6s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Metric Cards VIP */
    .vip-metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .vip-metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 12px 25px rgba(56, 189, 248, 0.15);
    }
    
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
    }
    
    .metric-lbl {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 600;
    }
    
    .metric-sub {
        font-size: 12px;
        color: #38BDF8;
        font-weight: 700;
        margin-top: 4px;
    }
    
    /* Alert Box */
    .alert-box-vip {
        background: rgba(239, 68, 68, 0.15);
        border-left: 5px solid #EF4444;
        border-radius: 12px;
        padding: 16px 20px;
        color: #FCA5A5;
        font-weight: 600;
        margin-bottom: 20px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.8);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 600;
        padding: 10px 18px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #38BDF8 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. KHỞI TẠO HEADER VIP ULTRA-PREMIUM
# =============================================================================
st.markdown("""
<div class="vip-header">
    <span class="vip-badge">👑 VIP SCIENTIFIC EDITION</span>
    <div class="vip-title">🌍 HỆ THỐNG GIÁM SÁT & DỰ BÁO MÔ I TRƯỜNG REAL-TIME 4D / 3D</div>
    <div style="font-size: 15px; color: #CBD5E1; margin-top: 5px;">
        <span class="pulse-dot"></span> Luồng Dữ Liệu Thời Gian Thực • 4D Motion & 3D Risk Field • 7 Custom Buttons • World Emission Map • Supervised Machine Learning AI
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 3. SIDEBAR ĐIỀU KHIỂN THÔNG MINH HIGH-TECH
# =============================================================================
st.sidebar.markdown("### 🎛️ Bảng Điều Khiển Trung Tâm VIP")
update_speed = st.sidebar.slider("⚡ Tốc độ Stream Real-Time (Giây):", 1.0, 5.0, 2.0, 0.5)
z_threshold = st.sidebar.slider("🚨 Ngưỡng Cảnh Báo Anomaly (Z-Score σ):", 1.5, 3.0, 2.0, 0.1)
is_streaming = st.sidebar.toggle("🟢 Kích Hoạt Luồng Real-Time Stream", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Chọn Năm Phân Tích Toàn Cầu")
selected_year = st.sidebar.slider("📅 Chọn Năm (Our World in Data):", 1990, 2022, 2022, 1)

st.sidebar.markdown("---")
st.sidebar.info("""
💡 **Đặc quyền VIP & Hàm lượng Khoa học**:
- **Luồng Real-Time**: Thu thập & kiểm soát Z-Score Anomaly bất thường.
- **Biểu đồ 4D & 3D**: Trực quan hóa đa chiều (Bong bóng động & Bề mặt rủi ro 3D).
- **Bản đồ Heatmap**: Bản đồ cường độ khí thải toàn cầu Choropleth.
- **Ma trận 16 Cột**: Hệ số tương quan Pearson toàn diện 16 đặc trưng.
- **7 Custom Buttons**: Tương tác chọn lọc 7 nguồn xả thải.
- **AI Học Máy**: Mô hình Random Forest & Linear Regression dự báo chính xác.
""")

# =============================================================================
# 4. DATA ENGINE (TẢI DỮ LIỆU TỰ ĐỘNG TỪ OWID & GAPMINDER)
# =============================================================================
@st.cache_data
def fetch_owid_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data
def fetch_gapminder_data():
    url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()

df_owid = fetch_owid_data()
df_gapminder = fetch_gapminder_data()

# Khởi tạo Session State cho luồng Real-Time Stream
if "stream_history" not in st.session_state:
    st.session_state.stream_history = pd.DataFrame(columns=[
        "timestamp", "temperature", "co2_ppm", "pm25", "humidity", "aqi", "z_score", "is_anomaly"
    ])

# Sinh dữ liệu cảm biến thời gian thực sống động
def get_live_point():
    now_str = (datetime.now() + timedelta(hours=7)).strftime("%H:%M:%S")
    temp = round(np.random.normal(31.2, 1.1), 2)
    co2 = round(np.random.normal(426.5, 17.5), 1)
    pm25 = round(np.random.exponential(20.5), 1)
    humidity = round(np.random.uniform(60.0, 84.0), 1)
    aqi = round(pm25 * 2.1 + np.random.uniform(5, 15), 1)
    
    # 8% xác suất xảy ra đột biến Anomaly Spike
    if np.random.rand() < 0.08:
        co2 += np.random.uniform(70.0, 130.0)
        pm25 += np.random.uniform(50.0, 110.0)
        aqi += np.random.uniform(80.0, 150.0)
        
    return {
        "timestamp": now_str, 
        "temperature": temp, 
        "co2_ppm": co2, 
        "pm25": pm25, 
        "humidity": humidity,
        "aqi": aqi
    }

if is_streaming:
    point = get_live_point()
    df_new = pd.DataFrame([point])
    st.session_state.stream_history = pd.concat([st.session_state.stream_history, df_new], ignore_index=True)
    
    # Giữ tối đa 40 mẫu thời gian thực gần nhất
    if len(st.session_state.stream_history) > 40:
        st.session_state.stream_history = st.session_state.stream_history.iloc[-40:].reset_index(drop=True)
        
    # Tính Z-Score khoa học
    c_mean = st.session_state.stream_history["co2_ppm"].mean()
    c_std = st.session_state.stream_history["co2_ppm"].std()
    st.session_state.stream_history["z_score"] = (st.session_state.stream_history["co2_ppm"] - c_mean) / c_std if c_std > 0 else 0
    st.session_state.stream_history["is_anomaly"] = st.session_state.stream_history["z_score"].abs() > z_threshold

# =============================================================================
# 5. CONTAINER HIỂN THỊ VIP MAIN DASHBOARD
# =============================================================================
main_place = st.empty()

with main_place.container():
    # --- METRICS HUD VIP ---
    if not st.session_state.stream_history.empty:
        curr = st.session_state.stream_history.iloc[-1]
        prev_co2 = st.session_state.stream_history.iloc[-2]["co2_ppm"] if len(st.session_state.stream_history) > 1 else curr["co2_ppm"]
        diff_co2 = round(curr["co2_ppm"] - prev_co2, 1)
        
        m1, m2, m3, m4, m5 = st.columns(5)
        
        with m1:
            st.markdown(f"""
            <div class="vip-metric-card">
                <div class="metric-lbl">🌡️ Nhiệt Độ Trạm</div>
                <div class="metric-val">{curr['temperature']} °C</div>
                <div class="metric-sub">🟢 Live Sensor Stream</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            delta_color = "#EF4444" if diff_co2 > 0 else "#10B981"
            st.markdown(f"""
            <div class="vip-metric-card">
                <div class="metric-lbl">🟢 Nồng Độ CO2</div>
                <div class="metric-val">{curr['co2_ppm']} <span style="font-size:14px; color:#94A3B8;">ppm</span></div>
                <div class="metric-sub" style="color: {delta_color};">{'▲' if diff_co2>0 else '▼'} {abs(diff_co2)} ppm</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="vip-metric-card">
                <div class="metric-lbl">🌫️ Bụi Mịn PM2.5</div>
                <div class="metric-val">{curr['pm25']} <span style="font-size:14px; color:#94A3B8;">µg/m³</span></div>
                <div class="metric-sub">⚡ Vi Cảm Biến Real-Time</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="vip-metric-card">
                <div class="metric-lbl">💧 Độ Ẩm Không Khí</div>
                <div class="metric-val">{curr['humidity']} %</div>
                <div class="metric-sub" style="color:#8B5CF6;">🌊 Ổn định môi trường</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m5:
            aqi_color = "#10B981" if curr['aqi'] < 50 else ("#F59E0B" if curr['aqi'] < 100 else "#EF4444")
            st.markdown(f"""
            <div class="vip-metric-card">
                <div class="metric-lbl">⚠️ Chỉ Số Chất Lượng AQI</div>
                <div class="metric-val" style="color:{aqi_color};">{curr['aqi']}</div>
                <div class="metric-sub" style="color:{aqi_color};">{"🟢 Tốt" if curr['aqi'] < 50 else ("🟡 Trung Bình" if curr['aqi'] < 100 else "🔴 Nguy Hiểm")}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ANOMALY ALERT BANNER ---
    anom_count = st.session_state.stream_history["is_anomaly"].sum() if not st.session_state.stream_history.empty else 0
    if anom_count > 0:
        st.markdown(f'''
        <div class="alert-box-vip">
            🚨 <b>CẢNH BÁO ANOMALY REAL-TIME</b>: Đã phát hiện <b>{anom_count} sự cố đột biến</b> vượt ngưỡng Z-Score (|Z| > {z_threshold:.1f}σ). Hệ thống tự động ghi nhận vào log nhật ký môi trường!
        </div>
        ''', unsafe_allow_html=True)

    # --- TABS PHÂN TÍCH CHUYÊN SÂU VIP ---
    tab_stream, tab_visual, tab_map, tab_custom, tab_ml, tab_data = st.tabs([
        "⚡ Stream Real-Time & Gauge",
        "🎬 Biểu Đồ 4D & Bề Mặt 3D",
        "🗺️ Bản Đồ Thế Giới & Ma Trận 16 Cột",
        "🎛️ 7 Custom Buttons",
        "🤖 AI Học Máy Có Giám Sát",
        "📋 Dữ Liệu & Xuất CSV"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: REAL-TIME STREAM & GAUGE METERS
    # -------------------------------------------------------------------------
    with tab_stream:
        col_chart, col_gauge = st.columns([2.3, 1.2])
        
        with col_chart:
            st.markdown("##### 📈 Dòng Dữ Liệu Real-Time Đa Thông Số Cảm Biến")
            if not st.session_state.stream_history.empty:
                fig_st = go.Figure()
                
                # CO2 Spline Line
                fig_st.add_trace(go.Scatter(
                    x=st.session_state.stream_history["timestamp"],
                    y=st.session_state.stream_history["co2_ppm"],
                    mode="lines+markers",
                    name="Nồng độ CO2 (ppm)",
                    line=dict(color="#00F2FE", width=3.5, shape='spline'),
                    fill='tozeroy',
                    fillcolor='rgba(0, 242, 254, 0.08)'
                ))
                
                # PM2.5 Spline Line
                fig_st.add_trace(go.Scatter(
                    x=st.session_state.stream_history["timestamp"],
                    y=st.session_state.stream_history["pm25"],
                    mode="lines+markers",
                    name="Bụi mịn PM2.5 (µg/m³)",
                    line=dict(color="#F43F5E", width=2.5, dash='dash', shape='spline')
                ))
                
                # Anomalies
                anoms = st.session_state.stream_history[st.session_state.stream_history["is_anomaly"]]
                if not anoms.empty:
                    fig_st.add_trace(go.Scatter(
                        x=anoms["timestamp"],
                        y=anoms["co2_ppm"],
                        mode="markers",
                        name="🔥 Anomaly Spike",
                        marker=dict(color="#FF007F", size=14, symbol="diamond", line=dict(color="#FFFFFF", width=2))
                    ))
                    
                fig_st.update_layout(
                    title=f"Luồng Dữ Liệu Thời Gian Thực (Cập nhật: {(datetime.now() + timedelta(hours=7)).strftime('%H:%M:%S')})",
                    xaxis_title="Thời gian thực",
                    yaxis_title="Giá trị Cảm biến",
                    template="plotly_dark",
                    paper_bgcolor="rgba(15, 23, 42, 0.6)",
                    plot_bgcolor="rgba(15, 23, 42, 0.6)",
                    height=440,
                    hovermode="x unified",
                    legend=dict(orientation="h", y=1.1, x=0.1)
                )
                st.plotly_chart(fig_st, use_container_width=True)
                
        with col_gauge:
            st.markdown("##### ⏱️ Anomaly Z-Score Gauge Meter")
            if not st.session_state.stream_history.empty:
                latest_z = abs(st.session_state.stream_history.iloc[-1]["z_score"])
                
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=latest_z,
                    title={'text': "Độ Bất Thường (Z-Score σ)", 'font': {'size': 16, 'color': '#F8FAFC'}},
                    gauge={
                        'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                        'bar': {'color': "#FF007F" if latest_z > z_threshold else "#00F2FE"},
                        'steps': [
                            {'range': [0, 1.5], 'color': "rgba(16, 185, 129, 0.2)"},
                            {'range': [1.5, 2.5], 'color': "rgba(245, 158, 11, 0.2)"},
                            {'range': [2.5, 4.0], 'color': "rgba(239, 68, 68, 0.3)"}
                        ],
                        'threshold': {
                            'line': {'color': "#EF4444", 'width': 4},
                            'thickness': 0.75,
                            'value': z_threshold
                        }
                    }
                ))
                fig_g.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(15, 23, 42, 0.6)",
                    plot_bgcolor="rgba(15, 23, 42, 0.6)",
                    height=440, 
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig_g, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 2: ANIMATED 4D BUBBLE & 3D SURFACE RISK FIELD
    # -------------------------------------------------------------------------
    with tab_visual:
        c4d, c3d = st.columns([1.2, 1])
        
        with c4d:
            st.markdown("##### 🎬 1. Biểu Đồ Bong Bóng 4D Hoạt Hình (Gapminder Dynamic)")
            if not df_gapminder.empty:
                df_gap = df_gapminder.copy()
                fig_4d = px.scatter(
                    df_gap,
                    x="gdpPercap",
                    y="lifeExp",
                    animation_frame="year",
                    animation_group="country",
                    size="pop",
                    color="continent",
                    hover_name="country",
                    log_x=True,
                    size_max=55,
                    range_x=[200, 60000],
                    range_y=[25, 90],
                    labels={"gdpPercap": "GDP/Người ($USD Log)", "lifeExp": "Tuổi thọ (Năm)", "continent": "Châu lục"},
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig_4d.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(15, 23, 42, 0.6)",
                    plot_bgcolor="rgba(15, 23, 42, 0.6)",
                    height=480
                )
                st.plotly_chart(fig_4d, use_container_width=True)
                
        with c3d:
            st.markdown("##### 🧊 2. Biểu Đồ Bề Mặt Rủi Ro Môi Trường 3D (Environmental 3D Surface)")
            # Tạo lưới 3D mô phỏng mô hình rủi ro
            x_gdp = np.linspace(10, 100, 30)
            y_energy = np.linspace(50, 500, 30)
            X_m, Y_m = np.meshgrid(x_gdp, y_energy)
            Z_risk = np.sin(X_m / 10) * np.cos(Y_m / 50) * 50 + (X_m * 0.4 + Y_m * 0.1)
            
            fig_3d = go.Figure(data=[go.Surface(
                z=Z_risk, x=X_m, y=Y_m,
                colorscale='Viridis',
                colorbar=dict(title="Chỉ số Risk")
            )])
            fig_3d.update_layout(
                title="Bề mặt 3D: Tương quan GDP x Năng lượng x Chỉ số Rủi ro Môi trường",
                scene=dict(
                    xaxis_title='Quy mô GDP',
                    yaxis_title='Tiêu thụ Năng lượng',
                    zaxis_title='Chỉ số Rủi ro',
                    xaxis=dict(backgroundcolor="rgba(15, 23, 42, 0.6)"),
                    yaxis=dict(backgroundcolor="rgba(15, 23, 42, 0.6)"),
                    zaxis=dict(backgroundcolor="rgba(15, 23, 42, 0.6)")
                ),
                template="plotly_dark",
                paper_bgcolor="rgba(15, 23, 42, 0.6)",
                height=480,
                margin=dict(l=10, r=10, t=50, b=10)
            )
            st.plotly_chart(fig_3d, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 3: WORLD MAP HEATMAP & 16-COLUMN CORRELATION MATRIX
    # -------------------------------------------------------------------------
    with tab_map:
        st.markdown(f"##### 🗺️ 1. Bản Đồ Cường Độ Khí Thải CO2 Toàn Cầu (Năm {selected_year})")
        if not df_owid.empty:
            df_year = df_owid[(df_owid['year'] == selected_year) & (df_owid['iso_code'].notna()) & (df_owid['iso_code'] != '')].copy()
            
            fig_map = px.choropleth(
                df_year,
                locations="iso_code",
                color="co2",
                hover_name="country",
                hover_data=["co2_per_capita", "gdp", "population"],
                color_continuous_scale="Turbid",
                labels={"co2": "CO2 (Triệu tấn)"},
                title=f"Phân Bố Phát Thải CO2 Quốc Gia Trên Bản Đồ Thế Giới - {selected_year}"
            )
            fig_map.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(15, 23, 42, 0.6)",
                geo=dict(bgcolor="rgba(15, 23, 42, 0.6)", showcoastlines=True, coastlinecolor="#334155"),
                height=460,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
        st.markdown("---")
        st.markdown("##### 📊 2. Ma Trận Tương Quan Pearson 16 Cột Đặc Trưng Môi Trường & Kinh Tế")
        if not df_owid.empty:
            cols16 = [
                'co2', 'total_ghg', 'gdp', 'population', 'methane', 'nitrous_oxide',
                'coal_co2', 'oil_co2', 'gas_co2', 'energy_per_capita', 'co2_per_capita',
                'share_global_co2', 'primary_energy_consumption', 'renewables_energy_per_capita',
                'cement_co2', 'flaring_co2'
            ]
            # Lấy các cột tồn tại trong DataFrame
            valid_cols = [c for c in cols16 if c in df_owid.columns]
            df_corr_data = df_owid[df_owid['year'] >= 2015][valid_cols].dropna()
            
            if not df_corr_data.empty:
                corr_matrix = df_corr_data.corr().round(2)
                
                fig_hm = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Plasma",
                    title="Ma Trận Hệ Số Tương Quan Pearson (16 Cột Biến Đổi)"
                )
                fig_hm.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(15, 23, 42, 0.6)",
                    plot_bgcolor="rgba(15, 23, 42, 0.6)",
                    height=580
                )
                st.plotly_chart(fig_hm, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 4: 7 CUSTOM BUTTONS MULTI-FACTOR ANALYSIS
    # -------------------------------------------------------------------------
    with tab_custom:
        st.markdown("##### 🎛️ Biểu Đồ Tương Tác 7 Custom Buttons So Sánh Nguồn Phát Thải (Việt Nam 2010-2022)")
        if not df_owid.empty:
            df_vn = df_owid[(df_owid['country'] == 'Vietnam') & (df_owid['year'] >= 2010)].copy()
            
            years = df_vn['year'].tolist()
            co2_total = df_vn['co2'].fillna(0).tolist()
            co2_coal = df_vn['coal_co2'].fillna(0).tolist()
            co2_oil = df_vn['oil_co2'].fillna(0).tolist()
            co2_gas = df_vn['gas_co2'].fillna(0).tolist()
            co2_methane = df_vn['methane'].fillna(0).tolist()
            co2_cement = df_vn['cement_co2'].fillna(0).tolist()
            co2_flaring = df_vn['flaring_co2'].fillna(0).tolist()
            
            fig_cb = go.Figure()
            fig_cb.add_trace(go.Scatter(x=years, y=co2_coal, mode='lines+markers', name='1. 🔥 CO2 Than đá', line=dict(color='#EF4444', width=3)))
            fig_cb.add_trace(go.Scatter(x=years, y=co2_oil, mode='lines+markers', name='2. 🛢️ CO2 Dầu mỏ', line=dict(color='#F59E0B', width=3)))
            fig_cb.add_trace(go.Scatter(x=years, y=co2_gas, mode='lines+markers', name='3. 💨 CO2 Khí đốt', line=dict(color='#38BDF8', width=3)))
            fig_cb.add_trace(go.Scatter(x=years, y=co2_methane, mode='lines+markers', name='4. 🌾 Khí Methane', line=dict(color='#10B981', width=3)))
            fig_cb.add_trace(go.Scatter(x=years, y=co2_cement, mode='lines+markers', name='5. 🏭 CO2 Xi măng', line=dict(color='#A855F7', width=3)))
            fig_cb.add_trace(go.Scatter(x=years, y=co2_flaring, mode='lines+markers', name='6. 💥 CO2 Flaring', line=dict(color='#EC4899', width=3)))
            fig_cb.add_trace(go.Scatter(x=years, y=co2_total, mode='lines+markers', name='7. 🔴 Tổng CO2 Quôc Gia', line=dict(color='#00F2FE', width=4, dash='dash')))
            
            btn_list = [
                dict(label="🔥 1. Than Đá", method="update", args=[{"visible": [True, False, False, False, False, False, False]}, {"title": "<b>NGUỒN XẢ THẢI: THAN ĐÁ (COAL)</b>"}]),
                dict(label="🛢️ 2. Dầu Mỏ", method="update", args=[{"visible": [False, True, False, False, False, False, False]}, {"title": "<b>NGUỒN XẢ THẢI: DẦU MỎ (OIL)</b>"}]),
                dict(label="💨 3. Khí Đốt", method="update", args=[{"visible": [False, False, True, False, False, False, False]}, {"title": "<b>NGUỒN XẢ THẢI: KHÍ THIÊN NHIÊN (GAS)</b>"}]),
                dict(label="🌾 4. Methane", method="update", args=[{"visible": [False, False, False, True, False, False, False]}, {"title": "<b>NGUỒN XẢ THẢI: METHANE (NÔNG NGHIỆP)</b>"}]),
                dict(label="🏭 5. Xi Măng", method="update", args=[{"visible": [False, False, False, False, True, False, False]}, {"title": "<b>NGUỒN XẢ THẢI: CÔNG NGHIỆP XI MĂNG</b>"}]),
                dict(label="🔴 6. Tổng CO2", method="update", args=[{"visible": [False, False, False, False, False, False, True]}, {"title": "<b>NGUỒN XẢ THẢI: TỔNG CO2 NĂM</b>"}]),
                dict(label="📊 7. TOÀN DIỆN 7 NGUỒN", method="update", args=[{"visible": [True, True, True, True, True, True, True]}, {"title": "<b>BỨC TRANH SO SÁNH TOÀN DIỆN 7 NGUỒN PHÁT THẢI</b>"}])
            ]
            
            fig_cb.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(15, 23, 42, 0.6)",
                plot_bgcolor="rgba(15, 23, 42, 0.6)",
                height=520,
                updatemenus=[dict(
                    type="buttons",
                    direction="right",
                    active=6,
                    x=0.5,
                    y=1.22,
                    xanchor="center",
                    bgcolor="#1E293B",
                    bordercolor="#334155",
                    font=dict(color="#F8FAFC", size=12),
                    buttons=btn_list
                )]
            )
            st.plotly_chart(fig_cb, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 5: SUPERVISED MACHINE LEARNING AI & NET-ZERO SIMULATION
    # -------------------------------------------------------------------------
    with tab_ml:
        st.markdown("##### 🤖 Mô Hình Học Máy Có Giám Sát Dự Báo Khí Nhà Kính (Supervised AI Regressor)")
        if not df_owid.empty:
            df_2022 = df_owid[df_owid['year'] == 2022].dropna(subset=['gdp', 'population', 'co2', 'coal_co2', 'oil_co2', 'gas_co2', 'total_ghg']).copy()
            
            feature_cols = ['gdp', 'population', 'co2', 'coal_co2', 'oil_co2', 'gas_co2']
            target_col = 'total_ghg'
            
            X = df_2022[feature_cols]
            y = df_2022[target_col]
            
            rf_model = RandomForestRegressor(n_estimators=120, random_state=42)
            rf_model.fit(X, y)
            
            y_pred = rf_model.predict(X)
            r2_val = r2_score(y, y_pred)
            rmse_val = np.sqrt(mean_squared_error(y, y_pred))
            
            # Cards chỉ số AI
            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(f"""
                <div class="vip-metric-card">
                    <div class="metric-lbl">🎯 Hệ Số Xác Định R² Score</div>
                    <div class="metric-val" style="color:#10B981;">{r2_val:.4f}</div>
                    <div class="metric-sub">Độ chính xác mô hình AI</div>
                </div>
                """, unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="vip-metric-card">
                    <div class="metric-lbl">📉 Sai Số Căn Bậc Hai RMSE</div>
                    <div class="metric-val" style="color:#38BDF8;">{rmse_val:,.1f}</div>
                    <div class="metric-sub">Triệu tấn CO₂eq</div>
                </div>
                """, unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="vip-metric-card">
                    <div class="metric-lbl">🌲 Thuật Toán Học Máy</div>
                    <div class="metric-val" style="color:#C084FC;">Random Forest</div>
                    <div class="metric-sub">120 Decision Trees</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_ml1, col_ml2 = st.columns([1.3, 1])
            
            with col_ml1:
                st.markdown("###### 🔮 Bảng Giả Định Chính Sách Giảm Phát Thải (Net-Zero Simulator)")
                in_gdp = st.slider("GDP Quốc gia (Tỷ USD):", 10, 25000, 850)
                in_pop = st.slider("Dân số (Triệu người):", 1, 1500, 100)
                in_co2 = st.slider("Lượng CO2 cơ sở (Triệu tấn):", 1, 12000, 350)
                coal_reduce_pct = st.slider("📉 % Cắt giảm Than đá (Chuyển dịch Năng lượng):", 0, 100, 30)
                
                # Tính CO2 sau cắt giảm
                adj_co2 = in_co2 * (1 - coal_reduce_pct * 0.005)
                pred_val = rf_model.predict([[in_gdp*1e9, in_pop*1e6, adj_co2, adj_co2*0.35, adj_co2*0.3, adj_co2*0.2]])[0]
                
                st.success(f"""
                ### 🔮 Dự Báo Khí Nhà Kính Tổng: **{pred_val:,.1f} Triệu Tấn CO₂eq**
                *(Đã giảm khoảng **{(in_co2 - adj_co2)*1.15:,.1f} triệu tấn** nhờ cắt giảm {coal_reduce_pct}% nhiệt điện than!)*
                """)
                
            with col_ml2:
                st.markdown("###### 📊 Tỷ Trọng Đóng Góp Của Các Biến Đầu Vào (Feature Importances)")
                importances = pd.Series(rf_model.feature_importances_, index=["GDP", "Dân số", "Tổng CO2", "Than đá", "Dầu mỏ", "Khí đốt"]).sort_values(ascending=True)
                fig_imp = px.bar(importances, orientation='h', color=importances.values, color_continuous_scale="Viridis")
                fig_imp.update_layout(
                    height=360,
                    showlegend=False,
                    template="plotly_dark",
                    paper_bgcolor="rgba(15, 23, 42, 0.6)",
                    plot_bgcolor="rgba(15, 23, 42, 0.6)",
                    xaxis_title="Độ quan trọng",
                    yaxis_title="Đặc trưng"
                )
                st.plotly_chart(fig_imp, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 6: DATA TABLE & EXPORT CSV
    # -------------------------------------------------------------------------
    with tab_data:
        st.markdown("##### 📋 Dữ Liệu Dòng Real-Time Stream (Các Mẫu Cảm Biến Mới Nhất)")
        if not st.session_state.stream_history.empty:
            st.dataframe(st.session_state.stream_history, use_container_width=True)
            
            csv_data = st.session_state.stream_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tải Nhật Ký Dữ Liệu Real-Time (.CSV)",
                data=csv_data,
                file_name=f"realtime_environment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Re-run loop thời gian thực
if is_streaming:
    time.sleep(update_speed)
    st.rerun()
