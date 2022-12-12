import React, { useState } from 'react';
import { FaWindows } from 'react-icons/fa';
import { Card, Col, Row, Button, Form, FormGroup, Input, Label, Container } from 'reactstrap';
import axios from 'axios';
const md5 = require('md5');

export default function SignUpForm() {

    // States for registration
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [telephone, setTelephone] = useState('');
    const [password, setPassword] = useState('');

    // States for checking the errors
    const [submitted, setSubmitted] = useState(false);
    const [error, setError] = useState(false);

    // Handling the name change
    const handleName = (e) => {
        setName(e.target.value);
        setSubmitted(false);
    };

    // Handling the email change
    const handleEmail = (e) => {
        setEmail(e.target.value);
        setSubmitted(false);
    };

    // Handling the email change
    const handleTelephone = (e) => {
        setTelephone(e.target.value);
        setSubmitted(false);
    };

    // Handling the password change
    const handlePassword = (e) => {
        setPassword(e.target.value);
        setSubmitted(false);
    };

    // Handling the form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        if (name === '' || email === '' || password === '' || telephone === '') {
            setError(true);
        } else {
            setSubmitted(true);
            setError(false);
            const obj = {
                name: name,
                email: email,
                telephone: telephone,
                password: password
            }

            axios.post('http://localhost/reactProject/insert.php',obj)
            .then(res=> console.log(res.data))
            .catch(error => {
                console.log(error.response)
            });
            setName('');
            setEmail('');
            setTelephone('');
            setPassword('');
        }
    };

    const handleBackToLogin = (e) => {
        e.preventDefault();
        window.location.href='/login';
    };

    // Showing success message
    const successMessage = () => {
        return (
        <div
            className="success"
            style={{
            display: submitted ? '' : 'none',
            }}>
            <h5>User {name} successfully registered!!</h5>
        </div>
        );
    };

    // Showing error message if error is true
    const errorMessage = () => {
        return (
        <div
            className="error"
            style={{
            display: error ? '' : 'none',
            }}>
            <h5>Please enter all the fields!</h5>
        </div>
        );
    };
    return (
        <main className="cr-app bg-light" >
        <Container fluid>
        <Row
          style={{
            height: '100vh',
            justifyContent: 'center',
            alignItems: 'center',
          }}>
          <Col md={6} lg={4}>
            <Card body>
            
                <Form>
                <h5 style={{width:'230%',position:'absolute', top:'-15%', left:'18%', fontSize:'2em'}}>Registration Form</h5>
                    <FormGroup>
                    <Label for="Username">Username</Label>
                    <Input onChange={handleName} value={name}type="text" />
                    </FormGroup>

                    <FormGroup>
                    <Label for="Email">Email</Label>
                    <Input onChange={handleEmail} value={email}type="text" />
                    </FormGroup>

                    <FormGroup>
                    <Label for="Telephone">Telephone</Label>
                    <Input onChange={handleTelephone} value={telephone}type="text" />
                    </FormGroup>

                    <FormGroup>
                    <Label for="Password">Password</Label>
                    <Input onChange={handlePassword} value={password}type="password" />
                    </FormGroup>

                    <hr />
                    <Button
                    size="lg"
                    className="bg-gradient-theme-left border-0"
                    block
                    onClick={handleSubmit}>
                    Sign up
                    </Button>

                    <Button
                    size="lg"
                    className="bg-gradient-theme-left border-0"
                    block
                    onClick={handleBackToLogin}>
                    Back to login
                    </Button>
                </Form>

                {/* Calling to the methods */}
                <div className="messages">
                    {errorMessage()}
                    {successMessage()}
                </div>
            </Card>
          </Col>
        </Row>
        </Container>
      </main>
    );
}
