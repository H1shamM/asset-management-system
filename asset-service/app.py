from flask import Flask, jsonify

from blueprints.asset_routes import asset_bp
from databases.mongodb_setup import mongo_client
from databases.redis_setup import redis_client

app = Flask(__name__)

app.register_blueprint(asset_bp, url_prefix='/assets')


@app.route("/health")
def health_check():
    errors = []
    try:
        mongo_client.admin.command("ping")
    except Exception as e:
        errors.append(f"MongoDB Error: {str(e)}")

    try:
        redis_client.ping()
    except Exception as e:
        errors.append(f"Redis Error: {str(e)}")

    if errors:
        return jsonify({
            'status': 'errors',
            'message': str(errors)
        }), 500
    return jsonify({'status': 'OK'}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
