import FormError from "./formError";

export default function QuestionForm({ formRef, question, errors, onClick }) {
  return (
    <div className="container">
      <h5 className="my-3 border-bottom pb-2">질문등록</h5>
      <form ref={formRef}>
        {errors && <FormError errors={errors} />}
        <div className="mb-3">
          <label htmlFor="subject">제목</label>
          <input
            type="text"
            className="form-control"
            name="subject"
            defaultValue={question && question.subject}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="content">내용</label>
          <textarea
            className="form-control"
            name="content"
            rows="10"
            defaultValue={question && question.content}
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary" onClick={onClick}>
          저장하기
        </button>
      </form>
    </div>
  );
}
