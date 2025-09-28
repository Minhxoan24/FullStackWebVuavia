import React, { useState, useRef } from "react";
import { Modal, Button, ProgressBar, Alert } from "react-bootstrap";
import { FaCloudUploadAlt, FaCheckCircle } from "react-icons/fa";
import { uploadAvatar } from "../../../Services/ApiUserService";
import "./ModalUploadAvatar.css";  // Thêm import CSS

export const ModalUploadAvatar = ({ show, handleClose, onSuccess }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [dragOver, setDragOver] = useState(false);
    const [progress, setProgress] = useState(0);
    const [alert, setAlert] = useState({ type: "", message: "" });  // Thay toast bằng alert state
    const fileInputRef = useRef(null);

    const handleFileChange = (file) => {
        if (file && file.type.startsWith("image/")) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setAlert({ type: "", message: "" });  // Clear alert
        } else {
            setAlert({ type: "danger", message: "Vui lòng chọn file ảnh hợp lệ!" });
        }
    };

    const handleInputChange = (e) => {
        const file = e.target.files[0];
        handleFileChange(file);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const file = e.dataTransfer.files[0];
        handleFileChange(file);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = () => {
        setDragOver(false);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setAlert({ type: "warning", message: "Vui lòng chọn ảnh trước!" });
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        setLoading(true);
        setProgress(0);
        setAlert({ type: "", message: "" });

        try {
            // Giả lập progress
            const interval = setInterval(() => {
                setProgress((prev) => {
                    if (prev >= 90) {
                        clearInterval(interval);
                        return 90;
                    }
                    return prev + 10;
                });
            }, 200);

            await uploadAvatar(formData);
            setProgress(100);
            clearInterval(interval);

            setAlert({ type: "success", message: "Avatar đã được cập nhật thành công!" });
            setTimeout(() => {
                onSuccess();
                handleClose();
                setSelectedFile(null);
                setPreview(null);
                setAlert({ type: "", message: "" });
            }, 2000);  // Delay để show success
        } catch (err) {
            console.error("Upload error:", err);
            setAlert({ type: "danger", message: "Có lỗi xảy ra khi upload avatar. Vui lòng thử lại!" });
        } finally {
            setLoading(false);
            setProgress(0);
        }
    };

    const openFileDialog = () => {
        fileInputRef.current.click();
    };

    return (
        <Modal show={show} onHide={handleClose} centered size="md">
            <Modal.Header closeButton>
                <Modal.Title className="d-flex align-items-center">
                    <FaCloudUploadAlt className="me-2 text-primary" />
                    Cập nhật Avatar
                </Modal.Title>
            </Modal.Header>
            <Modal.Body className="text-center p-4">
                {alert.message && (
                    <Alert variant={alert.type} dismissible onClose={() => setAlert({ type: "", message: "" })}>
                        {alert.message}
                    </Alert>
                )}
                <div
                    className={`upload-zone ${dragOver ? "drag-over" : ""}`}
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onClick={openFileDialog}
                    style={{ cursor: "pointer", minHeight: "200px", padding: "2rem", borderRadius: "0.375rem" }}
                >
                    {preview ? (
                        <div className="d-flex flex-column align-items-center">
                            <img
                                src={preview}
                                alt="Preview"
                                className="rounded-circle mb-3 shadow"
                                style={{ width: "120px", height: "120px", objectFit: "cover" }}
                            />
                            <p className="text-muted mb-0">Click để chọn ảnh khác hoặc kéo thả</p>
                        </div>
                    ) : (
                        <div className="d-flex flex-column align-items-center">
                            <FaCloudUploadAlt size={48} className="text-secondary mb-3" />
                            <h5 className="text-muted">Kéo thả ảnh vào đây</h5>
                            <p className="text-muted">hoặc click để chọn file</p>
                        </div>
                    )}
                </div>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleInputChange}
                    style={{ display: "none" }}
                />
                {loading && (
                    <div className="mt-3">
                        <ProgressBar now={progress} label={`${progress}%`} animated />
                        <p className="text-muted mt-2">Đang upload...</p>
                    </div>
                )}
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose} disabled={loading}>
                    Hủy
                </Button>
                <Button variant="primary" onClick={handleUpload} disabled={loading || !selectedFile}>
                    {loading ? "Đang tải..." : "Cập nhật"}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};
