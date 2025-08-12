const ProductCard = ({ product }) => {
    return (
        <div className="product-card">
            <div className="product-logo">

                <img src={product.image} alt={product.name} className="product-image" />
                <div className="product-info">
                </div>
                <div className="product-details">

                </div>
            </div>
        </div>

    );
}