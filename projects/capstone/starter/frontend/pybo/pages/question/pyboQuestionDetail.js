import { Badge, Button, Card, Container, Form } from "react-bootstrap";
import { useRouter } from "next/router";
import useSWR from "swr";
import PyboNavBar from "../../components/pyboNavBar";
import {useState} from "react";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function PyboQuestionDetail() {
  const router = useRouter();
  const questionId = router.query["question_id"];

  const { data, error } = useSWR(`http://127.0.0.1:5000/question/detail/${questionId}/`, fetcher);

  const [answerContent, setAnswerContent] = useState("");
  const [answerSet, setAnswerSet] = useState([]);

  const submitAnswer = (e) => {
    e.preventDefault();

    const newAnswer = {
      content: answerContent,
    };

    setAnswerSet([...answerSet, newAnswer]);

    setAnswerContent("");
  };

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  const question = data;
  const user = question.user;

  return (
    <>
      <PyboNavBar />
      <Container>
        <h2 className="border-bottom py-2">{question.subject}</h2>
        <Card className="my-3">
          <Card.Body>
            <Card.Text>{question.content}</Card.Text>
            <div className="d-flex justify-content-end">
              {question.modify_date && (
                <Badge bg="light" className="text-dark p-2 text-start mx-3">
                  <div className="mb-2">modified at</div>
                  <div>{question.modify_date}</div>
                </Badge>
              )}
              <Badge bg="light" className="text-dark p-2 text-start mx-3">
                <div className="mb-2">{user && user.username}</div>
                <div>{question.create_date}</div>
              </Badge>
            </div>
            <div className="my-3">
              <Button variant="outline-secondary" size="sm" className="mx-1">
                수정
              </Button>
              <Button variant="outline-secondary" size="sm">
                삭제
              </Button>
            </div>
          </Card.Body>
        </Card>
        <h5 className="border-bottom my-3 py-2">
          {question.answer_set && question.answer_set.length}개의 답변이 있습니다.
        </h5>
        <Card className="my-3">
          <Card.Body>
            {question.answer_set &&
              question.answer_set.map((answer) => (
                <div key={answer.id}>
                  <Card.Text>{answer.content}</Card.Text>
                  <div className="d-flex justify-content-end">
                    {answer.modify_date && (
                      <Badge bg="light" className="text-dark p-2 text-start mx-3">
                        <div className="mb-2">modified at</div>
                        <div>{answer.modify_date}</div>
                      </Badge>
                    )}
                    <Badge bg="light" className="text-dark p-2 text-start mx-3">
                      <div className="mb-2">{user && user.username}</div>
                      <div>{answer.create_date}</div>
                    </Badge>
                  </div>
                  <div className="my-3">
                    <Button variant="outline-secondary" size="sm" className="mx-1">
                      수정
                    </Button>
                    <Button variant="outline-secondary" size="sm">
                      삭제
                    </Button>
                  </div>
                </div>
              ))}
          </Card.Body>
        </Card>
        <Form onSubmit={submitAnswer}>
          <div className="mb-3">
            <Form.Control
              as="textarea"
              rows={10}
              value={answerContent}
              onChange={(e) => setAnswerContent(e.target.value)}
            />
          </div>
          <Button type="submit">Submit Answer</Button>
        </Form>
      </Container>
    </>
  );
}
