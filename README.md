<<<<<<< HEAD
# ROBO-ADVISOR-SIGNAL
## 1. Thông tin dự án
- Tên dự án: Robo-Advisor Trading Bot
- Ngôn ngữ: Python
- Nền tảng: Bitget Spot API
- Mục đích: Phân tích dữ liệu thị trường và tạo tín hiệu giao dịch tự động
## 2. Mô tả hệ thống
Hệ thống là một bot phân tích thị trường tài chính theo thời gian thực, sử dụng dữ liệu giá và khối lượng từ Bitget API.
Bot thực hiện:
- Thu thập dữ liệu nến (candlestick)
- Tính toán các chỉ báo kỹ thuật
- Xác định tín hiệu giao dịch
- Hiển thị kết quả trên terminal
- Gửi thông báo qua Telegram
## 3. Dữ liệu sử dụng
- Nguồn: Bitget Public API
- Loại dữ liệu:
  - Giá đóng cửa (Close price)
  - Khối lượng giao dịch (Volume)
  - Timestamp
- Khung thời gian: 5 phút
## 4. Danh sách tài sản theo dõi
Hệ thống chỉ theo dõi các token thuộc nhóm Tokenized US Stocks trên Bitget:
AAPLon, ABNBon, ACNon, ADBEon, AMDon, APPon, AVGOon, AXPon, BAon, BIDUon, CMGon, COINon, COSTon, CRCLon, CRMon, DASHon, DISon, EQIXon, FIGon, FUTUon, GEon, GMEon, GOOGLon, GSon, HIMSon, HOODon, INTCon, INTUon, JDon, LINon, MAon, MARAon, METAon, MRVLon, MSFTon, MSTRon, MUon, NFLXon, NOWon, NVDAon, PANWon, PBRon, PLTRon, PYPLon, RDDTon, RIOTon, SBETon, SHOPon, SPGIon, SPOTon, TSLAon, TSMon, UNHon, WFCon
## 5. Phương pháp phân tích
### 5.1 EMA (Exponential Moving Average)
- EMA9: xu hướng ngắn hạn
- EMA21: xu hướng trung hạn
Tín hiệu:
- EMA9 cắt lên EMA21 → xu hướng tăng
- EMA9 cắt xuống EMA21 → xu hướng giảm
### 5.2 RSI (Relative Strength Index)
- RSI < 30: vùng quá bán
- RSI > 70: vùng quá mua
### 5.3 Volume
- So sánh volume hiện tại với trung bình 20 phiên
- Volume cao → xác nhận tín hiệu mạnh
## 6. Logic tạo tín hiệu
Hệ thống tạo tín hiệu theo điều kiện:
- BUY: EMA9 cắt lên EMA21 + RSI thấp
- SELL: EMA9 cắt xuống EMA21 + RSI cao
- WATCH BUY: xu hướng tăng + volume xác nhận
- WATCH SELL: xu hướng giảm + volume xác nhận
- HOLD: không có tín hiệu rõ ràng
## 7. Kết quả đầu ra
Khi chạy chương trình, hệ thống sẽ:
- Hiển thị giá và tín hiệu trên terminal
- In các chỉ số: RSI, EMA9, EMA21, Volume
- Cập nhật theo chu kỳ thời gian 30 giây
=======
# 🤖FUTURES-SIGNAL-BOTT
## 📌 Giới thiệu
Dự án xây dựng một **Signal Bot hỗ trợ giao dịch Futures (tiền giả lập)** trên thị trường crypto.
Bot không tự động đặt lệnh mà:
- Quét thị trường liên tục
- Phát hiện tín hiệu có xác suất cao
- Gửi cảnh báo để người dùng vào lệnh thủ công trong thời gian ngắn
## ⚙️ Môi trường hoạt động
- Nguồn dữ liệu: API Binance
- Số lượng cặp: ≥ 20 cặp USDT (BTC, ETH, SOL,...)
- Khung thời gian: 1 phút (1m)
- Chu kỳ quét: 30 giây/lần
- Hình thức: Bot tín hiệu (không auto trade)
## 🧠 Chiến lược (Alpha)
Bot sử dụng 3 chỉ báo chính:
###  1. RSI (Chỉ số sức mạnh tương đối)
Trong đó:
- RS = trung bình tăng / trung bình giảm 
 Ý nghĩa:
- RSI < 40 → thị trường quá bán → có thể tăng
- RSI > 60 → thị trường quá mua → có thể giảm
###  2. Volume 
 Volume Ratio = Volume hiện tại / Volume trung bình 20 phiên
 Ý nghĩa:
- Volume Ratio > 1.2 → thanh khoản tăng nhẹ
- Volume Ratio > 1.5 → dòng tiền mạnh (có ý nghĩa giao dịch)
- Volume Ratio > 2.0 → dòng tiền đột biến (biến động lớn có thể xảy ra)

Lưu ý:
- Bot KHÔNG coi mọi mức tăng volume là tín hiệu vào lệnh.  
- Chỉ khi volume tăng đủ mạnh (≥ 1.5 lần) mới được sử dụng để xác nhận tín hiệu.
  
=>> Kết hợp thêm với biến động giá để tránh nhiễu:
- Volume cao nhưng giá đi ngang → bỏ qua
- Volume cao + giá biến động → tín hiệu đáng chú ý
###  3. Xu hướng EMA
 Ý nghĩa:
- EMA9 > EMA21 → xu hướng tăng
- EMA9 < EMA21 → xu hướng giảm
## 🚨 Điều kiện phát tín hiệu
### Tín hiệu LONG
- RSI < 40  
- Volume > 1.2  
- EMA9 > EMA21  
=>> Thị trường có khả năng đảo chiều tăng
### Tín hiệu SHORT
- RSI > 60  
- Volume > 1.2  
- EMA9 < EMA21  
=>> Thị trường có khả năng giảm
### Tín hiệu WATCH
- Volume > 1.3  
=>> Có thể sắp có biến động mạnh
###  Tín hiệu HOLD
=>> Không đủ điều kiện → bỏ qua
## 📲 Kết quả hiển thị
Bot gửi tín hiệu qua Telegram gồm:
- Tên coin
- Giá hiện tại
- RSI
- Biến động %
- Volume
- Loại tín hiệu
- Lý do
## Ví dụ tín hiệu
🟢 BTCUSDT → LONG  
💰 Giá: 67,000  
📊 RSI: 35  
📈 Biến động: +1.4%  
🔊 Volume: 1.45x  
🧠 RSI thấp + Volume tăng + Xu hướng tăng  

>>>>>>> 645596dc3b3c576d85270e33c1020eb9a01fec01
