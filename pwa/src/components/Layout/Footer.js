import React from 'react';

import { Navbar, Nav, NavItem } from 'reactstrap';

import SourceLink from 'components/SourceLink';

const Footer = () => {
  return (
    <Navbar>
      <Nav navbar>
        <NavItem>
          2022 Cornell University; Powered by React with React Reduction
        </NavItem>
      </Nav>
    </Navbar>
  );
};

export default Footer;
