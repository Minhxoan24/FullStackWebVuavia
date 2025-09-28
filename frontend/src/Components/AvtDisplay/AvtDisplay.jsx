import React, { useState } from "react";
import { ModalUploadAvatar } from "../Modal/ModalUploadAvatar/ModalUploadAvatar";

const AvatarDisplay = ({ avatarUrl, onAvatarUpdated }) => {
    const [showModal, setShowModal] = useState(false);

    return (
        <div className="avatar-container position-relative d-inline-block">
            <img
                src={avatarUrl}
                alt="Avatar"
                className="rounded-circle"
                style={{ width: "100px", height: "100px", objectFit: "cover" }}
            />
            <div
                className="avatar-overlay"
                onClick={() => setShowModal(true)}
            >
                <i className="bi bi-pencil-fill"></i>
            </div>

            {showModal && (
                <ModalUploadAvatar
                    show={showModal}
                    handleClose={() => setShowModal(false)}
                    onSuccess={onAvatarUpdated}
                />
            )}
        </div>
    );
};

export default AvatarDisplay;
