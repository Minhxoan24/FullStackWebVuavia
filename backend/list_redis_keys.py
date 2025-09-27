import os
from dotenv import load_dotenv
import redis

load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
print('Connecting to Redis', REDIS_HOST, REDIS_PORT)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
try:
    keys = r.keys('otp:*')
    print('OTP keys:', keys)
    for k in keys:
        print(k, r.get(k))
except Exception as e:
    print('Error listing keys:', e)
    raise
