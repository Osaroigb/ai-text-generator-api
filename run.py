from app import app
from app.config import Config
from app.database import init_db

if __name__ == "__main__":
    init_db()
    app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=True)