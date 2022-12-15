/*
dashboard page
*/
import Page from 'components/Page';
import React from 'react';

import {
  Button,
  Card,
  CardBody,
  CardImg,
  CardImgOverlay,
  CardLink,
  CardText,
  CardTitle,
  Col,
  ListGroup,
  Row,
} from 'reactstrap';


class DashboardPage extends React.Component {

  　　constructor(props) {
    　　　　super(props);
    　　　　this.state = {img: '/api/live'}
    　　}

  componentDidMount() {
    // this is needed, because InfiniteCalendar forces window scroll
    window.scrollTo(0, 0);
    /*
    this.timer = setInterval(()=>{
      this.setState({img: '/api/live?t='+new Date().valueOf()})
    }, 400)
    */
  }

  　　componentWillUnmount() {
    　　　　clearInterval(this.timer);
    　　}


  openDoor = () => {


    fetch("/api/openDoor")
      .then(res => res.json())
      .then(
        (result) => {
          alert('Door opened!!')
          console.log(result)
        },
        (error) => {
          alert('Server error!!')
          console.log(error)
        }
      )
  }

  render() {
    return (
      <Page
        className="DashboardPage"
        title="Dashboard"
        breadcrumbs={[{ name: 'Dashboard', active: true }]}
      >
      <Row style={{margin: '10px 20px 20px 10px'}}>
        <Card inverse className="text-center" style={{margin: '0 auto', maxWidth: '500px'}}>
          <CardImg  src={this.state.img} alt="Card image cap" />
        </Card>
      </Row>
      <Row style={{margin: '10px 20px 20px 10px'}}>
          <Button style={{margin: '0 auto'}} onClick={this.openDoor}>Open Door</Button>
      </Row>

      </Page>
    );
  }
}
export default DashboardPage;
