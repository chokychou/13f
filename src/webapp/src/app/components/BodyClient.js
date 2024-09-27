"use client";

import { useState, useEffect } from 'react'
import { tabs } from "./tab_list"
import ThirteenF from "./ThirteenF";
import SearchForm from "./SearchForm";

function TabContent({ selectedTab, data }) {
  return (
    <div className="border p-4 rounded-lg">
      {selectedTab === tabs._13_filings && <ThirteenF data={data} />}
    </div>
  );
}

export default function BodyClient({ width: searchbarWidth, selectedTab /* Choose  */ }) {
  var styles = { width: `calc(100% - ${searchbarWidth})`, position: "relative", left: searchbarWidth, top: 0, height: "100vh" };
  const [searchTerm, setSearchTerm] = useState(""); // State to store search text
  const [matchedTerm, setMatchedTerm] = useState({});
  const [showDropdown, setShowDropdown] = useState(false); // State for dropdown visibility
  const [data, setData] = useState(null);

  const handleSearchCallback = (searchTerm) => {
    setSearchTerm(searchTerm); // Update search text state
  };

  const handleListItemClick = (cusip) => {
    setSearchTerm(cusip); // Set matchedTerm to term.cusip
    setShowDropdown(false); // Hide the dropdown after selection
  };
  

  useEffect(() => {
    if (searchTerm) { // Only fetch if searchTerm is not empty
      fetch('/api/match_issuer?text=' + searchTerm)
        .then((res) => res.json())
        .then((data) => {
          // Validate the data
          if (data.result) {
            setMatchedTerm(data.result);
          } else {
            console.error('Invalid match_issuer response: ', data);
            // Handle the error appropriately (e.g., display an error message)
          }
        });
    }
  }, [searchTerm]); // Add text to the dependency array


  useEffect(() => {
    const fetchData = async () => {
      if (selectedTab === tabs._13_filings && searchTerm) {
        console.log("Fetching 13F data");
        const res = await fetch('/api/get_form?cusip=' + searchTerm);
        const data = await res.json();
        if (data.result)
          setData(data.result);
      }
    };
    fetchData();
  }, [selectedTab, searchTerm]);

  return (
    <>
      <div style={styles} className="flex min-h-screen flex-col p-5">
        <SearchForm searchCallback={handleSearchCallback} setShowDropdown={setShowDropdown} />

        {showDropdown && ( // Conditional rendering of the dropdown
          <div className=" w-full mt-0 ">
            <ul className="w-full absolute bg-gray-700 rounded-md shadow-md z-10">
              {matchedTerm.length > 0 && ( // Only map if matchedTerm is not empty
                matchedTerm.map((term, index) => (
                  <li
                    key={index}
                    className="px-4 py-2 hover:bg-gray-100"
                    onMouseDown={() => { handleListItemClick(term.cusip); }}
                  >
                    {term.name}
                  </li>
                ))
              )}
            </ul>
          </div>
        )}

        <TabContent selectedTab={selectedTab} data={data} />
      </div>
    </>
  );
}
