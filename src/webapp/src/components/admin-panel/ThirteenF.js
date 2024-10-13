import React, { useState } from "react";
import {
    Table,
    TableHeader,
    TableColumn,
    TableBody,
    TableRow,
    TableCell,
    getKeyValue,
} from "@nextui-org/react";

function handleSortHelper(a, b, key) {
    // Handle numeric sorting for 'shares_held' and 'value'
    if (key === "shares_held" || key === "value") {
        return a[key] - b[key];
    } else {
        // Handle string sorting for other keys
        return a[key].localeCompare(b[key]);
    }
}

function handleSort(rows, sortConfig) {
    const sortedRows = [...rows]; // Create a copy to avoid mutating the original array

    if (sortConfig.direction === "ascending") {
        sortedRows.sort((a, b) => {
            return handleSortHelper(a, b, sortConfig.key)
        });
    }

    if (sortConfig.direction === "descending") {
        sortedRows.sort((a, b) => {
            return handleSortHelper(b, a, sortConfig.key)
        });
    }

    return sortedRows;
}

export default function ThirteenF({ data }) {
    var rows;

    const [sortConfig, setSortConfig] = useState({ key: null, direction: null });

    if (!data) {
        return;
    }

    try {
        rows = data.map((owner, index) => ({
            key: index.toString(),
            cik_name: owner.name,
            shares_held: owner.number,
            value: owner.value,
            last_updated_date: new Date(owner.last_updated_date).toLocaleDateString(
                "en-US",
                { month: "2-digit", day: "2-digit", year: "numeric" }
            ),
        }));
    } catch (error) {
        console.error("Error processing owner data:", error);
        // Handle the error gracefully, e.g., display a message to the user
    }

    const columns = [
        {
            key: "cik_name",
            label: "NAME (CIK)",
        },
        {
            key: "shares_held",
            label: "SHARS HELD",
        },
        {
            key: "value",
            label: "VALUE",
        },
        {
            key: "last_updated_date",
            label: "REPORT DATE",
        },
    ];

    return (
        <div className="flex flex-col gap-3 p-3">
            <Table
                aria-label="Example table with dynamic content"
                selectionMode="single"
                defaultSelectedKeys={["2"]}
                className="text-sm border rounded-lg"
            >
                <TableHeader columns={columns}>
                    {(column) => (
                        <TableColumn key={column.key}>
                            <button onClick={() =>
                                setSortConfig({
                                    key: column.key,
                                    direction:
                                        sortConfig.direction === "ascending"
                                            ? "descending"
                                            : "ascending",
                                })
                            }>
                                <span style={{ display: sortConfig.key === column.key ? 'inline' : 'none' }}>
                                    {sortConfig.key === column.key &&
                                        sortConfig.direction === "ascending"
                                        ? " ▲"
                                        : " ▼"}
                                </span>
                                {column.label}
                            </button>
                        </TableColumn>
                    )}
                </TableHeader>
                <TableBody
                    items={sortConfig.key ? handleSort(rows, sortConfig) : rows}
                >
                    {(item) => (
                        <TableRow key={item.key}>
                            {(columnKey) => (
                                <TableCell>{getKeyValue(item, columnKey)}</TableCell>
                            )}
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
}
