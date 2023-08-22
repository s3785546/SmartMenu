import React, { useState, useEffect } from 'react';

function ViewUsersPage() {

    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch('/api/view_users/')
            .then(response => response.json())
            .then(data => setUsers(data));
    }, []); 

    return (
        <div>
            <h2>All Customers</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                        <th>Age</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.id}</td>
                            <td>{user.firstname}</td>
                            <td>{user.lastname}</td>
                            <td>{user.email}</td>
                            <td>{user.age}</td>
                            <td>{user.role}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ViewUsersPage;
