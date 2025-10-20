# flask_monitoring

Pre-Requisites:

-Downloaded Docker 
-Downloaded Docker-Compose

Steps
1. Clone the Repository
2. cd into the directory
3. run "docker-compose up --build" in the terminal
4. access into the following urls
   http://localhost:5001 - Flask App
   http://localhost:5001/metrics - Flask Metrics
   http://localhost:9090/ - Prometheus UI
   http://localhost:3000/ - Grafana UI
5. In Grafana UI, under Connections > Add new connection > Prometheus > URL: http://prometheus:9090
6. You can configure dashboards in the metric and monitor the metrics using virtualizations


Tech Stack Summary
Web Application Framework: Python + Flask 🐍

Purpose: To create the simple web application that displays the hit counter. Flask is a lightweight Python framework for building web apps quickly.

Role: Handles incoming HTTP requests, interacts with Redis, and serves the HTML response.

Metrics Exposition: prometheus-flask-exporter

Purpose: A Python library added to the Flask app to automatically collect basic metrics (like request latency, counts) and expose them, along with custom metrics (like the Redis connection status), on a /metrics endpoint.

Role: Makes the application's performance data available in a format Prometheus can understand.

In-Memory Data Store: Redis 💾

Purpose: Used as a fast, simple database to store and increment the visitor counter (hits).

Role: Persists the count between requests and provides quick read/write access.

Containerization: Docker 🐳

Purpose: To package the Flask application (with its Python environment and dependencies) and the Redis database into isolated, portable units called containers.

Role: Ensures the application runs consistently regardless of the underlying machine, defined by the Dockerfile.

Local Orchestration: Docker Compose 🎶

Purpose: To define and run the multi-container application (Flask, Redis, Prometheus, Grafana) easily with a single command (docker-compose up).

Role: Manages the lifecycle of the containers, sets up a network for them to communicate (using service names like redis and prometheus), and maps ports. Defined by docker-compose.yml.

Metrics Collection & Storage: Prometheus 📈

Purpose: To scrape (collect) the metrics exposed by the Flask application's /metrics endpoint at regular intervals.

Role: Stores the collected metrics as time-series data and allows querying using PromQL. Configured via prometheus.yml.

Visualization & Dashboarding: Grafana 📊

Purpose: To connect to Prometheus as a data source, query the collected metrics, and display them in user-friendly graphs and dashboards.

Role: Provides the visual interface for monitoring the application's performance and health (e.g., request rates, latency, Redis connection status).

In short, you built a containerized web application using Flask and Redis, instrumented it to expose metrics, and set up a standard monitoring stack (Prometheus + Grafana) to collect and visualize those metrics, all orchestrated locally with Docker Compose.
