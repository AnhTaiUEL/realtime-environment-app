import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# =============================================================================
# 1. CẤU HÌNH TRANG VÀ NGUYÊN TẮC THIẾT KẾ CẠNH TRANH (ACADEMIC DESIGN SYSTEM)
# =============================================================================
st.set_page_config(
    page_title="Hệ Thống Giám Sát & Dự Báo Môi Trường Real-Time",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện khoa học chuyên nghiệp
st.markdown("""
<style>
    .main-title {
        font-size: 26px;
        font-weight: 800;
        color: #1E293B;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 14px;
        color: #64748B;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .alert-card {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 12px;
        border-radius: 6px;
        color: #991B1B;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. TIÊU ĐỀ HỌC THUẬT & TỔNG QUAN DỰ ÁN
# =============================================================================
st.markdown('<div class="main-title">🌍 HỆ THỐNG GIÁM SÁT VÀ DỰ BÁO PHÁT THẢI KHÍ NHÀ KÍNH & CẢM BIẾN REAL-TIME</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ứng dụng Khoa học Dữ liệu Trực tuyến: Tích hợp Real-Time Stream Ingestion, Thuật toán Phát hiện Bất thường (Anomaly Detection) & Machine Learning</div>', unsafe_allow_html=True)

# Sidebar Cấu hình
st.sidebar.header("⚙️ Cấu Hình Hệ Thống Real-Time")
dataset_choice = st.sidebar.selectbox(
    "Nguồn Dữ Liệu Thực Tế:",
    ["Trạm Cảm Biến Môi Trường Real-Time (Mô phỏng IoT Stream)",
     "World Bank API - GDP & Khí Thải Lịch Sử",
     "Our World in Data (Oxford Dataset)"]
)

update_interval = st.sidebar.slider("Tần suất cập nhật (Giây):", min_value=1, max_value=5, value=2)
anomaly_threshold = st.sidebar.slider("Ngưỡng cảnh báo bất thường Z-Score (σ):", min_value=1.5, max_value=3.0, value=2.0, step=0.1)

is_live = st.sidebar.toggle("🟢 Bật/Tắt Luồng Real-Time Stream", value=True)

# =============================================================================
# 3. KHO DỮ LIỆU BAN ĐẦU VÀ MÁY PHÁT LUỒNG DỮ LIỆU (DATA STREAM GENERATOR)
# =============================================================================
@st.cache_data
def load_historical_worldbank():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()

df_owid = load_historical_worldbank()

# Khởi tạo Session State lưu trữ dữ liệu luồng Real-Time
if "stream_df" not in st.session_state:
    st.session_state.stream_df = pd.DataFrame(columns=["timestamp", "temperature", "co2_ppm", "pm25", "humidity", "z_score", "is_anomaly"])

# =============================================================================
# 4. KHU VỰC HIỂN THỊ REAL-TIME CONTAINER (DÙNG STREAMLIT EMPTY CONTAINER)
# =============================================================================
placeholder = st.empty()

# Hàm cập nhật dữ liệu Real-Time
def generate_realtime_point():
    now_str = (datetime.now() + timedelta(hours=7)).strftime("%H:%M:%S")
    
    # Mô phỏng chỉ số môi trường từ trạm cảm biến IoT
    temp = round(np.random.normal(30.5, 1.5), 2)
    co2 = round(np.random.normal(420.0, 15.0), 1)
    pm25 = round(np.random.exponential(18.0), 1)
    humidity = round(np.random.uniform(60.0, 85.0), 1)
    
    # Thi thoảng cố tình tạo điểm bất thường (Anomaly spike)
    if np.random.rand() < 0.08:
        co2 += np.random.uniform(50.0, 90.0)
        pm25 += np.random.uniform(40.0, 80.0)
        
    return {
        "timestamp": now_str,
        "temperature": temp,
        "co2_ppm": co2,
        "pm25": pm25,
        "humidity": humidity
    }

# =============================================================================
# 5. VÒNG LẶP REAL-TIME STREAMING ENGINE
# =============================================================================
if is_live:
    new_point = generate_realtime_point()
    
    # Chuyển đổi và đẩy dữ liệu mới vào chuỗi
    temp_df = pd.DataFrame([new_point])
    st.session_state.stream_df = pd.concat([st.session_state.stream_df, temp_df], ignore_index=True)
    
    # Giữ lại 30 điểm gần nhất
    if len(st.session_state.stream_df) > 30:
        st.session_state.stream_df = st.session_state.stream_df.iloc[-30:].reset_index(drop=True)
        
    # Tính toán chỉ số thống kê toán học Z-Score cho việc Phát hiện Bất thường (Anomaly Detection)
    co2_mean = st.session_state.stream_df["co2_ppm"].mean()
    co2_std = st.session_state.stream_df["co2_ppm"].std()
    
    if co2_std > 0:
        st.session_state.stream_df["z_score"] = (st.session_state.stream_df["co2_ppm"] - co2_mean) / co2_std
    else:
        st.session_state.stream_df["z_score"] = 0
        
    st.session_state.stream_df["is_anomaly"] = st.session_state.stream_df["z_score"].abs() > anomaly_threshold

# Render giao diện chính trong Container
with placeholder.container():
    # --- METRICS BẢNG ĐIỀU KHIỂN SỐ LƯỢNG REAL-TIME ---
    col1, col2, col3, col4 = st.columns(4)
    
    if not st.session_state.stream_df.empty:
        latest = st.session_state.stream_df.iloc[-1]
        prev_co2 = st.session_state.stream_df.iloc[-2]["co2_ppm"] if len(st.session_state.stream_df) > 1 else latest["co2_ppm"]
        delta_co2 = round(latest["co2_ppm"] - prev_co2, 1)
        
        with col1:
            st.metric("🌡️ Nhiệt độ Cảm biến", f"{latest['temperature']} °C", delta=None)
        with col2:
            st.metric("🟢 Nồng độ CO2", f"{latest['co2_ppm']} ppm", delta=f"{delta_co2} ppm")
        with col3:
            st.metric("🌫️ Bụi mịn PM2.5", f"{latest['pm25']} µg/m³")
        with col4:
            st.metric("💧 Độ ẩm không khí", f"{latest['humidity']} %")
    
    st.markdown("---")
    
    # --- CẢNH BÁO BẤT THƯỜNG (ANOMALY DETECTION SYSTEM) ---
    anomalies_count = st.session_state.stream_df["is_anomaly"].sum() if not st.session_state.stream_df.empty else 0
    if anomalies_count > 0:
        st.markdown(f'<div class="alert-card">⚠️ CẢNH BÁO KHOA HỌC: Phát hiện {anomalies_count} điểm bất thường vọt ngưỡng Z-Score (|Z| > {anomaly_threshold}σ) trong luồng dữ liệu thời gian thực!</div><br>', unsafe_allow_html=True)
    
    # --- TAB PHÂN TÍCH VÀ ĐỒ THỊ ---
    tab1, tab2, tab3 = st.tabs(["📈 Chuỗi Thời Gian Real-Time", "📊 Ma Trận Tương Quan (Heatmap)", "🔮 Dự báo AI (Machine Learning)"])
    
    with tab1:
        st.subheader("📊 Luồng Cập Nhật Chuỗi Thời Gian Trực Tiếp (Real-Time Time-Series Stream)")
        if not st.session_state.stream_df.empty:
            fig_stream = go.Figure()
            
            # Đường Nồng độ CO2
            fig_stream.add_trace(go.Scatter(
                x=st.session_state.stream_df["timestamp"],
                y=st.session_state.stream_df["co2_ppm"],
                mode="lines+markers",
                name="CO2 (ppm)",
                line=dict(color="#10B981", width=3)
            ))
            
            # Điểm bất thường (Anomaly points)
            anom_df = st.session_state.stream_df[st.session_state.stream_df["is_anomaly"]]
            if not anom_df.empty:
                fig_stream.add_trace(go.Scatter(
                    x=anom_df["timestamp"],
                    y=anom_df["co2_ppm"],
                    mode="markers",
                    name="Cảnh báo Bất thường (Z-Score > σ)",
                    marker=dict(color="#EF4444", size=12, symbol="x")
                ))
                
            fig_stream.update_layout(
                title=f"Dòng Dữ Liệu Cảm Biến Cập Nhật Liên Tục (Thời gian thực: {datetime.now().strftime('%H:%M:%S')})",
                xaxis_title="Thời gian thực",
                yaxis_title="Nồng độ CO2 (ppm)",
                template="plotly_white",
                height=420
            )
            st.plotly_chart(fig_stream, use_container_width=True)
            
    with tab2:
        st.subheader("🔥 Ma Trận Tương Quan Tức Thời (Real-Time Correlation Heatmap)")
        if len(st.session_state.stream_df) >= 5:
            num_df = st.session_state.stream_df[["temperature", "co2_ppm", "pm25", "humidity"]].astype(float)
            corr = num_df.corr()
            
            fig_heat = px.imshow(
                corr,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                title="Ma Trận Tương Quan Giữa Các Yếu Tố Môi Trường Real-Time"
            )
            fig_heat.update_layout(height=420, template="plotly_white")
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("Đang tích lũy mẫu dữ liệu stream để tính toán ma trận tương quan...")
            
    with tab3:
        st.subheader("🔮 Mô Hình Học Máy Có Giám Sát Dự Báo Phát Thải (Supervised ML Model)")
        if not df_owid.empty:
            df_2022 = df_owid[df_owid['year'] == 2022].dropna(subset=['gdp', 'population', 'total_ghg']).copy()
            
            X = df_2022[['gdp', 'population']]
            y = df_2022['total_ghg']
            
            ml_model = LinearRegression()
            ml_model.fit(X, y)
            
            st.success("✅ Mô hình Linear Regression đã huấn luyện thành công trên dữ liệu World Bank / OWID!")
            
            col_gdp, col_pop = st.columns(2)
            with col_gdp:
                input_gdp = st.number_input("Dự kiến GDP Quốc gia (Tỷ USD):", min_value=10.0, max_value=25000.0, value=800.0)
            with col_pop:
                input_pop = st.number_input("Dự kiến Dân số (Triệu người):", min_value=1.0, max_value=1500.0, value=100.0)
                
            pred_ghg = ml_model.predict([[input_gdp * 1e9, input_pop * 1e6]])[0]
            st.markdown(f"### 🎯 Kết quả AI Dự Báo Tổng Phát Thải Khí Nhà Kính: **{pred_ghg:,.2f} Triệu tấn CO₂ tương đương**")

# Tự động Re-run để cập nhật Real-time liên tục
if is_live:
    time.sleep(update_interval)
    st.rerun()
