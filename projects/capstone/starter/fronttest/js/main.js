function fetchData() {
  fetch("http://127.0.0.1:5000/question/list")
    .then(function (data) {
      return data.json();
    })
    .then(function (data) {
      var questions = data.questions;

      var template = `
        <table class="table">
            <thead>
                <tr class="text-center table-dark">
                    <th>번호</th>
                    <th style="width: 50%;">제목</th>
                    <th>글쓴이</th>
                    <th>작성일시</th>
                </tr>
            </thead>
            <tbody>
                <tr class="text-center">{rows}</tr>
            </tbody>
        </table>
  `;

      var rows = "";
      questions.forEach(function (question) {
        var {
          id,
          subject,
          user: { username },
          create_date,
        } = question;
        var row = `
        <tr>
          <td>${id}</td>
          <td><a href="http://127.0.0.1:5000/question/detail/${id}">${subject}</a></td>
          <td>${username}</td>
          <td>${create_date}</td>
        </tr>
      `;

        rows += row;
      });

      template = template.replace("{rows}", rows);

      var tableDiv = document.querySelector("#question-list");
      tableDiv.innerHTML = template;
    });
}


document.querySelector('#load').addEventListener('click', function(e) {
  e.preventDefault();
  fetchData();
})

