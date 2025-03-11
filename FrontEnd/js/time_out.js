const timeoutDuration = 30*60*1000; 

function clearToken() {
  localStorage.removeItem('access_token');
  console.log('JWT token cleared from localStorage');
}

setTimeout(clearToken, timeoutDuration);