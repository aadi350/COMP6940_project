import React from 'react';
import MUIDataTable from "mui-datatables";

export default function Forecast({ socket }) {

    const [weatherFiltered, setWeatherFiltered] = React.useState(0);
    const [weatherKeys, setWeatherKeys] = React.useState(0);

    const columns = ["Name", "Company", "City", "State"];

    const data = [
        ["Joe James", "Test Corp", "Yonkers", "NY"],
        ["John Walsh", "Test Corp", "Hartford", "CT"],
        ["Bob Herm", "Test Corp", "Tampa", "FL"],
        ["James Houston", "Test Corp", "Dallas", "TX"],
    ];

    const options = {
        filterType: 'checkbox',
        elevation:'0'
    };

    socket.emit('getData', (filtered, keys) => {
        console.log();
    });

    return (
        <div>
            <h3>Forecast</h3>            
            <MUIDataTable
                title={"Employee List"}
                data={data}
                columns={columns}
                options={options}
            />
        </div>
    )
}