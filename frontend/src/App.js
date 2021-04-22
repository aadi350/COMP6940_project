import React from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import io from "socket.io-client";
import './App.css';

import Welcome from './views/Welcome.js';
import Home from './views/Home.js';

function App() {
  const socket = io();
  socket.emit('test', "hello", (msg) => {
    console.log(msg);
  });
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Welcome} />
        <Route exact path="/crop" component={Home} />
      </Switch>
    </Router>
  );
}

export default App;
