import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import SensorDataList from './components/SensorDataList';

function App() {

  //Define state variables
  const [sensorData, setSensorData] = useState([{}]);
  const [phMin, setPHMin] = useState(5.5);
  const [phMax, setPHMax] = useState(7);
  const [ecMin, setECMin] = useState(1.2);
  const [lightOnHour, setLightOnHour] = useState(8);
  const [lightOffHour, setLightOffHour] = useState(18);
  const [ph, setPH] = useState(0);
  const [ec, setEC] = useState(0);
  const [timestamp, setTimeStamp] = useState('');


  useEffect(() => {
    getCurrentSettings();
    getRecentSensorData();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      getSensorData();
      getRecentSensorData();
    }, 1000);
    return () => clearInterval(interval);
  }, []);


  const getCurrentSettings = () =>{
    axios.get('http://127.0.0.1:8000/settings')
    .then(
      response => {
      console.log(response.data);
      setPHMin(response.data["phmin"]);
      setPHMax(response.data["phmax"]);
      setECMin(response.data["ecmin"]);
      setLightOnHour(response.data["lighthouron"]);
      setLightOffHour(response.data["lighthouroff"]);
      }
    )//resolve the promise
    .catch(
      (error)=>{
      console.log(error);
      }
    )  
  }

  const getSensorData = () =>{
    axios.get('http://127.0.0.1:8000/sensordata')
    .then(
      response => {
      console.log(response.data);
      setPH(response.data["PH"]);
      setEC(response.data["EC"]);
      setTimeStamp(response.data["time"]);
      }
    )//resolve the promise
    .catch(
      (error)=>{
      console.log(error);
      }
    )
  }

  const getRecentSensorData = () =>{
    axios.get('http://127.0.0.1:8000/sensordatas')
    .then(
      response => {
      console.log(response.data);
      setSensorData(response.data);
      }
    )//resolve the promise
    .catch(
      (error)=>{
      console.log(error);
      }
    )  
  }

  const addSensorData = (sensorData) =>{
    axios.post('http://127.0.0.1:8000/sensordata',sensorData)
     .then(response=>{
      alert("Sensor data added successfully!");
      })
     .catch((err)=>{console.log(err);}) 
  }

  const setSettings = () => {
    const settings = {"phmin":phMin, "phmax":phMax, "ecmin":ecMin, "lighthouron":lightOnHour, "lighthouroff":lightOffHour};
    axios.post('http://127.0.0.1:8000/settings',settings)
    .then(response=>{
     alert("Settings updated successfully!");
     })
    .catch((err)=>{console.log(err);}) 
  }

  // useEffect(() => {
  //   const sensorData = {"ph":ph, "ec":ec};
  //   addSensorData(sensorData);
  //   getRecentSensorData();
  // },[ph,ec]);


  return (
    <div className="container">
      <div 
        className="text-center mt-3 list-group-item justify-content-center align-items-center mx-auto"
        style={{"width":"80vw", "backgroundColor":"#ffffff"}}>
        <h2 className="card text-white bg-primary mb-1 pb-2">ANT System</h2>
        <h6 className="card text-white bg-primary mb-1 pb-1">Manage ANT System</h6>
        <div className="card-body">
          <h5 className="card text-white bg-dark pb-1">Current Sensor Reading</h5>
            <h3 id="timestamp">Time:{timestamp}</h3>
            <h3 id="PH">PH:{ph}</h3>
            <h3 id="EC">EC:{ec}</h3>
          <h5 className="card text-white bg-dark pb-1">ANT Setting</h5>
          <span className="card-text">
            <label className="form-label">PH MIN</label>
            <input value={phMin} onChange= {event => setPHMin(event.target.value)} className="mb-2 form-control stud-name" placeholder="Enter PH MIN value" />
            <label className="form-label">PH MAX</label>
            <input value={phMax} onChange= {event => setPHMax(event.target.value)} className="mb-2 form-control stud-email" placeholder="Enter PH MAX value" />
            <label className="form-label">EC MIN</label>
            <input value={ecMin} onChange= {event => setECMin(event.target.value)} className="mb-2 form-control stud-phone" placeholder="Enter EC MIN value" />
            <label className="form-label">LIGHT ON HOUR</label>
            <input value={lightOnHour} onChange= {event => setLightOnHour(event.target.value)} className="mb-2 form-control stud-phone" placeholder="Enter LIGHT ON HOUR value" />
            <label className="form-label">LIGHT OFF HOUR</label>
            <input value={lightOffHour} onChange= {event => setLightOffHour(event.target.value)} className="mb-3 form-control stud-phone" placeholder="Enter LIGHT OFF HOUR value" />
            <button onClick= {setSettings} className="btn btn-outline-primary mb-4" style={{'fontweight':"bold"}}>Change Settings</button>
          </span>
          <h5 className="card text-white bg-dark pb-1">Sensor Reading History</h5>
          <div>
            <SensorDataList
            sensorDataListVar= {sensorData}/>
          </div>
        </div>
        <h6 className="card text-dark bg-warning py-1">All rights reserved &copy; 2022</h6>    
      </div>
    </div>
  );
}

export default App;
