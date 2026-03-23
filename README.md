
# 🚀 Dodge AI - Intelligent SQL Query System

An AI-powered system that converts natural language into SQL queries, detects broken business flows, visualizes relationships, and provides analytics — all in one platform.

---

## 🌟 Features

### 🤖 AI-Powered SQL Generation
- Convert plain English queries into SQL
- Example:
  - "Show orders of customer 320000083"
  - "How many orders"
  - "Latest orders"

---

### 🚨 Broken Flow Detection
Detect missing business processes:
- Orders without payment
- Orders without delivery

---

### 🌐 Graph Visualization
- Dynamic relationship graph
- Customer → Order → Delivery/Payment flow

---

### 📊 Analytics Dashboard
- Total orders
- Orders per customer
- Interactive charts

---

### 🎨 Modern UI
- Glassmorphism design
- Animated background
- Interactive experience

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- PostgreSQL
- Groq API (LLM)

### Frontend
- React.js
- Cytoscape.js (Graph)
- Chart.js (Analytics)

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone Repo
```bash
git clone https://github.com/yourusername/dodge-ai.git
cd dodge-ai
````

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Run server:

```bash
uvicorn main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd ../frontend
npm install
npm start
```

---

## 🔌 API Endpoints

| Endpoint     | Method | Description        |
| ------------ | ------ | ------------------ |
| `/chat`      | POST   | AI SQL + execution |
| `/graph`     | POST   | Relationship graph |
| `/analytics` | GET    | Dashboard insights |
| `/orders`    | GET    | Get orders         |

---

## 🧪 Example Queries

```text
show orders
how many orders
latest orders
orders of customer 320000083
find orders without payment
show orders without delivery
```

---

## 🌐 Deployment

### Backend

* Render

### Frontend

* Vercel

---

## 🎯 Key Highlights

* AI + SQL automation
* Business anomaly detection
* Data visualization
* Full-stack deployment

---

## 📌 Future Improvements

* Multi-table joins
* Authentication system
* Advanced analytics
* Real-time updates

---

## 👨‍💻 Author

**Apoorva Singh**

---


