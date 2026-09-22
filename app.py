from flask import Flask, render_template_string, jsonify
import random

app = Flask(__name__)

# ============================================================
# API DATA
# ============================================================

@app.route("/api/stats")
def stats():
    return jsonify({
        "revenue": random.randint(48000, 65000),
        "users": random.randint(8500, 12000),
        "orders": random.randint(1200, 1900),
        "conversion": round(random.uniform(7.5, 10.5), 1)
    })


@app.route("/api/analytics")
def analytics():
    return jsonify({
        "months": [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ],
        "revenue": [
            12000, 18000, 15000, 24000,
            29000, 36000, 41000, 52000,
            58000, 63000, 71000, 85000
        ],
        "users": [
            1200, 1900, 2700, 3500,
            4900, 6200, 7800, 9500,
            10500, 11800, 13200, 15000
        ],
        "orders": [
            320, 450, 520, 680,
            790, 920, 1100, 1250,
            1380, 1490, 1600, 1780
        ]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "NOVA",
        "service": "Flask",
        "port": 80
    })


# ============================================================
# COMPLETE FRONTEND
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>NOVA | 3D Analytics</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    background: #050509;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    overflow-x: hidden;
}

/* ============================================================
   3D BACKGROUND
============================================================ */

#three-bg {
    position: fixed;
    inset: 0;
    z-index: -10;
}

#three-bg canvas {
    display: block;
}

.glow {
    position: fixed;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    filter: blur(140px);
    opacity: .12;
    pointer-events: none;
    z-index: -5;
}

.glow1 {
    background: #7c3aed;
    top: 5%;
    left: 0;
}

.glow2 {
    background: #2563eb;
    right: 0;
    bottom: 5%;
}


/* ============================================================
   NAVBAR
============================================================ */

nav {
    position: fixed;
    top: 18px;
    left: 50%;
    transform: translateX(-50%);

    width: min(1200px, 94%);
    height: 64px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 22px;

    border: 1px solid rgba(255,255,255,.12);
    border-radius: 40px;

    background: rgba(5,5,12,.65);
    backdrop-filter: blur(25px);

    z-index: 1000;
}

.logo {
    font-size: 23px;
    font-weight: 900;
}

.logo span {
    color: #8b5cf6;
}

.nav-links {
    display: flex;
    gap: 28px;
    list-style: none;
}

.nav-links a {
    color: #888;
    text-decoration: none;
    font-size: 14px;
    transition: .3s;
}

.nav-links a:hover {
    color: white;
}

.nav-btn {
    border: none;
    border-radius: 30px;
    padding: 11px 20px;
    background: white;
    color: black;
    font-weight: bold;
    cursor: pointer;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    min-height: 100vh;

    display: flex;
    align-items: center;
    justify-content: center;

    text-align: center;
    padding: 120px 20px 60px;
}

.hero-content {
    max-width: 950px;
}

.badge {
    display: inline-block;

    padding: 9px 16px;

    border-radius: 30px;

    border: 1px solid rgba(139,92,246,.35);

    background: rgba(139,92,246,.1);

    color: #c4b5fd;

    font-size: 13px;

    margin-bottom: 28px;
}

.hero h1 {
    font-size: clamp(60px, 10vw, 125px);

    line-height: .86;

    letter-spacing: -8px;

    background: linear-gradient(
        120deg,
        #fff,
        #a78bfa,
        #60a5fa,
        #fff
    );

    background-size: 300%;

    -webkit-background-clip: text;

    color: transparent;

    animation: gradient 6s linear infinite;
}

@keyframes gradient {
    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }
}

.hero p {
    max-width: 650px;

    margin: 35px auto;

    color: #888;

    font-size: 18px;

    line-height: 1.7;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 15px;
}

.btn {
    padding: 15px 25px;

    border-radius: 35px;

    text-decoration: none;

    font-weight: bold;

    transition: .3s;
}

.btn:hover {
    transform: translateY(-4px);
}

.primary {
    background: white;
    color: black;
}

.secondary {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.15);
    color: white;
}


/* ============================================================
   MAIN
============================================================ */

main {
    width: min(1250px, 92%);
    margin: auto;
}

section {
    padding: 100px 0;
    scroll-margin-top: 100px;
}

.heading {
    margin-bottom: 45px;
}

.heading h2 {
    font-size: clamp(40px, 6vw, 70px);
    letter-spacing: -4px;
}

.heading p {
    margin-top: 15px;
    color: #777;
}


/* ============================================================
   STAT CARDS
============================================================ */

.stats {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 18px;
}

.stat {
    padding: 25px;

    min-height: 165px;

    border-radius: 24px;

    border: 1px solid rgba(255,255,255,.09);

    background: rgba(255,255,255,.04);

    backdrop-filter: blur(20px);

    transition: .3s;
}

.stat:hover {
    transform: translateY(-7px);

    border-color: rgba(139,92,246,.5);
}

.stat-label {
    color: #777;
    font-size: 14px;
}

.stat-value {
    font-size: 34px;
    font-weight: 800;
    margin-top: 25px;
}

.change {
    color: #4ade80;
    margin-top: 7px;
    font-size: 13px;
}


/* ============================================================
   CHARTS
============================================================ */

.charts {
    margin-top: 25px;

    display: grid;

    grid-template-columns: 1.5fr 1fr;

    gap: 22px;
}

.chart-card {
    min-height: 390px;

    padding: 28px;

    border-radius: 26px;

    border: 1px solid rgba(255,255,255,.09);

    background: rgba(255,255,255,.04);

    backdrop-filter: blur(20px);
}

.chart-card h3 {
    margin-bottom: 25px;
}

.chart-container {
    position: relative;
    height: 290px;
}


/* ============================================================
   FEATURE CARDS
============================================================ */

.features {
    display: grid;

    grid-template-columns: repeat(3,1fr);

    gap: 22px;
}

.feature {
    padding: 35px;

    min-height: 260px;

    border-radius: 27px;

    border: 1px solid rgba(255,255,255,.09);

    background: rgba(255,255,255,.04);

    transition: .35s;
}

.feature:hover {
    transform: translateY(-10px);
    border-color: rgba(139,92,246,.5);
}

.icon {
    width: 58px;
    height: 58px;

    display: grid;
    place-items: center;

    border-radius: 18px;

    background: linear-gradient(
        135deg,
        #7c3aed,
        #2563eb
    );

    font-size: 25px;

    margin-bottom: 25px;
}

.feature h3 {
    font-size: 23px;
    margin-bottom: 12px;
}

.feature p {
    color: #777;
    line-height: 1.7;
}


/* ============================================================
   PROJECTS
============================================================ */

.projects {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 22px;
}

.project {
    border-radius: 25px;
    overflow: hidden;

    border: 1px solid rgba(255,255,255,.09);

    background: rgba(255,255,255,.04);

    transition: .35s;
}

.project:hover {
    transform: translateY(-8px);
}

.project-image {
    height: 190px;

    display: grid;
    place-items: center;

    font-size: 60px;

    background:
        radial-gradient(
            circle,
            #4c1d95,
            #050509
        );
}

.project-info {
    padding: 25px;
}

.project-info p {
    color: #777;
    line-height: 1.6;
    margin-top: 10px;
}

.tag {
    display: inline-block;

    margin-top: 18px;

    padding: 6px 12px;

    border-radius: 20px;

    background: rgba(139,92,246,.12);

    color: #a78bfa;

    font-size: 12px;
}


/* ============================================================
   CTA
============================================================ */

.cta {
    text-align: center;
}

.cta-box {
    padding: 90px 25px;

    border-radius: 35px;

    border: 1px solid rgba(255,255,255,.1);

    background:
        radial-gradient(
            circle,
            rgba(124,58,237,.2),
            rgba(255,255,255,.03)
        );
}

.cta h2 {
    font-size: clamp(45px,7vw,80px);
    letter-spacing: -5px;
}

.cta p {
    color: #777;
    margin: 20px auto 35px;
}


/* ============================================================
   FOOTER
============================================================ */

footer {
    padding: 35px;
    text-align: center;
    color: #444;

    border-top: 1px solid rgba(255,255,255,.06);
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media(max-width:900px) {

    .nav-links {
        display: none;
    }

    .stats {
        grid-template-columns: repeat(2,1fr);
    }

    .charts {
        grid-template-columns: 1fr;
    }

    .features,
    .projects {
        grid-template-columns: 1fr;
    }
}

@media(max-width:550px) {

    .stats {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        letter-spacing: -5px;
    }

    .buttons {
        flex-direction: column;
    }
}

</style>

</head>


<body>


<div id="three-bg"></div>

<div class="glow glow1"></div>
<div class="glow glow2"></div>


<!-- NAVBAR -->

<nav>

    <div class="logo">
        NOVA<span>.</span>
    </div>

    <ul class="nav-links">

        <li>
            <a href="#home">Home</a>
        </li>

        <li>
            <a href="#dashboard">Dashboard</a>
        </li>

        <li>
            <a href="#analytics">Analytics</a>
        </li>

        <li>
            <a href="#projects">Projects</a>
        </li>

        <li>
            <a href="#features">Features</a>
        </li>

    </ul>

    <button
        class="nav-btn"
        onclick="goContact()">

        Get Started

    </button>

</nav>


<!-- HERO -->

<section
    class="hero"
    id="home">

    <div class="hero-content">

        <div class="badge">
            ✦ NEXT GENERATION PLATFORM
        </div>

        <h1>
            Build Beyond<br>
            Reality.
        </h1>

        <p>
            A futuristic analytics platform combining
            interactive 3D graphics, real-time data,
            animated charts and modern UI.
        </p>

        <div class="buttons">

            <a
                href="#dashboard"
                class="btn primary">

                Explore Dashboard

            </a>

            <a
                href="#analytics"
                class="btn secondary">

                View Analytics →

            </a>

        </div>

    </div>

</section>


<main>


<!-- DASHBOARD -->

<section id="dashboard">

    <div class="heading">

        <h2>Dashboard.</h2>

        <p>
            Live metrics from the Flask backend.
        </p>

    </div>


    <div class="stats">


        <div class="stat">

            <div class="stat-label">
                Revenue
            </div>

            <div
                class="stat-value"
                id="revenue">

                $52,430

            </div>

            <div class="change">
                ↑ 18.4%
            </div>

        </div>


        <div class="stat">

            <div class="stat-label">
                Users
            </div>

            <div
                class="stat-value"
                id="users">

                9,842

            </div>

            <div class="change">
                ↑ 24.2%
            </div>

        </div>


        <div class="stat">

            <div class="stat-label">
                Orders
            </div>

            <div
                class="stat-value"
                id="orders">

                1,524

            </div>

            <div class="change">
                ↑ 12.7%
            </div>

        </div>


        <div class="stat">

            <div class="stat-label">
                Conversion
            </div>

            <div
                class="stat-value"
                id="conversion">

                8.7%

            </div>

            <div class="change">
                ↑ 2.1%
            </div>

        </div>


    </div>


    <!-- CHARTS -->

    <div class="charts">


        <div class="chart-card">

            <h3>Revenue Overview</h3>

            <div class="chart-container">

                <canvas id="revenueChart"></canvas>

            </div>

        </div>


        <div class="chart-card">

            <h3>User Growth</h3>

            <div class="chart-container">

                <canvas id="usersChart"></canvas>

            </div>

        </div>


        <div class="chart-card">

            <h3>Orders</h3>

            <div class="chart-container">

                <canvas id="ordersChart"></canvas>

            </div>

        </div>


        <div class="chart-card">

            <h3>Traffic Sources</h3>

            <div class="chart-container">

                <canvas id="trafficChart"></canvas>

            </div>

        </div>


    </div>

</section>


<!-- ANALYTICS -->

<section id="analytics">

    <div class="heading">

        <h2>Analytics.</h2>

        <p>
            Visualize your application's performance.
        </p>

    </div>


    <div class="features">


        <div class="feature">

            <div class="icon">⚡</div>

            <h3>
                Real-Time Data
            </h3>

            <p>
                Dashboard statistics are retrieved
                from Flask API endpoints.
            </p>

        </div>


        <div class="feature">

            <div class="icon">📊</div>

            <h3>
                Animated Charts
            </h3>

            <p>
                Interactive line, bar and doughnut
                charts with smooth animations.
            </p>

        </div>


        <div class="feature">

            <div class="icon">🚀</div>

            <h3>
                Cloud Ready
            </h3>

            <p>
                Designed to run inside your Docker
                container on AWS EC2.
            </p>

        </div>


    </div>

</section>


<!-- PROJECTS -->

<section id="projects">

    <div class="heading">

        <h2>Projects.</h2>

        <p>
            A modern application ecosystem.
        </p>

    </div>


    <div class="projects">


        <div class="project">

            <div class="project-image">
                ◈
            </div>

            <div class="project-info">

                <h3>
                    Analytics Engine
                </h3>

                <p>
                    Real-time data visualization
                    and performance monitoring.
                </p>

                <span class="tag">
                    Analytics
                </span>

            </div>

        </div>


        <div class="project">

            <div class="project-image">
                ☁
            </div>

            <div class="project-info">

                <h3>
                    Cloud Platform
                </h3>

                <p>
                    Scalable infrastructure designed
                    for modern applications.
                </p>

                <span class="tag">
                    Cloud
                </span>

            </div>

        </div>


        <div class="project">

            <div class="project-image">
                ⚙
            </div>

            <div class="project-info">

                <h3>
                    Automation
                </h3>

                <p>
                    Automated development and
                    deployment workflows.
                </p>

                <span class="tag">
                    DevOps
                </span>

            </div>

        </div>


    </div>

</section>


<!-- FEATURES -->

<section id="features">

    <div class="heading">

        <h2>Features.</h2>

        <p>
            Everything inside a single Flask application.
        </p>

    </div>


    <div class="features">


        <div class="feature">

            <div class="icon">
                ◉
            </div>

            <h3>
                3D Interface
            </h3>

            <p>
                WebGL particles, rotating geometry
                and mouse interaction.
            </p>

        </div>


        <div class="feature">

            <div class="icon">
                📈
            </div>

            <h3>
                Analytics
            </h3>

            <p>
                Live API-powered charts and
                dashboard metrics.
            </p>

        </div>


        <div class="feature">

            <div class="icon">
                🔒
            </div>

            <h3>
                Production Ready
            </h3>

            <p>
                Flask server configured for Docker
                and AWS deployment.
            </p>

        </div>


    </div>

</section>


<!-- CTA -->

<section class="cta" id="contact">

    <div class="cta-box">

        <h2>
            Enter the future.
        </h2>

        <p>
            One application. One container.
            Complete digital experience.
        </p>

        <a
            href="#home"
            class="btn primary">

            Back to Top

        </a>

    </div>

</section>


</main>


<footer>

    NOVA © 2026

    <br><br>

    Flask · Three.js · Chart.js

</footer>


<script>

/* ============================================================
   THREE.JS
============================================================ */

const scene = new THREE.Scene();

const camera =
    new THREE.PerspectiveCamera(
        70,
        window.innerWidth /
        window.innerHeight,
        0.1,
        1000
    );

camera.position.z = 5;


const renderer =
    new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
    });

renderer.setPixelRatio(
    Math.min(
        window.devicePixelRatio,
        2
    )
);

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

document
    .getElementById("three-bg")
    .appendChild(
        renderer.domElement
    );


/* PARTICLES */

const particleGeometry =
    new THREE.BufferGeometry();

const particleCount = 2500;

const positions =
    new Float32Array(
        particleCount * 3
    );

for (
    let i = 0;
    i < particleCount * 3;
    i++
) {
    positions[i] =
        (Math.random() - .5) * 25;
}

particleGeometry.setAttribute(
    "position",

    new THREE.BufferAttribute(
        positions,
        3
    )
);

const particleMaterial =
    new THREE.PointsMaterial({

        color: 0x8b5cf6,

        size: .025,

        transparent: true,

        opacity: .8
    });

const particles =
    new THREE.Points(
        particleGeometry,
        particleMaterial
    );

scene.add(particles);


/* ICOSAHEDRON */

const sphere =
    new THREE.Mesh(

        new THREE.IcosahedronGeometry(
            1.7,
            3
        ),

        new THREE.MeshBasicMaterial({

            color: 0x7c3aed,

            wireframe: true,

            transparent: true,

            opacity: .3
        })
    );

scene.add(sphere);


/* TORUS */

const torus =
    new THREE.Mesh(

        new THREE.TorusGeometry(
            2.4,
            .025,
            16,
            100
        ),

        new THREE.MeshBasicMaterial({

            color: 0x60a5fa,

            transparent: true,

            opacity: .45
        })
    );

torus.rotation.x =
    Math.PI / 2;

scene.add(torus);


/* MOUSE */

let mouseX = 0;
let mouseY = 0;

document.addEventListener(
    "mousemove",
    function(e) {

        mouseX =
            e.clientX /
            window.innerWidth - .5;

        mouseY =
            e.clientY /
            window.innerHeight - .5;
    }
);


/* ANIMATION */

function animate() {

    requestAnimationFrame(
        animate
    );

    sphere.rotation.x += .001;
    sphere.rotation.y += .002;

    torus.rotation.z += .001;

    particles.rotation.y += .0002;

    camera.position.x +=
        (
            mouseX * .35 -
            camera.position.x
        ) * .02;

    camera.position.y +=
        (
            -mouseY * .35 -
            camera.position.y
        ) * .02;

    renderer.render(
        scene,
        camera
    );
}

animate();


/* RESIZE */

window.addEventListener(
    "resize",
    function() {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    }
);


/* ============================================================
   CHART CONFIG
============================================================ */

const chartOptions = {

    responsive: true,

    maintainAspectRatio: false,

    animation: {
        duration: 1800,
        easing: "easeOutQuart"
    },

    interaction: {
        intersect: false,
        mode: "index"
    },

    plugins: {

        legend: {

            labels: {
                color: "#aaa"
            }
        }
    },

    scales: {

        x: {

            ticks: {
                color: "#666"
            },

            grid: {
                display: false
            }
        },

        y: {

            ticks: {
                color: "#666"
            },

            grid: {
                color:
                    "rgba(255,255,255,.05)"
            }
        }
    }
};


/* ============================================================
   REVENUE CHART
============================================================ */

const revenueChart =
    new Chart(

        document.getElementById(
            "revenueChart"
        ),

        {

            type: "line",

            data: {

                labels: [],

                datasets: [{

                    label: "Revenue",

                    data: [],

                    borderColor:
                        "#8b5cf6",

                    backgroundColor:
                        "rgba(139,92,246,.12)",

                    borderWidth: 3,

                    fill: true,

                    tension: .45,

                    pointRadius: 4,

                    pointHoverRadius: 8
                }]
            },

            options: chartOptions
        }
    );


/* ============================================================
   USERS CHART
============================================================ */

const usersChart =
    new Chart(

        document.getElementById(
            "usersChart"
        ),

        {

            type: "bar",

            data: {

                labels: [],

                datasets: [{

                    label: "Users",

                    data: [],

                    backgroundColor:
                        "rgba(96,165,250,.65)",

                    borderRadius: 10
                }]
            },

            options: chartOptions
        }
    );


/* ============================================================
   ORDERS CHART
============================================================ */

const ordersChart =
    new Chart(

        document.getElementById(
            "ordersChart"
        ),

        {

            type: "line",

            data: {

                labels: [],

                datasets: [{

                    label: "Orders",

                    data: [],

                    borderColor:
                        "#22c55e",

                    backgroundColor:
                        "rgba(34,197,94,.10)",

                    borderWidth: 3,

                    fill: true,

                    tension: .4
                }]
            },

            options: chartOptions
        }
    );


/* ============================================================
   TRAFFIC CHART
============================================================ */

const trafficChart =
    new Chart(

        document.getElementById(
            "trafficChart"
        ),

        {

            type: "doughnut",

            data: {

                labels: [
                    "Direct",
                    "Google",
                    "Social",
                    "Referral"
                ],

                datasets: [{

                    data: [
                        35,
                        30,
                        20,
                        15
                    ],

                    borderWidth: 0,

                    hoverOffset: 15
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "68%",

                animation: {

                    animateRotate: true,

                    animateScale: true,

                    duration: 1800
                },

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            color: "#aaa",

                            padding: 18
                        }
                    }
                }
            }
        }
    );


/* ============================================================
   LOAD CHART DATA
============================================================ */

async function loadAnalytics() {

    try {

        const response =
            await fetch(
                "/api/analytics"
            );

        const data =
            await response.json();


        revenueChart.data.labels =
            data.months;

        revenueChart
            .data
            .datasets[0]
            .data =
            data.revenue;


        usersChart.data.labels =
            data.months;

        usersChart
            .data
            .datasets[0]
            .data =
            data.users;


        ordersChart.data.labels =
            data.months;

        ordersChart
            .data
            .datasets[0]
            .data =
            data.orders;


        revenueChart.update();

        usersChart.update();

        ordersChart.update();

    }

    catch(error) {

        console.error(error);

    }
}

loadAnalytics();


/* ============================================================
   LIVE STATS
============================================================ */

async function updateStats() {

    try {

        const response =
            await fetch(
                "/api/stats"
            );

        const data =
            await response.json();


        document.getElementById(
            "revenue"
        ).innerText =
            "$" +
            data.revenue.toLocaleString();


        document.getElementById(
            "users"
        ).innerText =
            data.users.toLocaleString();


        document.getElementById(
            "orders"
        ).innerText =
            data.orders.toLocaleString();


        document.getElementById(
            "conversion"
        ).innerText =
            data.conversion + "%";

    }

    catch(error) {

        console.error(error);

    }
}

updateStats();

setInterval(
    updateStats,
    5000
);


/* ============================================================
   NAVIGATION
============================================================ */

function goContact() {

    document
        .getElementById("contact")
        .scrollIntoView({
            behavior: "smooth"
        });
}

</script>

</body>
</html>
"""


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML)


# ============================================================
# IMPORTANT:
# LISTEN ON PORT 80
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=False
    )
