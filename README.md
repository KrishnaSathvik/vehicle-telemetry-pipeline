# 🚗 Real-Time Vehicle Telemetry Pipeline

This project simulates, processes, and visualizes real-time vehicle telemetry (e.g., GPS, speed, fuel level, engine temperature) using Kafka, Spark Structured Streaming, Cassandra, and Streamlit.

---

## 🔧 Tech Stack

- **Python 3.10+**
- **Kafka + Zookeeper (via Docker)**
- **Apache Spark Structured Streaming**
- **Apache Cassandra (via Docker)**
- **Streamlit (Real-time Dashboard)**
- **Faker** for simulated data

---

## 📈 Features

- 🚘 Real-time telemetry data generation (vehicle_id, speed, GPS, fuel, engine_temp)
- ⚡ Spark streaming pipeline with anomaly detection:
  - Over-speed (> 100 mph)
  - Overheat (> 110°C)
  - Low fuel (< 10%)
- 🗃️ Data stored in Cassandra (vehicle_data and alerts)
- 📊 Streamlit dashboard with:
  - Vehicle ID filter
  - Speed & Fuel charts
  - Alerts display
  - Auto-refresh every 5 seconds

---

## 📂 Folder Structure

```
vehicle-telemetry-pipeline/
├── kafka/                 # Kafka + Zookeeper docker-compose
├── cassandra/             # Cassandra schema (init.cql)
├── data_simulator/        # Python script for generating telemetry
├── spark_processor/       # Spark Structured Streaming pipeline
├── dashboard/             # Streamlit dashboard UI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How to Run the Project

### 🐘 1. Start Kafka
```bash
cd kafka
docker-compose up -d
```

### 🗄️ 2. Start Cassandra
```bash
docker run --name cassandra -d -p 9042:9042 cassandra
```

### 🧱 3. Setup Tables in Cassandra
```bash
docker exec -it cassandra cqlsh
```

Then run the contents of `cassandra/init.cql`

### 🛰️ 4. Start Vehicle Data Simulator
```bash
cd data_simulator
python simulator.py
```

### 🔥 5. Start Spark Streaming Processor
```bash
cd spark_processor
python processor.py
```

### 📊 6. Start Dashboard
```bash
cd dashboard
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) to view the dashboard.

---

## 📷 Screenshots (optional)
Add screenshots of dashboard and charts here.

---

## 📜 License

MIT License
