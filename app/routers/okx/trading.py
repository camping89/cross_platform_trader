from fastapi import APIRouter, HTTPException, Depends
from ...services.okx.okx_trading_service import OKXTradingService
from ...models.okx.trade import OKXTradeRequest, OKXTradeResponse, CancelOKXOrderRequest, ModifyOKXOrderRequest
from typing import List, Optional

def get_router(trading_service: OKXTradingService) -> APIRouter:
    router = APIRouter(prefix="/trading", tags=["OKX Trading"])

    @router.post("/place-order",
        response_model=OKXTradeResponse,
        summary="Place Order",
        description="Place a new trading order on OKX")
    async def place_order(trade_request: OKXTradeRequest):
        """
        Place a trading order (Market/Limit orders)
        
        This endpoint allows you to place spot and derivatives trading orders:
        - **market**: Execute immediately at best available price
        - **limit**: Execute when price reaches specified level
        - **post_only**: Only add liquidity (maker orders)
        - **fok**: Fill or kill - execute completely or cancel
        - **ioc**: Immediate or cancel - fill available quantity then cancel
        
        **Trading Modes:**
        - **cash**: Spot trading mode
        - **cross**: Cross margin mode
        - **isolated**: Isolated margin mode
        
        **Order Sides:**
        - **buy**: Purchase the base currency
        - **sell**: Sell the base currency
        
        **Examples:**
        - Market Buy: `{"inst_id": "BTC-USDT", "side": "buy", "ord_type": "market", "sz": "10", "td_mode": "cash"}`
        - Limit Sell: `{"inst_id": "ETH-USDT", "side": "sell", "ord_type": "limit", "px": "2000", "sz": "0.1", "td_mode": "cash"}`
        """
        try:
            result = await trading_service.place_order(trade_request)
            
            if not result.success:
                raise HTTPException(status_code=400, detail=result.s_msg)
                
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/cancel-order",
        response_model=OKXTradeResponse,
        summary="Cancel Order",
        description="Cancel an existing order")
    async def cancel_order(cancel_request: CancelOKXOrderRequest):
        """
        Cancel a pending order
        
        This endpoint cancels orders that are still pending (not filled/canceled):
        
        **Requirements:**
        - **inst_id**: The instrument ID (required)
        - **ord_id** OR **cl_ord_id**: Order ID or Client Order ID (one required)
        
        **Order States that can be canceled:**
        - **live**: Pending order waiting to be filled
        - **partially_filled**: Partially executed order
        
        **Cannot cancel orders with states:**
        - **filled**: Already completely executed
        - **canceled**: Already canceled
        - **rejected**: Order was rejected
        
        **Example:**
        `{"inst_id": "BTC-USDT", "ord_id": "12345"}`
        """
        try:
            result = await trading_service.cancel_order(cancel_request)
            
            if not result.success:
                raise HTTPException(status_code=400, detail=result.s_msg)
                
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/modify-order",
        response_model=OKXTradeResponse,
        summary="Modify Order",
        description="Modify an existing order")
    async def modify_order(modify_request: ModifyOKXOrderRequest):
        """
        Modify a pending order
        
        This endpoint modifies orders that are still pending (not filled/canceled):
        
        **Requirements:**
        - **inst_id**: The instrument ID (required)
        - **ord_id** OR **cl_ord_id**: Order ID or Client Order ID (one required)
        - **new_sz** OR **new_px**: New size or new price (at least one required)
        
        **Modifiable Parameters:**
        - **new_sz**: Change order quantity/size
        - **new_px**: Change order price (limit orders only)
        
        **Order States that can be modified:**
        - **live**: Pending order waiting to be filled
        - **partially_filled**: Partially executed order (can modify remaining quantity)
        
        **Examples:**
        - Change size: `{"inst_id": "BTC-USDT", "ord_id": "12345", "new_sz": "0.002"}`
        - Change price: `{"inst_id": "ETH-USDT", "ord_id": "67890", "new_px": "1800"}`
        """
        try:
            result = await trading_service.modify_order(modify_request)
            
            if not result.success:
                raise HTTPException(status_code=400, detail=result.s_msg)
                
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/orders",
        summary="Get Orders",
        description="Get order history")
    async def get_orders(
        inst_id: Optional[str] = None,
        inst_type: str = "SPOT",
        state: Optional[str] = None,
        limit: str = "100"
    ):
        """
        Get order history (last 7 days)
        
        This endpoint retrieves your recent order history with filtering options:
        
        **Query Parameters:**
        - **inst_id**: Filter by specific instrument (e.g., "BTC-USDT")
        - **inst_type**: Instrument type filter
          - **SPOT**: Spot trading pairs
          - **MARGIN**: Margin trading
          - **SWAP**: Perpetual swaps
          - **FUTURES**: Futures contracts
          - **OPTION**: Options contracts
        - **state**: Filter by order state
          - **filled**: Completely executed orders
          - **canceled**: Canceled orders
          - **live**: Pending orders
          - **partially_filled**: Partially executed orders
        - **limit**: Number of results (max 100, default 100)
        
        **Examples:**
        - All BTC orders: `?inst_id=BTC-USDT`
        - All filled orders: `?state=filled`
        - Recent 50 orders: `?limit=50`
        """
        try:
            orders = await trading_service.get_orders(
                inst_id=inst_id,
                ult_type=inst_type,
                state=state,
                limit=limit
            )
            
            return {
                "status": "success",
                "data": orders,
                "count": len(orders)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/order/{inst_id}",
        summary="Get Order Details",
        description="Get details of a specific order")
    async def get_order_details(
        inst_id: str,
        ord_id: Optional[str] = None,
        cl_ord_id: Optional[str] = None
    ):
        """
        Get detailed information of a specific order
        
        This endpoint retrieves comprehensive details of a single order:
        
        **Path Parameters:**
        - **inst_id**: The instrument ID (e.g., "BTC-USDT")
        
        **Query Parameters:**
        - **ord_id**: Platform-assigned order ID
        - **cl_ord_id**: Your custom client order ID
        
        **Note**: Either `ord_id` OR `cl_ord_id` must be provided
        
        **Response includes:**
        - Order status and execution details
        - Fill price and quantity information
        - Timestamps and fees
        - Position and margin details
        
        **Examples:**
        - By Order ID: `/order/BTC-USDT?ord_id=12345`
        - By Client ID: `/order/ETH-USDT?cl_ord_id=my_order_001`
        """
        if not ord_id and not cl_ord_id:
            raise HTTPException(
                status_code=400, 
                detail="Either ord_id or cl_ord_id must be provided"
            )
            
        try:
            order = await trading_service.get_order_details(
                inst_id=inst_id,
                ord_id=ord_id,
                cl_ord_id=cl_ord_id
            )
            
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
                
            return {
                "status": "success",
                "data": order
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router