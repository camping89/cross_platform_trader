from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import uvicorn
from contextlib import asynccontextmanager
from app.config import settings
from app.models.mt5.notification import NotificationConfig

from app.routers.mt5 import market_info, orders, history, position, risk_management, trading, account, notification, automation, reporting, signal
from app.routers.okx import trading as okx_trading, market as okx_market, account as okx_account

from app.services.mt5.mt5_base_service import MT5BaseService
from app.services.mt5.mt5_trading_service import MT5TradingService
from app.services.mt5.mt5_market_service import MT5MarketService
from app.services.mt5.mt5_order_service import MT5OrderService
from app.services.mt5.mt5_position_service import MT5PositionService
from app.services.mt5.mt5_history_service import MT5HistoryService
from app.services.mt5.mt5_account_service import MT5AccountService
from app.services.mt5.mt5_risk_service import MT5RiskService
from app.services.mt5.mt5_notification_service import MT5NotificationService
from app.services.mt5.mt5_automation_service import MT5AutomationService
from app.services.mt5.mt5_reporting_service import MT5ReportingService
from app.services.mt5.mt5_signal_service import MT5SignalService

from app.services.okx.okx_base_service import OKXBaseService
from app.services.okx.okx_trading_service import OKXTradingService
from app.services.okx.okx_market_service import OKXMarketService
from app.services.okx.okx_account_service import OKXAccountService

# Initialize services with shared MT5 connection
mt5_base_service = MT5BaseService()

# Create MT5 service instances
mt5_trading_service = MT5TradingService(mt5_base_service)
mt5_market_service = MT5MarketService(mt5_base_service)
mt5_order_service = MT5OrderService(mt5_base_service)
mt5_position_service = MT5PositionService(mt5_base_service)
mt5_history_service = MT5HistoryService(mt5_base_service)
mt5_account_service = MT5AccountService(mt5_base_service)
mt5_risk_service = MT5RiskService(mt5_base_service)
mt5_notification_service = MT5NotificationService(mt5_base_service)
mt5_automation_service = MT5AutomationService(mt5_base_service)
mt5_reporting_service = MT5ReportingService(mt5_base_service)
mt5_signal_service = MT5SignalService(mt5_base_service)

# Initialize services with shared OKX connection
okx_base_service = OKXBaseService()

# Create OKX service instances
okx_trading_service = OKXTradingService(okx_base_service)
okx_market_service = OKXMarketService(okx_base_service)
okx_account_service = OKXAccountService(okx_base_service)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application
    Handles startup and shutdown events
    """
    # Startup: Connect to MT5 and OKX
    try:
        # Connect to MT5
        mt5_connected = await mt5_base_service.connect(
            login=settings.MT5_LOGIN,
            password=settings.MT5_PASSWORD,
            server=settings.MT5_SERVER
        )
        if not mt5_connected:
            logger.warning("Failed to connect to MT5")
        else:
            logger.info("MT5 connection established")
        
        # Connect to OKX
        okx_connected = await okx_base_service.connect(
            api_key=settings.OKX_API_KEY,
            secret_key=settings.OKX_SECRET_KEY,
            passphrase=settings.OKX_PASSPHRASE,
            is_sandbox=settings.OKX_IS_SANDBOX
        )
        if not okx_connected:
            logger.warning("Failed to connect to OKX")
        else:
            logger.info("OKX connection established")
        
        # Initialize notification service (only if MT5 connected)
        if mt5_connected:
            notification_config = NotificationConfig(
                telegram_token=settings.TELEGRAM_BOT_TOKEN,
                telegram_chat_id=settings.TELEGRAM_CHAT_ID,
                discord_webhook=settings.DISCORD_WEBHOOK_URL,
            )
            await mt5_notification_service.initialize(notification_config)
            logger.info("Notification service initialized")
            
            # Start automation tasks
            await mt5_automation_service.start_automation()
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    
    yield  # Application running
    
    # Shutdown: Cleanup connections
    if mt5_base_service.initialized:
        logger.info("Shutting down MT5 connection")
        await mt5_automation_service.stop_automation()
        await mt5_base_service.shutdown()
        
    if okx_base_service.initialized:
        logger.info("Shutting down OKX connection")
        await okx_base_service.shutdown()

# Initialize FastAPI with lifespan
app = FastAPI(
    title="Trading API",
    description="API for automated trading through MetaTrader 5",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health",
         summary="Check status",
         description="Check connection status",
         tags=["Health Check"])
async def health_check():
    """Check connection status endpoint"""
    mt5_status = "connected" if mt5_base_service.initialized else "disconnected"
    okx_status = "connected" if okx_base_service.initialized else "disconnected"
    
    overall_status = "healthy" if (mt5_base_service.initialized or okx_base_service.initialized) else "unhealthy"
    
    return {
        "status": overall_status,
        "services": {
            "mt5": mt5_status,
            "okx": okx_status
        },
        "message": f"MT5: {mt5_status}, OKX: {okx_status}"
    }

# Include routers with mt5 prefix
app.include_router(
    trading.get_router(mt5_trading_service, mt5_notification_service),
    prefix="/mt5"
)
app.include_router(
    market_info.get_router(mt5_market_service),
    prefix="/mt5"
)
app.include_router(
    orders.get_router(mt5_order_service),
    prefix="/mt5"
)
app.include_router(
    history.get_router(mt5_history_service),
    prefix="/mt5"
)
app.include_router(
    position.get_router(mt5_position_service, mt5_notification_service),
    prefix="/mt5"
)
app.include_router(
    account.get_router(mt5_account_service),
    prefix="/mt5"
)
app.include_router(
    risk_management.get_router(mt5_risk_service),
    prefix="/mt5"
)
app.include_router(
    notification.get_router(mt5_notification_service),
    prefix="/mt5"
)
app.include_router(
    automation.get_router(mt5_automation_service),
    prefix="/mt5"
)
app.include_router(
    reporting.get_router(mt5_reporting_service),
    prefix="/mt5"
)
app.include_router(
    signal.get_router(mt5_signal_service, mt5_notification_service),
    prefix="/mt5"
)

# Include OKX routers with okx prefix
app.include_router(
    okx_trading.get_router(okx_trading_service),
    prefix="/okx"
)
app.include_router(
    okx_market.get_router(okx_market_service),
    prefix="/okx"
)
app.include_router(
    okx_account.get_router(okx_account_service),
    prefix="/okx"
)

def main():
    """
    Main entry point for debugging
    """
    logger.info("Starting MT5 Trading API")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )

if __name__ == "__main__":
    main() 