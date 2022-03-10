import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../App.css';
import SensorDataList from './SensorDataList';

function QueryData(){
    const [sensorData, setSensorData] = useState([{}]);
    const [date, setDate] = useState('');
    const [ph, setPH] = useState(0);
    const [ec, setEC] = useState(0);
    const [timestamp, setTimeStamp] = useState('');

    const getSensorDataByDate = () =>{
        axios.get(`http://127.0.0.1:8000/searchSensorDatasByDate/<datetime.date:date>?date=${date}`)
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

    return (
        <div>
        <h5 className="card text-white bg-dark pb-1">Sensor Reading History</h5>
        <label className="form-label">Date To Query (YYYY-MM-DD)</label>
        <input value={date} onChange= {event => setDate(event.target.value)} className="mb-2 form-control stud-name" placeholder="Enter date to query" />
        <button onClick= {() => getSensorDataByDate()} className="btn btn-outline-primary mb-4" style={{'fontweight':"bold"}}>Query</button>
        <div>
          <SensorDataList
          sensorDataListVar= {sensorData}/>
        </div>
        <h6 className="card text-dark bg-warning py-1">All rights reserved &copy; 2022</h6>    
      </div>
    );
}

export default QueryData;