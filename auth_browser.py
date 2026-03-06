"""
GKeepSync - Browser OAuth Authentication
Mở browser để user đăng nhập Google, trích xuất oauth_token,
đổi thành master token qua gpsoauth.exchange_token().
"""

import hashlib
import webbrowser
from typing import Callable, Optional

import gpsoauth
from utils.logger import logger

# Google EmbeddedSetup URL
EMBEDDED_SETUP_URL = "https://accounts.google.com/EmbeddedSetup"


def get_master_token_via_browser(
    email: str,
    on_success: Optional[Callable[[str], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
    on_waiting: Optional[Callable[[], None]] = None,
):
    """
    Mở browser để user đăng nhập Google, trích xuất oauth_token từ cookie,
    rồi dùng gpsoauth.exchange_token() để lấy master token.

    Vì không thể tự động trích xuất cookie từ browser bình thường,
    ta dùng cách thủ công: hướng dẫn user copy oauth_token từ DevTools.
    
    Args:
        email: Google email
        on_success: callback(master_token: str) khi thành công
        on_error: callback(error_msg: str) khi lỗi
        on_waiting: callback() khi đang chờ user
    """
    # Open the EmbeddedSetup page in system browser
    webbrowser.open(EMBEDDED_SETUP_URL)
    logger.info("Opened browser for Google EmbeddedSetup login.")
    if on_waiting:
        on_waiting()


def exchange_oauth_for_master(email: str, oauth_token: str) -> tuple[bool, str]:
    """
    Đổi oauth_token (lấy từ cookie sau khi đăng nhập EmbeddedSetup)
    thành master token qua gpsoauth.exchange_token().

    Args:
        email: Google email
        oauth_token: Token từ cookie 'oauth_token'

    Returns:
        (success, master_token_or_error_msg)
    """
    try:
        android_id = hashlib.md5(email.encode()).hexdigest()[:16]
        result = gpsoauth.exchange_token(email, oauth_token, android_id)

        if "Token" in result:
            master_token = result["Token"]
            logger.info("Successfully exchanged oauth_token for master token.")
            return True, master_token
        else:
            error = result.get("Error", str(result))
            logger.error("exchange_token failed: %s", error)
            return False, f"Google trả về lỗi: {error}"
    except Exception as e:
        logger.error("exchange_token exception: %s", e)
        return False, f"Lỗi: {e}"
