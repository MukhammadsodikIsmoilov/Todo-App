import axios from "axios";

let BASE_URL;

if(process.env.NODE_ENV === 'production')
  BASE_URL = process.env.REACT_APP_PROD_BASE_URL;
else 
  BASE_URL = process.env.REACT_APP_DEV_BASE_URL


export async function fetchTaskList() {
  const res = await axios({
    method: "GET",
    url: `${BASE_URL}/todos`,
    headers: {
      Accept: "application/json",
    },
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data;
}

export async function fetchActiveTasks() {
  const res = await axios({
    method: "GET",
    url: `${BASE_URL}/todos&active=True`,
    headers: {
      Accept: "application/json",
    },
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data;
}

export async function fetchCompletedTasks() {
  const res = await axios({
    method: "GET",
    url: `${BASE_URL}/todos&is_completed=True`,
    headers: {
      Accept: "application/json",
    },
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data;
}

export async function addNewTask(todo) {
  const res = await axios({
    method: "POST",
    url: `${BASE_URL}/todos/create/`,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    data: {
      title: todo,
    },
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data;
}

export async function deleteTask(todo) {
  const res = await axios({
    method: "DELETE",
    url: `${BASE_URL}/todos/${todo.id}/delete/`,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    data: todo,
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data.message;
}

export async function clearTasks() {
  const res = await axios({
    method: "DELETE",
    url: `${BASE_URL}/todos/delete/`,
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data.message;
}

export async function updateTask(todo) {
  const res = await axios({
    method: "PUT",
    url: `${BASE_URL}/todos/${todo.id}/update/`,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    data: {
      title: todo.title,
      is_completed: todo.is_completed,
    },
  });

  if (res.status >= 400) throw new Error(res.data.error);

  return res.data;
}
