import React from "react";

const QuantityInput = ({ value, min = 1, max = 10, onChange }) => {
    const handleIncrease = () => {
        if (value < max) {
            onChange(value + 1);
        }
    };

    const handleDecrease = () => {
        if (value > min) {
            onChange(value - 1);
        }
    };

    const handleChange = (e) => {
        const newValue = parseInt(e.target.value, 10);
        if (!isNaN(newValue) && newValue >= min && newValue <= max) {
            onChange(newValue);
        }
    };

    return (
        <div className="d-flex align-items-center">
            <button
                className="btn btn-outline-secondary btn-sm"
                onClick={handleDecrease}
                disabled={value <= min}
            >
                -
            </button>
            <input
                type="number"
                className="form-control text-center mx-2"
                style={{ width: "60px" }}
                value={value}
                min={min}
                max={max}
                onChange={handleChange}
            />
            <button
                className="btn btn-outline-secondary btn-sm"
                onClick={handleIncrease}
                disabled={value >= max}
            >
                +
            </button>
        </div>
    );
};

export default QuantityInput;
