import React from "react";
import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, getKeyValue } from "@nextui-org/react";

export default function ThirteenF({ data }) {
    if (!data) {
        return <p>Invalid cusip / stock</p>
    }

    if (!data) {
        return <p>Loading...</p>
    }

    var rows = [];
    try {
        rows = data.map((owner, index) => ({
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
