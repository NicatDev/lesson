import { Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import CategoriesPage from "./pages/CategoriesPage.jsx";
import CreateProductPage from "./pages/CreateProductPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import ProductsPage from "./pages/ProductsPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import { logout } from "./api.js";

function Layout({ children }) {
  const navigate = useNavigate();
  const authed = !!localStorage.getItem("access");

  return (
    <div className="layout">
      <header className="header">
        <Link to="/" className="brand">
          Mağaza
        </Link>
        <nav className="nav">
          <Link to="/categories">Kateqoriyalar</Link>
          <Link to="/products">Məhsullar</Link>
          <Link to="/products/new">Məhsul yarat</Link>
          <a href="/api/docs/" target="_blank" rel="noreferrer">
            Swagger
          </a>
          {!authed ? (
            <>
              <Link to="/login">Giriş</Link>
              <Link to="/register">Qeydiyyat</Link>
            </>
          ) : (
            <button
              type="button"
              className="linkish"
              onClick={() => {
                logout();
                navigate("/login");
              }}
            >
              Çıxış
            </button>
          )}
        </nav>
      </header>
      <main className="main">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/products" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/categories" element={<CategoriesPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/products/new" element={<CreateProductPage />} />
        <Route path="*" element={<p className="muted">Səhifə tapılmadı.</p>} />
      </Routes>
    </Layout>
  );
}
