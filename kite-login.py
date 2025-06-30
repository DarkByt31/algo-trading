from kiteconnect import KiteConnect

API_KEY = "8kb1ag60chrc88ol"
API_SECRET = "26y0pw6mdwkurjn6e2z01hqtxti942zj"



kite = KiteConnect(api_key=API_KEY)
print(kite.login_url())
request_token = input("Enter request token: ")
data = kite.generate_session(request_token, api_secret=API_SECRET)
print(data["access_token"])
