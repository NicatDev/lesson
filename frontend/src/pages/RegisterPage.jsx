import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../api.js";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function set(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(form);
      navigate("/login");
    } catch (err) {
      const data = err.response?.data;
      const msg =
        typeof data === "string"
          ? data
          : data
            ? Object.entries(data)
                .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : v}`)
                .join("; ")
            : "Qeydiyyat alınmadı";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h1>Qeydiyyat</h1>
      <form onSubmit={onSubmit}>
        <div className="field">
          <label>İstifadəçi adı</label>
          <input value={form.username} onChange={(e) => set("username", e.target.value)} required />
        </div>
        <div className="field">
          <label>Şifrə</label>
          <input
            type="password"
            value={form.password}
            onChange={(e) => set("password", e.target.value)}
            required
            minLength={6}
          />
        </div>
        <div className="row">
          <div className="field">
            <label>Ad</label>
            <input value={form.first_name} onChange={(e) => set("first_name", e.target.value)} />
          </div>
          <div className="field">
            <label>Soyad</label>
            <input value={form.last_name} onChange={(e) => set("last_name", e.target.value)} />
          </div>
        </div>
        <div className="field">
          <label>Telefon</label>
          <input value={form.phone_number} onChange={(e) => set("phone_number", e.target.value)} />
        </div>
        {error ? <div className="error">{error}</div> : null}
        <button type="submit" disabled={loading}>
          {loading ? "Gözləyin…" : "Qeydiyyat"}
        </button>
      </form>
      <p className="muted" style={{ marginTop: "1rem" }}>
        Artıq hesabınız var? <Link to="/login">Giriş</Link>
      </p>
    </div>
  );
}
