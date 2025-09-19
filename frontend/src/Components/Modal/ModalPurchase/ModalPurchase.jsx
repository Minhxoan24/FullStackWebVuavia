// src/Components/Modal/ModalPurchaseTypeProduct.jsx
import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Modal, Button as BootstrapButton } from "react-bootstrap";

import SpecList from "../../../Components/Product/SpecList";
import QuantityInput from "../../../Components/Product/QuantityInput";
import Button from "../../../Components/Buttons/ButtonBuy";
import { getTypeProductById } from "../../../Services/ApiTypeProduct";
import createOrder from "../../../Services/OrderService";

const ModalPurchaseTypeProduct = ({ show, onClose, id }) => {
  const [product, setProduct] = useState(null);
  const [qty, setQty] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  // Fetch product detail
  useEffect(() => {
    const fetchProduct = async () => {
      if (!id) return;

      setLoading(true);
      setError(null);

      try {
        const data = await getTypeProductById(id);
        setProduct(data);
      } catch (err) {
        setError("Lỗi khi tải sản phẩm.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (show && id) {
      fetchProduct();
    }
  }, [id, show]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat("vi-VN").format(price);
  };

  // xử lý mua hàng
  const handleBuy = async (e) => {
    e.preventDefault();
    const orderData = {
      type_product_id: product?.id,
      quantity: qty,

    };



    // Call createOrder with the orderData
    try {
      const result = await createOrder(orderData);
      console.log("Order created successfully:", result);
      alert("Đơn hàng đã được tạo thành công!");
      onClose();

    }
    catch (error) {
      console.error("Error creating order:", error);
      alert("Đã xảy ra lỗi khi tạo đơn hàng.");
    }


  };

  // Parse description safely
  let descriptionData = {};
  try {
    if (product?.description) {
      descriptionData =
        typeof product.description === "string"
          ? JSON.parse(product.description)
          : product.description;
    }
  } catch (e) {
    console.error("Lỗi parse description:", e);
  }


  return (
    <Modal
      show={show}
      onHide={onClose}
      size="lg"
      centered
      backdrop={true}
      scrollable
    >
      <Modal.Header closeButton>
        <Modal.Title>Chi tiết sản phẩm</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {loading ? (
          <div className="text-center py-4">
            <div className="spinner-border" role="status"></div>
            <p className="mt-2">Đang tải thông tin sản phẩm...</p>
          </div>
        ) : error ? (
          <div className="alert alert-danger">{error}</div>
        ) : product ? (
          <div className="row g-4">
            {/* Hình ảnh */}
            <div className="col-lg-6">
              <img
                src={product.image}
                alt={product.name}
                className="img-fluid rounded"
                style={{ maxHeight: 300, objectFit: "contain" }}
              />
            </div>

            {/* Thông tin */}
            <div className="col-lg-6">
              <h5 className="fw-bold">{product.name}</h5>
              <div className="text-success fw-semibold mb-2">
                Còn sẵn: {product.quantity ?? 0} sản phẩm
              </div>

              <p className="text-danger fs-5 fw-bold">
                {formatPrice(product.price)} đ
              </p>



              <SpecList specs={descriptionData} />
              <div className="my-3">
                <QuantityInput
                  value={qty}
                  min={1}
                  max={product.quantity ?? 1}
                  onChange={setQty}
                />
              </div>

              <div className="mt-3 small text-muted">
                Mã: HMT{String(product.id).padStart(2, "0")}
              </div>
            </div>
          </div>
        ) : (
          <div className="alert alert-warning">
            Không tìm thấy sản phẩm với ID: {id}
          </div>
        )}
      </Modal.Body>

      <Modal.Footer>
        <Button text="MUA TÀI KHOẢN" onClick={handleBuy} />
      </Modal.Footer>
    </Modal>
  );
};

export default ModalPurchaseTypeProduct;
