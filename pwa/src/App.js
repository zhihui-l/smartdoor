import MainLayout  from 'components/MainLayout';
import React from 'react';
import componentQueries from 'react-component-queries';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';
import './styles/reduction.scss';
import { Spinner } from 'reactstrap';

import AuthPage from 'pages/AuthPage';
const UsersPage = React.lazy(() => import('pages/UsersPage'));
const DashboardPage = React.lazy(() => import('pages/DashboardPage'));
const LogPage = React.lazy(() => import('pages/LogPage'));


const PageSpinner = ({ color = 'primary' }) => {
  return (
    <div className="cr-page-spinner">
      <Spinner color={color} />
    </div>
  );
};


const getBasename = () => {
  return `/${process.env.PUBLIC_URL.split('/').pop()}`;
};

class App extends React.Component {
  render() {
    return (
      <BrowserRouter basename={getBasename()}>
          <Switch>
           <Route exact path="/login" component={AuthPage} />
            <MainLayout breakpoint={this.props.breakpoint}>
              <React.Suspense fallback={<PageSpinner />}>
                <Route exact path="/" component={DashboardPage} />
                <Route exact path="/users" component={UsersPage} />
                <Route exact path="/log" component={LogPage} />
              </React.Suspense>
            </MainLayout>
            <Redirect to="/" />
          </Switch>
      </BrowserRouter>
    );
  }
}

const query = ({ width }) => {
  if (width < 575) {
    return { breakpoint: 'xs' };
  }

  if (576 < width && width < 767) {
    return { breakpoint: 'sm' };
  }

  if (768 < width && width < 991) {
    return { breakpoint: 'md' };
  }

  if (992 < width && width < 1199) {
    return { breakpoint: 'lg' };
  }

  if (width > 1200) {
    return { breakpoint: 'xl' };
  }

  return { breakpoint: 'xs' };
};

export default componentQueries(query)(App);
