from flask import Flask, render_template_string, jsonify
import random
import time

app = Flask(__name__)


# ============================================================
# BACKEND DATA
# ============================================================

START_TIME = time.time()

def generate_stats():
    return {
        "revenue": random.randint(48000, 62000),
        "users": random.randint(8500, 11000),
        "orders": random.randint(1200, 1800),
        "conversion": round(random.uniform(7.5, 10.5), 1)
    }


@app.route("/api/stats")
def stats():
    return jsonify(generate_stats())


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


# ============================================================
# EVERYTHING BELOW IS THE FRONTEND
# ============================================================

HTML = r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>NOVA — 3D Analytics</title>


<!-- Chart.js -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>


<style>

/* ============================================================
   GLOBAL
============================================================ */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    background: #050507;
    color: white;
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    overflow-x: hidden;
}

button,
input {
    font-family: inherit;
}


/* ============================================================
   3D BACKGROUND
============================================================ */

#three-container {
    position: fixed;
    inset: 0;

    z-index: -10;

    pointer-events: none;
}

#three-container canvas {
    display: block;
}


/* ============================================================
   BACKGROUND GLOW
============================================================ */

.glow {
    position: fixed;

    width: 500px;
    height: 500px;

    border-radius: 50%;

    filter: blur(140px);

    opacity: .15;

    pointer-events: none;

    z-index: -5;
}

.glow.one {
    background: #7c3aed;

    top: 10%;
    left: 5%;
}

.glow.two {
    background: #2563eb;

    right: 5%;
    bottom: 10%;
}


/* ============================================================
   NAVBAR
============================================================ */

.navbar {

    position: fixed;

    top: 18px;

    left: 50%;

    transform: translateX(-50%);

    width: min(1200px, 94%);

    height: 65px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 22px;

    border: 1px solid
        rgba(255,255,255,.1);

    border-radius: 40px;

    background:
        rgba(8,8,14,.65);

    backdrop-filter:
        blur(25px);

    z-index: 1000;
}


.logo {

    font-size: 22px;

    font-weight: 900;

    letter-spacing: -1px;
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

    transition: .25s;
}

.nav-links a:hover {
    color: white;
}


.nav-button {

    border: none;

    padding: 11px 19px;

    border-radius: 30px;

    background: white;

    color: black;

    font-weight: 700;

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

    padding: 120px 20px 70px;
}

.hero-content {
    max-width: 1000px;
}


.badge {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    padding: 9px 16px;

    border-radius: 30px;

    background:
        rgba(139,92,246,.1);

    border:
        1px solid
        rgba(139,92,246,.3);

    color: #c4b5fd;

    font-size: 13px;

    margin-bottom: 28px;
}


.hero h1 {

    font-size:
        clamp(60px, 10vw, 130px);

    line-height: .86;

    letter-spacing: -8px;

    background:
        linear-gradient(
            120deg,
            #ffffff,
            #a78bfa,
            #60a5fa,
            #ffffff
        );

    background-size: 300%;

    -webkit-background-clip: text;

    color: transparent;

    animation:
        gradientMove 6s linear infinite;
}


@keyframes gradientMove {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }
}


.hero p {

    max-width: 650px;

    margin: 35px auto 0;

    color: #888;

    font-size: 18px;

    line-height: 1.7;
}


.hero-buttons {

    margin-top: 40px;

    display: flex;

    justify-content: center;

    gap: 15px;
}


.btn {

    padding: 15px 25px;

    border-radius: 35px;

    text-decoration: none;

    font-weight: 700;

    transition: .3s;
}

.btn:hover {
    transform:
        translateY(-4px);
}


.btn-primary {

    background: white;

    color: black;
}


.btn-secondary {

    color: white;

    border:
        1px solid
        rgba(255,255,255,.15);

    background:
        rgba(255,255,255,.05);
}


/* ============================================================
   MAIN
============================================================ */

main {

    width: min(
        1250px,
        92%
    );

    margin: auto;
}


section {

    padding: 100px 0;

    scroll-margin-top: 100px;
}


.section-heading {

    margin-bottom: 45px;
}


.section-heading h2 {

    font-size:
        clamp(40px, 6vw, 70px);

    letter-spacing: -4px;
}


.section-heading p {

    color: #777;

    max-width: 600px;

    line-height: 1.7;

    margin-top: 15px;
}


/* ============================================================
   DASHBOARD
============================================================ */

.dashboard {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 18px;
}


.stat-card {

    padding: 25px;

    min-height: 160px;

    border-radius: 24px;

    border:
        1px solid
        rgba(255,255,255,.09);

    background:
        rgba(255,255,255,.04);

    backdrop-filter:
        blur(20px);

    transition: .35s;
}


.stat-card:hover {

    transform:
        translateY(-7px);

    border-color:
        rgba(139,92,246,.5);

    box-shadow:
        0 25px 60px
        rgba(0,0,0,.3);
}


.stat-top {

    display: flex;

    align-items: center;

    justify-content: space-between;

    color: #777;

    font-size: 14px;
}


.stat-icon {

    width: 40px;

    height: 40px;

    border-radius: 12px;

    display: grid;

    place-items: center;

    background:
        rgba(139,92,246,.15);

    color: #a78bfa;
}


.stat-value {

    font-size: 34px;

    font-weight: 800;

    margin-top: 25px;
}


.stat-change {

    color: #4ade80;

    font-size: 13px;

    margin-top: 5px;
}


/* ============================================================
   CHARTS
============================================================ */

.charts {

    display: grid;

    grid-template-columns:
        1.6fr 1fr;

    gap: 22px;

    margin-top: 25px;
}


.chart-card {

    min-height: 390px;

    padding: 28px;

    border-radius: 26px;

    border:
        1px solid
        rgba(255,255,255,.09);

    background:
        rgba(255,255,255,.04);

    backdrop-filter:
        blur(20px);
}


.chart-card h3 {

    font-size: 20px;

    margin-bottom: 25px;
}


.chart-wrapper {

    position: relative;

    height: 290px;
}


/* ============================================================
   FEATURE CARDS
============================================================ */

.features {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 22px;
}


.feature {

    min-height: 270px;

    padding: 35px;

    border-radius: 28px;

    border:
        1px solid
        rgba(255,255,255,.09);

    background:
        rgba(255,255,255,.035);

    transition: .4s;
}


.feature:hover {

    transform:
        translateY(-10px)
        rotateX(3deg);

    border-color:
        rgba(139,92,246,.45);
}


.feature-icon {

    width: 58px;

    height: 58px;

    display: grid;

    place-items: center;

    border-radius: 18px;

    font-size: 25px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );

    margin-bottom: 28px;
}


.feature h3 {

    font-size: 23px;

    margin-bottom: 13px;
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

    grid-template-columns:
        repeat(3, 1fr);

    gap: 22px;
}


.project {

    overflow: hidden;

    border-radius: 25px;

    border:
        1px solid
        rgba(255,255,255,.09);

    background:
        rgba(255,255,255,.04);

    transition: .35s;
}


.project:hover {

    transform:
        translateY(-8px);

    box-shadow:
        0 30px 80px
        rgba(0,0,0,.35);
}


.project-image {

    height: 190px;

    display: grid;

    place-items: center;

    font-size: 55px;

    background:
        radial-gradient(
            circle,
            #4c1d95,
            #08080d
        );
}


.project-info {
    padding: 25px;
}


.project-info h3 {
    margin-bottom: 10px;
}


.project-info p {

    color: #777;

    font-size: 14px;

    line-height: 1.6;
}


.project-tag {

    display: inline-block;

    margin-top: 18px;

    padding: 6px 11px;

    border-radius: 20px;

    background:
        rgba(139,92,246,.12);

    color: #a78bfa;

    font-size: 12px;
}


/* ============================================================
   ACTIVITY
============================================================ */

.activity {

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 22px;
}


.activity-card {

    padding: 30px;

    border-radius: 25px;

    border:
        1px solid
        rgba(255,255,255,.08);

    background:
        rgba(255,255,255,.04);
}


.activity-item {

    display: flex;

    align-items: center;

    gap: 15px;

    padding: 17px 0;

    border-bottom:
        1px solid
        rgba(255,255,255,.06);
}


.activity-item:last-child {
    border-bottom: none;
}


.activity-dot {

    width: 10px;

    height: 10px;

    border-radius: 50%;

    background: #8b5cf6;

    box-shadow:
        0 0 15px
        #8b5cf6;
}


.activity-text {
    flex: 1;
}


.activity-text strong {
    display: block;
}


.activity-text small {
    color: #666;
}


/* ============================================================
   CTA
============================================================ */

.cta {

    text-align: center;

    padding:
        130px 30px;
}


.cta-box {

    padding: 90px 30px;

    border-radius: 35px;

    border:
        1px solid
        rgba(255,255,255,.1);

    background:
        radial-gradient(
            circle at center,
            rgba(124,58,237,.2),
            rgba(255,255,255,.03)
        );
}


.cta h2 {

    font-size:
        clamp(45px, 7vw, 80px);

    letter-spacing: -5px;

    margin-bottom: 20px;
}


.cta p {

    color: #777;

    max-width: 600px;

    margin: auto;

    line-height: 1.7;
}


/* ============================================================
   FOOTER
============================================================ */

footer {

    padding: 35px;

    text-align: center;

    color: #444;

    border-top:
        1px solid
        rgba(255,255,255,.06);
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media(max-width:950px) {

    .dashboard {
        grid-template-columns:
            repeat(2,1fr);
    }

    .charts {
        grid-template-columns: 1fr;
    }

    .features,
    .projects {
        grid-template-columns: 1fr;
    }

    .activity {
        grid-template-columns: 1fr;
    }

}


@media(max-width:600px) {

    .nav-links {
        display: none;
    }

    .navbar {
        width: 94%;
    }

    .dashboard {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        letter-spacing: -5px;
    }

    section {
        padding: 70px 0;
    }

}

</style>

</head>


<body>


<!-- ========================================================
     3D BACKGROUND
========================================================= -->

<div id="three-container"></div>

<div class="glow one"></div>
<div class="glow two"></div>


<!-- ========================================================
     NAVBAR
========================================================= -->

<nav class="navbar">

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
        class="nav-button"
        onclick="scrollToContact()">

        Get Started

    </button>

</nav>


<!-- ========================================================
     HERO
========================================================= -->

<section class="hero" id="home">

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
            animated charts and a modern dashboard.

        </p>

        <div class="hero-buttons">

            <a
                href="#dashboard"
                class="btn btn-primary">

                Explore Dashboard

            </a>

            <a
                href="#analytics"
                class="btn btn-secondary">

                View Analytics →

            </a>

        </div>

    </div>

</section>


<main>


<!-- ========================================================
     DASHBOARD
========================================================= -->

<section id="dashboard">

    <div class="section-heading">

        <h2>
            Dashboard.
        </h2>

        <p>
            Real-time metrics powered by the Flask backend.
        </p>

    </div>


    <div class="dashboard">


        <div class="stat-card">

            <div class="stat-top">

                <span>Revenue</span>

                <div class="stat-icon">
                    $
                </div>

            </div>

            <div
                class="stat-value"
                id="revenue">

                $52,430

            </div>

            <div class="stat-change">
                ↑ 18.4% this month
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-top">

                <span>Users</span>

                <div class="stat-icon">
                    ◉
                </div>

            </div>

            <div
                class="stat-value"
                id="users">

                9,842

            </div>

            <div class="stat-change">
                ↑ 24.2% this month
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-top">

                <span>Orders</span>

                <div class="stat-icon">
                    ◈
                </div>

            </div>

            <div
                class="stat-value"
                id="orders">

                1,524

            </div>

            <div class="stat-change">
                ↑ 12.7% this month
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-top">

                <span>Conversion</span>

                <div class="stat-icon">
                    %
                </div>

            </div>

            <div
                class="stat-value"
                id="conversion">

                8.7%

            </div>

            <div class="stat-change">
                ↑ 2.1% this month
            </div>

        </div>


    </div>


<!-- CHARTS -->

<div class="charts">


    <div class="chart-card">

        <h3>
            Revenue Overview
        </h3>

        <div class="chart-wrapper">

            <canvas id="revenueChart"></canvas>

        </div>

    </div>


    <div class="chart-card">

        <h3>
            User Growth
        </h3>

        <div class="chart-wrapper">

            <canvas id="usersChart"></canvas>

        </div>

    </div>


    <div class="chart-card">

        <h3>
            Orders
        </h3>

        <div class="chart-wrapper">

            <canvas id="ordersChart"></canvas>

        </div>

    </div>


    <div class="chart-card">

        <h3>
            Traffic Sources
        </h3>

        <div class="chart-wrapper">

            <canvas id="trafficChart"></canvas>

        </div>

    </div>


</div>

</section>


<!-- ========================================================
     ANALYTICS
========================================================= -->

<section id="analytics">

    <div class="section-heading">

        <h2>
            Analytics.
        </h2>

        <p>
            Interactive performance visualization.
        </p>

    </div>


    <div class="activity">


        <div class="activity-card">

            <h3>
                Recent Activity
            </h3>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        New user registered
                    </strong>

                    <small>
                        2 minutes ago
                    </small>

                </div>

            </div>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        Deployment completed
                    </strong>

                    <small>
                        18 minutes ago
                    </small>

                </div>

            </div>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        Analytics updated
                    </strong>

                    <small>
                        34 minutes ago
                    </small>

                </div>

            </div>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        Database backup completed
                    </strong>

                    <small>
                        1 hour ago
                    </small>

                </div>

            </div>


        </div>


        <div class="activity-card">

            <h3>
                System Status
            </h3>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        API Server
                    </strong>

                    <small>
                        Operational
                    </small>

                </div>

            </div>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        Database
                    </strong>

                    <small>
                        Operational
                    </small>

                </div>

            </div>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        CDN
                    </strong>

                    <small>
                        Operational
                    </small>

                </div>

            </div>


            <div class="activity-item">

                <div class="activity-dot"></div>

                <div class="activity-text">

                    <strong>
                        Deployment
                    </strong>

                    <small>
                        Operational
                    </small>

                </div>

            </div>


        </div>


    </div>

</section>


<!-- ========================================================
     PROJECTS
========================================================= -->

<section id="projects">

    <div class="section-heading">

        <h2>
            Projects.
        </h2>

        <p>
            Explore the platform ecosystem.
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
                    High-performance analytics
                    infrastructure with real-time
                    data visualization.
                </p>

                <span class="project-tag">
                    Analytics
                </span>

            </div>

        </div>


        <div class="project">

            <div class="project-image">
                ◉
            </div>

            <div class="project-info">

                <h3>
                    Cloud Platform
                </h3>

                <p>
                    Scalable cloud infrastructure
                    designed for modern applications.
                </p>

                <span class="project-tag">
                    Cloud
                </span>

            </div>

        </div>


        <div class="project">

            <div class="project-image">
                ⚡
            </div>

            <div class="project-info">

                <h3>
                    Automation
                </h3>

                <p>
                    Automated workflows connecting
                    development and deployment.
                </p>

                <span class="project-tag">
                    DevOps
                </span>

            </div>

        </div>


    </div>

</section>


<!-- ========================================================
     FEATURES
========================================================= -->

<section id="features">

    <div class="section-heading">

        <h2>
            Features.
        </h2>

        <p>
            Everything packed into one application.
        </p>

    </div>


    <div class="features">


        <div class="feature">

            <div class="feature-icon">
                ◈
            </div>

            <h3>
                3D Experience
            </h3>

            <p>
                Interactive WebGL environment with
                particles, geometry and mouse-based
                movement.
            </p>

        </div>


        <div class="feature">

            <div class="feature-icon">
                ⚡
            </div>

            <h3>
                Real-Time API
            </h3>

            <p>
                Flask API endpoints continuously
                provide backend data to the frontend.
            </p>

        </div>


        <div class="feature">

            <div class="feature-icon">
                📊
            </div>

            <h3>
                Animated Charts
            </h3>

            <p>
                Smooth line, bar, doughnut and
                interactive analytics visualizations.
            </p>

        </div>


    </div>

</section>


<!-- ========================================================
     CTA
========================================================= -->

<section class="cta" id="contact">

    <div class="cta-box">

        <h2>
            Enter the future.
        </h2>

        <p>

            One Flask application.
            One deployment.
            Complete digital experience.

        </p>

        <br>

        <a
            href="#home"
            class="btn btn-primary">

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


<!-- ========================================================
     JAVASCRIPT
========================================================= -->

<script>


/* ============================================================
   THREE.JS 3D WORLD
============================================================ */

const scene =
    new THREE.Scene();


const camera =
    new THREE.PerspectiveCamera(
        70,
        window.innerWidth /
        window.innerHeight,
        .1,
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
    .getElementById(
        "three-container"
    )
    .appendChild(
        renderer.domElement
    );


/* PARTICLES */

const particleGeometry =
    new THREE.BufferGeometry();


const particleCount = 3000;


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


/* MAIN 3D OBJECT */

const sphereGeometry =
    new THREE.IcosahedronGeometry(
        1.7,
        3
    );


const sphereMaterial =
    new THREE.MeshBasicMaterial({

        color: 0x7c3aed,

        wireframe: true,

        transparent: true,

        opacity: .3

    });


const sphere =
    new THREE.Mesh(
        sphereGeometry,
        sphereMaterial
    );


scene.add(sphere);


/* TORUS */

const torusGeometry =
    new THREE.TorusGeometry(
        2.4,
        .025,
        16,
        120
    );


const torusMaterial =
    new THREE.MeshBasicMaterial({

        color: 0x60a5fa,

        transparent: true,

        opacity: .45

    });


const torus =
    new THREE.Mesh(
        torusGeometry,
        torusMaterial
    );


torus.rotation.x =
    Math.PI / 2;


scene.add(torus);


/* SECOND TORUS */

const torus2 =
    torus.clone();


torus2.scale.set(
    .7,
    .7,
    .7
);


torus2.rotation.y =
    Math.PI / 3;


scene.add(torus2);


/* MOUSE */

let mouseX = 0;
let mouseY = 0;


document.addEventListener(
    "mousemove",
    event => {

        mouseX =
            event.clientX /
            window.innerWidth - .5;

        mouseY =
            event.clientY /
            window.innerHeight - .5;

    }
);


/* ANIMATION */

function animate3D() {

    requestAnimationFrame(
        animate3D
    );


    sphere.rotation.x += .001;
    sphere.rotation.y += .002;


    torus.rotation.z += .0015;

    torus2.rotation.x += .001;


    particles.rotation.y += .0002;


    camera.position.x +=
        (
            mouseX * .4 -
            camera.position.x
        ) * .02;


    camera.position.y +=
        (
            -mouseY * .4 -
            camera.position.y
        ) * .02;


    renderer.render(
        scene,
        camera
    );
}


animate3D();


/* RESIZE */

window.addEventListener(
    "resize",
    () => {

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

Chart.defaults.color =
    "#777";

Chart.defaults.borderColor =
    "rgba(255,255,255,.06)";


const commonOptions = {

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

                color: "#aaa",

                usePointStyle: true

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

                    fill: true,

                    tension: .45,

                    borderWidth: 3,

                    pointRadius: 4,

                    pointHoverRadius: 8

                }]

            },

            options: commonOptions

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

            options: commonOptions

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
                        "rgba(34,197,94,.1)",

                    fill: true,

                    tension: .4,

                    borderWidth: 3,

                    pointRadius: 4

                }]

            },

            options: commonOptions

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

                            padding: 18,

                            usePointStyle: true

                        }

                    }

                }

            }

        }

    );


/* ============================================================
   LOAD ANALYTICS FROM FLASK
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

        revenueChart.data.datasets[0]
            .data =
            data.revenue;


        usersChart.data.labels =
            data.months;

        usersChart.data.datasets[0]
            .data =
            data.users;


        ordersChart.data.labels =
            data.months;

        ordersChart.data.datasets[0]
            .data =
            data.orders;


        revenueChart.update();

        usersChart.update();

        ordersChart.update();

    }

    catch(error) {

        console.error(
            "Analytics error:",
            error
        );

    }

}


loadAnalytics();


/* ============================================================
   LIVE DASHBOARD STATS
============================================================ */

async function updateStats() {

    try {

        const response =
            await fetch(
                "/api/stats"
            );


        const data =
            await response.json();


        document
            .getElementById(
                "revenue"
            )
            .innerText =
            "$" +
            data.revenue
                .toLocaleString();


        document
            .getElementById(
                "users"
            )
            .innerText =
            data.users
                .toLocaleString();


        document
            .getElementById(
                "orders"
            )
            .innerText =
            data.orders
                .toLocaleString();


        document
            .getElementById(
                "conversion"
            )
            .innerText =
            data.conversion +
            "%";

    }

    catch(error) {

        console.error(
            "Stats error:",
            error
        );

    }

}


/* update every 5 seconds */

updateStats();

setInterval(
    updateStats,
    5000
);


/* ============================================================
   NAVIGATION
============================================================ */

function scrollToContact() {

    document
        .getElementById(
            "contact"
        )
        .scrollIntoView({
            behavior: "smooth"
        });

}

</script>


</body>

</html>
"""


# ============================================================
# MAIN PAGE
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HTML
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
