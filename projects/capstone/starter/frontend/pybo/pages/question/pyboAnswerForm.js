import Head from "next/head";
import useSWR from 'swr'
import {useRouter} from "next/router";
import { Button, Container, Form } from "react-bootstrap";
import PyboNavBar from "../../components/pyboNavBar";
import {useState} from "react";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function PyboAnswerForm() {
  const router = useRouter();
  const questionId = router.query["question_id"]

  const { data, error, isLoading } = useSWR(
    `http://127.0.0.1:5000/question/detail/${questionId}/`,
    fetcher,
  );

  const [answerContent, setAnswerContent] = useState("")

  if (error) return <div>failed to load</div>;
  if (isLoading) return <div>loading...</div>;

  console.log(data)

  return (
    <>
      <Head>
        <title>Modify the Answer</title>
      </Head>
      <PyboNavBar />
      <Container>
        <h5 className="my-3 border-bottom pb-2">Modify the Answer</h5>
        <Form>
          <div className="mb-3">
            <Form.Label>Content</Form.Label>
            <Form.Control as="textarea" rows={10} value={answerContent} onChange={(e) => setAnswerContent(e.target.value)} />
          </div>
          <Button variant="primary" type="submit">
            Save
          </Button>
        </Form>
      </Container>
    </>
  );
}
