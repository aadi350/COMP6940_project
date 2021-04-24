import React from 'react';
import MUIDataTable from "mui-datatables";
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Box from '@material-ui/core/Box';


const useStyles = makeStyles((theme) => ({
    button: {
        backgroundColor: '#E75757',
        fontFamily: 'monospace',
        fontSize: 14,
        fontWeight: 400,
        textTransform: 'none'
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

export default function Predict({ pData, pCols, setCols, setpData }) {
    const classes = useStyles();
    const predictData = React.useRef(pData);
    const predictColumns = React.useRef(pCols);
    const [columns, setColumns] = React.useState(predictColumns.current);
    const [data, setData] = React.useState(predictData.current);
    const [crop, setCrop] = React.useState('');
    const [model, setModel] = React.useState('');

    React.useEffect(() => {
        return () => {
            setCols(predictColumns.current);
            setpData(predictData.current);
        }
    }, [setpData, setCols, predictData, predictColumns]);

    const handleAgeChange = (event) => {
        setCrop(event.target.value);
    };

    const handleModelChange = (event) => {
        setModel(event.target.value);
    };

    const options = {
        filterType: 'checkbox',
        elevation: 0,
        filter: false,
        selectableRows: 'none',
        download: false,
        print: false,
        viewColumns: false,
    };

    const getData = () => {
        console.log('check',JSON.stringify({
            crop: crop,
            model: model
        }));
        fetch('/main/prediction',
            {
                method: 'POST',
                headers: {
                    "content_type": "application/json",
                },
                body: JSON.stringify({
                    crop: crop,
                    model: model
                })
            })
            .then(res => res.json())
            .then(data => {
                predictColumns.current = data.columns;
                predictData.current = data.data;
                setColumns(predictColumns.current);
                setData(predictData.current);
            });
    }

    return (
        <div>
            <h2>Predictions</h2>
            <Box display='flex' alignItems='center' className={classes.root}>

                <FormControl variant="outlined" className={classes.formControl}>
                    <InputLabel id="demo-simple-select-outlined-label">Crop</InputLabel>
                    <Select
                        labelId="demo-simple-select-outlined-label"
                        id="demo-simple-select-outlined"
                        value={crop}
                        onChange={handleAgeChange}
                        label="Crop"
                    >
                        <MenuItem value="">
                            <em>None</em>
                        </MenuItem>
                        <MenuItem value={'peas'}>Pigeon Peas</MenuItem>
                        <MenuItem value={'citrus'}>Citrus</MenuItem>
                        <MenuItem value={'potato'}>Potato</MenuItem>
                    </Select>
                </FormControl>
                <FormControl variant="outlined" className={classes.formControl}>
                    <InputLabel id="demo-simple-select-outlined-label">Model</InputLabel>
                    <Select
                        labelId="demo-simple-select-outlined-label"
                        id="demo-simple-select-outlined"
                        value={model}
                        onChange={handleModelChange}
                        label="Model"
                    >
                        <MenuItem value="">
                            <em>None</em>
                        </MenuItem>
                        <MenuItem value={'pymc3'}>pymc3</MenuItem>
                        <MenuItem value={'lr'}>lr</MenuItem>
                        <MenuItem value={'ridge'}>ridge</MenuItem>
                    </Select>
                </FormControl>
                <Button variant="contained" className={classes.button} onClick={getData}>Get Prediction</Button>
            </Box>
            <MUIDataTable
                data={data}
                columns={columns}
                options={options}
            />
        </div>
    )
}