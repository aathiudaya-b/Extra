document.getElementById('learnForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  const res = await fetch('https://extra-fm3q.onrender.com/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  document.getElementById('planOutput').innerText = result.plan;
});

async function chatWithAgent() {
  const message = document.getElementById('chatInput').value;

  const res = await fetch('https://extra-fm3q.onrender.com/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: message })
  });

  const result = await res.json();
  document.getElementById('chatOutput').innerText = result.reply;
}
