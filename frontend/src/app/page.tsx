"use client";

import { useEffect, useState } from "react";

export default function EditableTableComponent() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [username, setUsername] = useState("");

  // Function to fetch items from the API
  const fetchItems = async () => {
    setLoading(true);
    setError(null); // Reset error state
    try {
      const response = await fetch("/api/"); // Adjust the endpoint
      if (!response.ok) {
        throw new Error("Failed to fetch items");
      }
      const data = await response.json();
      setItems(data);
    } catch (error) {
      console.error("Error fetching items:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems(); // Initial fetch
    const intervalId = setInterval(fetchItems, 60000);
    return () => clearInterval(intervalId);
  }, []);

  const [editableItems, setEditableItems] = useState([]);

  useEffect(() => {
    // Create editable states for each item
    const initializedEditableItems = items.map(item => ({
      id: item.pk_id,
      name: item.name,
      is_active: item.is_active,
      created_date: item.created_date,
      modified_date: item.modified_date
    }));
    setEditableItems(initializedEditableItems);
  }, [items]);

  // Function to handle updates to an item
  const handleUpdate = async (id, name, isActive) => {
    try {
        const formData = new FormData();
        formData.append("pk_id", id);
        formData.append("name", name);
        formData.append("is_active", isActive);
    //   const updatedItem = { pk_id:id, name, is_active: isActive }; // Only include necessary fields
      const response = await fetch("/api/update", {
        method: "PUT",
        // headers: { "Content-Type": "application/json" },
        body: formData
      });

      if (!response.ok) {
        // console.log(updatedItem)
        throw new Error("Failed to update item");
      }

      await fetchItems(); // Refresh the table after update
    } catch (error) {
      console.error("Error updating item:", error);
      setError(error.message);
    }
  };

  const handleInputChange = (id, newName) => {
    setEditableItems((prevItems) =>
      prevItems.map((item) =>
        item.id === id ? { ...item, name: newName } : item
      )
    );
  };

  const handleCheckboxChange = (id, newIsActive) => {
    setEditableItems((prevItems) =>
      prevItems.map((item) =>
        item.id === id ? { ...item, is_active: newIsActive } : item
      )
    );
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null); // Reset error state

    try {
      const response = await fetch("/api/testing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name:username }),
      });
      if (!response.ok) {
        throw new Error("Failed to submit data");
      }

      // Fetch updated data after submission
      await fetchItems();
      setUsername(""); // Clear the input field
    } catch (error) {
      console.error("Error submitting data:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
        <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
          required
          className="border p-2"
        />
        <button type="submit" className="bg-blue-500 text-white p-2 ml-2">
          Submit
        </button>
        {loading && <p>Loading...</p>}
        {error && <p className="text-red-500">{error}</p>}
      </form>

      <h1>Editable Items Table</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <table className="min-w-full border">
        <thead>
          <tr>
            <th className="border">ID</th>
            <th className="border">Name</th>
            <th className="border">Active</th>
            <th className="border">Action</th>
            <th className="border">Created at </th>
            <th className="border">Modified at </th>
          </tr>
        </thead>
        <tbody>
          {editableItems.map((item) => (
            <tr key={item.id}>
              <td className="border">{item.id}</td>
              
              <td className="border">
                <input
                  type="text"
                  value={item.name} // Controlled input
                  onChange={(e) => handleInputChange(item.id, e.target.value)}
                />
              </td>
              <td className="border">
                <input
                  type="checkbox"
                  checked={item.is_active} // Controlled checkbox
                  onChange={(e) => handleCheckboxChange(item.id, e.target.checked)}
                />
              </td>
              <td className="border">
                <button
                  onClick={() => handleUpdate(item.id, item.name, item.is_active)}
                  className="bg-green-500 text-white p-1"
                >
                  Save
                </button>
              </td>
              <td className="border">{item.created_date}</td>
              <td className="border">{item.modified_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}