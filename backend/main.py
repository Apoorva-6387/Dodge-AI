import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from groq import Groq

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

app = FastAPI()

# -------------------------------
# CORS (React connect)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# DB CONNECTION
# -------------------------------
conn = psycopg2.connect(
    dbname="Dodge_ai",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
conn = psycopg2.connect(os.getenv("DATABASE_URL"))

# -------------------------------
# GROQ CLIENT
# -------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------
# REQUEST MODEL
# -------------------------------
class QueryRequest(BaseModel):
    query: str

# -------------------------------
#  GUARDRAILS (IMPORTANT)
# -------------------------------
def is_valid_query(query):
    keywords = ["order", "invoice", "payment", "delivery"]
    return any(k in query.lower() for k in keywords)

# -------------------------------
#  AI FUNCTION (SMART PROMPT)
# -------------------------------
def generate_sql(question):
    prompt = f"""
    You are an expert PostgreSQL query generator.

    Convert user question into SQL.

    STRICT RULES:
    - Use ONLY: orders(id, customer_id)
    - NO JOIN
    - Return ONLY SQL
    - No explanation

    SMART LOGIC:
    - "how many", "count" → COUNT(*)
    - "latest", "recent" → ORDER BY id DESC
    - "top", "limit" → LIMIT
    - "customer X" → WHERE customer_id = X
    - default → SELECT *

    Examples:

    Q: show orders
    A: SELECT * FROM orders LIMIT 10;

    Q: latest orders
    A: SELECT * FROM orders ORDER BY id DESC LIMIT 10;

    Q: how many orders
    A: SELECT COUNT(*) FROM orders;

    Q: show orders of customer 320000083
    A: SELECT * FROM orders WHERE customer_id = 320000083 LIMIT 10;

    Now generate SQL:

    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    print("Generated SQL:", sql)

    return sql

def fallback_sql(query):
    q = query.lower()

    if "count" in q or "how many" in q:
        return "SELECT COUNT(*) FROM orders;"

    if "latest" in q or "recent" in q:
        return "SELECT * FROM orders ORDER BY id DESC LIMIT 10;"

    if "customer" in q:
        import re
        match = re.search(r'\d+', q)
        if match:
            cid = match.group()
            return f"SELECT * FROM orders WHERE customer_id = {cid} LIMIT 10;"

    return "SELECT * FROM orders LIMIT 10;"

def detect_broken_flow(query):
    q = query.lower()

    #  delivery cases
    if "without delivery" in q or "no delivery" in q:
        return """
        SELECT o.id 
        FROM orders o
        LEFT JOIN deliveries d ON o.id = d.order_id
        WHERE d.id IS NULL;
        """

    #  payment cases
    if "without payment" in q or "no payment" in q:
        return """
        SELECT o.id 
        FROM orders o
        LEFT JOIN payments p ON o.id = p.invoice_id
        WHERE p.id IS NULL;
        """

    return None
# -------------------------------
#  TEST API
# -------------------------------
@app.get("/test-db")
def test_db():
    return {"status": "DB connected"}

# -------------------------------
#  GET ORDERS
# -------------------------------
@app.get("/orders")
def get_orders():
    cur = conn.cursor()
    cur.execute("SELECT id, customer_id FROM orders LIMIT 10")
    rows = cur.fetchall()

    return {
        "data": [
            {"id": row[0], "customer_id": row[1]}
            for row in rows
        ]
    }

# -------------------------------
# FILTER BY CUSTOMER
# -------------------------------
@app.get("/orders/{customer_id}")
def get_orders_by_customer(customer_id: int):
    cur = conn.cursor()

    cur.execute(
        "SELECT id, customer_id FROM orders WHERE customer_id = %s LIMIT 10",
        (customer_id,)
    )

    rows = cur.fetchall()

    return {
        "data": [
            {"id": row[0], "customer_id": row[1]}
            for row in rows
        ]
    }

# -------------------------------
#  CHAT API (FINAL VERSION)
# -------------------------------
@app.post("/chat")
def chat(request: QueryRequest):
    try:
        print("User Query:", request.query)

        # 🔥 Step 1: Broken flow FIRST
        sql = detect_broken_flow(request.query)

        # 🔥 Step 2: AI SQL
        if not sql:
            sql = generate_sql(request.query)

        # 🔥 Step 3: CLEAN SQL
        sql = sql.strip()

        # 🔥 Step 4: FALLBACK (VERY IMPORTANT)
        if not sql.lower().startswith("select"):
            print("⚠️ Invalid SQL from AI, using fallback...")
            sql = fallback_sql(request.query)

        print("Final SQL:", sql)

        # 🛡️ Safety (double check)
        if not sql.lower().startswith("select"):
            return {"error": "Only SELECT queries allowed"}

        # 🔥 Step 5: Execute
        cur = conn.cursor()
        cur.execute(sql)

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        result = [dict(zip(columns, row)) for row in rows]

        return {
            "question": request.query,
            "sql": sql,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}
    # -------------------------------
#  GRAPH API (DYNAMIC)
# -------------------------------
@app.post("/graph")
def generate_graph(request: QueryRequest):
    query = request.query.lower()

    nodes = []
    edges = []

    # Always track what is added
    added = set()

    def add_node(id, label):
        if id not in added:
            nodes.append({"data": {"id": id, "label": label}})
            added.add(id)

    #LOGIC

    if "order" in query:
        add_node("customer", "Customer")
        add_node("order", "Order")

        edges.append({
            "data": {"source": "customer", "target": "order"}
        })

    if "delivery" in query:
        add_node("customer", "Customer")
        add_node("order", "Order")
        add_node("delivery", "Delivery")

        edges.append({
            "data": {"source": "customer", "target": "order"}
        })
        edges.append({
            "data": {"source": "order", "target": "delivery"}
        })

    if "payment" in query:
        add_node("customer", "Customer")
        add_node("order", "Order")
        add_node("payment", "Payment")

        edges.append({
            "data": {"source": "customer", "target": "order"}
        })
        edges.append({
            "data": {"source": "order", "target": "payment"}
        })

    return {
        "nodes": nodes,
        "edges": edges
    }
@app.get("/analytics")
def get_analytics():
    cur = conn.cursor()

    # Total orders
    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    # Orders per customer (top 5)
    cur.execute("""
        SELECT customer_id, COUNT(*) 
        FROM orders 
        GROUP BY customer_id 
        LIMIT 5
    """)
    customer_data = cur.fetchall()

    return {
        "total_orders": total_orders,
        "customers": [
            {"customer_id": row[0], "count": row[1]}
            for row in customer_data
        ]
    }