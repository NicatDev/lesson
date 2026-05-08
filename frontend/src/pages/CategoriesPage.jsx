import { useEffect, useState } from "react";
import { api } from "../api.js";

export default function CategoriesPage() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const { data } = await api.get("/categories/");
        if (!cancelled) setItems(Array.isArray(data) ? data : data.results || []);
      } catch (e) {
        if (!cancelled) setError("Kateqoriyalar yüklənmədi.");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="card wide">
      <h1>Kateqoriyalar</h1>
      {error ? <div className="error">{error}</div> : null}
      <div className="grid-list">
        {items.map((c) => (
          <div key={c.id} style={{ borderBottom: "1px solid #eee", padding: "0.35rem 0" }}>
            <strong>{c.name}</strong>{" "}
            <span className="pill">id: {c.id}</span>
            {c.description ? <div className="muted">{c.description}</div> : null}
          </div>
        ))}
      </div>
    </div>
  );
}
