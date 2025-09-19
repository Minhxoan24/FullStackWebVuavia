// Định nghĩa các đường dẫn (paths) của ứng dụng
const PATHS = {
    // Trang chính
    HOME: "/",

    // Các đường dẫn liên quan đến tài khoản
    ACC_VIET: "/mua-via-viet",
    ACC_NGOAI: "/mua-via-ngoai",
    ACC_XMDT: "/mua-via-xmdt",
    ACC_902: "/mua-via-902",
    ZALO: "/mua-via-zalo",
    CLONE: "/mua-via-clone",
    OUTLOOK: "/mua-via-outlook",
    SWITTER: "/mua-via-switter",
    THU_THUAT: "/mua-via-thuthuat",
    ACC_SPAM: "/mua-via-spam",

    // Đăng ký và đăng nhập
    REGISTER: "/register",
    LOGIN: "/login",

    // Các mẹo và hướng dẫn
    TIPS: "/tips",
    TIP_USE_FACE: "/tip-use-face",
    TIP_CREATE_ADS: "/tip-create-ads",
    PROXY_TUTORIAL: "/proxy-tutorial",

    // Thêm paths cho user pages
    PAGE_ACCOUNT: "/account",
    MY_ACCOUNT: "/my-account",
    MY_ORDERS: "/my-orders",
    TRANSACTION_HISTORY: "/transaction-history",
    RECHARGE: "/recharge",
    OVERVIEW: "/overview",
    ORDER_DETAIL: "/order-detail/:orderId",
    MY_VOUCHER: "/my-voucher",
    DETAIL_TYPE_PRODUCT: "/detail-type-product/:id"
};

export default PATHS;