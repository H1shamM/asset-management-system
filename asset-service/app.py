from flask import Flask

from databases.mongodb_setup import mongo_client
from databases.redis_setup import redis_client
from blueprints.asset_routes import asset_bp

app = Flask(__name__)

app.register_blueprint(asset_bp, url_prefix='/assets')

@app.route("/health")
def health_check():
    try:
        # Verify MongoDB connection
        mongo_client.admin.command("ping")
        # Verify Redis connection
        redis_client.ping()
        return {"status": "OK"}, 200
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
