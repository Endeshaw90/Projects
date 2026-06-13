import React, { useContext } from "react";
import { AuthContext } from "../auth/AuthContext.jsx";

function Navbar({ setPage }) {
  const { logout } = useContext(AuthContext);

  return (
    <nav style={{ display: "flex", gap: "1rem", padding: "1rem", background: "#222", color: "#fff" }}>
      <button onClick={() => setPage("products")}>Products</button>
      <button onClick={() => setPage("customers")}>Customers</button>
      <button onClick={() => setPage("orders")}>Orders</button>
      <button onClick={logout} style={{ marginLeft: "auto" }}>Logout</button>
    </nav>
  );
}

export default Navbar;
