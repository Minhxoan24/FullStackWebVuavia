import React from "react";

const QuantityInput = ({ value, onChange, min = 1, max = 99 }) => {
    const dec = () => onChange(Math.max(min, (value || 1) - 1));
    const inc = () => onChange(Math.min(max, (value || 1) + 1));

    return (
        <div className="d-inline-flex align-items-center border rounded">
            <button type="button" className="btn btn-light" onClick={dec}>-</button>
            <input
                type="number"
                className="form-control text-center border-0"
                style={{ width: 72 }}
                value={value}
                min={min}
                max={max}
                onChange={(e) => {
                    const n = Number(e.target.value);
                    if (Number.isNaN(n)) return;
                    onChange(Math.max(min, Math.min(max, n)));
                }}
            />
            <button type="button" className="btn btn-light" onClick={inc}>+</button>
        </div>
    );
};

export default QuantityInput;
