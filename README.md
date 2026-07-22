#  Olist E-Commerce Data Analysis & BI Dashboard

## Tổng quan dự án
Dự án phân tích dữ liệu toàn diện dựa trên bộ dữ liệu thương mại điện tử **Olist (Brazil)**. Mục tiêu của dự án là thiết kế quy trình ETL tự động để làm sạch dữ liệu thô, xây dựng mô hình dữ liệu đa chiều (Star Schema), và trực quan hóa các chỉ số kinh doanh cốt lõi (Sales, Churn Rate, Delivery Performance) thông qua PowerBI.

Dự án phục vụ mục đích phân tích hỗ trợ ra quyết định (Decision Support), giúp tối ưu hóa chuỗi cung ứng và gia tăng tỷ lệ giữ chân khách hàng.

## Tech Stack & Công cụ
- **Tiền xử lý dữ liệu (ETL):** Python (Pandas, Numpy)
- **Môi trường phát triển:** Visual Studio Code, Jupyter Notebook
- **Mô hình hóa & Trực quan hóa (BI):** PowerBI Desktop
- **Ngôn ngữ truy vấn:** DAX (Data Analysis Expressions)

## Cấu trúc dự án
\`\`\`text
├── .doc/                   # Chứa tài liệu thiết kế, rule, CLAUDE.md
├── data/                   # Thư mục chứa dữ liệu (đã được ignore trên git)
│   ├── raw/                # Dữ liệu CSV thô ban đầu
│   └── processed/          # Dữ liệu đã qua xử lý (sẵn sàng cho PowerBI)
├── notebooks/              # Jupyter notebooks dùng để EDA (Exploratory Data Analysis)
├── scripts/                # Script Python chạy pipeline ETL
├── powerbi/                # Thư mục chứa file Dashboard (.pbix)
├── reports/                # Báo cáo review chéo (AI Generated)
├── requirements.txt        # Danh sách thư viện Python cần thiết
├── .gitignore              # Các file/thư mục không push lên GitHub
└── README.md               # Tài liệu mô tả dự án
\`\`\`

## Hướng dẫn cài đặt và sử dụng

### Bước 1: Clone repository
\`\`\`bash
git clone <your-github-repo-url>
cd <your-project-folder>
\`\`\`

### Bước 2: Thiết lập môi trường Python
\`\`\`bash
python -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
\`\`\`

### Bước 3: Chạy Data Pipeline
Đảm bảo bạn đã tải bộ dữ liệu Olist từ Kaggle và đặt các file CSV vào thư mục `data/raw/`.
Sau đó chạy lệnh:
\`\`\`bash
python scripts/main_etl.py
\`\`\`
Dữ liệu sạch sẽ được xuất ra thư mục `data/processed/`.

### Bước 4: Mở Dashboard
Mở file `powerbi/Olist_Dashboard.pbix` bằng PowerBI Desktop và Refresh dữ liệu nếu cần.

---
