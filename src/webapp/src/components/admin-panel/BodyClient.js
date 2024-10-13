"use client";

import { useState, useEffect } from 'react'
import { tabs } from "../../lib/tab_list"
import ThirteenF from "./ThirteenF";
import SearchForm from "./SearchForm";

function TabContent({ selectedTab, data }) {
  return (
    <div className="border p-4 rounded-lg">
      {selectedTab === tabs._13_filings && <ThirteenF data={data} />}
    </div>
  );
}

export default function BodyClient({ selectedTab }) {
  const [searchTerm, setSearchTerm] = useState(""); // State to store search text
  const [data, setData] = useState(null);

  const handleSearchCallback = (searchTerm) => {
    setSearchTerm(searchTerm); // Update search text state
  };

  useEffect(() => {
    const fetchData = async () => {
      if (selectedTab === tabs._13_filings && searchTerm) {
        const res = await fetch('/api/get_form?cusip=' + searchTerm);
        const data = await res.json();
          if (data.result) {
          setData(data.result);
        }
      }
    };
    fetchData();
  }, [selectedTab, searchTerm]);

  return (
    <>
      <div className="flex min-h-screen flex-col p-5">
        <SearchForm searchCallback={handleSearchCallback}/>
        <TabContent selectedTab={selectedTab} data={data} />
      </div>
    </>
  );
}
