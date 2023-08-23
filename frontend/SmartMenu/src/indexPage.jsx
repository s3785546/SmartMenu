import React, { useState, useEffect } from 'react';

function IndexPage() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [role, setRole] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        
        fetch('/api/is_authenticated/', {
            credentials: 'include',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            setIsAuthenticated(data.is_authenticated);
            setRole(data.role);
        });
    }, []);

    const handleLogout = (event) => {
        event.preventDefault();
        fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Logged out successfully") {
                localStorage.removeItem('access_token');
                setIsAuthenticated(false);
                setRole('');
            }
        });
    };

    return (
        <div>
            <h1>Welcome to Smart Menu</h1>
            
            {isAuthenticated ? (
                <a href="/" onClick={handleLogout}>Logout</a>
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
