import { Container } from "reactstrap";
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import '../App.css';
import React, {useState, useEffect} from 'react';

function Navigate(){
    return(
      <div>
        <Navbar bg ="primary" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="/">ANT System</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/">ANT Home</Nav.Link>
              <Nav.Link href="/sensorreading">Live Sensor Reading</Nav.Link>
              <Nav.Link href="/datalog">Data Log</Nav.Link>
              <Nav.Link href="/querybydate">Query Data</Nav.Link>
              <Nav.Link href="/settings">Settings</Nav.Link>
              <Nav.Link href="/about">About Us</Nav.Link>
          </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      </div>
    );
}

export default Navigate;