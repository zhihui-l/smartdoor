import React from 'react';
import {
  Button,
  Nav,
  Navbar,
  NavItem,
  Container,
  NavLink as BSNavLink,
} from 'reactstrap';
import {
  MdClearAll,
} from 'react-icons/md';
import sidebarBgImage from 'assets/img/sidebar/sidebar-4.jpg';
import { FaGithub } from 'react-icons/fa'; 
import {
  MdBorderAll,
  MdDashboard,
  MdWeb,
} from 'react-icons/md';
import { NavLink } from 'react-router-dom';




const sidebarBackground = {
  backgroundImage: `url("${sidebarBgImage}")`,
  backgroundSize: 'cover',
  backgroundRepeat: 'no-repeat',
};



const navItems = [
  { to: '/', name: 'dashboard', exact: true, Icon: MdDashboard },
  { to: '/users', name: 'users', exact: false, Icon: MdWeb },
  { to: '/log', name: 'log', exact: false, Icon: MdBorderAll }
];

class Sidebar extends React.Component {

  handleClick = name => () => {
    this.setState(prevState => {
      const isOpen = prevState[`isOpen${name}`];

      return {
        [`isOpen${name}`]: !isOpen,
      };
    });
  };

  render() {
    return (
      <aside className="cr-sidebar" data-image={sidebarBgImage}>
        <div className="cr-sidebar__background" style={sidebarBackground} />
        <div className="cr-sidebar__content">
          <Navbar>
          <a href={process.env.REACT_APP_SOURCE_URL} target="_blank" rel="noopener noreferrer" className="navbar-brand d-flex">
              <span className="text-white">
                Smart Door <FaGithub />
              </span>
            </a>
          </Navbar>
          <Nav vertical>
            {navItems.map(({ to, name, exact, Icon }, index) => (
              <NavItem key={index} className="cr-sidebar__nav-item">
                <BSNavLink
                  id={`navItem-${name}-${index}`}
                  className="text-uppercase"
                  tag={NavLink}
                  to={to}
                  activeClassName="active"
                  exact={exact}
                >
                  <Icon className="cr-sidebar__nav-item-icon" />
                  <span className="">{name}</span>
                </BSNavLink>
              </NavItem>
            ))}

          </Nav>
        </div>
      </aside>
    );
  }
}




const Content = ({ tag: Tag, className, ...restProps }) => {
  const classes = 'cr-content '+className;

  return <Tag className={classes} {...restProps} />;
};

Content.defaultProps = {
  tag: Container,
};


class Header extends React.Component {

  handleSidebarControlButton = event => {
    event.preventDefault();
    event.stopPropagation();

    document.querySelector('.cr-sidebar').classList.toggle('cr-sidebar--open');
  };

  render() {
    return (
      <Navbar light expand className='cr-header bg-white'>
        <Nav navbar className="mr-2">
          <Button outline onClick={this.handleSidebarControlButton}>
            <MdClearAll size={25} />
          </Button>
        </Nav>


        <Nav navbar className="cr-header__nav-right">
          <Button outline onClick={function(){window.location.href = '/login'}}>Logout
          </Button>
        </Nav>
      </Navbar>
    );
  }
}


const Footer = () => {
  return (
    <Navbar>
      <Nav navbar>
        <NavItem>
          2022 Cornell University; Powered by React 
        </NavItem>
      </Nav>
    </Navbar>
  );
};




class MainLayout extends React.Component {
  static isSidebarOpen() {
    return document
      .querySelector('.cr-sidebar')
      .classList.contains('cr-sidebar--open');
  }

  componentWillReceiveProps({ breakpoint }) {
    if (breakpoint !== this.props.breakpoint) {
      this.checkBreakpoint(breakpoint);
    }
  }

  componentDidMount() {
    this.checkBreakpoint(this.props.breakpoint);
  }

  // close sidebar when
  handleContentClick = event => {
    // close sidebar if sidebar is open and screen size is less than `md`
    if (
      MainLayout.isSidebarOpen() &&
      (this.props.breakpoint === 'xs' ||
        this.props.breakpoint === 'sm' ||
        this.props.breakpoint === 'md')
    ) {
      this.openSidebar('close');
    }
  };

  checkBreakpoint(breakpoint) {
    switch (breakpoint) {
      case 'xs':
      case 'sm':
      case 'md':
        return this.openSidebar('close');

      case 'lg':
      case 'xl':
      default:
        return this.openSidebar('open');
    }
  }

  openSidebar(openOrClose) {
    if (openOrClose === 'open') {
      return document
        .querySelector('.cr-sidebar')
        .classList.add('cr-sidebar--open');
    }
    document.querySelector('.cr-sidebar').classList.remove('cr-sidebar--open');
  }

  render() {
    const { children } = this.props;
    return (
      <main className="cr-app bg-light">
        <Sidebar />
        <Content fluid onClick={this.handleContentClick}>
          <Header />
          {children}
          <Footer />
        </Content>
      </main>
    );
  }
}

export default MainLayout;
