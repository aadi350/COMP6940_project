import React from 'react';
import MUIDataTable from "mui-datatables";
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Chart from "react-google-charts";

const useStyles = makeStyles({
    button: {
        backgroundColor: '#E75757',
        color: 'black',
        fontFamily: 'monospace',
        fontSize: 14,
        fontWeight: 400,
        textTransform: 'none'
    }
});

export default function Forecast({ fData, fCols, setfCols, setfData }) {
    const classes = useStyles();
    const wData = React.useRef(fData);
    const wColumns = React.useRef(fCols);
    const [data, setData] = React.useState(wData.current);
    const [columns, setColumns] = React.useState(wColumns.current);

    React.useEffect(() => {
        return () => {
            setfCols(wColumns.current);
            setfData(wData.current);
        }
    }, [setfData, setfCols, wData, wColumns]);

    const options = {
        filterType: 'checkbox',
        elevation: 0,
        filter: false,
        selectableRows: 'none',
        download: false,
        print: false,
    };

    const getData = () => {

        fetch('/main/forecast').then(res => res.json()).then(data => {
            console.log(data.columns);
            console.log(data.data);
            wData.current = data.data;
            wColumns.current = data.columns;
            setData(wData.current);
            setColumns(wColumns.current);
        });
    }

    return (
        <div>
            <h2>Forecast</h2>
            {/* <Chart
                width={'1000px'}
                height={'500px'}
                chartType="LineChart"
                loader={<div>Loading Chart</div>}
                data={[].concat([columns])}
                options={{
                    hAxis: {
                        title: 'Week',
                    },
                    vAxis: {
                        title: 'Forecast',
                    },
                }}
                rootProps={{ 'data-testid': '1' }}
            /> */}
            <MUIDataTable
                title={
                    <Button variant="contained" className={classes.button} onClick={getData}>Get Forecast</Button>
                }
                data={data}
                columns={columns}
                options={options}
            />
        </div>
    )
}