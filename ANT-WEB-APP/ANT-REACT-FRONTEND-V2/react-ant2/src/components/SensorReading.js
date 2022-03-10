import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../App.css';
import SensorDataList from './SensorDataList';

function SensorReading(){
    const [sensorData, setSensorData] = useState([{}]);
    const [ph, setPH] = useState(0);
    const [ec, setEC] = useState(0);
    const [timestamp, setTimeStamp] = useState('');

    useEffect(() => {
        getRecentSensorData();
      }, []);

    useEffect(() => {
        const interval = setInterval(() => {
          getSensorData();
          getRecentSensorData();
        }, 1000);
        return () => clearInterval(interval);
      }, []);

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
    return (
        <div>
        <div className="card-body">
          <h5 className="card text-white bg-dark pb-1">Current Sensor Reading</h5>
            <h3 id="timestamp">Time:{timestamp}</h3>
            <h3 id="PH">PH:{ph}</h3>
            <h3 id="EC">EC:{ec}</h3>
        </div>
        <h5 className="card text-white bg-dark pb-1">Recent Sensor Reading History</h5>
        <div>
          <SensorDataList
          sensorDataListVar= {sensorData}/>
        </div>
        <h6 className="card text-dark bg-warning py-1">All rights reserved &copy; 2022</h6>    
      </div>
    );
}

export default SensorReading