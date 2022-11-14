import bg11Image from 'assets/img/bg/background_1920-11.jpg';
import bg18Image from 'assets/img/bg/background_1920-18.jpg';
import bg1Image from 'assets/img/bg/background_640-1.jpg';
import bg3Image from 'assets/img/bg/background_640-3.jpg';
import user1Image from 'assets/img/users/100_1.jpg';
import { UserCard } from 'components/Card';
import Page from 'components/Page';
import { bgCards, gradientCards, overlayCards } from 'demos/cardPage';
import { getStackLineChart, stackLineChartOptions } from 'demos/chartjs';
import React from 'react';
import { Line } from 'react-chartjs-2';
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
  ListGroupItem,
  Row,
  Table,
  CardHeader
} from 'reactstrap';

const CardPage = () => {
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
                    <th>User</th>
                    <th>Photo</th>
                    <th>Status</th>
                    <th>CreatedTime</th>
                    <th>LastInTime</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">Zhihui Liu</th>
                    <td>[link]</td>
                    <td>Active</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td><Button>Delete</Button></td>
                  </tr>
                  <tr>
                    <th scope="row">Zhi Liu</th>
                    <td>[link]</td>
                    <td>Active</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td><Button>Delete</Button></td>
                  </tr>                  <tr>
                    <th scope="row">Zhui Lu</th>
                    <td>[link]</td>
                    <td>Active</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td><Button>Delete</Button></td>
                  </tr>                  <tr>
                    <th scope="row">Zhi Li</th>
                    <td>[link]</td>
                    <td>Active</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td>{new Date().toLocaleString()}</td>
                    <td><Button>Delete</Button></td>
                  </tr>
                </tbody>
              </Table>
            </CardBody>
          </Card>
        </Col>
      </Row>

      <button>Add User</button>

    </Page>
  );
};

export default CardPage;
