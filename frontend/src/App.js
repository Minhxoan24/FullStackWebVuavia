import React from 'react';
// import Header from './Components/Header/Header';
// import Footer from './Components/Footer/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
// import Navbar from './Components/Navbar/Navbar';


import { BrowserRouter } from 'react-router-dom';
import AppRoutes from './Routes/index.jsx';


const App = () => {
  return (
    <BrowserRouter>
      <AppRoutes />

    </BrowserRouter>
  );
}




export default App;
