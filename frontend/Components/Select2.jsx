"use client";

import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import * as Icon from "react-bootstrap-icons";

export default function Select2({ props, label, id, onChange }) {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [DropDownList, setDropdownList] = useState(id);

    useEffect(() => {
        setDropdownList(id); // dropdown list when `id` changes
    }, [id]);

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    const handleSearch = (event) => {
        const value = event.target.value.toLowerCase();
        setSearchTerm(value);
        const filteredList = id.filter((item) => item.toLowerCase().includes(value));
        setDropdownList(filteredList);
    };

    const handleSelection = (selectedValue) => {
        console.log(`Selected ${label}:`, selectedValue); 
        props.setFieldValue(label, selectedValue);
        onChange(selectedValue);
        setIsOpen(false);
    };

    return (
        <div className="container mb-4">
            <Form.Group as={Col} md="4" controlId={label}>
                <Form.Label>{label}</Form.Label>
                <Form.Control
                    type="text"
                    value={props.values[label]} 
                    readOnly
                    onClick={toggleDropdown}
                />
                {isOpen && (
                    <div className="dropdown-container">
                        <input
                            type="text"
                            placeholder="Search..."
                            className="form-control"
                            value={searchTerm}
                            onChange={handleSearch}
                        />
                        <ul className="list-group">
                            {DropDownList.map((item, index) => (
                                <li key={index} className="list-group-item" onClick={() => handleSelection(item)}>
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </Form.Group>
        </div>
    );
}
