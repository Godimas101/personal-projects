import json
from wyze_sdk import Client

# New native Wyze account (not SSO)
email = 'thecanadianspace.contact@gmail.com'
password = 'WyzeP@ssword'
key_id = '623277ae-5569-42b5-8f52-eb963add4ea6'
api_key = 'SrVxxg1FZ79lHSEvfKOZ182sz8NHiku59vqbMZupvUvMmI0keu6qBjgBIp2k'

print("Starting diagnostics...")

try:
    client = Client(email=email, password=password, key_id=key_id, api_key=api_key)
    print("SUCCESS: Login successful!")

    # Also try to fetch scale data to confirm device sharing works
    print("\nFetching scale devices...")
    try:
        scales = client.scale.list()
        if scales:
            for scale in scales:
                print(f"  Scale found: {scale.nickname} (mac={scale.mac})")
        else:
            print("  No scales found — make sure the scale is shared to this account.")
    except AttributeError:
        # Try alternate attribute name
        devices = client.devices_list()
        scales = [d for d in devices if 'scale' in d.type.lower()]
        if scales:
            for s in scales:
                print(f"  Scale found: {s.nickname} (mac={s.mac})")
        else:
            print(f"  No scales found. All devices: {[d.type for d in devices]}")

except Exception as e:
    print(f"FAILED: An error occurred.")
    print(f"Error Message: {e}")

    if hasattr(e, 'response') and e.response is not None:
        print(f"Raw Server Response: {e.response.text}")
    else:
        print("No raw server response found. Check your network or credentials.")
grep -q '^WYZE_REFRESH_TOKEN=' /root/n8n-docker-caddy/.env && sed -i 's|^WYZE_REFRESH_TOKEN=.*|WYZE_REFRESH_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiN2Y4YmMwLWFhNWQtNDJmNi04MmY2LWZlZjFlMzFjN2M4NyJ9.eyJhdWQiOlsib2F1dGgyLXJlc291cmNlIiwibmF0aXZlX29hdXRoMl9yZXNvdXJjZSJdLCJ1c2VyX2NvdW50cnkiOiJVUyIsInVzZXJfaWQiOiJiMmE2NDhhNWEzYjM0MzRjOWU5YWFhODBjYzIyMDg4YiIsInVzZXJfbmFtZSI6InRoZWNhbmFkaWFuc3BhY2UuY29udGFjdEBnbWFpbC5jb20iLCJzY29wZSI6WyJuYXRpdmUiXSwiYXRpIjoic29ENGVlVUVxZWltRjVqV3hpSEVxLU5aTFZnIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnd5emUuY29tIiwiY3JlYXRlZF9hdCI6MTc3MjUwMzAwNywiZXhwIjoxNzc0OTIyMjA3LCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6ImdoQ3dtenA0ZWhieEJrYVhFeU9oOVJYRng0USIsImNsaWVudF9pZCI6IjhjMGUwM2NhLTA3NjAtNDI5ZS1hNTdiLTkxYzNkZGEwZjFiOCJ9.I1YcNmdj0rbyrQemU-66N9gqbbrGIHA32xbobxUIbmnbHIwn24QuxgiaSp6iHL1ZhQerfASa3N8Yl6urzTmgZJeQo8aCtIW-Wc08DdHYIAOBOcORYdPParbtm0_32L13pxAfYE-v9pAT9KcoSUvc-UBnxm0aTAzTu1IJRn2Qxt_epFZAgdTH8Ca94mpwjyJZxAcKmMYc4DMK2yfEZGaepvCx_NsixD6Q5_5G99I6FVwXJSLTsI8AoRLlfND-ceBhBYNXS0GsGnt0DVA_6Zwl63pBfPbX0DW0qAWio4GZFgTc0_-r55vOUqaw72w6jGhZgr3OXEckd69Oe6LUKN2VMw|' /root/n8n-docker-caddy/.env || echo 'WYZE_REFRESH_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiN2Y4YmMwLWFhNWQtNDJmNi04MmY2LWZlZjFlMzFjN2M4NyJ9.eyJhdWQiOlsib2F1dGgyLXJlc291cmNlIiwibmF0aXZlX29hdXRoMl9yZXNvdXJjZSJdLCJ1c2VyX2NvdW50cnkiOiJVUyIsInVzZXJfaWQiOiJiMmE2NDhhNWEzYjM0MzRjOWU5YWFhODBjYzIyMDg4YiIsInVzZXJfbmFtZSI6InRoZWNhbmFkaWFuc3BhY2UuY29udGFjdEBnbWFpbC5jb20iLCJzY29wZSI6WyJuYXRpdmUiXSwiYXRpIjoic29ENGVlVUVxZWltRjVqV3hpSEVxLU5aTFZnIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnd5emUuY29tIiwiY3JlYXRlZF9hdCI6MTc3MjUwMzAwNywiZXhwIjoxNzc0OTIyMjA3LCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6ImdoQ3dtenA0ZWhieEJrYVhFeU9oOVJYRng0USIsImNsaWVudF9pZCI6IjhjMGUwM2NhLTA3NjAtNDI5ZS1hNTdiLTkxYzNkZGEwZjFiOCJ9.I1YcNmdj0rbyrQemU-66N9gqbbrGIHA32xbobxUIbmnbHIwn24QuxgiaSp6iHL1ZhQerfASa3N8Yl6urzTmgZJeQo8aCtIW-Wc08DdHYIAOBOcORYdPParbtm0_32L13pxAfYE-v9pAT9KcoSUvc-UBnxm0aTAzTu1IJRn2Qxt_epFZAgdTH8Ca94mpwjyJZxAcKmMYc4DMK2yfEZGaepvCx_NsixD6Q5_5G99I6FVwXJSLTsI8AoRLlfND-ceBhBYNXS0GsGnt0DVA_6Zwl63pBfPbX0DW0qAWio4GZFgTc0_-r55vOUqaw72w6jGhZgr3OXEckd69Oe6LUKN2VMw' >> /root/n8n-docker-caddy/.env