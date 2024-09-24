import React from "react";
import { useState, useEffect } from 'react'
import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, getKeyValue } from "@nextui-org/react";

function GetThirteenF(cusip) {
    const [data, setData] = useState(null)

    useEffect(() => {
        fetch('/api/get_form?cusip=' + cusip)
            .then((res) => res.json())
            .then((data) => {
                setData(data)
            })
    }, [cusip]) // Add cusip to the dependency array
    return data;
}

export default function ThirteenF({ cusip }) {

    if (!cusip) {
        return <p>Invalid cusip / stock</p>
    }

    var data = GetThirteenF(cusip)

    if (!data) {
        return <p>Loading...</p>
    }

    var rows = [];
    try {
        console.log(data.result)
        rows = data.result.map((owner, index) => ({
          key: index.toString(), 
          cik: owner.cik,
          cik_name: "TODO",
          shares_held: owner.number,
          value: owner.value,
        }));
      } catch (error) {
        console.error("Error processing owner data:", error);
        // Handle the error gracefully, e.g., display a message to the user
      }

    const columns = [
        {
            key: "cik",
            label: "CIK",
        },
        {
            key: "cik_name",
            label: "NAME",
        },
        {
            key: "shares_held",
            label: "SHARS HELD",
        },
        {
            key: "value",
            label: "VALUE",
        },
    ];

    return (
        <>
            <Table aria-label="Example table with dynamic content">
                <TableHeader columns={columns}>
                    {(column) => <TableColumn key={column.key}>{column.label}</TableColumn>}
                </TableHeader>
                <TableBody items={rows}>
                    {(item) => (
                        <TableRow key={item.key}>
                            {(columnKey) => <TableCell>{getKeyValue(item, columnKey)}</TableCell>}
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </>
    )
}
