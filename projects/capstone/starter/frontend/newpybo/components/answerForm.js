import FormError from "./formError";

export default function AnswerForm({ formRef, answer, errors, onClick }) {
  return (
    <div className="container">
      <h5 className="my-3 border-bottom pb-2">답변 수정</h5>
      <form ref={formRef}>
        {errors && <FormError errors={errors} />}
        <div className="mb-3">
          <label htmlFor="content">답변내용</label>
          <textarea
            className="form-control"
            name="content"
            rows="10"
            defaultValue={answer && answer.content}
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary" onClick={onClick}>
          저장하기
        </button>
      </form>
    </div>
  );
}
