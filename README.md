# aquaflow-ai
# AquaFlow AI Monitor

AquaFlow AI Monitor is a smart water pipeline monitoring system designed to detect unusual behavior in water distribution networks. The system analyzes sensor readings such as flow rate and pressure to identify potential issues like leaks, pipe bursts, or abnormal water usage.

The goal of this project is to demonstrate how real-time sensor data combined with machine learning can help monitor critical infrastructure more efficiently.

## Tech Stack
- FastAPI – Backend API for handling sensor data and system logic  
- Scikit-learn – Used to implement the Isolation Forest model for anomaly detection  
- React + Vite – Frontend dashboard for visualizing sensors, alerts, and anomalies  
- SQLAlchemy – ORM used for managing the database  

## Features
- Monitor water pipeline sensors in real time  
- Detect abnormal patterns in flow rate and pressure using machine learning  
- Generate alerts when unusual readings are detected  
- Visual dashboard to track sensors, anomalies, and system status  

## System Architecture

Sensor Data → FastAPI Backend → Anomaly Detection Model → Alerts → Dashboard
