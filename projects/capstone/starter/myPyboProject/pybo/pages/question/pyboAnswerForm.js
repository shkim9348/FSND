import Head from "next/head";
import useSWR from "swr";
import { useRouter } from "next/router";
import { Button, Container, Form } from "react-bootstrap";
import PyboNavBar from "../../components/pyboNavBar";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function PyboAnswerForm() {
  // router
  const router = useRouter();
  const answerId = router.query["answer_id"];
  const questionId = router.query["question_id"];

  // useSWR
  const {
    data: answerData,
    error,
    isLoading,
  } = useSWR(`http://127.0.0.1:5000/answer/modify/${answerId}`, fetcher);

  const setAnswerContent = (content) => {
    answerData.content = content;
  };

  const saveAnswer = (e) => {
    e.preventDefault();

    // TODO : Need user_id when use auth0
    const modifyAnswer = {
      content: answerData.content,
      user_id: 1,
    };

    fetch(`http://127.0.0.1:5000/answer/modify/${answerId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(modifyAnswer),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error(error);
      });

    // Go to Question detail
    window.location.href =
      window.location.origin + `/question/pyboQuestionDetail?question_id=${questionId}`;
  };

  if (error) return <div>Failed to load</div>;
  if (isLoading) return <div>Loading...</div>;

  return (
    <>
      <Head>
        <title>Modify the Answer</title>
      </Head>
      <PyboNavBar />
      <Container>
        <h5 className="my-3 border-bottom pb-2">Modify the Answer</h5>
        <Form onSubmit={saveAnswer}>
          <div className="mb-3">
            <Form.Label>Content</Form.Label>
            <Form.Control
              as="textarea"
              rows={10}
              defaultValue={answerData.content}
              onChange={(e) => setAnswerContent(e.target.value)}
            />
          </div>
          <Button variant="primary" type="submit">
            Save
          </Button>
        </Form>
      </Container>
    </>
  );
}
