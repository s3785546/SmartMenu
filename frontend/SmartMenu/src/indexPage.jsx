import React, { useState, useEffect } from 'react';

function IndexPage() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [role, setRole] = useState('');


    useEffect(() => {
        fetch('/api/is_authenticated/')
            .then(response => response.json())
            .then(data => {
                setIsAuthenticated(data.is_authenticated);
                setRole(data.role);
            });
    }, []); 

    return (
        <div>
            <h1>Welcome to Smart Menu</h1>
            
            {isAuthenticated ? (
                <a href="/logout">Logout</a>
            ) : (
                <a href="/login">Login</a>
            )}

            <hr />
            <a href="/create_user">Create User</a>
            <hr />
            <a href="/viewUsers">View Users</a>

            {isAuthenticated && role === 'restaurant' && (
                <>
                    <hr />
                    <a href="/dashboard">Restaurant Dashboard</a>
                </>
            )}
        </div>
    );
}

export default IndexPage;
