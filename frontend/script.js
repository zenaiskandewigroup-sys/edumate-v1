///// ====== Auto-detect API base ======
function detectApiBase() {
  const origin = window.location.origin || "";
  if (origin.includes("localhost") || origin.includes("127.0.0.1")) {
    return "http://127.0.0.1:8080";
  }
  return origin;
}
const API_BASE = detectApiBase();

///// ====== API helpers ======
async function apiPost(path, body = {}) {
  if (!path.startsWith("/")) path = "/" + path;
  const url = `${API_BASE}${path}`;
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

async function apiGet(path) {
  if (!path.startsWith("/")) path = "/" + path;
  const url = `${API_BASE}${path}`;
  return fetch(url, { method: "GET" });
}

///// ====== Utils ======
function norm(s) {
  return String(s || "").trim().replace(/\s+/g, " ").toLowerCase();
}
function qText(q) {
  return q.q || q.question || q.text || "";
}
function escapeHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/>/g, "&gt;")
    .replace(/</g, "&lt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

///// ====== SPLASH ======
window.addEventListener("DOMContentLoaded", () => {
  const overlay = document.getElementById("loadingOverlay");
  overlay && overlay.classList.add("hidden");

  if (document.body.classList.contains("splash")) {
    setTimeout(() => (window.location.href = "login.html"), 1500);
  }

  const quizBtn = document.getElementById("startQuiz");
  if (quizBtn) quizBtn.addEventListener("click", startQuizRequest);
});

///// ====== LOGIN ======
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById("loginMessage");
    msgEl && (msgEl.innerText = "");

    const username = document.getElementById("username").value || "";
    const password = document.getElementById("password").value || "";

    if (!username || !password) {
      msgEl.innerText = "Username dan password wajib diisi.";
      return;
    }

    try {
      const res = await apiPost("/api/auth/login", { username, password });
      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        msgEl.innerText = data.msg || data.error || "Login gagal.";
        return;
      }

      localStorage.setItem("username", username);
      msgEl.innerText = "Login berhasil. Mengalihkan...";
      setTimeout(() => (window.location.href = "home.html"), 800);
    } catch {
      msgEl.innerText = "Gagal terhubung ke server.";
    }
  });
}

///// ====== REGISTER ======
const regForm = document.getElementById("registerForm");
if (regForm) {
  regForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById("registerMessage");
    msgEl.innerText = "";

    const username = document.getElementById("reg_username").value || "";
    const password = document.getElementById("reg_password").value || "";

    if (!username || !password) {
      msgEl.innerText = "Username dan password wajib diisi.";
      return;
    }

    try {
      const res = await apiPost("/api/auth/register", { username, password });
      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        msgEl.innerText = data.msg || data.error || "Register gagal.";
        return;
      }

      msgEl.innerText = "Register berhasil. Silakan login.";
      setTimeout(() => (window.location.href = "login.html"), 1000);
    } catch {
      msgEl.innerText = "Gagal terhubung ke server.";
    }
  });
}

///// ====== QUIZ ======
let quizState = {
  questions: [],
  quizId: null,
  current: 0,
  answers: {},
};

async function startQuizRequest() {
  const username = localStorage.getItem("username");
  if (!username) {
    alert("Silakan login dulu.");
    return;
  }

  const category = document.getElementById("quizCategory")?.value || "umum";
  const total = parseInt(document.getElementById("quizTotal")?.value) || 10;

  try {
    const res = await apiPost("/api/quiz", { username, category, total });
    const text = await res.text();
    console.log("DEBUG RAW QUIZ OUTPUT:", text);

    let data = {};
    try {
      data = JSON.parse(text);
    } catch {
      console.warn("⚠️ Gagal parse JSON quiz, fallback ke array.");
    }

    const questions =
      data.questions ||
      data.quiz ||
      data.items ||
      (Array.isArray(data) ? data : []);

    if (!res.ok || !Array.isArray(questions) || questions.length === 0) {
      throw new Error(data.error || "Soal tidak tersedia / kosong.");
    }

    startQuiz(questions, data.quiz_id || data.id || null);
  } catch (err) {
    console.error("Quiz error:", err);
    alert("Gagal memulai quiz: " + err.message);
  }
}

function startQuiz(questions, quizId) {
  quizState.questions = questions.map((q, i) => ({ ...q, index: i }));
  quizState.quizId = quizId;
  quizState.current = 0;
  quizState.answers = {};

  document.getElementById("quizSetup")?.classList.add("hidden");
  document.getElementById("quizResult")?.classList.add("hidden");
  document.getElementById("quizGame")?.classList.remove("hidden");

  showQuestion();
}

function showQuestion() {
  const q = quizState.questions[quizState.current];
  if (!q) return console.warn("❌ Tidak ada pertanyaan ditemukan.");

  const qEl = document.getElementById("quizQuestion");
  const optEl = document.getElementById("quizOptions");
  const progressEl = document.getElementById("quizProgress");
  const nextBtn = document.getElementById("btnNext");

  qEl.textContent = qText(q) || "(soal tidak tersedia)";
  optEl.innerHTML = "";

  nextBtn.classList.remove("hidden");
  nextBtn.disabled = true;

  (q.options || []).forEach((opt) => {
    const box = document.createElement("div");
    box.className = "quiz-option";
    box.textContent = opt;
    box.addEventListener("click", () => {
      Array.from(optEl.children).forEach((c) => c.classList.remove("selected"));
      box.classList.add("selected");
      quizState.answers[q.index] = opt;
      nextBtn.disabled = false;
    });
    optEl.appendChild(box);
  });

  progressEl.textContent = `Soal ${quizState.current + 1} dari ${quizState.questions.length}`;
  nextBtn.onclick = nextQuestion;
}

function nextQuestion() {
  try {
    const q = quizState.questions[quizState.current];
    const sel = document.querySelector(".quiz-option.selected");
    if (sel) quizState.answers[q.index] = sel.textContent;

    quizState.current++;

    if (quizState.current < quizState.questions.length) {
      showQuestion();
    } else {
      finishQuiz();
    }
  } catch (err) {
    console.error("❌ Error nextQuestion:", err);
    alert("Terjadi error saat lanjut ke soal berikutnya.");
  }
}

function finishQuiz() {
  document.getElementById("quizGame")?.classList.add("hidden");
  const resultEl = document.getElementById("quizResult");
  resultEl.classList.remove("hidden");

  const total = quizState.questions.length;
  let correct = 0;

  const reviewHtml = quizState.questions.map((q) => {
    const userAns = quizState.answers[q.index];
    const correctAns = normalizeAnswer(q.answer, q.options);
    const isCorrect = norm(userAns) === norm(correctAns);

    if (isCorrect) correct++;

    const optsHtml = (q.options || [])
      .map((opt) => {
        const cls =
          norm(opt) === norm(correctAns)
            ? "correct-opt"
            : norm(opt) === norm(userAns) && !isCorrect
            ? "wrong-opt"
            : "";
        return `<div class="opt ${cls}">${escapeHtml(opt)}</div>`;
      })
      .join("");

    return `
      <div class="review-item">
        <b>${escapeHtml(qText(q))}</b>
        <div>${optsHtml}</div>
        <p>Jawaban kamu: ${escapeHtml(userAns || "(kosong)")}<br>
           Jawaban benar: ${escapeHtml(correctAns)}</p>
      </div>`;
  });

  const scorePercent = total > 0 ? Math.round((correct / total) * 100) : 0;
  resultEl.innerHTML = `<h2>Skor kamu: ${scorePercent}% (${correct}/${total})</h2>${reviewHtml.join("")}`;
}

function normalizeAnswer(ans, options = []) {
  if (!ans) return "";
  const a = String(ans).trim();
  if (/^[A-Da-d]$/.test(a)) {
    const idx = a.toUpperCase().charCodeAt(0) - 65;
    return options[idx] || a;
  }
  const num = parseInt(a);
  if (!isNaN(num) && options[num]) return options[num];
  return a;
}

///// ====== CHAT ======
const chatForm = document.getElementById("chatForm");
if (chatForm) {
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("chatInput");
    const msg = input.value.trim();
    if (!msg) return;

    const username = localStorage.getItem("username") || "anonymous";
    appendChat("user", msg);

    try {
      const res = await apiPost("/api/chat", { username, message: msg });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || "Gagal kirim chat");
      appendChat("bot", data.reply);
    } catch (err) {
      appendChat("bot", "⚠️ Gagal kirim pesan: " + err.message);
    }
    input.value = "";
  });
}

function appendChat(role, text) {
  const box = document.getElementById("chatBox");
  if (!box) return;
  const div = document.createElement("div");
  div.className = `chat-message ${role}`;
  div.innerHTML = `
    <div class="chat-bubble">
      <span class="avatar">${role === "user" ? "👤" : "🤖"}</span>
      <span class="msg-text">${escapeHtml(text)}</span>
    </div>
  `;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

///// ====== LOGOUT ======
const btnLogout = document.getElementById("btnLogout");
if (btnLogout) {
  btnLogout.addEventListener("click", () => {
    localStorage.removeItem("username");
    window.location.href = "login.html";
  });
}


