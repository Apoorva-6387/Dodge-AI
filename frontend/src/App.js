import { useState } from "react";
import CytoscapeComponent from "react-cytoscapejs";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

function App() {

  // ✅ ADD THIS LINE (IMPORTANT)
  const API = process.env.REACT_APP_API_URL;

  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [graphData, setGraphData] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  const handleSearch = async () => {
    try {

      // ✅ UPDATED CHAT API
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResult(data);

      // ✅ UPDATED GRAPH API
      const graphRes = await fetch(`${API}/graph`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const graph = await graphRes.json();
      setGraphData([...graph.nodes, ...graph.edges]);

      // ✅ UPDATED ANALYTICS API
      const analyticsRes = await fetch(`${API}/analytics`);
      const analyticsData = await analyticsRes.json();
      setAnalytics(analyticsData);

    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Chart Data
  const chartData = analytics && {
    labels: analytics.customers.map(c => c.customer_id),
    datasets: [
      {
        label: "Orders per Customer",
        data: analytics.customers.map(c => c.count),
        backgroundColor: "#00c6ff",
      },
    ],
  };

  return (
    <div style={styles.page}>

      <div style={styles.blob1}></div>
      <div style={styles.blob2}></div>

      <div style={styles.sticker1}>💻</div>
      <div style={styles.sticker2}>📊</div>
      <div style={styles.sticker3}>🤖</div>
      <div style={styles.sticker4}>⚡</div>

      <div style={styles.particle1}></div>
      <div style={styles.particle2}></div>
      <div style={styles.particle3}></div>

      <div style={styles.container}>
        <h1 style={styles.title}>🚀 AI SQL Query System</h1>

        <div style={styles.inputBox}>
          <input
            type="text"
            placeholder="Ask your data anything..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={styles.input}
          />
          <button onClick={handleSearch} style={styles.button}>
            🔍 Ask AI
          </button>
        </div>

        {result && (
          <div style={styles.resultBox}>
            <h3>✨ AI Response</h3>
            <pre style={styles.resultText}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        {analytics && (
          <div style={styles.resultBox}>
            <h3>📊 Analytics Dashboard</h3>
            <p>Total Orders: {analytics.total_orders}</p>
            <Bar data={chartData} />
          </div>
        )}

        <div style={styles.graphBox}>
          <h3>🌐 Data Relationship Graph</h3>

          <CytoscapeComponent
            elements={graphData}
            style={{ width: "100%", height: "500px" }}
            layout={{
              name: "breadthfirst",
              directed: true,
              padding: 100,
              spacingFactor: 2,
              animate: true,
            }}
            stylesheet={[
              {
                selector: "node",
                style: {
                  label: "data(label)",
                  "background-color": "#00c6ff",
                  color: "#fff",
                  width: 70,
                  height: 70,
                  "font-size": "14px",
                  "text-valign": "center",
                  "text-halign": "center",
                  "text-outline-width": 2,
                  "text-outline-color": "#000",
                  "shadow-blur": 20,
                  "shadow-color": "#00c6ff",
                },
              },
              {
                selector: "edge",
                style: {
                  width: 4,
                  "line-color": "#ffffff",
                  "target-arrow-color": "#ffffff",
                  "target-arrow-shape": "triangle",
                  "curve-style": "bezier",
                },
              },
            ]}
          />
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #0f2027, #2c5364)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    position: "relative",
    overflow: "hidden",
    fontFamily: "Segoe UI",
  },

  blob1: {
    position: "absolute",
    width: "300px",
    height: "300px",
    background: "radial-gradient(circle, #00c6ff, transparent)",
    borderRadius: "50%",
    top: "10%",
    left: "5%",
    filter: "blur(80px)",
  },

  blob2: {
    position: "absolute",
    width: "300px",
    height: "300px",
    background: "radial-gradient(circle, #ff4ecd, transparent)",
    borderRadius: "50%",
    bottom: "10%",
    right: "5%",
    filter: "blur(80px)",
  },

  sticker1: { position: "absolute", top: "10%", left: "8%", fontSize: "40px" },
  sticker2: { position: "absolute", top: "70%", left: "10%", fontSize: "35px" },
  sticker3: { position: "absolute", top: "20%", right: "8%", fontSize: "40px" },
  sticker4: { position: "absolute", bottom: "10%", right: "10%", fontSize: "35px" },

  particle1: { position: "absolute", width: "10px", height: "10px", background: "#00c6ff", borderRadius: "50%", top: "30%", left: "40%" },
  particle2: { position: "absolute", width: "8px", height: "8px", background: "#ff4ecd", borderRadius: "50%", top: "60%", left: "60%" },
  particle3: { position: "absolute", width: "6px", height: "6px", background: "#fff", borderRadius: "50%", top: "20%", left: "70%" },

  container: {
    width: "85%",
    padding: "30px",
    borderRadius: "25px",
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(25px)",
    boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
    color: "#fff",
    zIndex: 2,
  },

  title: {
    textAlign: "center",
    marginBottom: "25px",
    fontSize: "32px",
    textShadow: "0 0 20px rgba(255,255,255,0.8)",
  },

  inputBox: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "25px",
  },

  input: {
    width: "60%",
    padding: "15px",
    borderRadius: "15px",
    border: "none",
    outline: "none",
    marginRight: "10px",
    fontSize: "15px",
  },

  button: {
    padding: "15px 25px",
    borderRadius: "15px",
    border: "none",
    background: "linear-gradient(45deg, #00c6ff, #0072ff)",
    color: "#fff",
    cursor: "pointer",
    fontWeight: "bold",
    boxShadow: "0 0 20px #00c6ff",
  },

  resultBox: {
    background: "rgba(255,255,255,0.08)",
    padding: "20px",
    borderRadius: "15px",
    marginBottom: "25px",
  },

  resultText: {
    fontSize: "13px",
    maxHeight: "200px",
    overflowY: "auto",
  },

  graphBox: {
    background: "rgba(255,255,255,0.08)",
    padding: "20px",
    borderRadius: "15px",
  },
};

export default App;