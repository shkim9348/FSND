import Head from "next/head";
import { useState } from "react";
import { Button, Container, Form } from "react-bootstrap";
import PyboNavBar from "../../components/pyboNavBar";

export default function PyboWriteQuestion() {
  const [questionSubject, setQuestionSubject] = useState("");
  const [questionContent, setQuestionContent] = useState("");

  const submitQuestion = (e) => {
    e.preventDefault();

    // TODO : Need user_id when use auth0
    const newQuestion = {
      subject: questionSubject,
      content: questionContent,
      user_id: 1,
    };

    fetch(`http://127.0.0.1:5000/question/create/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newQuestion),
    })
      .then((response) => response.json())
      .then(() => {
        // Go to Home
        window.location.href = window.location.origin;
      })
      .catch((error) => {
        // 서버로부터 응답이 실패했을 때 처리할 코드 작성
        console.error(error);
      });
  };

  return (
    <>
      <Head>
        <title>Write the Question</title>
      </Head>
      <PyboNavBar />
      <Container>
        <h5 className="my-3 border-bottom pb-2">Write the Question</h5>
        <Form onSubmit={submitQuestion}>
          <div className="mb-3">
            <Form.Label>Subject</Form.Label>
            <Form.Control
              type="text"
              value={questionSubject}
              onChange={(e) => setQuestionSubject(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <Form.Label>Content</Form.Label>
            <Form.Control
              as="textarea"
              rows={10}
              value={questionContent}
              onChange={(e) => setQuestionContent(e.target.value)}
            />
          </div>
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Container>
    </>
  );
}
