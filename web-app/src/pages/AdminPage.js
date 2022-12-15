import React, { useEffect, useState } from 'react';
import { FaWindows } from 'react-icons/fa';
import { Card, Col, Row, Button, Form, FormGroup, Input, Label, Container } from 'reactstrap';
import Page from 'components/Page';

export default function AdminForm() {

    // States for registration
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [telephone, setTelephone] = useState('');
    const [password, setPassword] = useState('');

    // States for checking the errors
    const [submitted, setSubmitted] = useState(false);
    const [error, setError] = useState(false);

    useEffect(()=>{
        fetch('/api/getInfo') 
        .then(res => res.json()) 
        .then( (result) => { 
            console.log(result) 
            setEmail(result.email);
            setTelephone(result.telephone);
        }, 
            (error) => { console.log(error) } )
        
    }, [])




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
        if (email != '' && telephone != '') {
            setSubmitted(true);
            setError(false);
            const obj = {
                name: name,
                email: email,
                telephone: telephone,
                password: password
            }
            fetch('/api/setInfo?email='+email+'&telephone='+telephone) 
            .then(res => res.json()) 
            .then( (result) => { 
                console.log(result) 
            }, 
                (error) => { console.log(error) } )

        } else {
            setError(true);
        }
    };

    // Showing success message
    const successMessage = () => {
        return (
        <div
            className="success"
            style={{
            display: submitted ? '' : 'none',
            }}>
            <h5>User {name} successfully submitted!!</h5>
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
        <Page
        title="Admin"
        breadcrumbs={[{ name: 'Admin', active: true }]}
        className="TablePage"
        >
        <Container fluid>
        <Row
          style={{
            height: '70vh',
            justifyContent: 'center',
            alignItems: 'center',
          }}>
          <Col md={6} lg={4}>
            <Card body>

                <Form>
                    <FormGroup>
                    <Label for="Email">Email</Label>
                    <Input onChange={handleEmail} value={email}type="text" />
                    </FormGroup>

                    <FormGroup>
                    <Label for="Telephone">Telephone</Label>
                    <Input onChange={handleTelephone} value={telephone}type="text" />
                    </FormGroup>

                    <hr />
                    <Button
                    size="lg"
                    className="bg-gradient-theme-left border-0"
                    block
                    onClick={handleSubmit}>
                    Submit
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
      </Page>
    );
}