import React from 'react'
import ReactDOM from 'react-dom'
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import App from './components/App'
import Home from './components/Main'
const routing = (
    <Router>
        <div>
            <Route path="/" component={App} />
            <Route path="/home" component={Home} />
        </div>
    </Router>
)
ReactDOM.render(routing, document.getElementById('app'))
