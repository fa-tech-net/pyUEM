class VendorLogin:

    def __init__(self, login=None, api_url=None, password=None, display_name=None, vendor=None):
        self._login = login
        self._api_url = api_url
        self._password = password
        self._display_name = display_name
        self._vendor = None


    def serialize(self):
        pass

