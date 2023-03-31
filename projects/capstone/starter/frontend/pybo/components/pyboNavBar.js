import { Navbar, Container, Nav } from "react-bootstrap";

export default function PyboNavBar() {
  return (
    <Navbar bg="light" variant="light" expand="lg" className="border-bottom">
      <Container fluid>
        <Navbar.Brand href="http://localhost:3000/">Pybo</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Item>
            <Nav.Link href="/">Sign up</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/">Sign in</Nav.Link>
          </Nav.Item>
        </Nav>
      </Container>
    </Navbar>
  );
}
