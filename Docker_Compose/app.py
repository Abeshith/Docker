from flask import Flask
import redis

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def home():
    count = redis_client.incr('counter')  # Increment counter
    return f"Hello, Docker! You have visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
