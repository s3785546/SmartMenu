import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import IndexPage from './indexPage.jsx';
import LoginPage from './loginPage.jsx';
import ViewUsersPage from './viewUsers.jsx';
import RegisterPage from './registerPage.jsx';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/" element={<IndexPage />} />
                    <Route path="/viewUsers" element={<ViewUsersPage />} />             
                    <Route path="/create_user" element={<RegisterPage />} />       
                </Routes>
            </div>
        </Router>
    );
}

export default App;