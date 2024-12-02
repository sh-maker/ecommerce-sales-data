import React from "react";
import ImportCSV from "./ImportCSV";
import FilterableTable from "./FilterableTable";
import './App.css';

const App = () => {
  return (
    <div className="App">
      <h1>Sales Dashboard</h1>
      <ImportCSV />
      <FilterableTable />
    </div>
  );
};

export default App;
