import os
from dotenv import load_dotenv
import redis

load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
email = os.getenv('TEST_EMAIL', 'minhxoandev@gmail.com')
key = f"otp:code:{email}"
print('Connecting to Redis', REDIS_HOST, REDIS_PORT)
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    val = r.get(key)
    print('Key:', key)
    print('Value:', val)
    if val:
        import json
        print('Parsed:', json.loads(val))
    else:
        print('No OTP key found in Redis')
except Exception as e:
    print('Redis error:', e)
    raise
