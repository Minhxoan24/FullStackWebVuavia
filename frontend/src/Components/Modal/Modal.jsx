import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import './Modal.css';

// Reusable Modal component
const Modal = ({ visible, title, message, type = 'info', onClose, onConfirm, showConfirm = false, confirmText = 'OK' }) => {
    const modalRef = useRef(null);
    const previousActive = useRef(null);
    const [rendered, setRendered] = useState(visible);
    const [phase, setPhase] = useState(visible ? 'idle' : 'exit');
    const [confirming, setConfirming] = useState(false);

    useEffect(() => {
        if (visible) {
            setRendered(true);
            setPhase('enter');
            const raf = requestAnimationFrame(() => requestAnimationFrame(() => setPhase('idle')));
            return () => cancelAnimationFrame(raf);
        }
        if (!visible && rendered) {
            setPhase('exit');
            const t = setTimeout(() => setRendered(false), 260);
            return () => clearTimeout(t);
        }
    }, [visible, rendered]);

    useEffect(() => {
        if (!rendered) return;
        previousActive.current = document.activeElement;
        document.body.classList.add('fp-modal-open');

        const t = setTimeout(() => {
            if (modalRef.current) {
                const focusEl = modalRef.current.querySelector('button, [tabindex]') || modalRef.current;
                try { focusEl.focus(); } catch (_) {}
            }
        }, 60);

        const onKey = (e) => { if (e.key === 'Escape' && typeof onClose === 'function') onClose(); };
        window.addEventListener('keydown', onKey);
        return () => {
            clearTimeout(t);
            window.removeEventListener('keydown', onKey);
            document.body.classList.remove('fp-modal-open');
            try { previousActive.current?.focus?.(); } catch (_) {}
        };
    }, [rendered, onClose]);

    if (!rendered) return null;

    const iconClass = type === 'success' ? 'fa-check-circle text-success' : type === 'error' ? 'fa-exclamation-circle text-danger' : 'fa-info-circle text-primary';

    const handleBackdropClick = (e) => {
        if (e.target !== e.currentTarget) return;
        // If the modal was shown as a confirm dialog, treat backdrop click as confirm
        if (showConfirm && typeof onConfirm === 'function') {
            try {
                // call onConfirm; caller usually handles closing
                onConfirm();
            } catch (err) {
                // fallback to close
                if (typeof onClose === 'function') onClose();
            }
            return;
        }

        if (typeof onClose === 'function') onClose();
    };

    const handleConfirm = async () => {
        if (typeof onConfirm !== 'function') {
            if (typeof onClose === 'function') onClose();
            return;
        }
        try {
            const maybePromise = onConfirm();
            if (maybePromise && typeof maybePromise.then === 'function') {
                setConfirming(true);
                await maybePromise;
                setConfirming(false);
            }
            if (typeof onClose === 'function') onClose();
        } catch (err) {
            setConfirming(false);
            try { modalRef.current?.focus(); } catch (_) {}
        }
    };

    const modalContent = (
        <div className={`fp-modal-backdrop fp-modal-backdrop--${phase}`} role="dialog" aria-modal="true" onClick={handleBackdropClick}>
            <div
                className={`fp-modal fp-modal--${type} fp-modal--phase-${phase}`}
                role="document"
                onClick={(e) => e.stopPropagation()}
                ref={modalRef}
                tabIndex={-1}
                aria-labelledby="fp-modal-title"
            >
                <div className="fp-modal__header d-flex align-items-center gap-3">
                    <i className={`fas ${iconClass} fp-modal__icon fa-2x`} aria-hidden="true" />
                    <h5 id="fp-modal-title" className="fp-modal__title">{title}</h5>
                    {/* Only show close button when explicitly requested (showConfirm true) */}
                    {showConfirm ? <button type="button" className="fp-modal__close" aria-label="Đóng" onClick={onClose}>&times;</button> : null}
                </div>
                <div className="fp-modal__body">
                    <p>{message}</p>
                </div>
                <div className="fp-modal__footer">
                    {showConfirm ? (
                        <button className="btn btn-primary d-flex align-items-center" onClick={handleConfirm} disabled={confirming}>
                            {confirming ? (<span className="spinner-border spinner-border-sm me-2" />) : null}
                            <span>{confirmText}</span>
                        </button>
                    ) : null}
                </div>
            </div>
        </div>
    );

    // Render modal into document.body to avoid stacking-context issues
    return ReactDOM.createPortal(modalContent, document.body);
};

export default Modal;
