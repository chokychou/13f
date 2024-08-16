"use client";

import { useState } from "react";

import BodyClient from "./components/BodyClient"
import SearchBarClient from "./components/SearchBarClient"

export default function Home() {
  const searchbarWidth = "20%";
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchTermChange = (newSearchTerm) => {
    setSearchTerm(newSearchTerm);
  };

  return (
    <>
      <SearchBarClient width={searchbarWidth} onSearchTermChange={handleSearchTermChange} />
      <BodyClient width={searchbarWidth} cusip={searchTerm} />
    </>
  );
}