import okx.Account as Account
import okx.Trade as Trade
import okx.PublicData as PublicData
import okx.MarketData as MarketData
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OKXBaseService:
    """
    Base service for OKX API connection management.
    Handles initialization, authentication, and cleanup of OKX API connection.
    
    Implements singleton pattern to ensure only one connection instance exists.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OKXBaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize base service with API clients.
        Skips if already initialized (singleton pattern).
        """
        if self._initialized:
            return
            
        self.api_key: Optional[str] = None
        self.secret_key: Optional[str] = None
        self.passphrase: Optional[str] = None
        self.is_sandbox: bool = False
        
        self.account_api: Optional[Account.AccountAPI] = None
        self.trade_api: Optional[Trade.TradeAPI] = None
        self.public_api: Optional[PublicData.PublicAPI] = None
        self.market_api: Optional[MarketData.MarketAPI] = None
        
    @property
    def initialized(self):
        """Check if OKX API connection is initialized"""
        return self._initialized
        
    async def connect(self, api_key: str, secret_key: str, passphrase: str, is_sandbox: bool = False) -> bool:
        """
        Connect to OKX API with credentials.
        
        Parameters:
        - api_key: OKX API key
        - secret_key: OKX secret key  
        - passphrase: OKX passphrase
        - is_sandbox: Use sandbox environment
        
        Returns:
        - bool: True if connection successful, False otherwise
        """
        try:
            self.api_key = api_key
            self.secret_key = secret_key
            self.passphrase = passphrase
            self.is_sandbox = is_sandbox
            
            # Initialize API clients
            self.account_api = Account.AccountAPI(
                api_key=api_key,
                api_secret_key=secret_key,
                passphrase=passphrase,
                use_server_time=False,
                flag='0' if not is_sandbox else '1'
            )
            
            self.trade_api = Trade.TradeAPI(
                api_key=api_key,
                api_secret_key=secret_key,
                passphrase=passphrase,
                use_server_time=False,
                flag='0' if not is_sandbox else '1'
            )
            
            self.public_api = PublicData.PublicAPI(
                api_key=api_key,
                api_secret_key=secret_key,
                passphrase=passphrase,
                use_server_time=False,
                flag='0' if not is_sandbox else '1'
            )
            
            self.market_api = MarketData.MarketAPI(
                api_key=api_key,
                api_secret_key=secret_key,
                passphrase=passphrase,
                use_server_time=False,
                flag='0' if not is_sandbox else '1'
            )
            
            # Test connection by getting account info
            result = self.account_api.get_account()
            if result['code'] != '0':
                logger.error(f"Failed to connect to OKX: {result['msg']}")
                return False
                
            self._initialized = True
            logger.info("OKX API connection established successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to OKX API: {str(e)}")
            return False

    async def ensure_connected(self) -> bool:
        """
        Verify OKX API connection is active.
        
        Returns:
        - bool: True if connected, False otherwise
        """
        if not self._initialized or not self.account_api:
            return False
            
        try:
            # Test connection with a simple API call
            result = self.account_api.get_account()
            return result['code'] == '0'
        except Exception:
            return False

    async def shutdown(self):
        """
        Shutdown OKX API connection and cleanup resources.
        Logs connection closure for monitoring.
        """
        if self._initialized:
            self.account_api = None
            self.trade_api = None
            self.public_api = None
            self.market_api = None
            self._initialized = False
            logger.info("OKX API connection closed")

    def __del__(self):
        """
        Cleanup method called when service is destroyed.
        Ensures OKX API connection is properly closed.
        """
        if self._initialized:
            self.account_api = None
            self.trade_api = None 
            self.public_api = None
            self.market_api = None
            self._initialized = False