import * as React from 'react';
import { Link } from 'react-router-dom';
import clsx from 'clsx';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import { Home, NaturePeople, WbSunny, History, Logout } from '@material-ui/icons';
import Dashboard from './Dashboard.js';
import Predict from './Predictions.js';
import Forecast from './Forecast';
import Archive from './Archive';

const drawerWidth = 220;

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        backgroundColor: '#FAFAFA',
        width: '100vw',
        height: '100vh'
    },
    appBar: {
        backgroundImage: `url('/agri2.jpg')`,
        backgroundSize: 'cover',
        zIndex: theme.zIndex.drawer + 1,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    menuButton: {
        marginRight: 36,
    },
    hide: {
        display: 'none',
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        boxSizing: 'border-box',
    },
    drawerOpen: {
        backgroundImage: `url('/agri2.jpg')`,
        width: drawerWidth,
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    drawerClose: {
        backgroundImage: `url('/agri2.jpg')`,
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        overflowX: 'hidden',
        width: `calc(${theme.spacing(7)} + 1px)`,
        [theme.breakpoints.up('sm')]: {
            width: `calc(${theme.spacing(9)} + 1px)`,
        },
    },
    toolbar: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: theme.spacing(0, 0),
        // necessary for content to be below app bar
        ...theme.mixins.toolbar,
    },
    content: {
        flexGrow: 1,
        padding: theme.spacing(0, 3),
    },
    text: {
        color: 'black',
        fontWeight: 500,
        fontSize: 22,
        fontFamily: 'monospace'
    },
    list: {
        color: '#17653C',
        fontWeight: 600,
        fontSize: 18,
        fontFamily: 'monospace'
    },
    listItem: {
        '&.Mui-selected': {
            backgroundColor: '#FCA83D',
        },
        '&.Mui-selected:hover': {
            backgroundColor: '#FCA83D',
        },
        '&:hover': {
            backgroundColor: '#FFEDD7',
        },
    }
}));

export default function MiniDrawer() {
    const classes = useStyles();
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    const [selectedIndex, setSelectedIndex] = React.useState(0);

    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };

    const handleListItemClick = (event, index) => {
        setSelectedIndex(index);
    };

    const getMenuIcon = (text) => {
        switch (text) {
            case "Home": return <Home />;
            case "Predictions": return <NaturePeople />;
            case "Forecasts": return <WbSunny />;
            case "Archive": return <History />;
            default: break;
        }
    }

    const getComponent = () => {
        switch (selectedIndex) {
            case 0: return <Dashboard />;
            case 1: return <Predict />;
            case 2: return <Forecast />;
            case 3: return <Archive />;
            default: break;
        }
    }

    return (
        <div className={classes.root}>
            <CssBaseline />
            <AppBar
                position="fixed"
                className={clsx(classes.appBar, {
                    [classes.appBarShift]: open,
                })}
            >
                <Toolbar style={{ width: '100%' }}>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        onClick={handleDrawerOpen}
                        edge="start"
                        className={clsx(classes.menuButton, {
                            [classes.hide]: open,
                        })}
                    >
                        <MenuIcon color={"action"} />
                    </IconButton>
                    <Typography variant="h6" noWrap className={classes.text} component="div" sx={{ flexGrow: 1 }}>
                        Online Crop Recommendation
                    </Typography>
                    <Link to="/" style={{ textDecoration: 'none' }}>
                        <IconButton color="black"><Logout /></IconButton>
                    </Link>
                </Toolbar>
            </AppBar>
            <Drawer
                variant="permanent"
                className={clsx(classes.drawer, {
                    [classes.drawerOpen]: open,
                    [classes.drawerClose]: !open,
                })}
                classes={{
                    paper: clsx({
                        [classes.drawerOpen]: open,
                        [classes.drawerClose]: !open,
                    }),
                }}
            >
                <div className={classes.toolbar}>
                    <IconButton onClick={handleDrawerClose}>
                        {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                    </IconButton>
                </div>
                <Divider />
                <List>
                    {['Home', 'Predictions', 'Forecasts', 'Archive'].map((text, index) => (
                        <ListItem
                            button
                            key={text}
                            selected={selectedIndex === index}
                            onClick={(event) => handleListItemClick(event, index)}
                            className={classes.listItem}
                        >
                            <ListItemIcon style={{ color: '#17653C' }}>
                                {getMenuIcon(text)}
                            </ListItemIcon>
                            <ListItemText primary={text} classes={{ primary: classes.list }} />
                        </ListItem>
                    ))}
                </List>
            </Drawer>
            <main className={classes.content}>
                <div className={classes.toolbar} />
                {getComponent()}
            </main>
        </div>
    );
}
