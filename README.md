# 🍔 DoorDash Wrapped

A Spotify Wrapped–inspired interactive dashboard that analyzes personal DoorDash order history to uncover trends in ordering behavior, cuisine preferences, and delivery performance.

---

## 📌 Overview

This project transforms raw DoorDash order data into a visually engaging, interactive experience. It combines **data engineering, feature engineering, and frontend visualization** to tell a story about ordering habits over time.

The final output is a browser-based dashboard with multiple slides, charts, and filters—designed to mimic the feel of a “year in review” product like Spotify Wrapped.

---

## 🚀 Features

### 📊 Data Analysis
- Cleaned and standardized messy real-world order data
- Created a **trip-level identifier** to group multi-item orders
- Engineered key metrics:
  - Total orders
  - Favorite restaurant & item
  - Most ordered cuisine
  - Average delivery time
  - Peak meal periods

### 📈 Visualizations
- Top ordered items (bar chart)
- Cuisine breakdown (bar chart)
- Meal time distribution (doughnut chart)
- Orders over time (monthly trend chart)
- Interactive month highlighting filter

### 🎨 Interactive Dashboard
- Slide-based navigation (Spotify Wrapped style)
- Smooth transitions and animations
- Neon-themed UI with custom styling
- Dynamic chart rendering using CSV inputs

---

## 🛠️ Tech Stack

### Backend / Data Processing
- **Python**
  - `pandas` → data cleaning & transformation
  - `geopy` → geocoding addresses (lat/long)
  - `hashlib` → trip ID generation

### Frontend / Visualization
- **JavaScript**
  - Chart.js → charts
  - PapaParse → CSV parsing
- **HTML/CSS**
  - Custom animations and layout
  - Slide-based storytelling UI
