import Head from "next/head";
import useSWR from "swr";
import { Button, Container, Form } from "react-bootstrap";
import PyboNavBar from "../../components/pyboNavBar";
import { useRouter } from "next/router";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function PyboModifyQuestion() {
  const router = useRouter();
  const questionId = router.query["question_id"];

  const {
    data: questionData,
    error,
    isLoading,
  } = useSWR(`http://127.0.0.1:5000/question/modify/${questionId}`, fetcher);

  const setQuestionSubject = (subject) => {
    questionData.subject = subject;
  }

  const setQuestionContent = (content) => {
    questionData.content = content;
  }

  const saveQuestion = (e) => {
    e.preventDefault();

    // TODO : Need user_id when use auth0
    const modifyQuestion = {
      subject: questionData.subject,
      content: questionData.content,
      user_id: 1,
    };

    fetch(`http://127.0.0.1:5000/question/modify/${questionId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(modifyQuestion),
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
        <title>Edit the Question</title>
      </Head>
      <PyboNavBar />
      <Container>
        <h5 className="my-3 border-bottom pb-2">Edit the Question</h5>
        <Form onSubmit={saveQuestion}>
          <div className="mb-3">
            <Form.Label>Subject</Form.Label>
            <Form.Control
              type="text"
              defaultValue={questionData.subject}
              onChange={(e) => setQuestionSubject(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <Form.Label>Content</Form.Label>
            <Form.Control
              as="textarea"
              rows={10}
              defaultValue={questionData.content}
              onChange={(e) => setQuestionContent(e.target.value)}
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
