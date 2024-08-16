"use client";

import React from "react";
import { useState, useEffect } from 'react'

export default function SearchBar({ width, onSearchTermChange }) {
  const [matchedTerm, setMatchedTerm] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [searchHistory, setSearchHistory] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false); // State for dropdown visibility

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
    // Search only if cusip is valid.
    if (matchedTerm.length > 0 && matchedTerm.includes(event.target.value)) {
      onSearchTermChange(event.target.value);
    }
  };

  const handleEnterPress = (event) => {
    if (event.key === 'Enter' && searchTerm) {
      // Check if the search term is already in the history
      if (!searchHistory.includes(searchTerm)) {
        // Do a ticker search
        handleInputChange(event);
        // Insert the new term to the front of the list
        setSearchHistory([searchTerm, ...searchHistory]);
      }
    }
  };

  const handleDeleteTerm = (index) => {
    // Create a new array without the term at the given index
    const newSearchHistory = [...searchHistory];
    newSearchHistory.splice(index, 1);

    // Update the state with the new history
    setSearchHistory(newSearchHistory);
  };

  useEffect(() => {
    if (searchTerm) { // Only fetch if searchTerm is not empty
      fetch('/api/match_issuer?text=' + searchTerm)
        .then((res) => res.json())
        .then((data) => {
          // Validate the data
          if (data.result && data.result.cusipCandidateList) {
            setMatchedTerm(data.result.cusipCandidateList);
          } else {
            console.error('Invalid match_issuer response: ', data);
            // Handle the error appropriately (e.g., display an error message)
          }
        });
    }
  }, [searchTerm]); // Add text to the dependency array

  const handleListItemClick = (cusip) => {
    setSearchTerm(cusip); // Set matchedTerm to term.cusip
    onSearchTermChange(cusip);
    setSearchHistory([searchTerm, ...searchHistory]);
    setShowDropdown(false); // Hide the dropdown after selection
  };

  return (
    <>
      <div style={{ width: width }} className="bg-gray-800 h-screen fixed top-0 left-0 shadow-lg">
        <ul className="flex flex-col items-center  h-full">
          <div className="flex items-center justify-center w-full h-16 bg-gray-700 px-3">
            <input
              type="text"
              placeholder="Search a stock..."
              className="w-full h-10 px-4 rounded-lg bg-gray-200 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchTerm}
              onChange={handleInputChange}
              onKeyDown={handleEnterPress}
              onClick={() => setShowDropdown(true)} // Show dropdown on click
              onBlur={() => setShowDropdown(false)} // Hide dropdown on blur
            />
          </div>
          {showDropdown && ( // Conditional rendering of the dropdown
            <div className=" w-full mt-0">
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
          {/* Add more navigation items here */}
          {searchHistory.length > 0 && searchHistory.map((term, index) => (
            <li key={index} className="my-4 flex items-center">
              <p className="text-white text-xl text-center">{term}</p>
              <button onClick={() => handleDeleteTerm(index)} className="ml-auto">🗑️</button>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
