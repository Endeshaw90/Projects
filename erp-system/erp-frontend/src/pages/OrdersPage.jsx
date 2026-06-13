import React, { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient.js";

function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [description, setDescription] = useState("");

  const fetchOrders = async () => {
    console.log("[ACTION] Fetching orders...");
    try {
      const res = await axiosClient.get("/orders");
      setOrders(res.data);
      console.log("[SUCCESS] Orders fetched:", res.data);
    } catch (err) {
      console.error("[ERROR] Fetching orders failed:", err);
    }
  };

  const addOrder = async () => {
    console.log(`[ACTION] Adding order: ${description}`);
    try {
      await axiosClient.post("/orders", { description });
      console.log(`[SUCCESS] Order added: ${description}`);
      setDescription("");
      fetchOrders();
    } catch (err) {
      console.error("[ERROR] Adding order failed:", err);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  return (
    <div>
      <h2>Orders</h2>
      <input
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Order description"
      />
      <button onClick={addOrder}>Add Order</button>
      <ul>
        {orders.map((o) => (
          <li key={o.id}>{o.description}</li>
        ))}
      </ul>
    </div>
  );
}

export default OrdersPage;
