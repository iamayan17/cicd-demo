from flask import Flask, jsonify
import socket
from datetime import datetime, timezone

app = Flask(__name__)

START_TIME = datetime.now(timezone.utc)


@app.route("/")
def home():
    hostname = socket.gethostname()

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NovaDeploy — CI/CD Platform</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: #070a12;
    --panel: rgba(15, 20, 35, .72);
    --border: rgba(255,255,255,.08);
    --text: #f5f7fb;
    --muted: #8993a7;
    --blue: #5b8cff;
    --purple: #9b6cff;
    --green: #2dd881;
}}

body {{
    min-height: 100vh;
    background:
        radial-gradient(circle at 10% 0%, rgba(91,140,255,.18), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(155,108,255,.16), transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: "DM Sans", sans-serif;
}}

body::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px);
    background-size: 40px 40px;
}}

.container {{
    width: min(1180px, 92%);
    margin: auto;
    position: relative;
    z-index: 1;
}}

nav {{
    height: 78px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
}}

.brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: "Space Grotesk";
    font-size: 19px;
    font-weight: 700;
}}

.logo {{
    width: 38px;
    height: 38px;
    border-radius: 11px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #5b8cff, #9b6cff);
    box-shadow: 0 8px 35px rgba(91,140,255,.35);
}}

.live {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 8px 13px;
    border-radius: 30px;
    background: rgba(45,216,129,.07);
    border: 1px solid rgba(45,216,129,.18);
    color: #72e9a8;
    font-size: 13px;
}}

.live-dot {{
    width: 7px;
    height: 7px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 12px var(--green);
    animation: pulse 1.8s infinite;
}}

@keyframes pulse {{
    50% {{ opacity: .35; transform: scale(.7); }}
}}

.hero {{
    padding: 88px 0 55px;
}}

.hero-grid {{
    display: grid;
    grid-template-columns: 1.35fr .65fr;
    gap: 60px;
    align-items: center;
}}

.eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #9db9ff;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 22px;
}}

h1 {{
    font-family: "Space Grotesk";
    font-size: clamp(48px, 7vw, 78px);
    line-height: .98;
    letter-spacing: -4px;
}}

.gradient {{
    background: linear-gradient(90deg, #fff 20%, #8bb0ff 55%, #b995ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.subtitle {{
    color: var(--muted);
    font-size: 17px;
    line-height: 1.75;
    max-width: 630px;
    margin-top: 24px;
}}

.buttons {{
    display: flex;
    gap: 12px;
    margin-top: 32px;
}}

.btn {{
    text-decoration: none;
    padding: 13px 19px;
    border-radius: 11px;
    font-size: 14px;
    font-weight: 600;
    transition: .25s;
}}

.primary {{
    color: white;
    background: linear-gradient(135deg, #4f7fff, #8b5cf6);
    box-shadow: 0 10px 35px rgba(79,127,255,.2);
}}

.secondary {{
    color: #c8d0df;
    background: rgba(255,255,255,.035);
    border: 1px solid var(--border);
}}

.btn:hover {{
    transform: translateY(-2px);
}}

.terminal {{
    background: rgba(8,12,23,.8);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 30px 90px rgba(0,0,0,.3);
}}

.terminal-head {{
    display: flex;
    gap: 7px;
    margin-bottom: 18px;
}}

.circle {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #42495a;
}}

.code {{
    font-family: monospace;
    font-size: 12px;
    line-height: 2;
    color: #8793aa;
}}

.green {{
    color: #50e89a;
}}

.blue {{
    color: #78a2ff;
}}

.purple {{
    color: #bd98ff;
}}

.metrics {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 50px;
}}

.card {{
    padding: 22px;
    border-radius: 17px;
    background: var(--panel);
    border: 1px solid var(--border);
    backdrop-filter: blur(15px);
}}

.label {{
    color: #707b91;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 12px;
}}

.value {{
    font-family: "Space Grotesk";
    font-size: 21px;
    font-weight: 600;
}}

.pipeline-title {{
    font-family: "Space Grotesk";
    font-size: 24px;
    margin-bottom: 18px;
}}

.pipeline {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 55px;
}}

.step {{
    position: relative;
    padding: 23px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
}}

.step-number {{
    width: 31px;
    height: 31px;
    display: grid;
    place-items: center;
    border-radius: 9px;
    background: rgba(91,140,255,.1);
    color: #82a7ff;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 16px;
}}

.step h3 {{
    font-family: "Space Grotesk";
    font-size: 15px;
    margin-bottom: 7px;
}}

.step p {{
    color: #707b91;
    font-size: 12px;
    line-height: 1.6;
}}

.check {{
    color: var(--green);
    float: right;
}}

footer {{
    border-top: 1px solid var(--border);
    padding: 28px 0;
    color: #596478;
    font-size: 12px;
    display: flex;
    justify-content: space-between;
}}

@media(max-width: 850px) {{
    .hero-grid {{
        grid-template-columns: 1fr;
    }}

    .metrics,
    .pipeline {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media(max-width: 550px) {{
    h1 {{
        font-size: 48px;
    }}

    .metrics,
    .pipeline {{
        grid-template-columns: 1fr;
    }}

    .hero {{
        padding-top: 60px;
    }}

    footer {{
        display: block;
        line-height: 2;
    }}
}}
</style>
</head>

<body>

<div class="container">

<nav>
    <div class="brand">
        <div class="logo">✦</div>
        NovaDeploy
    </div>

    <div class="live">
        <span class="live-dot"></span>
        All systems operational
    </div>
</nav>


<section class="hero">

<div class="hero-grid">

<div>

    <div class="eyebrow">
        ● PRODUCTION ENVIRONMENT
    </div>

    <h1>
        Deploy with
        <span class="gradient">confidence.</span>
    </h1>

    <p class="subtitle">
        A modern CI/CD deployment platform running on
        Docker and Amazon EC2. Every commit moves through
        an automated build, push and deployment pipeline.
    </p>

    <div class="buttons">
        <a href="/health" class="btn primary">
            Check Health →
        </a>

        <a href="/api/status" class="btn secondary">
            API Status
        </a>
    </div>

</div>


<div class="terminal">

<div class="terminal-head">
    <span class="circle"></span>
    <span class="circle"></span>
    <span class="circle"></span>
</div>

<div class="code">
<span class="blue">$</span> docker ps<br><br>

<span class="green">STATUS</span><br>

<span class="green">●</span>
container running<br>

<span class="purple">IMAGE</span><br>

cicd-demo:latest<br>

<span class="purple">HOST</span><br>

{hostname}<br><br>

<span class="blue">✓</span>
deployment successful
</div>

</div>

</div>

</section>


<div class="metrics">

<div class="card">
<div class="label">STATUS</div>
<div class="value green">● RUNNING</div>
</div>

<div class="card">
<div class="label">PLATFORM</div>
<div class="value">Docker</div>
</div>

<div class="card">
<div class="label">INFRASTRUCTURE</div>
<div class="value">Amazon EC2</div>
</div>

<div class="card">
<div class="label">UTC TIME</div>
<div class="value" id="clock">--:--:--</div>
</div>

</div>


<div class="pipeline-title">
Deployment pipeline
</div>

<div class="pipeline">

<div class="step">
<div class="step-number">01</div>
<h3>Git Push <span class="check">✓</span></h3>
<p>
Source code pushed to the main branch.
</p>
</div>

<div class="step">
<div class="step-number">02</div>
<h3>Docker Build <span class="check">✓</span></h3>
<p>
Application packaged into a container image.
</p>
</div>

<div class="step">
<div class="step-number">03</div>
<h3>Docker Hub <span class="check">✓</span></h3>
<p>
Versioned image pushed to the registry.
</p>
</div>

<div class="step">
<div class="step-number">04</div>
<h3>EC2 Deploy <span class="check">✓</span></h3>
<p>
EC2 pulls the latest image and starts it.
</p>
</div>

</div>


<footer>
<div>NovaDeploy • CI/CD Demonstration</div>
<div>Docker · GitHub Actions · AWS EC2</div>
</footer>

</div>


<script>
function updateClock() {{
    const now = new Date();

    document.getElementById("clock").innerText =
        now.toISOString()
           .replace("T", " ")
           .substring(0, 19);
}}

updateClock();
setInterval(updateClock, 1000);
</script>

</body>
</html>
"""


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "NovaDeploy",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "running",
        "service": "NovaDeploy",
        "environment": "production",
        "platform": "Docker",
        "infrastructure": "Amazon EC2",
        "hostname": socket.gethostname(),
        "started_at": START_TIME.isoformat()
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=False
    )
