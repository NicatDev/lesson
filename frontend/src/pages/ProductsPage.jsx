import { useEffect, useMemo, useState } from "react";
import { api } from "../api.js";

const defaultFilters = {
  page: "1",
  page_size: "10",
  ordering: "-created_at",
  category: "",
  name: "",
  sku: "",
  is_active: "",
  price_min: "",
  price_max: "",
};

export default function ProductsPage() {
  const [filters, setFilters] = useState(defaultFilters);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const query = useMemo(() => {
    const p = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => {
      if (v !== "" && v != null) p.set(k, v);
    });
    return p.toString();
  }, [filters]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const { data: res } = await api.get(`/products/?${query}`);
        if (!cancelled) setData(res);
      } catch {
        if (!cancelled) setError("Məhsullar yüklənmədi.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [query]);

  function setFilter(key, value) {
    setFilters((f) => ({ ...f, [key]: value }));
  }

  function apply() {
    setFilters((f) => ({ ...f, page: "1" }));
  }

  const results = data?.results ?? [];
  const total = data?.count;

  return (
    <div className="card wide">
      <h1>Məhsullar (geniş API)</h1>
      <p className="muted">
        Filter və sıralama backend üzrədir. Sadə siyahı üçün:{" "}
        <code>/api/products/simple/?category=ID&amp;ordering=-created_at</code>
      </p>

      <div className="row">
        <div className="field">
          <label>Səhifə</label>
          <input value={filters.page} onChange={(e) => setFilter("page", e.target.value)} />
        </div>
        <div className="field">
          <label>Səhifə ölçüsü</label>
          <input
            value={filters.page_size}
            onChange={(e) => setFilter("page_size", e.target.value)}
          />
        </div>
        <div className="field">
          <label>Sıralama (məs: price, -created_at)</label>
          <input value={filters.ordering} onChange={(e) => setFilter("ordering", e.target.value)} />
        </div>
      </div>
      <div className="row">
        <div className="field">
          <label>Kateqoriya ID</label>
          <input value={filters.category} onChange={(e) => setFilter("category", e.target.value)} />
        </div>
        <div className="field">
          <label>Ad (contains)</label>
          <input value={filters.name} onChange={(e) => setFilter("name", e.target.value)} />
        </div>
        <div className="field">
          <label>SKU (contains)</label>
          <input value={filters.sku} onChange={(e) => setFilter("sku", e.target.value)} />
        </div>
        <div className="field">
          <label>Aktiv (true/false)</label>
          <input
            placeholder="true və ya false"
            value={filters.is_active}
            onChange={(e) => setFilter("is_active", e.target.value)}
          />
        </div>
      </div>
      <div className="row">
        <div className="field">
          <label>Qiymət min</label>
          <input value={filters.price_min} onChange={(e) => setFilter("price_min", e.target.value)} />
        </div>
        <div className="field">
          <label>Qiymət max</label>
          <input value={filters.price_max} onChange={(e) => setFilter("price_max", e.target.value)} />
        </div>
      </div>
      <div className="toolbar">
        <button type="button" className="secondary" onClick={apply}>
          Filteri tətbiq et
        </button>
        <span className="muted">{loading ? "Yüklənir…" : total != null ? `Cəmi: ${total}` : null}</span>
      </div>

      {error ? <div className="error">{error}</div> : null}

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Ad</th>
              <th>Kateqoriya</th>
              <th>Qiymət</th>
              <th>SKU</th>
              <th>yaradılıb</th>
            </tr>
          </thead>
          <tbody>
            {results.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.category_name || p.category}</td>
                <td>{p.price}</td>
                <td>{p.sku}</td>
                <td>{p.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
