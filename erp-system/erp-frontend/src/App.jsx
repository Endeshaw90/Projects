import React, { useState, useContext } from "react";
import { AuthProvider, AuthContext } from "./auth/AuthContext.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import ProductsPage from "./pages/ProductsPage.jsx";
import CustomersPage from "./pages/CustomersPage.jsx";
import OrdersPage from "./pages/OrdersPage.jsx";
import Navbar from "./components/Navbar.jsx";

function AppContent() {
  const { token } = useContext(AuthContext);   // ✅ read token directly from context
  const [page, setPage] = useState("products");

  if (!token) {
    return <LoginPage />;
  }

  return (
    <div>
      <Navbar setPage={setPage} />
      {page === "products" && <ProductsPage />}
      {page === "customers" && <CustomersPage />}
      {page === "orders" && <OrdersPage />}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
