import React, { useState } from "react";
import axios from "axios";
import ExportVisibleDataButton from "./exportCSV";
import './FilterableTable.css'; // Import the new CSS file

const FilterableTable = () => {
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({
    date_range: "",
    category: "",
    delivery_status: "",
    platform: "",
    state: "",
  });

  const fetchData = () => {
    axios
      .get("http://127.0.0.1:8000/api/filterable-data/", {
        params: filters,
      })
      .then((response) => setData(response.data))
      .catch((error) => console.error(error));
  };

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSearch = () => {
    fetchData(); // Fetch data when the "Search" button is clicked
  };

  const handleClear = () => {
    // Clear the filter values
    setFilters({
      date_range: "",
      category: "",
      delivery_status: "",
      platform: "",
      state: "",
    });
    setData([]); // Optionally clear the data as well
  };

  return (
    <div className="filterable-table-container">
      <h2>Filterable Sales Data Table</h2>
      
      <div className="filters-section">
        <input
          type="text"
          name="date_range"
          value={filters.date_range}
          placeholder="YYYY-MM-DD,YYYY-MM-DD"
          onChange={handleChange}
        />
        <input
          type="text"
          name="category"
          value={filters.category}
          placeholder="Category"
          onChange={handleChange}
        />
        <input
          type="text"
          name="delivery_status"
          value={filters.delivery_status}
          placeholder="Delivery Status"
          onChange={handleChange}
        />
        <input
          type="text"
          name="platform"
          value={filters.platform}
          placeholder="Platform"
          onChange={handleChange}
        />
        <input
          type="text"
          name="state"
          value={filters.state}
          placeholder="State"
          onChange={handleChange}
        />
        <div className="buttons-container">
          <button onClick={handleSearch}>Search</button>
          <button onClick={handleClear}>Clear</button>
        </div>
      </div>

      {/* Conditionally render Export button if data is available */}
      {data.length > 0 && <ExportVisibleDataButton visibleData={data} />}
      
      <table>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Product Name</th>
            <th>Platform</th>
            <th>Quantity Sold</th>
            <th>Selling Price</th>
            <th>Sale Date</th>
            <th>Delivery Status</th>
            <th>State</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.order_id}</td>
              <td>{row.product__product_name}</td>
              <td>{row.platform}</td>
              <td>{row.quantity_sold}</td>
              <td>{row.selling_price}</td>
              <td>{row.date_of_sale}</td>
              <td>{row.delivery__delivery_status}</td>
              <td>{row.delivery__delivery_address_state}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FilterableTable;
