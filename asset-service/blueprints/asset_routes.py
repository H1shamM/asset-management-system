import json
import os
import uuid
from datetime import datetime

import requests
from flask import Blueprint, jsonify, request, url_for

from databases.redis_setup import redis_client
from databases.mongodb_setup import get_db

asset_bp = Blueprint('asset', __name__)
db = get_db()
SECURITY_SERVICE_URL = os.getenv("SECURITY_SERVICE_URL", "http://security-service:8080")  # Docker service name


# --------------------------
# CORE FEATURE 1: Get asset with Caching
# --------------------------
@asset_bp.route("/<string:asset_id>", methods=["GET"])
def get_asset(asset_id):
    # Check Redis cache first
    cached_asset = redis_client.get(asset_id)
    if cached_asset:
        return jsonify(json.loads(cached_asset))

    # MongoDB fallback
    asset = db.assets.find_one({"id": asset_id}, {"_id": 0})
    if not asset:
        return jsonify({"error": "asset not found"}), 404

    # Security Scan
    try:
        scan_response = requests.get(
            f"http://security-service:8080/security/scan/{asset_id}",
            timeout=2
        )
        if scan_response.ok:
            scan = scan_response.json()
            asset["security_scan"] = scan
            asset["vulnerabilities"] = scan["findings"]
            asset["scan_summary"] = scan["summary"]
    except requests.exceptions.RequestException:
        asset["security_scan"] = {"error": "Scan unavailable"}

    # Cache asset for 1 hour
    redis_client.setex(asset_id, 3600, json.dumps(asset))
    return jsonify(asset), 200


# --------------------------
# CORE FEATURE 2: List assets with Inventory
# --------------------------
@asset_bp.route("/", methods=["GET"])
def get_assets():
    # Attempt cache hit
    cache_key = "all_assets"
    if cached := redis_client.get(cache_key):
        return jsonify(json.loads(cached))

    # Fetch from DB
    assets = list(db.assets.find({}, {"_id": 0}))

    # Enrich with Security Scan
    for asset in assets:

        asset_id = asset.get("id")
        if not asset_id:
            asset["security_scan"] = {"error": "no asset id"}
            continue

        try:
            resp = requests.get(
                f"http://security-service:8080/security/scan/{asset_id}",
                timeout=2
            )
            if resp.ok:
                scan = resp.json()
                asset["security_scan"] = scan
                asset["vulnerabilities"] = scan["findings"]
                asset["scan_summary"] = scan["summary"]
            else:
                asset["security_scan"] = {"error": "scan failed"}
        except requests.exceptions.RequestException:
            asset["security_scan"] = {"error": "Scan unavailable"}

    # Cache enriched data
    redis_client.setex(cache_key, 300, json.dumps(assets))  # 5-minute cache
    return jsonify(assets)


# --------------------------
#  Create asset
# --------------------------
@asset_bp.route("/", methods=["POST"])
def add_asset():
    REQUIRED_FIELDS = {"id", "type", "owner", "status", "tags"}
    payload = request.get_json()
    if not payload or not REQUIRED_FIELDS.issubset(request.json):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(payload["tags"], list) or not all(isinstance(t, str) for t in payload["tags"]):
        return jsonify({"error": "tags must be a list of strings"}), 400

    new_asset = {
        "id": payload["id"],  # UUID generation
        **request.json,
        "created_at": datetime.utcnow().isoformat()
    }


    #check duplication
    if db.assets.find_one({"id": new_asset["id"]}):
        return jsonify({"error": "Asset already exists"}), 409


    # DB insert
    try:
        result = db.assets.insert_one(new_asset)
    except Exception as e:
        return jsonify({"error": "Database insert failed"}), 500

    new_asset["_id"] = str(result.inserted_id)


    # Cache invalidation
    redis_client.delete("all_assets")  # Invalidate asset list cache

    resp = jsonify(new_asset)
    resp.status_code = 201
    resp.headers["Location"] = url_for("asset.get_asset",
                                       asset_id=new_asset["id"],
                                       _external=True)

    return resp