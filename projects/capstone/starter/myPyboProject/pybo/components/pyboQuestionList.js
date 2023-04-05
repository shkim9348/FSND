import { Button, Col, Container, Form, InputGroup, Pagination, Row, Table } from "react-bootstrap";
import Link from "next/link";
import useSWR from "swr";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function PyboQuestionList() {
  const { data, error } = useSWR("http://127.0.0.1:5000/question/list", fetcher);

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <Container className="my-3">
      <Row className="my-3">
        <Col className="col-6">
          <Button variant="primary" href="/">
            Create Question
          </Button>
        </Col>
        <Col className="col-6">
          <InputGroup>
            <Form.Control placeholder="Input keyword" />
            <Button variant="outline-secondary" id="btn_search">
              Search
            </Button>
          </InputGroup>
        </Col>
      </Row>
      <Table>
        <thead>
          <tr className="text-center table-dark">
            <th>No.</th>
            <th style={{ width: "50%" }}>Subject</th>
            <th>User</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {data.questions &&
            data.questions.map(function (q) {
              return (
                <tr id={q.id} className="text-center">
                  <td>{q.id}</td>
                  <td className="text-start">
                    <Link href={`/question/${q.id}`}>{q.subject} </Link>
                  </td>
                  <td>{q.user.username}</td>
                  <td>{q.create_date}</td>
                </tr>
              );
            })}
        </tbody>
      </Table>
      <Pagination className="justify-content-center">
        <Pagination.Prev />
        <Pagination.Item>{1}</Pagination.Item>
        <Pagination.Ellipsis />

        <Pagination.Item>{10}</Pagination.Item>

        <Pagination.Ellipsis />
        <Pagination.Item>{40}</Pagination.Item>
        <Pagination.Next />
      </Pagination>
    </Container>
  );
}
