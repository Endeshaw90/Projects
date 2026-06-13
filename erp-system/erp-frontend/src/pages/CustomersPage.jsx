import React, { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient.js";

function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState("");

  const fetchCustomers = async () => {
    console.log("[ACTION] Fetching customers...");
    try {
      const res = await axiosClient.get("/customers");
      setCustomers(res.data);
      console.log("[SUCCESS] Customers fetched:", res.data);
    } catch (err) {
      console.error("[ERROR] Fetching customers failed:", err);
    }
  };

  const addCustomer = async () => {
    console.log(`[ACTION] Adding customer: ${name}`);
    try {
      await axiosClient.post("/customers", { name });
      console.log(`[SUCCESS] Customer added: ${name}`);
      setName("");
      fetchCustomers();
    } catch (err) {
      console.error("[ERROR] Adding customer failed:", err);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  return (
    <div>
      <h2>Customers</h2>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Customer name"
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((c) => (
          <li key={c.id}>{c.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default CustomersPage;
