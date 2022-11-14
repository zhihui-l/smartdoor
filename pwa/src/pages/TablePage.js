import Page from 'components/Page';
import React from 'react';
import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

const tableTypes = ['', 'bordered', 'striped', 'hover'];

const TablePage = () => {
  return (
    <Page
      title="Log"
      breadcrumbs={[{ name: 'Log', active: true }]}
      className="TablePage"
    >


      <Row>
        <Col>
          <Card className="mb-3">
            <CardHeader>Log</CardHeader>
            <CardBody>
              <Table responsive>
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>User</th>
                    <th>Status</th>
                    <th>Method</th>
                    <th>Photo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">{new Date().toLocaleString()}</th>
                    <td>Zhihui Liu</td>
                    <td>Facial Recog</td>
                    <td>Approved</td>
                    <td>[link]</td>
                  </tr>
                  <tr>
                    <th scope="row">{new Date().toLocaleString()}</th>
                    <td>Zhihui Liu</td>
                    <td>Facial Recog</td>
                    <td>Approved</td>
                    <td>[link]</td>
                  </tr>                  <tr>
                    <th scope="row">{new Date().toLocaleString()}</th>
                    <td>Zhihui Liu</td>
                    <td>Facial Recog</td>
                    <td>Approved</td>
                    <td>[link]</td>
                  </tr>                  <tr>
                    <th scope="row">{new Date().toLocaleString()}</th>
                    <td>Zhihui Liu</td>
                    <td>Facial Recog</td>
                    <td>Approved</td>
                    <td>[link]</td>
                  </tr>
                </tbody>
              </Table>
            </CardBody>
          </Card>
        </Col>
      </Row>

    </Page>
  );
};

export default TablePage;
