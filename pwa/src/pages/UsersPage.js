import Page from 'components/Page';
import React from 'react';
import {
  Button,
  Card,
  CardBody,
  Col,
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
