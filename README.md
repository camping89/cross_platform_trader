# 🚀 EXNESS MT5 Trading Service

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![MetaTrader5](https://img.shields.io/badge/MetaTrader5-5.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Dịch vụ API giao dịch tự động hoàn chỉnh cho MetaTrader 5 với sàn Exness**

Hệ thống cung cấp RESTful API để thực hiện giao dịch tự động, quản lý rủi ro, theo dõi signal và thông báo thời gian thực thông qua MT5 terminal.

## 📋 Tính năng chính

### 🎯 Trading Operations
- ✅ **Market Orders** - Thực hiện lệnh thị trường ngay lập tức
- ✅ **Pending Orders** - Quản lý lệnh chờ (Limit, Stop)
- ✅ **Position Management** - Quản lý positions (đóng, sửa SL/TP, hedge)
- ✅ **Automated Trading** - Giao dịch tự động theo lịch và điều kiện

### 📊 Market Analysis
- ✅ **Real-time Prices** - Giá thời gian thực
- ✅ **Symbol Information** - Thông tin chi tiết symbols
- ✅ **OHLC Data** - Dữ liệu nến (candlestick)
- ✅ **Tick History** - Lịch sử tick data

### 🛡️ Risk Management
- ✅ **Position Sizing** - Tính toán kích thước position tối ưu
- ✅ **Trailing Stop** - Quản lý trailing stop loss
- ✅ **Portfolio Risk** - Phân tích rủi ro portfolio
- ✅ **Hedge Positions** - Tạo positions hedge

### 🤖 Advanced Features
- ✅ **Grid Trading** - Chiến lược grid trading
- ✅ **Martingale** - Chiến lược martingale
- ✅ **Signal Trading** - Lưu trữ và theo dõi signals
- ✅ **Scheduled Trading** - Giao dịch theo lịch
- ✅ **Conditional Orders** - Lệnh có điều kiện

### 📱 Notifications
- ✅ **Telegram Bot** - Thông báo qua Telegram
- ✅ **Discord Webhook** - Thông báo qua Discord
- ✅ **Real-time Alerts** - Cảnh báo thời gian thực

## 🏗️ Kiến trúc hệ thống

```
FastAPI Application
├── 🌐 API Routers           # REST API endpoints
├── 🔧 Services             # Business logic layer
│   ├── MT5BaseService      # Connection management
│   ├── TradingService      # Trading operations
│   ├── MarketService       # Market data
│   ├── RiskService         # Risk management
│   ├── AutomationService   # Automated strategies
│   ├── SignalService       # Signal management
│   └── NotificationService # Alerts & notifications
├── 📊 Models              # Data structures (Pydantic)
├── 🛠️ Utils               # Helper functions
└── 💾 Database            # MongoDB for signals/automation
```

## 📦 Cài đặt

### Prerequisites
- **Python 3.8+**
- **MetaTrader 5 Terminal** 
- **Exness Trading Account**
- **MongoDB** (cho signals và automation)

### 1. Clone repository
```bash
git clone <repository-url>
cd exness-mt5-trading-service
```

### 2. Tạo virtual environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment
Tạo file `.env`:
```env
# MT5 Settings
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server

# Notification Settings
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
DISCORD_WEBHOOK_URL=your_discord_webhook

# MongoDB Settings
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=mt5_trading
```

### 5. Cấu hình MT5 Terminal

#### **Bật AutoTrading:**
1. Mở MT5 Terminal
2. `Tools → Options → Expert Advisors`
3. ✅ Enable `"Allow algorithmic trading"`
4. ✅ Enable `"Allow DLL imports"`
5. ✅ Enable `"Allow WebRequest for listed URL"`
6. Restart MT5 Terminal

#### **Kiểm tra AutoTrading Button:**
- Trên toolbar MT5, tìm button "AutoTrading" (🤖)
- Đảm bảo nó đang **ENABLED** (màu xanh lá)

### 6. Chạy ứng dụng
```bash
python -m app.main
```

Server sẽ chạy tại: `http://localhost:8000`

## 📚 API Documentation

### 🔗 Swagger UI
Truy cập: `http://localhost:8000/docs`

### 📊 API Endpoints Overview

#### **🎯 Trading APIs** (`/trading`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/trading/market-order` | Thực hiện lệnh thị trường |

#### **📈 Market Data APIs** (`/market`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/market/symbols` | Lấy/tìm kiếm symbols |
| `GET` | `/market/symbols/{symbol}/info` | Thông tin chi tiết symbol |
| `GET` | `/market/symbols/{symbol}/price` | Giá thời gian thực |
| `GET` | `/market/symbols/{symbol}/ticks` | Lịch sử tick data |
| `GET` | `/market/symbols/{symbol}/ohlc` | Dữ liệu OHLC |

#### **📋 Position Management APIs** (`/positions`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/positions/` | Lấy tất cả positions |
| `DELETE` | `/positions/{ticket}` | Đóng position |
| `POST` | `/positions/{ticket}/modify` | Sửa SL/TP |
| `POST` | `/positions/close-all` | Đóng tất cả positions |
| `POST` | `/positions/hedge/{ticket}` | Tạo hedge position |

#### **📝 Orders Management APIs** (`/orders`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders/pending` | Lấy pending orders |
| `POST` | `/orders/pending` | Tạo pending order |
| `DELETE` | `/orders/pending/{ticket}` | Hủy pending order |

#### **👤 Account APIs** (`/account`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/account/info` | Thông tin tài khoản |

#### **🛡️ Risk Management APIs** (`/risk`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/risk/position-size` | Tính position size |
| `POST` | `/risk/trailing-stop` | Quản lý trailing stop |
| `POST` | `/risk/portfolio-risk` | Phân tích rủi ro portfolio |

#### **📊 Trading Signals APIs** (`/signals`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/signals/` | Thêm signal |
| `GET` | `/signals/` | Lấy signals theo symbol |
| `DELETE` | `/signals/{signal_id}` | Xóa signal |
| `GET` | `/signals/symbols` | Lấy danh sách symbols |
| `GET` | `/signals/timeframes` | Lấy danh sách timeframes |

#### **🤖 Automation APIs** (`/automation`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/automation/schedule` | Lên lịch giao dịch |
| `POST` | `/automation/conditional` | Tạo lệnh có điều kiện |
| `POST` | `/automation/grid` | Thiết lập grid trading |
| `POST` | `/automation/martingale` | Thiết lập martingale |

## 💡 Ví dụ sử dụng

### 1. Thực hiện Market Order
```bash
curl -X POST "http://localhost:8000/trading/market-order" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "BTCUSD",
       "order_type": "BUY",
       "amount": 1000,
       "stop_loss": 45000,
       "take_profit": 50000,
       "comment": "BTC Long"
     }'
```

### 2. Lấy thông tin tài khoản
```bash
curl -X GET "http://localhost:8000/account/info"
```

### 3. Lấy giá symbol
```bash
curl -X GET "http://localhost:8000/market/symbols/BTCUSD/price"
```

### 4. Đóng tất cả positions
```bash
curl -X POST "http://localhost:8000/positions/close-all"
```

### 5. Thêm trading signal
```bash
curl -X POST "http://localhost:8000/signals/" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "BTCUSD",
       "signal_type": "UP",
       "timeframe": "1",
       "entry_price": 47500
     }'
```

## 🚨 Troubleshooting

### ❌ Lỗi: "AutoTrading disabled by client"

**Nguyên nhân:** MT5 Terminal chưa bật AutoTrading

**Giải pháp:**
1. **Bật AutoTrading trong MT5:**
   ```
   Tools → Options → Expert Advisors
   ✅ Allow algorithmic trading
   ✅ Allow DLL imports
   ✅ Allow WebRequest for listed URL
   ```

2. **Kiểm tra AutoTrading Button:**
   - Trên toolbar MT5, button "AutoTrading" (🤖) phải màu xanh
   - Nếu màu đỏ, click để enable

3. **Restart MT5 Terminal** sau khi thay đổi cấu hình

4. **Kiểm tra trading status:**
   ```bash
   curl -X GET "http://localhost:8000/account/info"
   ```

### ❌ Lỗi: "Failed to connect to MT5"

**Giải pháp:**
1. Kiểm tra MT5 Terminal đang chạy
2. Kiểm tra thông tin đăng nhập trong `.env`
3. Đảm bảo internet connection ổn định
4. Restart MT5 và API service

### ❌ Lỗi: "Symbol not found"

**Giải pháp:**
1. Kiểm tra symbol name chính xác: `BTCUSD`, `XAUUSD`
2. Đảm bảo symbol có trong Market Watch của MT5
3. Sử dụng API để search symbols:
   ```bash
   curl -X GET "http://localhost:8000/market/symbols?search=BTC"
   ```

## 🔧 Development

### Chạy trong development mode
```bash
python -m app.main
```

### Chạy với Gunicorn (Production)
```bash
gunicorn app.main:app -c gunicorn.conf.py
```

### Testing APIs
1. Truy cập Swagger UI: `http://localhost:8000/docs`
2. Sử dụng Postman collection
3. Test với curl commands

## 📊 Monitoring

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### Logs
- Application logs: Console output
- MT5 Terminal logs: `MT5_DATA_FOLDER/Logs/`
- Error tracking via notification services

## 🔒 Security

- **API Authentication:** Implement JWT/API keys cho production
- **Network Security:** Sử dụng HTTPS, firewall rules
- **Credential Management:** Store sensitive data trong environment variables
- **Rate Limiting:** Implement rate limiting cho API endpoints

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Support

- **Email:** your-email@example.com
- **Telegram:** @your_telegram
- **Discord:** Your Discord Server

## ⚠️ Disclaimer

**CẢNH BÁO:** Giao dịch forex và CFD có rủi ro cao. Bạn có thể mất tất cả tiền đầu tư. Sử dụng hệ thống này hoàn toàn có trách nhiệm của bạn. Tác giả không chịu trách nhiệm về bất kỳ tổn thất nào.

---

**Made with ❤️ for the Trading Community**
