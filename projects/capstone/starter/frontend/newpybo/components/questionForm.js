import FormError from "./formError";

export default function QuestionForm({ formRef, question, errors, onClick }) {
  return (
    <div className="container">
      <h5 className="my-3 border-bottom pb-2">Write the Post!</h5>
      <form ref={formRef}>
        {errors && <FormError errors={errors} />}
        <div className="mb-3">
          <label htmlFor="subject">Subejct</label>
          <input
            type="text"
            className="form-control"
            name="subject"
            placeholder="(required)"
            defaultValue={question && question.subject}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="content">Content</label>
          <textarea
            className="form-control"
            name="content"
            rows="10"
            placeholder="(required)"
            defaultValue={question && question.content}
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary" onClick={onClick}>
          Save the Post
        </button>
      </form>
    </div>
  );
}
