"use client";

import { useState } from "react";
import BodyClient from "./components/BodyClient"
import NavBarClient from "./components/NavBarClient"
import { tabs } from "./components/tab_list"


export default function Home() {
  const searchbarWidth = "20%";

  const [selectedTab, setSelectedTab] = useState(tabs._13_filings); 

  const handleTabChange = (tabName) => {
    setSelectedTab(tabName);
  };

  return (
    <>
      <NavBarClient width={searchbarWidth} selectedTabCallback={handleTabChange} /> 
      <BodyClient width={searchbarWidth} selectedTab={selectedTab} />
    </>
  );
}