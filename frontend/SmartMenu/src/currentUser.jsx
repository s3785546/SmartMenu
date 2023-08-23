import React, { useState, useEffect } from 'react';

function CurrentUser() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        fetch('/api/current_user/', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch user data.");
            }
            return response.json();
        })
        .then(data => {
            setUser(data);
        })
        .catch(err => {
            setError(err.message);
        });
    }, []);

    return (
        <div>
            {error && <p>Error: {error}</p>}
            {user ? (
                <div>
                    <h2>Logged in as:</h2>
                    <p>Name: {user.firstname} {user.lastname}</p>
                    <p>Email: {user.email}</p>
                    <p>Role: {user.role}</p>
                </div>
            ) : (
                <p>You are not logged in.</p>
            )}
        </div>
    );
}

export default CurrentUser;
