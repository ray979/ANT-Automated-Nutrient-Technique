import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import SensorReading from './components/SensorReading';
import Navigate from './components/Navigate';
import {BrowserRouter as Router, Switch, Route, Routes} from 'react-router-dom';
import Settings from './components/Settings';
import DataLog from './components/DataLog';
import QueryData from './components/QueryData';
import Home from './components/Home';
import About from './components/About';



function App() {
  return(
    <div className='App'>
    <div className="container">
      <div 
      className="text-center mt-3 list-group-item justify-content-center align-items-center mx-auto"
      style={{"width":"80vw", "backgroundColor":"#ffffff"}}>
        <Navigate/>

        <Router>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/sensorreading" element={<SensorReading/>} />
          <Route path="/settings" element={<Settings/>} />
          <Route path="/datalog" element={<DataLog/>}/>
          <Route path="/querybydate" element={<QueryData/>}/>
          <Route path="/about" element={<About/>} />
        </Routes>
        </Router>


      </div>
    </div>
    </div>

  );



}

export default App;
