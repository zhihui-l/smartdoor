
import Page from 'components/Page';
import React from 'react';

import {
  Button,
} from 'reactstrap';


class DashboardPage extends React.Component {
  componentDidMount() {
    // this is needed, because InfiniteCalendar forces window scroll
    window.scrollTo(0, 0);
  }

  openDoor = () => {
    alert('Opened');
  }

  render() {
    return (
      <Page
        className="DashboardPage"
        title="Dashboard"
        breadcrumbs={[{ name: 'Dashboard', active: true }]}
      >

      <row>

      <Button onClick={this.openDoor}>Open Door</Button>


      </row>

      </Page>
    );
  }
}
export default DashboardPage;
