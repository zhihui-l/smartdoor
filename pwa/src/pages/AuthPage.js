import React from 'react';
import { Card, Col, Row, Button, Form, FormGroup, Input, Label, Container } from 'reactstrap';
const md5 = require('md5');


class AuthForm extends React.Component {


  
  handleLogIn = event => {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    if (username === 'kevin') {
      if (md5(password) === 'e10adc3949ba59abbe56e057f20f883e'){
        window.location.href='/';
      }
      else{
        alert('Incorrect username or password')
      }
    }
    else{
      alert('Incorrect username or password')
    }
  };

  handleSignUp = event => {
    event.
    window.location.href='/sign-up';

  };

  render() {
    const {
      children,
    } = this.props;

    return (
      <Form onSubmit={this.handleSubmit}>
        <FormGroup>
          <Label for="Username">Username</Label>
          <Input id="username" type="text" />
        </FormGroup>
        <FormGroup>
          <Label for="Password">Password</Label>
          <Input id="password" type="password" />
        </FormGroup>

        <hr />
        <Button
          size="lg"
          className="bg-gradient-theme-left border-0"
          block
          onClick={this.handleLogIn}>
          Login
        </Button>

        <Button
          size="lg"
          className="bg-gradient-theme-left border-0"
          block
          onClick={this.handleSignUp}>
          Sign up
        </Button>


        {children}
      </Form>
    );
  }
}

class AuthPage extends React.Component {

  render() {
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
        <h5 style={{width:'230%',position:'absolute', top:'-35%', left:'10%', fontSize:'2em'}}>Access Control System</h5>
          <Card body>
            <AuthForm />
          </Card>
        </Col>
      </Row>
      </Container>
    </main>
    );
  }
}

export default AuthPage;
