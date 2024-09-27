"use client";

import React from "react";
import { useState, useEffect } from 'react'
import Button from 'react-bootstrap/Button';
import { tabs } from "./tab_list"

function RenderSidebar({ callback }) {
  const [selectedTab, setSelectedTab] = useState(tabs._13_filings);

  const handleTabClick = (tabName) => {
    setSelectedTab(tabName);
    if (callback) {
      callback(tabName);
    }
  };

  return (
    <>
      <div className="flex items-center justify-center h-16 bg-gray-900">
        <span className="text-white font-bold uppercase">Dashboard</span>
      </div>
      <Button variant={selectedTab === tabs._13_filings ? "primary bg-blue-500 text-white" : "secondary"} onClick={() => handleTabClick(tabs._13_filings)}>
        13 Filings
      </Button>
    </>
  );
}

export default function NavBarClient({ width, selectedTabCallback }) {
  return (
    <>
      <div style={{ width: width }} className="hidden md:flex flex-col w-64 bg-gray-800 h-screen fixed top-0 left-0 shadow-lg">
        <RenderSidebar callback={selectedTabCallback} />
      </div>
    </>
  );
}
