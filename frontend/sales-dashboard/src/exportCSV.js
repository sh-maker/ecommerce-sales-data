import React from "react";
import './exportCSV.css';  // Import the CSS file for the button

const ExportVisibleDataButton = ({ visibleData }) => {
  const handleExport = () => {
    if (!visibleData || visibleData.length === 0) {
      alert("No data available to export!");
      return;
    }

    // Create CSV content
    const headers = [
      "Order ID",
      "Category",
      "Platform",
      "Quantity Sold",
      "Selling Price",
      "Date of Sale",
      "Delivery Status",
      "Delivery State",
    ];
    const csvRows = [headers.join(",")];
    visibleData.forEach((row) => {
      csvRows.push(
        [
          row.order_id,
          row.product__category,
          row.platform,
          row.quantity_sold,
          row.selling_price,
          row.date_of_sale,
          row.delivery__delivery_status,
          row.delivery__delivery_address_state,
        ].join(",")
      );
    });
    const csvContent = csvRows.join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    // Create download link
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "visible_data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="export-button-container">
      <button className="export-button" onClick={handleExport}>
        Export Data
      </button>
    </div>
  );
};

export default ExportVisibleDataButton;
