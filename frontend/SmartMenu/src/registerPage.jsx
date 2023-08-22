import React, { useState } from 'react';

function CreateUserPage() {
    const [formData, setFormData] = useState({
        firstname: '',
        lastname: '',
        email: '',
        password: '',
        age: '',
        role: 'customer'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    }

    const handleSubmit = (e) => {
        e.preventDefault();
    
        fetch('/api/create_user/', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("success")
            } else {
                alert("fail")
            }
        });
    }

    return (
        <div>
            <h2>Create a New User</h2>
            <form onSubmit={handleSubmit}>
                First Name: <input type="text" name="firstname" value={formData.firstname} onChange={handleChange} required /><br /><br />
                Last Name: <input type="text" name="lastname" value={formData.lastname} onChange={handleChange} required /><br /><br />
                Email: <input type="email" name="email" value={formData.email} onChange={handleChange} required /><br /><br />
                Password: <input type="password" name="password" value={formData.password} onChange={handleChange} required /><br /><br />
                Age: <input type="number" name="age" value={formData.age} onChange={handleChange} /><br /><br />
                Role:
                <select name="role" value={formData.role} onChange={handleChange}>
                    <option value="customer">Customer</option>
                    <option value="restaurant">Restaurant Owner</option>
                </select><br /><br />
                <input type="submit" value="Submit" />
            </form>
        </div>
    );
}

export default CreateUserPage;
