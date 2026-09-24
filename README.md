# 👑 HỆ THỐNG VIP SCIENTIFIC: GIÁM SÁT VÀ DỰ BÁO MÔ I TRƯỜNG REAL-TIME 4D / 3D
> **Dự án Khoa học Dữ liệu VIP Ultra-Premium Edition (Real-Time Analytics, 4D Motion, 3D Risk Field, World Map Heatmap, 16-Column Pearson Matrix, 7 Custom Buttons & Machine Learning AI)**
> 
> 🎓 **Sinh viên thực hiện**: Đặng Trương Anh Tài (MSSV: K24406H) - Lớp Phân Tích Dữ Liệu Nâng Cao (UEL)  
> 🌐 **Link Ứng Dụng Trực Tuyến**: [https://realtime-environment-app-j5rzt5ukfk3wdudlzpckub.streamlit.app](https://realtime-environment-app-j5rzt5ukfk3wdudlzpckub.streamlit.app)  
> 📂 **Mã Nguồn Public GitHub**: [https://github.com/AnhTaiUEL/realtime-environment-app](https://github.com/AnhTaiUEL/realtime-environment-app)  

---

## 🔬 1. NỘI DUNG HÀM LƯỢNG KHOA HỌC VÀ TÍNH NĂNG VIP NỔI BẬT

Ứng dụng được xây dựng trên nền tảng thiết kế **Dark Cyber-Glow & Glassmorphic Design System** hiện đại với **6 Tab phân tích chuyên sâu**:

1. **⚡ Luồng Real-Time Stream Ingestion & Đồng Hồ Anomaly Gauge Meter**:
   - Tích hợp luồng dữ liệu thời gian thực (`st.empty()`, `st.rerun()`) cập nhật tự động cảm biến $CO_2$, PM2.5, Nhiệt độ, Độ ẩm và AQI.
   - Thuật toán toán học kiểm soát bất thường Z-Score:
     $$Z = \frac{X - \mu}{\sigma}$$
   - Tự động bật thẻ cảnh báo đỏ (*Anomaly Banner Alert Box*) khi bất thường $|Z| > 2.0\sigma$.

2. **🎬 Biểu Đồ Bong Bóng 4D & Bề Mặt 3D (4D Motion & 3D Environmental Risk Field)**:
   - *Biểu đồ 4D Bong bóng hoạt hình*: Nút PLAY/PAUSE chuyển động theo thời gian thể hiện 4 chiều dữ liệu (GDP, Tuổi thọ, Dân số, Châu lục).
   - *Biểu đồ 3D Bề mặt rủi ro*: Trực quan hóa mặt cong không gian 3 chiều $Z = f(\text{GDP}, \text{Năng lượng})$ hỗ trợ xoay 360 độ tương tác.

3. **🗺️ Bản Đồ Thế Giới Choropleth & Ma Trận Tương Quan 16 Cột Pearson**:
   - *Bản đồ Heatmap*: Hiển thị cường độ phát thải $CO_2$ trên bản đồ toàn cầu theo từng năm.
   - *Ma trận Pearson 16 cột*: Tính toán chỉ số tương quan $r \in [-1, 1]$ của 16 biến môi trường & kinh tế xã hội.

4. **🎛️ Biểu Đồ Tương Tác 7 Custom Buttons (Chuyển Đổi 7 Nguồn Thải)**:
   - Cho phép người dùng bấm chuyển đổi góc nhìn 7 nguồn: Than đá, Dầu mỏ, Khí thiên nhiên, Methane nông nghiệp, Công nghiệp Xi măng, Khí đốt Flaring và Bức tranh tổng hợp toàn diện.

5. **🤖 AI Học Máy Có Giám Sát & Bảng Giả Định Chính Sách Net-Zero**:
   - Thuật toán `RandomForestRegressor` dự báo tổng lượng Khí nhà kính với chỉ số $R^2 \approx 0.99$.
   - Tính toán tỷ trọng đóng góp các biến (*Feature Importances*).
   - *Net-Zero Simulator*: Thanh trượt giả định chính sách cắt giảm than đá và dự báo kết quả tức thì.

6. **📋 Dữ Liệu Real-Time & Xuất File CSV**:
   - Cho phép lọc và xuất toàn bộ dữ liệu dòng cảm biến dưới dạng tệp `.CSV`.

---

## 📁 2. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
DA NC/
├── app.py                  # Mã nguồn ứng dụng Web Streamlit VIP Real-Time 4D/3D chính
├── requirements.txt        # Danh sách thư viện Python (streamlit, plotly, scikit-learn, v.v.)
├── README.md               # Báo cáo học thuật & Hướng dẫn triển khai chi tiết
├── Bao_Cao_Do_An_PTDLNC.docx # Báo cáo nộp bài Word chuyên nghiệp
└── Slides/                 # Slide bài giảng Chương 3: Trực quan hóa Dữ liệu
```

---

## 🚀 3. CÁC BƯỚC CẬP NHẬT LÊN STREAMLIT CLOUD

1. Mở Repository GitHub: [https://github.com/AnhTaiUEL/realtime-environment-app](https://github.com/AnhTaiUEL/realtime-environment-app)
2. Bấm vào tệp `app.py` -> Nút ✏️ (Edit) hoặc `Upload files` -> Dán/Tải nội dung `app.py` mới -> Bấm **Commit changes**.
3. Streamlit Cloud sẽ tự động làm mới (Auto-redeploy) trang web [https://realtime-environment-app-j5rzt5ukfk3wdudlzpckub.streamlit.app](https://realtime-environment-app-j5rzt5ukfk3wdudlzpckub.streamlit.app) chỉ trong 10-15 giây!
