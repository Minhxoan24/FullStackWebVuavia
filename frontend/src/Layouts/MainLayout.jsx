import React from "react";
import { Outlet } from "react-router-dom";
import Header from "../Components/Header/Header.jsx";
import Navbar from "../Components/Navbar/Navbar.jsx";
import Footer from "../Components/Footer/Footer.jsx";
import "bootstrap/dist/css/bootstrap.min.css";
import "./MainLayout.css";

const MainLayout = () => {
    return (
        <div>
            {/* Phần cố định trên cùng */}
            <div className="fixed-top">
                {/* Header */}

                <Header />


                {/* Navbar */}

                <Navbar />


            </div>

            {/* Nội dung chính */}
            <div style={{ paddingTop: "110px" }}>
                <main>
                    <Outlet />
                </main>
                <Footer />
            </div>
        </div>
    );
};

export default MainLayout;



// import React from 'react';
// import { Outlet } from 'react-router-dom';
// import Header from '../Components/Header/Header.jsx';
// import Navbar from '../Components/Navbar/Navbar.jsx';
// import Footer from '../Components/Footer/Footer.jsx';
// import 'bootstrap/dist/css/bootstrap.min.css';
// const MainLayout = () => {
//     return (
//         <div>
//             <div className='fixed-top'>
//                 <Header />
//                 <Navbar />
//             </div>
//             <div style={{ paddingTop: '140px' }}>
//                 <main>
//                     <Outlet />
//                 </main>
//                 <Footer />
//             </div>
//         </div>
//     );


// }
// export default MainLayout;