import gpsoauth
import requests
import gkeepapi
from core.config_manager import ConfigManager

class AuthManager:
    def __init__(self):
        self.keep = gkeepapi.Keep()
        self.config = ConfigManager.load_config()
        self.email = self.config.get("email", "")
        self.master_token = self.config.get("master_token", "")

    def is_logged_in(self):
        """Check if we have a valid token saved and try to authenticate."""
        if not self.email or not self.master_token:
            return False
            
        try:
            # Login via gkeepapi using master token (bypass password)
            self.keep.resume(self.email, self.master_token)
            return True
        except gkeepapi.exception.LoginException:
            return False
        except Exception as e:
            print(f"Auth error: {e}")
            return False

    def login_with_master_token(self, email, master_token):
        """Standard manual login using a master token."""
        try:
            self.keep.resume(email, master_token)
            
            # Save to config if successful
            self.email = email
            self.master_token = master_token
            ConfigManager.update_key("email", email)
            ConfigManager.update_key("master_token", master_token)
            
            return True, "Login successful"
        except gkeepapi.exception.LoginException:
            return False, "Invalid Master Token or Email"
        except Exception as e:
            return False, f"Error: {e}"

    def exchange_oauth_for_master(self, oauth_token):
        """Exchange the Chrome Extension oauth_token for a long-lived master token."""
        try:
            # The client needs an email to perform the exchange with gpsoauth,
            # but sometimes the Chrome API doesn't allow the extension to scrape the email.
            # In those cases, Google Identity endpoints still allow fetching the user info
            # if we pass the pure oauth_token.
            
            email = self._fetch_email_from_token(oauth_token)
            if not email:
                return False, "Could not extract email from token"
                
            # Perform the OAuth exchange
            response = gpsoauth.exchange_token(email, oauth_token, gpsoauth.get_mac_id())
            
            if 'Token' not in response:
                return False, "Google rejected the token exchange"
                
            master_token = response['Token']
            
            # Try logging in with the new master token
            return self.login_with_master_token(email, master_token)
            
        except Exception as e:
            return False, f"Exchange error: {e}"

    def _fetch_email_from_token(self, oauth_token):
        """Use the Google API to retrieve the user's email given a valid OAuth token."""
        try:
            headers = {"Authorization": f"Bearer {oauth_token}"}
            resp = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("email")
            return None
        except:
            return None
            
    def logout(self):
        """Clear local credentials."""
        self.email = ""
        self.master_token = ""
        ConfigManager.update_key("email", "")
        ConfigManager.update_key("master_token", "")
        # Note: gkeepapi doesn't have an explicit 'logout' method since it uses stateless tokens
        self.keep = gkeepapi.Keep() 
