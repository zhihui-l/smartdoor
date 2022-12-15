import Page from 'components/Page';
import React from 'react';
import { 
  Button,
  Card, 
  CardBody, 
  CardHeader, 
  CardImg,
  Col, 
  Row, 
  Table,
} from 'reactstrap';



class TablePage extends React.Component {

  　　constructor(props) {
    　　　　super(props);
    　　　　this.state = {log: [], img: ''}
    　　}

    getLog(){
      fetch("/api/getLog")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({log: result})
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
    this.getLog()
  }





  getPhoto(lid){

    this.setState({img: '/api/getLogImg?id='+lid})

  }

    imgOnClick(){
      this.setState({img: ''})
    }

  render(){
    let card = '';
    if(this.state.img !== ''){
      card = (<Row onClick={this.imgOnClick.bind(this)} style={{width: '500px', position: 'fixed', top: '50px', right: '40px', zIndex: '999'}}>
      <Card inverse className="text-center" style={{margin: '0 auto', maxWidth: '500px'}}>
        <CardImg  src={this.state.img}  alt="Card image cap" />
      </Card>
    </Row>)
    }
  return (
    <Page
      title="Log"
      breadcrumbs={[{ name: 'Log', active: true }]}
      className="TablePage"
    >

    {card}
      <Row>
        <Col>
          <Card className="mb-3">
            <CardHeader>Log</CardHeader>
            <CardBody>
              <Table responsive>
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Type</th>
                    <th>User</th>
                    <th>Photo</th>
                  </tr>
                </thead>
                <tbody>
                {this.state.log.map(u=>{
                  let button = '';
                  if(u[5]){
                    
                    button = <Button onClick={this.getPhoto.bind(this, u[0])}>show</Button>
                  }


                  return (
                    <tr>
                    <th scope="row">{new Date(u[4].substr(0, u[4].length-4)).toLocaleString()}</th>
                    <td>{u[1]}</td>
                    <td>{u[3]}</td>
                    <td>{button}</td>
                  </tr>
                  )})}
                </tbody>
              </Table>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Page>
  );
  }
};

export default TablePage;
