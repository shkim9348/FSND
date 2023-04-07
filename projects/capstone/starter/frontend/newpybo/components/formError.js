export default function FormError({ errors }) {
  return (
    <div className="alert alert-danger" role="alert">
      {Object.entries(errors).map((error) => (
        <div key={error[0]}>
          <strong>{error[0]}</strong>
          <ul>
            {error[1].map((message) => (
              <li key={message}>{message}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
