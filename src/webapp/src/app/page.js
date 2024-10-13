"use client";

import { useState } from "react";
import BodyClient from "./components/BodyClient"
import { tabs } from "../lib/tab_list"
import { Sidebar } from "../components/admin-panel/sidebar";
import { cn } from "@/lib/utils";
import { useStore } from "@/hooks/use-store";
import { useSidebar } from "@/hooks/use-sidebar";


export default function Home() {
  const [selectedTab, setSelectedTab] = useState(""); 

  const sidebar = useStore(useSidebar, (x) => x);
  if (!sidebar) return null;
  const { getOpenState, settings } = sidebar;

  const handleTabChange = (tabName) => {
    setSelectedTab(tabName);
  };

  return (
    <>
      <Sidebar selectedTabCallback={handleTabChange} /> 
      <main
        className={cn(
          "min-h-[calc(100vh_-_56px)] bg-zinc-50 dark:bg-zinc-900 transition-[margin-left] ease-in-out duration-300",
          !settings.disabled && (!getOpenState() ? "lg:ml-[90px]" : "lg:ml-72")
        )}
      >
        <BodyClient selectedTab={selectedTab} />
      </main>
    </>
  );
}