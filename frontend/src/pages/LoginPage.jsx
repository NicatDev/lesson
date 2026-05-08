import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login } from "../api.js";

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/products");
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (typeof err.response?.data === "object"
          ? JSON.stringify(err.response.data)
          : "Giriş alınmadı");
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h1>Giriş</h1>
      <form onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="u">İstifadəçi adı</label>
          <input
            id="u"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </div>
        <div className="field">
          <label htmlFor="p">Şifrə</label>
          <input
            id="p"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </div>
        {error ? <div className="error">{error}</div> : null}
        <button type="submit" disabled={loading}>
          {loading ? "Gözləyin…" : "Daxil ol"}
        </button>
      </form>
      <p className="muted" style={{ marginTop: "1rem" }}>
        Hesab yoxdur? <Link to="/register">Qeydiyyat</Link>
      </p>
    </div>
  );
}
