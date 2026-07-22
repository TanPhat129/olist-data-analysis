# OLIST E-COMMERCE DATA ANALYSIS PROJECT

## 1. Mục tiêu dự án
Xây dựng hệ thống phân tích dữ liệu bán lẻ toàn diện từ tập dữ liệu Olist (Brazil). 
Mục tiêu đầu ra: Một Dashboard PowerBI tương tác sâu, phân tích 3 khía cạnh:
- Sales Performance (Doanh thu & Lợi nhuận)
- Customer Lifetime & Cohort Analysis (Vòng đời & Tỉ lệ giữ chân khách hàng)
- Supply Chain & Logistics (Hiệu suất giao hàng)

## 2. Tech Stack & Công cụ
- IDE: Visual Studio Code
- Version Control: Git / GitHub (Cấu trúc repo chuẩn Data Science)
- ETL (Tiền xử lý): Python (Pandas, Numpy, Jupyter Notebook)
- Data Modeling & BI: PowerBI Desktop
- Ngôn ngữ tính toán: DAX (Data Analysis Expressions)

## 3. Kiến trúc Dữ liệu (Star Schema)
Hệ thống sử dụng Lược đồ hình sao (Star Schema) với quy tắc nối bảng 1-Many (1 chiều từ Dim xuống Fact):
- Fact_Sales (Trung tâm)
- Fact_Reviews (Phụ)
- Fact_Payments (Phụ)
- Dim_Customer (Lưu ý: Dùng customer_unique_id để đếm số user thực tế)
- Dim_Product (Phải merge từ điển tiếng Anh)
- Dim_Seller
- Dim_Date (Bảng thời gian chuẩn)

## 4. Coding Style & Naming Convention
- Tên bảng (Table): Viết hoa chữ cái đầu, dùng prefix. VD: `Fact_Sales`, `Dim_Product`.
- Tên cột (Column): Viết thường, phân cách bằng dấu gạch dưới (snake_case) trong Python, và Capitalize Each Word trong PowerBI để lên Dashboard cho đẹp.
- Biến (Measure DAX): Bắt buộc dùng prefix `[_]`. VD: `[_Total_Revenue]`, `[_Retention_Rate]`. Xuống dòng và thụt lề chuẩn (formatter) cho DAX.

## 5. UI/UX Guideline (PowerBI)
- Style: Dark Mode hoặc Clean Minimalist.
- Font: Segoe UI (chuẩn Microsoft) hoặc DIN.
- Layout: 
  + Top: Các thẻ số liệu tổng quan (KPI Cards - Revenue, Orders, Active Users).
  + Left: Bộ lọc thời gian (Date Slicer) và Danh mục.
  + Center/Right: Các biểu đồ (Bar, Line, Matrix cho Cohort).

## 6. Quy trình triển khai & Commit Rule
- Tuân thủ quy trình 14 bước Agentic Workflow.
- Commit chuẩn Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`.
- Script ETL Python phải có comment giải thích rõ lý do xử lý null/duplicate.