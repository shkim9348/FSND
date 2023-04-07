import useSWR from "swr";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export class Question {
  constructor(id, subject, content, create_date, user_id, user, modify_date, voter) {
    this.id = id;
    this.subject = subject;
    this.content = content;
    this.create_date = create_date;
    this.user_id = user_id;
    this.user = user;
    this.modify_date = modify_date;
    this.voter = voter;
  }

  // question list
  static getAll(page, kw) {
    const { data: questions, error } = useSWR(
      `${process.env.API_URL}/question/?page=${page}&kw=${kw}`,
      fetcher,
      {
        keepPreviousData: true,
        revalidateOnFocus: false,
      },
    );
    return {
      questions,
      error,
    }
  }

  // static async getAllQuestions() {
  //   const response = await fetch("/api/questions");
  //   const data = await response.json();
  //   return data;
  // }

  // static async getQuestionById(id) {
  //   const response = await fetch(`/api/questions/${id}`);
  //   const data = await response.json();
  //   return data;
  // }

  // async save() {
  //   const response = await fetch("/api/questions", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify(this),
  //   });
  //   const data = await response.json();
  //   return data;
  // }

  // async update() {
  //   const response = await fetch(`/api/questions/${this.id}`, {
  //     method: "PUT",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify(this),
  //   });
  //   const data = await response.json();
  //   return data;
  // }

  // static async deleteQuestionById(id) {
  //   const response = await fetch(`/api/questions/${id}`, {
  //     method: "DELETE",
  //   });
  //   const data = await response.json();
  //   return data;
  // }
}
