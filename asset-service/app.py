from flask import Flask
from databases.redis_setup import redis_client
from blueprints.asset_routes import asset_bp

app = Flask(__name__)

app.register_blueprint(asset_bp, url_prefix='/assets')


@app.route("/")
def health_check():
    return {"status": "OK", "redis": redis_client.ping()}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
