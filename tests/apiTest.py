from Landray.api import Oauth
from Landray.api import Open

ob = Oauth()

print(ob.get_access_token())

ob = Open()
body = {
    "authModes": [],
    "returnUrl": "http://return_url_ente/test",
    "customTag": "test_customTag_by_yz",
    "notifyUrl": "http://notify_url_ente/test"
}
print(ob.create_enterprise_authentications(body))
