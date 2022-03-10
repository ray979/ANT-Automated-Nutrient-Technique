import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../App.css';
import SensorDataList from './SensorDataList';

function DataLog(){
    const [sensorData, setSensorData] = useState([{}]);
    const [ph, setPH] = useState(0);
    const [ec, setEC] = useState(0);
    const [timestamp, setTimeStamp] = useState('');

    useEffect(() => {
        getAllSensorData();
      }, []);

    // useEffect(() => {
    //     const interval = setInterval(() => {
    //       getRecentSensorData();
    //     }, 1000);
    //     return () => clearInterval(interval);
    //   }, []);

    const getAllSensorData = () =>{
        axios.get('http://127.0.0.1:8000/allsensordatas')
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
        <div>
          <button onClick= {getAllSensorData} className="btn btn-outline-primary mb-4" style={{'fontweight':"bold"}}>Refresh</button>
          <SensorDataList
          sensorDataListVar= {sensorData}/>
        </div>
        <h6 className="card text-dark bg-warning py-1">All rights reserved &copy; 2022</h6>    
      </div>
    );
}

export default DataLog;