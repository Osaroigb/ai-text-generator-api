from app import app
from app.database import init_db
from app.config import Config, logging

if __name__ == "__main__":
    init_db()
    logging.info("Database connected successfully!")

    app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=True)