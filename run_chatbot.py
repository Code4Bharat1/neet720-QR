from waitress import serve
from chat_bot import app
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=6002)