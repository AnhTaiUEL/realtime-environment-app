# 🌍 HỆ THỐNG GIÁM SÁT VÀ DỰ BÁO PHÁT THẢI KHÍ NHÀ KÍNH & CẢM BIẾN REAL-TIME
> **Dự án Khoa học Dữ liệu Nâng cao (Real-Time Analytics & Machine Learning Web Application)**
> 
> 🎓 **Tác giả / Nhóm thực hiện**: Học viên / Sinh viên Phân Tích Dữ Liệu Nâng Cao (PTDLNC)
> 🌐 **Ứng dụng Trực tuyến**: Triển khai trực tiếp trên Streamlit Community Cloud / GitHub / Heroku

---

## 📌 1. NỘI DUNG HÀM LƯỢNG KHOA HỌC (SCIENTIFIC RIGOR & FEATURES)

Hệ thống được thiết kế đáp ứng các tiêu chuẩn nghiên cứu khoa học dữ liệu hiện đại với 4 trụ cột kỹ thuật cốt lõi:

1. **⚡ Real-Time Ingestion & Streaming Engine**:
   - Sử dụng kiến trúc vòng lặp tự động cập nhật dữ liệu dòng (*Stream Data*) theo thời gian thực mà không làm gián đoạn trải nghiệm người dùng (`st.empty()`, `st.rerun()`).

2. **📊 Thuật toán Phát hiện Bất thường Khoa học (Mathematical Anomaly Detection)**:
   - Áp dụng chỉ số thống kê $Z$-Score toán học để phát hiện tự động các điểm spike/bất thường ô nhiễm theo thời gian thực:
     $$Z = \frac{X - \mu}{\sigma}$$
   - Trong đó $\mu$ là trung bình mẫu và $\sigma$ là độ lệch chuẩn. Khi $|Z| > 2.0\sigma$, hệ thống tự động kích hoạt cảnh báo nguy hiểm (*Anomaly Alert*).

3. **🔥 Ma trận Tương quan Đa biến Real-Time (Correlation Matrix Heatmap)**:
   - Tính toán ma trận tương quan Pearson ($r$) liên tục cho các yếu tố môi trường để phục vụ bài toán lựa chọn đặc trưng (*Feature Selection*).

4. **🤖 Mô hình Học máy Có Giám sát Dự báo Phát thải (Supervised Machine Learning)**:
   - Tích hợp mô hình Hồi quy tuyến tính (*Linear Regression*) huấn luyện trên dữ liệu thực tế của Ngân hàng Thế giới (World Bank) và Đại học Oxford (OWID) để dự báo tổng phát thải $CO_2$ ròng.

---

## 📁 2. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
DA NC/
├── app.py                  # Mã nguồn ứng dụng Web Streamlit Real-Time chính
├── requirements.txt        # Danh sách thư viện Python phục vụ triển khai Cloud
├── README.md               # Báo cáo học thuật & Hướng dẫn triển khai chi tiết
└── Slides/                 # Slide bài giảng Chương 3: Trực quan hóa Dữ liệu
```

---

## 🚀 3. HƯỚNG DẪN TRIỂN KHAI LÊN STREAMLIT COMMUNITY CLOUD / GITHUB (CHỈ TRONG 3 BƯỚC)

### 🔹 Bước 1: Đưa Dự án lên GitHub (Public hoặc Private)
1. Mở trang [GitHub.com](https://github.com/) và bấm **New Repository**.
2. Đặt tên kho lưu trữ: `realtime-environmental-monitoring`.
3. Tải lên 3 tập tin: `app.py`, `requirements.txt`, và `README.md`.

### 🔹 Bước 2: Triển khai trực tuyến trên Streamlit Cloud (Miễn phí 100%)
1. Truy cập trang web: [share.streamlit.io](https://share.streamlit.io/)
2. Bấm **New App** -> Đăng nhập bằng tài khoản GitHub.
3. Chọn Repository: `realtime-environmental-monitoring`, Main file path: `app.py`.
4. Nhấn **Deploy!** -> Chỉ sau 1 phút, ứng dụng của bạn sẽ có **Đường dẫn Web trực tuyến công khai** (dạng `https://realtime-monitoring.streamlit.app`) để nộp bài!

---

## 💻 4. HƯỚNG DẪN CHẠY THỬ TRÊN MÁY CỤC BỘ (LOCAL RUN)

```bash
pip install -r requirements.txt
streamlit run app.py
```
