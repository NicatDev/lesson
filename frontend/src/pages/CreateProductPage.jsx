import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";

export default function CreateProductPage() {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    name: "",
    slug: "",
    description: "",
    price: "",
    stock: "0",
    sku: "",
    is_active: true,
    category: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const { data } = await api.get("/categories/");
        const list = Array.isArray(data) ? data : data.results || [];
        if (!cancelled) {
          setCategories(list);
          if (list.length && !form.category) {
            setForm((f) => ({ ...f, category: String(list[0].id) }));
          }
        }
      } catch {
        /* ignore */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  function set(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    if (!localStorage.getItem("access")) {
      setError("Əvvəl giriş edin.");
      navigate("/login");
      return;
    }
    setLoading(true);
    try {
      const payload = {
        name: form.name,
        slug: form.slug || undefined,
        description: form.description,
        price: form.price,
        stock: Number(form.stock) || 0,
        sku: form.sku,
        is_active: Boolean(form.is_active),
        category: Number(form.category),
      };
      await api.post("/products/", payload);
      navigate("/products");
    } catch (err) {
      const data = err.response?.data;
      const msg =
        typeof data === "string"
          ? data
          : data
            ? JSON.stringify(data)
            : "Yaradılma alınmadı (401 üçün yenidən giriş edin).";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card wide" style={{ maxWidth: 560 }}>
      <h1>Məhsul yarat</h1>
      <form onSubmit={onSubmit}>
        <div className="field">
          <label>Ad</label>
          <input value={form.name} onChange={(e) => set("name", e.target.value)} required />
        </div>
        <div className="field">
          <label>Slug (istəyə bağlı)</label>
          <input value={form.slug} onChange={(e) => set("slug", e.target.value)} />
        </div>
        <div className="field">
          <label>Təsvir</label>
          <textarea value={form.description} onChange={(e) => set("description", e.target.value)} />
        </div>
        <div className="row">
          <div className="field">
            <label>Qiymət</label>
            <input value={form.price} onChange={(e) => set("price", e.target.value)} required />
          </div>
          <div className="field">
            <label>Ehtiyat</label>
            <input value={form.stock} onChange={(e) => set("stock", e.target.value)} />
          </div>
        </div>
        <div className="field">
          <label>SKU</label>
          <input value={form.sku} onChange={(e) => set("sku", e.target.value)} required />
        </div>
        <div className="field">
          <label>Kateqoriya</label>
          <select value={form.category} onChange={(e) => set("category", e.target.value)} required>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>
            <input
              type="checkbox"
              checked={!!form.is_active}
              onChange={(e) => set("is_active", e.target.checked)}
            />{" "}
            Aktiv
          </label>
        </div>
        {error ? <div className="error">{error}</div> : null}
        <button type="submit" disabled={loading}>
          {loading ? "Gözləyin…" : "Yarat"}
        </button>
      </form>
    </div>
  );
}
