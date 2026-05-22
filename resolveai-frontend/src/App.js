import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API = "https://resolveai-hrol.onrender.com";

function App() {
  const [page, setPage] = useState("home");

  return (
    <div className="app">
      <nav className="navbar">
        <h1 className="logo">ResolveAI</h1>
        <div className="nav-links">
          <button onClick={() => setPage("home")} className={page === "home" ? "active" : ""}>Submit Complaint</button>
          <button onClick={() => setPage("track")} className={page === "track" ? "active" : ""}>Track Complaint</button>
          <button onClick={() => setPage("admin")} className={page === "admin" ? "active" : ""}>Admin Dashboard</button>
        </div>
      </nav>

      <div className="content">
        {page === "home" && <SubmitComplaint />}
        {page === "track" && <TrackComplaint />}
        {page === "admin" && <AdminDashboard />}
      </div>
    </div>
  );
}

function SubmitComplaint() {
  const [text, setText] = useState("");
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!text || !email) {
      setError("Please fill in both fields");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(`${API}/submit-complaint`, {
        complaint_text: text,
        email: email
      });
      setResult(res.data);
    } catch (e) {
      setError("Something went wrong. Make sure backend is running.");
    }
    setLoading(false);
  };

  return (
    <div className="page">
      <h2>Submit a Complaint</h2>
      <p className="subtitle">Describe your issue in plain language. Our AI will route it to the right department.</p>

      {!result ? (
        <div className="form-card">
          <textarea
            placeholder="Describe your complaint here... e.g. My bank has been charging extra fees on my account without explanation."
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={6}
          />
          <input
            type="email"
            placeholder="Your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          {error && <p className="error">{error}</p>}
          <button onClick={handleSubmit} disabled={loading} className="submit-btn">
            {loading ? "Analyzing..." : "Submit Complaint"}
          </button>
        </div>
      ) : (
        <div className="result-card">
          <div className="success-icon">✓</div>
          <h3>Complaint Submitted Successfully</h3>
          <div className="result-grid">
            <div className="result-item">
              <span className="label">Complaint ID</span>
              <span className="value highlight">{result.complaint_id}</span>
            </div>
            <div className="result-item">
              <span className="label">Category</span>
              <span className="value">{result.category}</span>
            </div>
            <div className="result-item">
              <span className="label">Routed To</span>
              <span className="value">{result.department}</span>
            </div>
            <div className="result-item">
              <span className="label">Expected Resolution</span>
              <span className="value">{result.resolution_time}</span>
            </div>
            <div className="result-item">
              <span className="label">Status</span>
              <span className="value status-badge">{result.status}</span>
            </div>
          </div>
          <p className="save-note">Save your Complaint ID to track status later.</p>
          <button onClick={() => setResult(null)} className="submit-btn">Submit Another</button>
        </div>
      )}
    </div>
  );
}

function TrackComplaint() {
  const [id, setId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleTrack = async () => {
    if (!id) return;
    setLoading(true);
    setError("");
    try {
      const res = await axios.get(`${API}/complaint-status/${id}`);
      if (res.data.error) {
        setError("Complaint ID not found");
        setResult(null);
      } else {
        setResult(res.data);
      }
    } catch (e) {
      setError("Something went wrong.");
    }
    setLoading(false);
  };

  return (
    <div className="page">
      <h2>Track Your Complaint</h2>
      <p className="subtitle">Enter your complaint ID to check the current status.</p>

      <div className="form-card">
        <input
          type="text"
          placeholder="Enter Complaint ID e.g. 3C67010E"
          value={id}
          onChange={(e) => setId(e.target.value.toUpperCase())}
        />
        {error && <p className="error">{error}</p>}
        <button onClick={handleTrack} disabled={loading} className="submit-btn">
          {loading ? "Searching..." : "Track Complaint"}
        </button>
      </div>

      {result && (
        <div className="result-card">
          <div className="result-grid">
            <div className="result-item">
              <span className="label">Complaint ID</span>
              <span className="value highlight">{result.complaint_id}</span>
            </div>
            <div className="result-item">
              <span className="label">Department</span>
              <span className="value">{result.department}</span>
            </div>
            <div className="result-item">
              <span className="label">Expected Resolution</span>
              <span className="value">{result.resolution_time}</span>
            </div>
            <div className="result-item">
              <span className="label">Status</span>
              <span className="value status-badge">{result.status}</span>
            </div>
            <div className="result-item">
              <span className="label">Submitted On</span>
              <span className="value">{result.created_at}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [updateId, setUpdateId] = useState("");
  const [updateStatus, setUpdateStatus] = useState("In Progress");
  const [updateMsg, setUpdateMsg] = useState("");

  const loadStats = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/dashboard-stats`);
      setStats(res.data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleUpdate = async () => {
    if (!updateId) return;
    try {
      await axios.put(`${API}/update-status/${updateId}`, {
        status: updateStatus
      });
      setUpdateMsg(`Status updated successfully for ${updateId}`);
      loadStats();
    } catch (e) {
      setUpdateMsg("Update failed. Check complaint ID.");
    }
  };

  return (
    <div className="page">
      <h2>Admin Dashboard</h2>
      <p className="subtitle">Monitor all complaints and update their status.</p>

      <button onClick={loadStats} className="submit-btn" style={{marginBottom: "2rem"}}>
        {loading ? "Loading..." : "Load Statistics"}
      </button>

      {stats && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-number">{stats.total_complaints}</span>
              <span className="stat-label">Total Complaints</span>
            </div>
            {stats.by_status.map((s, i) => (
              <div className="stat-card" key={i}>
                <span className="stat-number">{s.count}</span>
                <span className="stat-label">{s.status}</span>
              </div>
            ))}
          </div>

          <h3 style={{marginTop: "2rem"}}>By Department</h3>
          <div className="dept-list">
            {stats.by_department.map((d, i) => (
              <div className="dept-item" key={i}>
                <span>{d.department}</span>
                <span className="dept-count">{d.count}</span>
              </div>
            ))}
          </div>

          <h3 style={{marginTop: "2rem"}}>Recent Complaints</h3>
          <table className="complaints-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Department</th>
                <th>Status</th>
                <th>Submitted</th>
              </tr>
            </thead>
            <tbody>
              {stats.recent_complaints.map((c, i) => (
                <tr key={i}>
                  <td>{c.complaint_id}</td>
                  <td>{c.department}</td>
                  <td><span className="status-badge">{c.status}</span></td>
                  <td>{c.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      <div className="form-card" style={{marginTop: "2rem"}}>
        <h3>Update Complaint Status</h3>
        <input
          type="text"
          placeholder="Complaint ID"
          value={updateId}
          onChange={(e) => setUpdateId(e.target.value.toUpperCase())}
        />
        <select value={updateStatus} onChange={(e) => setUpdateStatus(e.target.value)}>
          <option>In Progress</option>
          <option>Under Review</option>
          <option>Resolved</option>
          <option>Rejected</option>
        </select>
        <button onClick={handleUpdate} className="submit-btn">Update Status</button>
        {updateMsg && <p className="success-msg">{updateMsg}</p>}
      </div>
    </div>
  );
}

export default App;