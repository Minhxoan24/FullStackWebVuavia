import React from "react";

const SpecList = ({ specs }) => {
    if (!specs || Object.keys(specs).length === 0) {
        return <p className="text-muted">Không có thông số kỹ thuật.</p>;
    }

    return (
        <ul className="list-unstyled">
            {Object.entries(specs).map(([key, value]) => (
                <li key={key} className="mb-1">
                    <strong>{key}:</strong> {value}
                </li>
            ))}
        </ul>
    );
};

export default SpecList;
