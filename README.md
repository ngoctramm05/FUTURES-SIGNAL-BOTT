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

