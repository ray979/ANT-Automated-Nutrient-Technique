import React from "react";
import SensorData from "./SensorData";
import Table from 'react-bootstrap/Table';

function SensorDataList(props){
    return(
        <Table striped bordered hover>
        <thead>
          <tr>
            <th>Date</th>
            <th>Time</th>
            <th>PH Reading</th>
            <th>EC Reading</th>
          </tr>
        </thead>
        <tbody>
            {
            props.sensorDataListVar.map(
                (data, index) =>{
                    return(<SensorData
                            sensordata={data} key={index}/>)
                }
            )
            }
        </tbody>
      </Table>


    )
}

export default SensorDataList;