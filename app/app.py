from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "blue")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

@app.route("/")
def home():
    return jsonify({
        "message": "Secure GitOps DevSecOps Platform",
        "status": "running",
        "version": APP_VERSION,
        "environment": ENVIRONMENT
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200

@app.route("/version")
def version():
    return jsonify({
        "version": APP_VERSION
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
