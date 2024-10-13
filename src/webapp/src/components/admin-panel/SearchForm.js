import * as React from "react";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command";
import { useState, useEffect } from 'react';
import { Transition } from '@headlessui/react'

export default function SearchForm({ searchCallback }) {
    const [searchTerm, setSearchTerm] = useState("");
    const [matchedTerm, setMatchedTerm] = useState({});
    const [showDropdown, setShowDropdown] = useState(false); // State to control dropdown visibility

    const handleListItemClick = (cusip) => {
        searchCallback(cusip);
        console.log(cusip)
        setShowDropdown(false); // Close dropdown after selection
    };

    // This effect will run whenever 'searchTerm' changes
    useEffect(() => {
        const fetchData = async () => {
            if (searchTerm.trim() !== "") {
                try {
                    const res = await fetch('/api/match_issuer?text=' + searchTerm);
                    const data = await res.json();
                    if (data.result) {
                        setMatchedTerm(data.result);
                    } else {
                        console.error('Invalid match_issuer response: ', data);
                    }
                } catch (error) {
                    console.error("Error fetching data:", error);
                }
            } else {
                setMatchedTerm([]);
            }
        };

        const timeoutId = setTimeout(() => {
            fetchData();
        }, 100);

        return () => clearTimeout(timeoutId);
    }, [searchTerm]);

    return (
        <div className="relative w-full p-3">
            <Command className={`border shadow-md md:min-w-[450px] ${showDropdown ? 'rounded-lg' : 'rounded-full'}`}>
                <CommandInput
                    placeholder="Type a command or search..."
                    className="w-full text-sm rounded-lg "
                    value={searchTerm}
                    onInput={(e) => setSearchTerm(e.target.value)}
                    onFocus={() => setShowDropdown(true)} // Show dropdown on focus
                />
                {/* Conditionally render CommandList based on showDropdown state */}
                <Transition
                    show={showDropdown}
                    enter="transition ease-out duration-200"
                    enterFrom="transform opacity-0 scale-95"
                    enterTo="transform opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leaveFrom="transform opacity-100 scale-100"
                    leaveTo="transform opacity-0 scale-95"
                >
                    <CommandList>
                        <CommandEmpty>No results found.</CommandEmpty>
                        <CommandGroup heading="Looking up">
                            {matchedTerm.length > 0 && (
                                matchedTerm.map((term, index) => (
                                    <CommandItem key={index} onSelect={() => handleListItemClick(term.cusip)}>
                                        {term.name}
                                    </CommandItem>
                                ))
                            )}
                        </CommandGroup>
                    </CommandList>
                </Transition>
            </Command>
        </div>
    );
}
