// src/utils/auth.js
export async function getUserInfo() {
  const access_token = localStorage.getItem('access_token');
  if (!access_token) return null;

  try {
    const response = await fetch('http://127.0.0.1:5000/get-user-info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + access_token
      }
    });

    if (!response.ok) return null;

    const data = await response.json();
    return data.user;
  } catch (err) {
    return null;
  }
}
