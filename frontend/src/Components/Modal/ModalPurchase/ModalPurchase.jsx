import React, { useContext, useState } from "react";
import { Modal, Button, Form, Alert, Spinner } from "react-bootstrap";
import { AuthContext } from "../../Context/AuthContext";

const ModalPurchase = ({ show, close, product }) => {
  const { user } = useContext(AuthContext);

  // State quản lý
  const [quantity, setQuantity] = useState(1);
  const [selectedVoucher, setSelectedVoucher] = useState(null);
  const [vouchers] = useState([]); // bạn có thể load từ API
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Tính tổng tiền
  const totalPrice = product
    ? (product.price - (selectedVoucher?.discount || 0)) * quantity
    : 0;

  // Đóng modal
  const handleCloseModal = () => {
    close();
    setQuantity(1);
    setSelectedVoucher(null);
    setError("");
    setSuccess(false);
  };

  // Áp dụng voucher
  const handleApplyVoucher = (voucher) => {
    setSelectedVoucher(voucher);
  };

  // Xử lý thanh toán
  const handleCheckout = async () => {
    setLoading(true);
    try {
      // TODO: gọi API thanh toán ở đây
      setTimeout(() => {
        setSuccess(true);
        setLoading(false);
      }, 1500);
    } catch (err) {
      setError("Thanh toán thất bại, vui lòng thử lại!");
      setLoading(false);
    }
  };

  if (!product) return null;

  return (
    <Modal show={show} onHide={handleCloseModal} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>Mua sản phẩm: {product.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {success && (
          <Alert variant="success">Thanh toán thành công! Đang chuyển hướng...</Alert>
        )}
        {error && <Alert variant="danger">{error}</Alert>}

        <div className="row">
          <div className="col-md-6">
            <img
              src={product.image}
              alt={product.name}
              className="img-fluid"
            />
            <p className="mt-2">{product.description}</p>
          </div>
          <div className="col-md-6">
            <Form.Group className="mb-3">
              <Form.Label>Số lượng</Form.Label>
              <Form.Control
                type="number"
                min="1"
                max={product.quantity}
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
              />
              <Form.Text>Còn lại: {product.quantity}</Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Voucher</Form.Label>
              <Form.Select
                onChange={(e) => {
                  const voucherId = e.target.value;
                  const voucher = vouchers.find((v) => v.id == voucherId);
                  if (voucher) handleApplyVoucher(voucher);
                  else setSelectedVoucher(null);
                }}
              >
                <option value="">Chọn voucher</option>
                {vouchers.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.code} - Giảm {v.discount}₫
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <h5>Tổng tiền: {totalPrice.toLocaleString("vi-VN")} ₫</h5>
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleCloseModal}>
          Hủy
        </Button>
        <Button
          variant="primary"
          onClick={handleCheckout}
          disabled={loading}
        >
          {loading ? <Spinner animation="border" size="sm" /> : "Thanh toán"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalPurchase;
