import Head from "next/head";
import { useRouter } from "next/router";
import { useRef } from "react";
import useSWR from "swr";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useAuthToken } from "@/contexts/context";
import Link from "next/link";
import FormError from "@/components/formError";
import { useAuth0 } from "@auth0/auth0-react";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function Question() {
  // auth
  const { user } = useAuth0();
  const accessToken = useAuthToken();

  // router
  const router = useRouter();

  // refs
  const formRef = useRef();

  // question
  const {
    data: question,
    error,
    mutate,
  } = useSWR(`${process.env.API_URL}/question/${router.query.id}/`, fetcher, {
    keepPreviousData: true,
    revalidateOnFocus: false,
  });

  // delete question
  const handleDeleteQuestion = (e, questionId) => {
    e.preventDefault();
    if (!confirm("Are you sure you want to delete?")) {
      return;
    }
    mutate(
      async () => {
        const deleted = await fetch(`${process.env.API_URL}/question/${questionId}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
          .then((res) => res.json())
          .then((data) => data);

        if (deleted.errors) {
          return { ...question, ...deleted };
        }

        router.push("/");
        return;
      },
      { revalidate: false },
    );
  };

  // add question voter
  const handleAddQuestionVoter = (e, questionId) => {
    e.preventDefault();

    if (question.voter.filter((voter) => voter.email == (user && user.email)).length) {
      alert("Already voted.");
      return;
    }
    mutate(
      async () => {
        const voters = await fetch(`${process.env.API_URL}/question/${questionId}/vote`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
          .then((res) => res.json())
          .then((data) => data);

        // error
        if (voters.errors) {
          return { ...question, ...voters };
        }

        return { ...question, voter: [...voters], errors: undefined };
      },
      { revalidate: false },
    );
  };

  // add answer voter
  const handleAddAnswerVoter = (e, questionId, answerId) => {
    e.preventDefault();

    const answer = question.answer_set.filter((answer) => answer.id == answerId)[0];
    if (answer.voter.filter((voter) => voter.email == (user && user.email)).length) {
      alert("Already voted.");
      return;
    }
    mutate(
      async () => {
        const voters = await fetch(
          `${process.env.API_URL}/question/${questionId}/answer/${answerId}/vote`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        )
          .then((res) => res.json())
          .then((data) => data);

        // error
        if (voters.errors) {
          return { ...question, ...voters };
        }

        const answers = question.answer_set.map((answer) => {
          if (answer.id == answerId) {
            answer.voter = voters;
          }
          return { ...answer };
        });

        return { ...question, answer_set: [...answers], errors: undefined };
      },
      { revalidate: false },
    );
  };

  // create answer
  const handleCreateAnswer = (e, questionId) => {
    e.preventDefault();

    // remote mutate -> local mutate
    mutate(
      async () => {
        const answer = await fetch(`${process.env.API_URL}/question/${questionId}/answer`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: (() => {
            const formDate = new FormData(formRef.current);
            return JSON.stringify({ content: formDate.get("content") });
          })(),
        })
          .then((res) => res.json())
          .then((data) => data);

        // error
        if (answer.errors) {
          return { ...question, ...answer };
        }

        // form textarea
        formRef.current["content"].value = "";

        return {
          ...question,
          answer_set: [...question.answer_set, answer],
          errors: undefined,
        };
      },
      { revalidate: false },
    );
  };

  // delete answer
  const handleDeleteAnswer = (e, questionId, answerId) => {
    e.preventDefault();
    if (!confirm("Are you sure you want to delete?")) {
      return;
    }
    mutate(
      async () => {
        const deleted = await fetch(
          `${process.env.API_URL}/question/${questionId}/answer/${answerId}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        )
          .then((res) => res.json())
          .then((data) => data);

        if (deleted.errors) {
          return { ...question, ...deleted };
        }

        const answers = question.answer_set.filter((answer) => answerId != answer.id);
        return { ...question, answer_set: [...answers], errors: undefined };
      },
      { revalidate: false },
    );
  };

  if (error) return <div>Failed to load</div>;
  if (!question) return <div></div>;

  return (
    <>
      <Head>
        <title>{question.subject}</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <div className="container my-3">
          <h2 className="border-bottom py-2">{question.subject}</h2>
          <div className="card my-3">
            <div className="card-body">
              <div className="card-text">
                <ReactMarkdown children={question.content} remarkPlugins={[remarkGfm]} />
              </div>
              <div className="d-flex justify-content-end">
                {question.modify_date && (
                  <div className="badge bg-light text-dark p-2 text-start mx-3">
                    <div className="mb-2">modified at</div>
                    <div>{new Date(question.modify_date).toLocaleString("en")}</div>
                  </div>
                )}
                <div className="badge bg-light text-dark p-2 text-start">
                  <div className="mb-2">{question.user.email}</div>
                  <div>{new Date(question.create_date).toLocaleString("en")}</div>
                </div>
              </div>
              <div className="my-3">
                <a
                  href="#"
                  className="recommend btn btn-sm btn-outline-secondary me-1"
                  onClick={(e) => handleAddQuestionVoter(e, question.id)}
                >
                  {" "}
                  VOTE
                  <span className="badge rounded-pill bg-success ms-2">
                    {question.voter.length}
                  </span>
                </a>
                {user && user.email == question.user.email && (
                  <>
                    <Link
                      href={`/question/modify?id=${question.id}`}
                      className="btn btn-sm btn-outline-secondary me-1"
                    >
                      Modify
                    </Link>
                    <a
                      href="#"
                      className="delete btn btn-sm btn-outline-secondary"
                      onClick={(e) => handleDeleteQuestion(e, question.id)}
                    >
                      Delete
                    </a>
                  </>
                )}
              </div>
            </div>
          </div>
          {question.answer_set.length > 0 ? (
            <h5 className="border-bottom my-3 py-2">
              Check the Answer! count: {question.answer_set.length}
            </h5>
          ) : (
            <h5 className="border-bottom my-3 py-2">The answer does not exist.</h5>
          )}
          {question.answer_set.map((answer) => (
            <div key={answer.id}>
              <a id="answer_{answer.id}"></a>
              <div className="card my-3">
                <div className="card-body">
                  <ReactMarkdown children={answer.content} remarkPlugins={[remarkGfm]} />
                  <div className="d-flex justify-content-end">
                    {answer.modify_date && (
                      <div className="badge bg-light text-dark p-2 text-start mx-3">
                        <div className="mb-2">modified at</div>
                        <div>{new Date(answer.modify_date).toLocaleString("en")}</div>
                      </div>
                    )}
                    <div className="badge bg-light text-dark p-2 text-start">
                      <div className="mb-2">{answer.user.email}</div>
                      <div>{new Date(answer.create_date).toLocaleString("en")}</div>
                    </div>
                  </div>
                  <div className="my-3">
                    <a
                      href="#"
                      className="recommend btn btn-sm btn-outline-secondary me-1"
                      onClick={(e) => handleAddAnswerVoter(e, question.id, answer.id)}
                    >
                      {" "}
                      VOTE
                      <span className="badge rounded-pill bg-success ms-2">
                        {answer.voter.length}
                      </span>
                    </a>
                    {user && user.email == answer.user.email && (
                      <>
                        <Link
                          href={`/answer/modify?id=${answer.id}&question_id=${question.id}`}
                          className="btn btn-sm btn-outline-secondary me-1"
                        >
                          Modify
                        </Link>
                        <a
                          href="#"
                          className="delete btn btn-sm btn-outline-secondary "
                          onClick={(e) => handleDeleteAnswer(e, question.id, answer.id)}
                        >
                          Delete
                        </a>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
          <form ref={formRef}>
            {question.errors && <FormError errors={question.errors} />}
            {user && (
              <>
                <div className="mb-3">
                  <textarea
                    disabled={user.email ? false : "disabled"}
                    name="content"
                    id="content"
                    className="form-control"
                    rows="10"
                  ></textarea>
                </div>
                <input
                  type="button"
                  value="Save the Answer"
                  className="btn btn-primary"
                  onClick={(e) => handleCreateAnswer(e, question.id)}
                />
              </>
            )}
          </form>
        </div>
      </main>
    </>
  );
}
