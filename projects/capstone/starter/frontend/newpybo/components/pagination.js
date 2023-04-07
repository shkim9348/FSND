export default function Pagination({ pagination, onPageChange }) {
  return (
    <ul className="pagination justify-content-center">
      {pagination.has_prev ? (
        <li className="page-item">
          <a
            className="page-link"
            onClick={() => onPageChange(pagination.prev_num)}
          >
            Prev
          </a>
        </li>
      ) : (
        <li className="page-item disabled">
          <a className="page-link" tabIndex="-1" aria-disabled="true">
            Prev
          </a>
        </li>
      )}
      {pagination.page_nums.map(function (page_num, i) {
        if (page_num) {
          if (page_num != pagination.page) {
            return (
              <li className="page-item" key={page_num}>
                <a
                  className="page-link"
                  onClick={() => onPageChange(page_num)}
                >
                  {page_num}
                </a>
              </li>
            );
          } else {
            return (
              <li className="page-item active" aria-current="page" key={page_num}>
                <a className="page-link" onClick={() => onPageChange(page_num)}>
                  {page_num}
                </a>
              </li>
            );
          }
        } else {
          return (
            <li className="disabled" key={Math.random()}>
              <a className="page-link">...</a>
            </li>
          );
        }
      })}
      {pagination.has_next ? (
        <li className="page-item">
          <a
            className="page-link"
            onClick={() => onPageChange(pagination.next_num)}
          >
            Next
          </a>
        </li>
      ) : (
        <li className="page-item disabled">
          <a className="page-link" tabIndex="-1" aria-disabled="true">
            Next
          </a>
        </li>
      )}
    </ul>
  );
}
