#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# --- MosDNS Admin URL ---
MOSDNS_ADMIN_URL = "http://127.0.0.1:9080"  # 修改为 9080

# --- 首页路由 ---
@app.route("/")
def index():
    return render_template("index.html")

# --- 示例 API: MosDNS 状态 ---
@app.route("/status")
def status():
    try:
        r = requests.get(f"{MOSDNS_ADMIN_URL}/metrics", timeout=3)
        if r.status_code == 200:
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error", "code": r.status_code})
    except requests.RequestException as e:
        return jsonify({"status": "error", "msg": str(e)})

# --- 示例 API: 获取配置信息 ---
@app.route("/config")
def config():
    # 这里可以扩展获取 MosDNS 配置的功能
    return jsonify({
        "mosdns_admin_url": MOSDNS_ADMIN_URL,
        "message": "这是一个示例配置接口"
    })

# --- 示例 API: 调用操作 ---
@app.route("/action", methods=["POST"])
def action():
    data = request.json or {}
    action_type = data.get("action", "")
    # 根据 action_type 可以执行不同操作
    return jsonify({"status": "ok", "action_received": action_type})

# --- 启动 ---
if __name__ == "__main__":
    # 从环境变量读取端口，systemd 会传入 FLASK_PORT
    port = int(os.environ.get("FLASK_PORT", 5001))
    # 监听 0.0.0.0，保证 systemd 启动和局域网访问
    app.run(host="0.0.0.0", port=port)
