"use client";

import { useState } from "react";
import Button from 'react-bootstrap/Button';
import ThirteenF from "./ThirteenF";

const tab_filings = "13 Filings";

function TabContent({ selectedTab, cusip }) {
    switch (selectedTab) {
        case tab_filings:
            return (
                <div className="border p-4 rounded-lg">
                    <ThirteenF cusip={cusip} />
                </div>
            );
        default:
            return (
                <div className="border p-4 rounded-lg">
                    <p>Select tab above</p>
                </div>
            );
    }
}

export default function BodyClient({ width: searchbarWidth, cusip }) {
    const [selectedTab, setSelectedTab] = useState("Empty");

    const handleTabClick = (tabName) => {
        setSelectedTab(tabName);
    };

    Button.defaultProps = {
        className: "px-4 py-2 rounded-lg mr-2",
    };

    var styles = { width: `calc(100% - ${searchbarWidth})`, position: "relative", left: searchbarWidth, top: 0, height: "100vh" };

    return (
        <>
            <div style={ styles } className="flex min-h-screen flex-col p-5">
                <div className="flex mb-8">
                    <Button variant={selectedTab === tab_filings ? "primary bg-blue-500 text-white" : "secondary"} onClick={() => handleTabClick(tab_filings)}>
                        Filings
                    </Button>
                </div>

                <TabContent selectedTab={selectedTab} cusip={cusip} />
            </div>
        </>
    );
}
