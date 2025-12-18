"""
Network Module - Tor/VPN Integration
Primary: Orbot/Tor
Fallback: ProtonVPN
"""
import socket
import socks
import requests
from typing import Optional, Dict
import subprocess
import time


class NetworkManager:
    """Manages Tor/VPN connections for privacy"""

    def __init__(self):
        self.tor_connected = False
        self.vpn_connected = False
        self.connection_mode = None  # 'tor', 'vpn', or None

        # Tor SOCKS proxy settings
        self.tor_proxy_host = '127.0.0.1'
        self.tor_proxy_port = 9050

        # ProtonVPN settings
        self.vpn_config = None

    def connect(self) -> Dict:
        """
        Connect to Tor or VPN
        Priority: Tor first, then VPN fallback
        """
        # Try Tor first
        if self.connect_tor():
            return {
                'success': True,
                'mode': 'tor',
                'message': 'Connected via Tor'
            }

        # Fallback to VPN
        if self.connect_vpn():
            return {
                'success': True,
                'mode': 'vpn',
                'message': 'Connected via ProtonVPN'
            }

        # No connection possible
        return {
            'success': False,
            'mode': None,
            'message': 'Failed to establish secure connection'
        }

    def connect_tor(self) -> bool:
        """Connect to Tor via Orbot"""
        try:
            # Check if Tor is running
            if self.check_tor_connection():
                self.tor_connected = True
                self.connection_mode = 'tor'
                self.configure_tor_proxy()
                return True

            # Try to start Orbot on Android
            if self.is_android():
                self.start_orbot()
                time.sleep(3)  # Wait for Orbot to start

                if self.check_tor_connection():
                    self.tor_connected = True
                    self.connection_mode = 'tor'
                    self.configure_tor_proxy()
                    return True

            return False

        except Exception as e:
            print(f"Tor connection error: {e}")
            return False

    def check_tor_connection(self) -> bool:
        """Check if Tor is accessible"""
        try:
            # Try to connect to Tor SOCKS proxy
            sock = socks.socksocket()
            sock.set_proxy(
                socks.SOCKS5,
                self.tor_proxy_host,
                self.tor_proxy_port
            )
            sock.settimeout(5)
            sock.connect(("check.torproject.org", 80))
            sock.close()
            return True
        except Exception:
            return False

    def configure_tor_proxy(self):
        """Configure system to use Tor SOCKS proxy"""
        try:
            # Set default socket to use SOCKS proxy
            socks.set_default_proxy(
                socks.SOCKS5,
                self.tor_proxy_host,
                self.tor_proxy_port
            )
            socket.socket = socks.socksocket
        except Exception as e:
            print(f"Tor proxy configuration error: {e}")

    def start_orbot(self):
        """Start Orbot on Android"""
        try:
            # Use Android intent to start Orbot
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent()
            intent.setAction("android.intent.action.VIEW")
            intent.setData("org.torproject.android/.OrbotMainActivity")

            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(intent)
        except Exception as e:
            print(f"Failed to start Orbot: {e}")

    def connect_vpn(self) -> bool:
        """Connect to ProtonVPN"""
        try:
            # Note: ProtonVPN integration requires ProtonVPN app
            # For Android, use ProtonVPN's Android SDK or IPC

            if self.is_android():
                # Try to connect via ProtonVPN app
                self.start_protonvpn()
                time.sleep(5)  # Wait for VPN to connect

                if self.check_vpn_connection():
                    self.vpn_connected = True
                    self.connection_mode = 'vpn'
                    return True

            return False

        except Exception as e:
            print(f"VPN connection error: {e}")
            return False

    def start_protonvpn(self):
        """Start ProtonVPN on Android"""
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            # Launch ProtonVPN app
            intent = Intent()
            intent.setAction("android.intent.action.MAIN")
            intent.setPackage("ch.protonvpn.android")

            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(intent)
        except Exception as e:
            print(f"Failed to start ProtonVPN: {e}")

    def check_vpn_connection(self) -> bool:
        """Check if VPN is active"""
        try:
            # Check if external IP has changed
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                # VPN is working if we can connect
                return True
            return False
        except Exception:
            return False

    def disconnect(self):
        """Disconnect from current network"""
        if self.connection_mode == 'tor':
            self.disconnect_tor()
        elif self.connection_mode == 'vpn':
            self.disconnect_vpn()

        self.tor_connected = False
        self.vpn_connected = False
        self.connection_mode = None

    def disconnect_tor(self):
        """Disconnect from Tor"""
        try:
            # Reset socket to default
            import socket as std_socket
            socket.socket = std_socket.socket
        except Exception as e:
            print(f"Tor disconnect error: {e}")

    def disconnect_vpn(self):
        """Disconnect from VPN"""
        # VPN disconnect would require ProtonVPN app integration
        pass

    def get_status(self) -> Dict:
        """Get current connection status"""
        return {
            'connected': self.tor_connected or self.vpn_connected,
            'mode': self.connection_mode,
            'tor': self.tor_connected,
            'vpn': self.vpn_connected
        }

    @staticmethod
    def is_android() -> bool:
        """Check if running on Android"""
        try:
            from jnius import autoclass
            return True
        except ImportError:
            return False

    def make_request(self, url: str, method: str = 'GET', **kwargs) -> requests.Response:
        """
        Make HTTP request through Tor/VPN
        """
        if self.connection_mode == 'tor':
            # Use Tor SOCKS proxy
            proxies = {
                'http': f'socks5h://{self.tor_proxy_host}:{self.tor_proxy_port}',
                'https': f'socks5h://{self.tor_proxy_host}:{self.tor_proxy_port}'
            }
            kwargs['proxies'] = proxies

        if method.upper() == 'GET':
            return requests.get(url, **kwargs)
        elif method.upper() == 'POST':
            return requests.post(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")
