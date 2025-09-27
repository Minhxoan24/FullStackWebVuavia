// src/Components/Modal/ModalPurchaseTypeProduct.jsx
import React, { useEffect, useState, useRef, useCallback } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./ModalPurchase.css";

import SpecList from "../../../Components/Product/SpecList";
import QuantityInput from "../../../Components/Product/QuantityInput";
import Button from "../../../Components/Buttons/ButtonBuy";
import { getTypeProductById } from "../../../Services/ApiTypeProduct";
import createOrder from "../../../Services/OrderService";
import ConfirmPurchaseModal from "../../../Components/Modal/ConfirmModal/ConfirmModal.js";
import { AuthContext } from '../../../Context/AuthContext.jsx';

const ModalPurchaseTypeProduct = ({ show, onClose, id }) => {
  const [product, setProduct] = useState(null);
  const [qty, setQty] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleCloseConfirm = () => setShowConfirm(false);
  const handleShowConfirm = () => setShowConfirm(true);
  const { refreshUser } = React.useContext(AuthContext);

  const dialogRef = useRef(null);
  const firstFieldRef = useRef(null);

  useEffect(() => {
    if (!show) return;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    firstFieldRef.current?.focus();

    const onKey = (e) => {
      if (e.key === "Escape") onClose();
      if (e.key === "Tab" && dialogRef.current) {
        const focusables = dialogRef.current.querySelectorAll(
          'a[href],button:not([disabled]),textarea,input,select,[tabindex]:not([tabindex="-1"])'
        );
        if (!focusables.length) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
    };
  }, [show, onClose]);

  const onBackdropClick = useCallback((e) => {
    if (e.target === e.currentTarget) onClose();
  }, [onClose]);

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
    handleShowConfirm();
  };

  const handleConfirmPurchase = async () => {
    if (!product) {
      alert("Sản phẩm chưa được tải. Vui lòng thử lại.");
      return;
    }

    const orderdata = {
      type_product_id: product.id,
      quantity: qty,
      discount_amount: 0,
    };

    handleCloseConfirm();
    try {
      const result = await createOrder(orderdata);
      console.log("Order created successfully:", result);
      alert("Đơn hàng đã được tạo thành công!");
      await refreshUser();
      onClose();
    } catch (error) {
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

  if (!show) return null;

  return (
    <>
      <div className="modal-backdrop-custom" onClick={onBackdropClick}>
        <div
          className="modal-dialog modal-lg modal-dialog-centered"
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
        >
          <div className="modal-content custom-modal">
            <div className="modal-header">
              {/* <h5 className="modal-title">Chi tiết sản phẩm</h5> */}
              {/* <button
                type="button"
                className="btn-close"
                onClick={onClose}
                aria-label="Close"
              ></button> */}
            </div>
            <div className="modal-body">
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
                    <div className="my-3 d-flex align-items-center gap-3">
                      <QuantityInput
                        value={qty}
                        min={1}
                        max={product.quantity ?? 1}
                        onChange={setQty}
                      />
                      <Button text="MUA TÀI KHOẢN" onClick={handleBuy} />
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
            </div>
          </div>
        </div>
      </div>
      <ConfirmPurchaseModal
        show={showConfirm}
        onClose={handleCloseConfirm}
        onConfirm={handleConfirmPurchase}
      />
    </>
  );
};

export default ModalPurchaseTypeProduct;
