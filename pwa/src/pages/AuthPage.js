import React from 'react';
import { Card, Col, Row, Button, Form, FormGroup, Input, Label, Container } from 'reactstrap';

class AuthForm extends React.Component {


  
  handleSubmit = event => {
    event.preventDefault();
    window.location.href='/';
  };


  render() {
    const {
      children,
    } = this.props;

    return (
      <Form onSubmit={this.handleSubmit}>
        <FormGroup>
          <Label for="Username">Username</Label>
          <Input type="text" />
        </FormGroup>
        <FormGroup>
          <Label for="Password">Password</Label>
          <Input type="password" />
        </FormGroup>

        <hr />
        <Button
          size="lg"
          className="bg-gradient-theme-left border-0"
          block
          onClick={this.handleSubmit}>
          Login
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
