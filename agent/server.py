"""FreeBee relay server -- the phone talks to THIS, and it runs the REAL Gemini
browser-use agent on the laptop, streaming live screenshots + the real reward
code back to the phone.

    pip install flask
    python agent/server.py           # -> http://<laptop-ip>:8000  (open on your phone)

Endpoints:
    GET  /                 -> the phone UI (index.html)
    POST /api/run          -> {url, code, email, reward, value} start a real agent run
    GET  /api/state        -> live status JSON (step text, frame seq, reward code)
    GET  /api/frame.png    -> latest screenshot from the real browser
"""
import base64
import json
import os
import re
import sys
import threading
import urllib.request

# freebee_agent sets the Win event-loop policy, loads agent/.env, and defines the LLM picker.
sys.path.insert(0, os.path.dirname(__file__))
from freebee_agent import resolve_llm, build_task  # noqa: E402

from flask import Flask, request, jsonify, send_file, send_from_directory, Response  # noqa: E402
import io  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
app = Flask(__name__, static_folder=None)

# shared live state (single active run -- fine for a demo)
STATE = {
    "running": False, "done": False, "error": None,
    "step_num": 0, "step_text": "Idle",
    "frame": None, "frame_seq": 0,
    "code": None, "final_text": None,
    "reward": None, "value": None, "email": None,
}
_lock = threading.Lock()


def _run_agent(url, code):
    """Runs in its own thread with its own asyncio loop."""
    import asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run_async(url, code))


async def _run_async(url, code):
    from browser_use import Agent, BrowserSession
    llm, provider, model = resolve_llm(None)

    async def on_step(*args):
        # browser-use calls this each step with (browser_state_summary, agent_output, step_number)
        try:
            step_no = args[2] if len(args) > 2 else STATE["step_num"] + 1
            STATE["step_num"] = step_no
            goal = ""
            if len(args) > 1 and args[1] is not None:
                goal = getattr(args[1], "next_goal", "") or ""
            STATE["step_text"] = goal or f"🐝 Working… step {step_no}"
        except Exception:
            pass

    import asyncio
    session = BrowserSession(headless=False)  # real visible Chrome on the laptop
    stop = asyncio.Event()

    async def frame_loop():
        # actively screenshot the real browser so the phone sees the live run
        while not stop.is_set():
            try:
                jpg = await session.take_screenshot(format="jpeg", quality=55)
                if jpg:
                    STATE["frame"] = jpg
                    STATE["frame_seq"] += 1
            except Exception:
                pass  # page not ready yet early on
            await asyncio.sleep(0.7)

    agent = Agent(task=build_task(url, code), llm=llm, browser_session=session,
                  register_new_step_callback=on_step)
    fl = asyncio.create_task(frame_loop())
    try:
        STATE["step_text"] = "🐝 Opening the survey…"
        result = await agent.run(max_steps=25)
        text = ""
        try:
            text = result.final_result() or ""
        except Exception:
            text = str(result)
        STATE["final_text"] = text
        m = re.search(r"\b([A-Z]{2}-?[A-Z0-9]{4,}|\d{4,})\b", text or "")
        STATE["code"] = m.group(1) if m else (text[:40] if text else "DONE")
        STATE["step_text"] = "✅ Reward claimed!"
    except Exception as e:
        STATE["error"] = str(e)
        STATE["step_text"] = "⚠️ " + str(e)[:80]
    finally:
        stop.set()
        try:
            await fl
        except Exception:
            pass
        STATE["running"] = False
        STATE["done"] = True


@app.post("/api/run")
def api_run():
    data = request.get_json(force=True, silent=True) or {}
    url = data.get("url")
    code = data.get("code", "")
    if not url:
        return jsonify({"ok": False, "error": "missing url"}), 400
    with _lock:
        if STATE["running"]:
            return jsonify({"ok": False, "error": "already running"}), 409
        STATE.update({"running": True, "done": False, "error": None,
                      "step_num": 0, "step_text": "🐝 Dispatching the bee…",
                      "frame": None, "frame_seq": 0, "code": None, "final_text": None,
                      "reward": data.get("reward"), "value": data.get("value"),
                      "email": data.get("email")})
    threading.Thread(target=_run_agent, args=(url, code), daemon=True).start()
    return jsonify({"ok": True})


@app.get("/api/state")
def api_state():
    return jsonify({k: v for k, v in STATE.items() if k != "frame"})


@app.get("/api/frame.jpg")
def api_frame():
    if not STATE["frame"]:
        return Response(status=204)
    return send_file(io.BytesIO(STATE["frame"]), mimetype="image/jpeg")


SCAN_PROMPT = (
    "You are reading a photo of a fast-food receipt. Find the customer-satisfaction "
    "survey code and details. Return ONLY strict JSON with these keys: "
    'merchant (string; if unclear use "McDonald\'s"), '
    'survey_url (for McDonald\'s use "https://www.mcdvoice.com"), '
    "survey_code (ALL digits only, no spaces or dashes), "
    "reward_description (string or null), reward_value_usd (number or null). "
    "The McDonald's code is 26 digits, usually printed after 'Survey Code:' in groups "
    "like 5-5-5-5-5-1. Read every digit carefully. If a field is unknown use null."
)


@app.post("/api/scan")
def api_scan():
    f = request.files.get("photo")
    if not f:
        return jsonify({"ok": False, "error": "no photo uploaded"}), 400
    img_b64 = base64.b64encode(f.read()).decode()
    key = os.environ.get("GOOGLE_API_KEY", "")
    payload = {"contents": [{"parts": [
        {"text": SCAN_PROMPT},
        {"inline_data": {"mime_type": f.mimetype or "image/jpeg", "data": img_b64}},
    ]}]}
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-2.5-flash:generateContent?key=" + key)
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            resp = json.load(r)
        text = resp["candidates"][0]["content"]["parts"][0]["text"]
        m = re.search(r"\{.*\}", text, re.S)
        data = json.loads(m.group(0)) if m else {}
        data["survey_code"] = re.sub(r"\D", "", str(data.get("survey_code") or ""))
        data["survey_url"] = data.get("survey_url") or "https://www.mcdvoice.com"
        data["merchant"] = data.get("merchant") or "McDonald's"
        return jsonify({"ok": True, **data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)[:200]}), 500


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:path>")
def static_files(path):
    return send_from_directory(ROOT, path)


if __name__ == "__main__":
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "localhost"
    print("=" * 56)
    print("  🐝  FreeBee is LIVE")
    print(f"  On your PHONE (same WiFi or your phone's hotspot) open:")
    print(f"       http://{ip}:8000")
    print("=" * 56)
    app.run(host="0.0.0.0", port=8000, threaded=True)
