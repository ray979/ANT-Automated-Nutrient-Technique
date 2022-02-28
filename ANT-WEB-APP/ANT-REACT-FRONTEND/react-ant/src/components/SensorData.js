import React from "react";


function SensorData(props){
    return(

        <tr>
            <td>{props.sensordata.date_posted}</td>
            <td>{props.sensordata.time_posted}</td>
            <td>{props.sensordata.ph}</td>
            <td>{props.sensordata.ec}</td>
        </tr>

    );
}

export default SensorData;