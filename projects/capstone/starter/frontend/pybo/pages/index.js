import Head from 'next/head';
import { Container, Row, Col, Button } from 'react-bootstrap';
import styles from '../styles/Home.module.css';

export default function Home() {
  return (
    <Container>
      <Row>
        <Col>
          <h1>Hello, Next.js with React Bootstrap!</h1>
          <p>
            This is an example of using React Bootstrap components in a Next.js
            application.
          </p>
          <Button variant="primary">Click me</Button>
        </Col>
      </Row>
    </Container>
  )
}
