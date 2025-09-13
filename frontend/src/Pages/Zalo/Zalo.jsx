import { Container, Row, Col, Button } from "react-bootstrap";
import "./Zalo.css";
import React, { useState, useEffect } from "react";
import Logo from "../../Assets/Logo/Logo";
import ProductCard from "../../Components/Card/ProdcutCard2.jsx";
import { getListtypeproductByCateGory } from "../../Services/ApiTypeProduct.jsx";

const Zalo = () => {
    const [dataTypeProduct, setDataTypeProduct] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getListtypeproductByCateGory(3);
                setDataTypeProduct(data || []);
                console.log("Sản phẩm đã tải:", data);
                setError(null);
            } catch (error) {
                console.error("Lỗi khi tải sản phẩm:", error);
                setError("Không thể tải sản phẩm. Vui lòng thử lại.");
                setDataTypeProduct([]);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div className="text-center">Đang tải...</div>;
    }

    if (error) {
        return <div className="text-center text-danger">{error}</div>;
    }

    return (
        <div className="accviet">
            {/* Banner */}
            <div className="banner-section">
                <Container>
                    <Row className="align-items-center">
                        <Col md={6}>
                            <h2 className="fw-bold text-primary">
                                Mua Nick, tài khoản Zalo trắng, cổ
                            </h2>
                            <p className="mt-3">
                                Chào mừng bạn đến với <strong>VuaVia.VN</strong>. Chúng tôi là một đơn vị cung cấp Nick, Tài khoản Zalo trắng, cổ đã có hoặc chưa có bạn bè. Đã có sẵn bạn bè, bảo mật thông tin, uy tín.


                            </p>
                            <div className="mt-4">
                                <Button variant="outline-danger" className="me-3">MUA NGAY</Button>
                                <Button variant="outline-danger">CẦN TƯ VẤN</Button>
                            </div>
                        </Col>
                        <Col md={6} className="text-center">
                            <img
                                src={Logo.LogoZAlo}
                                alt="Facebook 3D"
                                className="img-fluid"
                                style={{ maxWidth: "400px" }}
                            />
                        </Col>
                    </Row>
                </Container>
            </div>

            {/* Content + Product */}
            <div className="content-section container">

                <h2 className="category-title fw-bold text-left mb-2">
                    Via Việt chuyên Dùng Chạy Quảng Cáo Facebook
                </h2>
                <hr style={{ border: "2px solid #F39C12", width: "100%", margin: "0 auto 30px auto" }} />



                <div className="row row-cols-1 row-cols-md-4 g-3">
                    {dataTypeProduct && dataTypeProduct.length > 0 ? (
                        dataTypeProduct.map((product) => (
                            <div key={product.id} className="col d-flex justify-content-center">
                                <ProductCard product={product} />
                            </div>
                        ))
                    ) : (
                        <div className="col-12 text-center">
                            <p>Không có sản phẩm nào trong danh mục này.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Zalo;
