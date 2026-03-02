from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

EMAIL = "aeneas.carpenter@gmail.com"
PASSWORD = "WyzeP@ssword"
KEY_ID = "22927812-6a45-4148-8564-ea86679df596"
API_KEY = "3vQpzlbdi9QJUyK5HxiM2gn9Qv2Hw4CXmcIQxNqZ6hPHm6PqwlZozhKTnL7P"

try:
    client = Client()
    response = client.login(
        email=EMAIL,
        password=PASSWORD,
        key_id=KEY_ID,
        api_key=API_KEY
    )
    print("Login successful!")
    # WyzeResponse is dict-like
    data = response.data if hasattr(response, 'data') else response
    print("\n--- RAW RESPONSE ---")
    print(dict(data))
    access_token = data.get('access_token') or data.get('accessToken', '')
    refresh_token = data.get('refresh_token') or data.get('refreshToken', '')
    print("\n--- TOKENS ---")
    print("ACCESS_TOKEN=" + access_token)
    print("REFRESH_TOKEN=" + refresh_token)

except WyzeApiError as e:
    print("API Error:", e)
except Exception as e:
    print("Other error:", e)
