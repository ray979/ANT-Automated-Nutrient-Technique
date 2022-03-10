import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../App.css';

function Settings(){
  //Define state variables
  const [sensorData, setSensorData] = useState([{}]);
  const [phMin, setPHMin] = useState(5.5);
  const [phMax, setPHMax] = useState(7);
  const [ecMin, setECMin] = useState(1.2);
  const [lightOnHour, setLightOnHour] = useState(8);
  const [lightOffHour, setLightOffHour] = useState(18);

  useEffect(() => {
    getCurrentSettings();
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

  const setSettings = () => {
    const settings = {"phmin":phMin, "phmax":phMax, "ecmin":ecMin, "lighthouron":lightOnHour, "lighthouroff":lightOffHour};
    axios.post('http://127.0.0.1:8000/settings',settings)
    .then(response=>{
     alert("Settings updated successfully!");
     })
    .catch((err)=>{console.log(err);}) 
  }

  return(
    <div>
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
    </div>
  )

}

export default Settings;