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
        Place a trading order with:
        - Instrument ID (e.g., BTC-USDT)
        - Trade mode (cash, cross, isolated)
        - Side (buy or sell)
        - Order type (market, limit, etc.)
        - Size
        - Optional price for limit orders
        - Optional position side for derivatives
        - Optional reduce only flag
        - Optional tag and client order ID
        
        Parameters:
        - trade_request: Trading order details
        
        Returns:
        - Order execution result with status and details
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
        Cancel an existing order by:
        - Instrument ID (required)
        - Order ID or Client Order ID (one required)
        
        Parameters:
        - cancel_request: Cancel order details
        
        Returns:
        - Cancellation result with status
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
        Modify an existing order:
        - Instrument ID (required)
        - Order ID or Client Order ID (one required)
        - New size or new price (at least one required)
        - Optional request ID
        
        Parameters:
        - modify_request: Modify order details
        
        Returns:
        - Modification result with status
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
        Get order history with optional filters:
        - inst_id: Filter by instrument ID
        - inst_type: Instrument type (SPOT, MARGIN, SWAP, FUTURES, OPTION)
        - state: Order state filter
        - limit: Number of results (max 100)
        
        Returns:
        - List of orders matching the criteria
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
        Get details of a specific order:
        - inst_id: Instrument ID (required)
        - ord_id: Order ID (optional if cl_ord_id provided)
        - cl_ord_id: Client order ID (optional if ord_id provided)
        
        Returns:
        - Order details if found
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