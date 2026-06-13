import React, { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient.js";

function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");

  const fetchProducts = async () => {
    console.log("[ACTION] Fetching products...");
    try {
      const res = await axiosClient.get("/products");
      setProducts(res.data);
      console.log("[SUCCESS] Products fetched:", res.data);
    } catch (err) {
      console.error("[ERROR] Fetching products failed:", err);
    }
  };

  const addProduct = async () => {
    console.log(`[ACTION] Adding product: ${name}`);
    try {
      await axiosClient.post("/products", { name });
      console.log(`[SUCCESS] Product added: ${name}`);
      setName("");
      fetchProducts();
    } catch (err) {
      console.error("[ERROR] Adding product failed:", err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div>
      <h2>Products</h2>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Product name"
      />
      <button onClick={addProduct}>Add Product</button>
      <ul>
        {products.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default ProductsPage;
