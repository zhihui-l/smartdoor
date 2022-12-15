import Page from 'components/Page';
import React from 'react';
import {
  Button,
  Card,
  CardBody,
  Col,
  Row,
  Table,
  CardHeader,
  InputGroup,
  InputGroupText,
  Input
} from 'reactstrap';


class CardPage extends React.Component {
  　　constructor(props) {
    　　　　super(props);
    　　　　this.state = {user: [], inp: ''}
    　　}

    getUser(){
      fetch("/api/getUser")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({user: result})
          console.log(result)
        },
        (error) => {
          console.log(error)
        }
      )
    }


  componentDidMount() {
    // this is needed, because InfiniteCalendar forces window scroll
    window.scrollTo(0, 0);
    this.getUser()
  }


  toggleActive(active, uid){
    let url = active ? '/api/deactiveUser' : '/api/activeUser';
      fetch(url + '?id='+uid)
      .then(res => res.json())
      .then(
        (result) => {
          this.getUser()
          console.log(result)
        },
        (error) => {
          console.log(error)
        }
      )
  }


  train(uid){
    fetch('/api/train?id='+uid)
    .then(res => res.json())
    .then(
      (result) => {
        console.log(result)
        if(result.status == true){
          alert('Please look at the PiTFT to train!!!')
        }
      },
      (error) => {
        console.log(error)
      }
    )
  }


  handelChange(value) {
    console.log(value) 
    console.log(this.state)
    this.setState({inp: value})
   
}

  add_user(){
    fetch('/api/addUser?name='+this.state.inp)
    .then(res => res.json())
    .then(
      (result) => {
        console.log(result)
        if(result.status == true){
          alert('User added!!!')
          this.getUser()
        }
      },
      (error) => {
        console.log(error)
      }
    )
  }


    render(){
  return (
    <Page title="Users" breadcrumbs={[{ name: 'users', active: true }]}>

<Row>
        <Col>
          <Card className="mb-3">
            <CardHeader>Users</CardHeader>
            <CardBody>
              <Table responsive>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>CreatedTime</th>
                    <th>ModifiedTime</th>
                    <th>Iteration</th>
                    <th></th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.user.map(u=>(
                    <tr>
                    <th scope="row">{u[0]}</th>
                    <td>{u[2]}</td>
                    <td>{u[1] ? 'Active' : 'Deactive'}</td>
                    <td>{new Date(u[3].substr(0, u[3].length-4)).toLocaleString()}</td>
                    <td>{new Date(u[4].substr(0, u[3].length-4)).toLocaleString()}</td>
                    <td>{u[5]}</td>
                    <td><Button onClick={this.toggleActive.bind(this, u[1], u[0])}>{u[1] ? 'Deactive' : 'Active'}</Button></td>
                    <td><Button onClick={this.train.bind(this, u[0])}>Train</Button></td>
                  </tr>
                  ))}
                </tbody>
              </Table>
            </CardBody>
          </Card>
        </Col>
      </Row>

      <Row style={{margin: '10px 20px 10px 20px'}}>
      <InputGroup >
        <Input placeholder="username" onChange={e=>{this.handelChange(e.target.value)}} />
        <button onClick={this.add_user.bind(this)}>Add User</button>
      </InputGroup>
      </Row>

      

    </Page>
  );
  }
};

export default CardPage;
