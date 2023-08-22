import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const navigate = useNavigate();  // Get the navigate function

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });  // <-- Close the fetch here

            if (response.ok) {
                alert("Login successful");
                navigate("/");  // Navigate to the dashboard upon successful login
            } else {
                alert("Login failed");
            }
        } catch (error) {
            console.error('There was an error!', error);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <p>
                    <label>Email:</label><br />
                    <input
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                    />
                </p>
                <p>
                    <label>Password:</label><br />
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                    />
                </p>
                <p>
                    <button type="submit">Login</button>
                </p>
            </form>
        </div>
    );
}

export default LoginPage;
