import requests
from typing import Optional


# Bad annonymous function
def greet(name: str):
    print(f"Hello, {name}!")

# # Output: Hello, Alice!
greet("Alice")

# Good with return type
def greet(name: str) -> str:
    if not name:
        raise ValueError("Name cannot be empty")

    return f"Hello, {name}!"

# # Output: Hello, Alice!
print(greet("Alice"))  

def find_user(user_id: int) -> Optional[dict]:
    # Simulating a user lookup
    users = {
        1: {"name": "Alice", "age": 30},
        2: {"name": "Bob", "age": 25}
    }
    return users.get(user_id)

# # Example existing user
print(find_user(2))

# # Example non-existing user
print(find_user(3))

# Bad way to handle exceptions
try:
    result = greet(None)
except:
    pass 

# Good way to handle exceptions
try:
    result = greet(None)
except ValueError as e:
    print(f"ค่าที่ป้อนไม่ถูกต้อง: {e}")
except KeyError as e:
    print(f"ไม่พบ key: {e}")

def call_api(url: str, timeout: float = 10.0) -> dict:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("คำขอหมดเวลา (timeout) ลองใหม่อีกครั้ง")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"เรียก API ไม่สำเร็จ: {e}")
        return {}

url = "https://jsonplaceholder.typicode.com/users/1"

response = call_api(url=url, timeout=5.0)

print(response)

def extract_username(response: dict) -> Optional[str]:
    # TODO: ดึง key "username" ออกจาก response แบบปลอดภัย (เผื่อไม่มี key นี้)
    return response.get("username", None)

print(extract_username(response))

def is_valid_url(url: str) -> bool:
    # TODO: ตรวจสอบว่า url ขึ้นต้นด้วย http:// หรือ https:// หรือไม่
    return url.startswith("http://") or url.startswith("https://")

print(is_valid_url("https://example.com"))  # True
print(is_valid_url("http://example.com"))   # True
print(is_valid_url("ftp://example.com"))    # False