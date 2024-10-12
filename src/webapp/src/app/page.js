"use client";

import { useState } from "react";
import BodyClient from "./components/BodyClient"
import NavBarClient from "./components/NavBarClient"
import { tabs } from "../lib/tab_list"


export default function Home() {
  // TODO: deprecate
  const searchbarWidth = "20%";

  const [selectedTab, setSelectedTab] = useState(tabs._13_filings); 

  const handleTabChange = (tabName) => {
    setSelectedTab(tabName);
  };

  return (
    <>
      <NavBarClient selectedTabCallback={handleTabChange} /> 
      <BodyClient width={searchbarWidth} selectedTab={selectedTab} />
    </>
  );
}