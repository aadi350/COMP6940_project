import React from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles({
    root: {
        display: 'flex',
        backgroundImage: `url('/agri.jpg')`,
        backgroundPosition: 'center',
        backgroundSize: 'cover',
        width: '100vw',
        height: '100vh'
    },
    card: {
        maxWidth: 1000,
        border: '1px solid black',
        backgroundColor: "#2EB479",
    },
    title: {
        fontSize: 24,
        fontWeight: 400,
        fontFamily: 'monospace'
    },
    subheader: {
        color: 'white',
        fontWeight: 200,
        fontFamily: 'monospace'
    },
    button: {
        backgroundColor: '#E75757',
        color: 'black',
        fontFamily: 'monospace',
        fontSize: 12,
        fontWeight: 400,
        textTransform: 'none'
    }
});


export default function Welcome() {
    const classes = useStyles();
    return (
        <Box display='flex' alignItems='center' className={classes.root}>
            <Grid container spacing={0} alignContent='center' direction='column'>
                <Card className={classes.card} variant='outlined' raised>
                    <CardHeader
                        classes={{ title: classes.title, subheader: classes.subheader }}
                        title="Online Crop Recommendation System"
                        subheader="COMP6940 G1"
                    />
                    <CardContent>
                        <Grid container spacing={0} alignContent='center' direction='column'>
                            <Link to="/crop" style={{textDecoration:'none'}}>
                                <Button variant="contained" className={classes.button}>Enter</Button>
                            </Link>
                        </Grid>
                    </CardContent>
                    <CardActions>
                    </CardActions>
                </Card>
            </Grid>
        </Box>
    )
}