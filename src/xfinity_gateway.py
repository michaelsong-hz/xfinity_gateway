from bs4 import BeautifulSoup as BS
import requests

TIMEOUT = 30
CONNECTED_DEVICES_PATH = '/connected_devices_computers.jst'
LOGIN_PATH = '/check.jst'

class XfinityGateway:

    def __init__(self, host, username, password):
        self.host = 'http://' + host
        self.username = username
        self.password = password

        self.last_results = {}
        self.session = requests.session()

    def login(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        self.session.post(self.host + LOGIN_PATH, data=data, timeout=TIMEOUT)

    def scan_devices(self):
        self._update_info()
        return self.last_results.keys()

    def get_device_name(self, device):
        return self.last_results.get(device)

    def _update_info(self):
        soup = self._get_devices_soup()
        try:
            headers = soup.find(id='online-private').table.find_all("tr")
        except AttributeError:
            self.login()
            soup = self._get_devices_soup()

        try:
            headers = soup.find(id='online-private').table.find_all("tr")
            for i, h in enumerate(headers):
                # Ignore first and last row, and blank rows
                if i == 0 or i == len(headers) - 1 or h == '\n':
                    continue
                self.last_results[h.find(id='macaddlocnew').parent.next_sibling] = \
                  h.find('a', {'class': 'label device-name private'}).text.strip('\t')
        except:
            raise(ValueError())

    def _get_devices_soup(self):
        html = self.session.get(self.host + CONNECTED_DEVICES_PATH, timeout=TIMEOUT).text
        return BS(html, 'html.parser')
