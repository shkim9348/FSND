import Head from "next/head";
import { useRouter } from "next/router";
import { useRef } from "react";
import useSWR from "swr";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { getCsrfToken, useAuthContext } from "@/contexts/context";
import Link from "next/link";
import FormError from "@/components/formError";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function Question() {
  // auth
  const { user, accessToken } = useAuthContext();

  // router
  const router = useRouter();

  // refs
  const formRef = useRef();

  // question
  const {
    data: question,
    error,
    mutate,
  } = useSWR(`${process.env.API_URL}/question/detail/${router.query.id}/`, fetcher, {
    keepPreviousData: true,
    revalidateOnFocus: false,
  });

  // delete question
  const handleDeleteQuestion = (e, questionId) => {
    e.preventDefault();
    if (!confirm("정말로 삭제하시겠습니까?")) {
      return;
    }
    mutate(
      async () => {
        const deleted = await fetch(`${process.env.API_URL}/question/delete/${questionId}`, {
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

  // add/remove question voter
  const handleAddQuestionVoter = (e, questionId) => {
    e.preventDefault();

    if (question.voter.filter((voter) => voter.email == user.email).length) {
      alert("이미 추천하셨습니다.");
      return;
    }
    mutate(
      async () => {
        const voters = await fetch(`${process.env.API_URL}/question/vote/${questionId}`, {
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

  // add/remove answer voter
  const handleAddAnswerVoter = (e, answerId) => {
    e.preventDefault();

    const answer = question.answer_set.filter((answer) => answer.id == answerId)[0];
    if (answer.voter.filter((voter) => voter.email == user.email).length) {
      alert("이미 추천하셨습니다.");
      return;
    }
    mutate(
      async () => {
        const voters = await fetch(`${process.env.API_URL}/answer/vote/${answerId}`, {
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

        const answers = question.answer_set.map((answer) => {
          if (answer.id == answerId) {
            answer.voter = voters;
          }
          return {...answer};
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
        const answer = await fetch(`${process.env.API_URL}/answer/create/${questionId}`, {
          method: "POST",
          headers: {
            // pybo server가 html/api 방식을 공유하기 때문에 form으로 전송
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: `Bearer ${accessToken}`,
          },
          credentials: "include",
          body: await (async () => {
            const formDate = new FormData(formRef.current);
            // csrftoken을 form fieldf 전송
            formDate.append("csrf_token", await getCsrfToken());
            return new URLSearchParams(formDate);
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
  const handleDeleteAnswer = (e, answerId) => {
    e.preventDefault();
    if (!confirm("정말로 삭제하시겠습니까?")) {
      return;
    }
    mutate(
      async () => {
        const deleted = await fetch(`${process.env.API_URL}/answer/delete/${answerId}`, {
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
        <title>Create Next App</title>
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
                <ReactMarkdown children={question.content} remarkPlugins={[remarkGfm]} />,
              </div>
              <div className="d-flex justify-content-end">
                {question.modify_date && (
                  <div className="badge bg-light text-dark p-2 text-start mx-3">
                    <div className="mb-2">modified at</div>
                    <div>{new Date(question.modify_date).toLocaleString("ko")}</div>
                  </div>
                )}
                <div className="badge bg-light text-dark p-2 text-start">
                  <div className="mb-2">{question.user.email}</div>
                  <div>{new Date(question.create_date).toLocaleString("ko")}</div>
                </div>
              </div>
              <div className="my-3">
                <a
                  href="#"
                  className="recommend btn btn-sm btn-outline-secondary"
                  onClick={(e) => handleAddQuestionVoter(e, question.id)}
                >
                  {" "}
                  추천
                  <span className="badge rounded-pill bg-success">{question.voter.length}</span>
                </a>
                {user.email == question.user.email && (
                  <>
                    <Link
                      href={`/question/modify?id=${question.id}`}
                      className="btn btn-sm btn-outline-secondary"
                    >
                      수정
                    </Link>
                    <a
                      href="#"
                      className="delete btn btn-sm btn-outline-secondary"
                      onClick={(e) => handleDeleteQuestion(e, question.id)}
                    >
                      삭제
                    </a>
                  </>
                )}
              </div>
            </div>
          </div>
          <h5 className="border-bottom my-3 py-2">
            {question.answer_set.length}개의 답변이 있습니다.
          </h5>
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
                        <div>{new Date(answer.modify_date).toLocaleString("ko")}</div>
                      </div>
                    )}
                    <div className="badge bg-light text-dark p-2 text-start">
                      <div className="mb-2">{answer.user.email}</div>
                      <div>{new Date(answer.create_date).toLocaleString("ko")}</div>
                    </div>
                  </div>
                  <div className="my-3">
                    <a
                      href="#"
                      className="recommend btn btn-sm btn-outline-secondary"
                      onClick={(e) => handleAddAnswerVoter(e, answer.id)}
                    >
                      {" "}
                      추천
                      <span className="badge rounded-pill bg-success">{answer.voter.length}</span>
                    </a>
                    {user.email == answer.user.email && (
                      <>
                        <Link
                          href={`/answer/modify?id=${answer.id}`}
                          className="btn btn-sm btn-outline-secondary"
                        >
                          수정
                        </Link>
                        <a
                          href="#"
                          className="delete btn btn-sm btn-outline-secondary "
                          onClick={(e) => handleDeleteAnswer(e, answer.id)}
                        >
                          삭제
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
              value="답변등록"
              className="btn btn-primary"
              onClick={(e) => handleCreateAnswer(e, question.id)}
            />
          </form>
        </div>
      </main>
    </>
  );
}
