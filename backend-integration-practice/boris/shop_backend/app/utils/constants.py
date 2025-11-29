class ResponseCode:
    # 1000–1999 系統層級／通用回應
    # 2000–2999 成功／一般操作
    # 3000–3999 驗證 & 授權（Authentication）
    # 4000–4999 用戶請求錯誤（Client Error）
    # 5000–5999 伺服器錯誤（Server Error）
    # 6000–6999 外部服務錯誤／第三方 API
    # 7000–7999 商業規則（Domain：Cart / Order / Inventory / Payment）

    SUCCESS = 2000  # Operation completed successfully

    UNAUTHORIZED = 3000  # Authentication failed or credentials invalid
    TOKEN_EXPIRED = 3001  # JWT token has expired
    PERMISSION_DENIED = 3002  # User lacks required permissions

    VALIDATION_ERROR = 4000  # Request data validation failed
    METHOD_NOT_ALLOWED = 4001  # HTTP method not supported
    NOT_FOUND = 4002  # Requested resource not found
    USER_NOT_FOUND = 4003  # Specific user not found
    USER_INACTIVE = 4004  # User account is inactive
    INVALID_TOKEN = 4005  # Invalid JWT token
    RESOURCE_NOT_AVAILABLE = 4006  # Resource not available
    RESOURCE_BUSY = 4007  # Resource is busy
    CONFLICT = 4008  # Data conflict or duplicate entry
    RATE_LIMITED = 4009
    FORBIDDEN = 4030  # Access forbidden
    UNKNOWN_ERROR = 4999  # Unhandled client error

    INTERNAL_ERROR = 5000  # Server internal error

    EXTERNAL_API_ERROR = 6000  # Third-party API error
    EXTERNAL_API_AUTHORIZATION_ERROR = 6001  # Third-party API auth error
    EXTERNAL_API_ACCESS_TOKEN_NOT_FOUND = 6002  # Third-party API token missing
    
    CART_EMPTY = 7000
    CART_ITEM_NOT_AVAILABLE = 7001
    INVENTORY_NOT_ENOUGH = 7100
    ORDER_ALREADY_PAID = 7200
    ORDER_NOT_PAYABLE = 7201
    PAYMENT_VERIFY_FAILED = 7300
    PAYMENT_GATEWAY_ERROR = 7301


class ResponseMessage:
    SUCCESS = 'success'  # General success message

    UNAUTHORIZED = 'unauthorized'  # Authentication failed
    TOKEN_EXPIRED = 'token expired'  # JWT token expired
    PERMISSION_DENIED = 'permission denied'  # Insufficient permissions
    INVALID_TOKEN = 'invalid token'
    FORBIDDEN = "forbidden"

    VALIDATION_ERROR = 'validation error'  # Input validation failed
    METHOD_NOT_ALLOWED = 'method not allowed'  # HTTP method not supported
    NOT_FOUND = 'resource not found'  # Resource does not exist
    USER_NOT_FOUND = 'user not found'  # User does not exist
    RESOURCE_NOT_AVAILABLE = 'resource not available'  # Resource not available
    RESOURCE_BUSY = 'resource busy'  # Resource is busy
    CONFLICT = 'data conflict'  # Data conflict or duplicate
    UNKNOWN_ERROR = 'request failed'  # Unhandled error
    RATE_LIMITED = "too many requests"

    INTERNAL_ERROR = 'internal error'  # Server internal error

    EXTERNAL_API_ERROR = 'external api error'  # Third-party API error
    EXTERNAL_API_AUTHORIZATION_ERROR = (
        'external api authorization error'  # Third-party API auth error
    )
    EXTERNAL_API_ACCESS_TOKEN_NOT_FOUND = (
        'external api access_token not found'  # Third-party API token missing
    )
    
    CART_EMPTY = "Cart is empty"
    CART_ITEM_NOT_AVAILABLE = "Cart contains unavailable item(s)"
    INVENTORY_NOT_ENOUGH = "Insufficient inventory"
    ORDER_ALREADY_PAID = "Order already paid"
    ORDER_NOT_PAYABLE = "Order is not payable"
    PAYMENT_VERIFY_FAILED = "Payment verification failed"
    PAYMENT_GATEWAY_ERROR = "Payment gateway error"