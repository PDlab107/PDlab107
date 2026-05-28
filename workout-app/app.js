const workouts = {
  Monday: {
    focus: "Push + chest/triceps (hypertrophy)",
    structure: "5 blocks x 4 mins = 20 mins. Work 40s, rest 20s.",
    exercises: [
      { name: "Push-Up", plan: "4 rounds x 8-15 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif", video: "https://www.youtube.com/watch?v=IODxDxX7oi4" },
      { name: "Dumbbell Floor Press", plan: "4 rounds x 10-12 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Floor-Press.gif", video: "https://www.youtube.com/watch?v=uUGDRwge4F8" },
      { name: "Pike Push-Up", plan: "3 rounds x 8-12 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pike-Push-Up.gif", video: "https://www.youtube.com/watch?v=qHQ_E-f5278" },
      { name: "Chair Dips", plan: "3 rounds x 10-15 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/06/Bench-Dips.gif", video: "https://www.youtube.com/watch?v=6kALZikXxLc" }
    ]
  },
  Tuesday: {
    focus: "Legs + glutes (strength + tone)",
    structure: "5 blocks x 4 mins = 20 mins. Work 45s, rest 15s.",
    exercises: [
      { name: "Goblet Squat", plan: "4 rounds x 10-15 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Goblet-Squat.gif", video: "https://www.youtube.com/watch?v=6xwGFn-J_Qk" },
      { name: "Romanian Deadlift", plan: "4 rounds x 10-12 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Romanian-Deadlift.gif", video: "https://www.youtube.com/watch?v=0zZ4x5h8N7Q" },
      { name: "Reverse Lunge", plan: "3 rounds x 8-12 reps/leg", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Reverse-Lunge.gif", video: "https://www.youtube.com/watch?v=wrwwXE_x-pQ" },
      { name: "Calf Raises", plan: "3 rounds x 15-20 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/05/Dumbbell-Calf-Raise.gif", video: "https://www.youtube.com/watch?v=-M4-G8p8fmc" }
    ]
  },
  Wednesday: {
    focus: "Back + biceps + core",
    structure: "5 blocks x 4 mins = 20 mins. Work 40s, rest 20s.",
    exercises: [
      { name: "One-Arm Row", plan: "4 rounds x 10-12 reps/arm", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/One-Arm-Dumbbell-Row.gif", video: "https://www.youtube.com/watch?v=pYcpY20QaE8" },
      { name: "Band or Towel Row", plan: "4 rounds x 12-15 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/06/Inverted-Row.gif", video: "https://www.youtube.com/watch?v=rloXYB8M3vU" },
      { name: "Hammer Curl", plan: "3 rounds x 10-12 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hammer-Curl.gif", video: "https://www.youtube.com/watch?v=zC3nLlEvin4" },
      { name: "Dead Bug", plan: "3 rounds x 30-40 sec", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dead-Bug.gif", video: "https://www.youtube.com/watch?v=4XLEnwUr8Hw" }
    ]
  },
  Thursday: {
    focus: "Upper-body density (fast pace)",
    structure: "Circuit style for 20 mins. Minimal rest.",
    exercises: [
      { name: "Incline Push-Up", plan: "12 reps per round", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Push-Up.gif", video: "https://www.youtube.com/watch?v=cfns5VDVVvk" },
      { name: "Arnold Press", plan: "10 reps per round", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Arnold-Press.gif", video: "https://www.youtube.com/watch?v=vj2w851ZHRM" },
      { name: "Lateral Raise", plan: "12 reps per round", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif", video: "https://www.youtube.com/watch?v=3VcKaXpzqRo" },
      { name: "Plank Shoulder Tap", plan: "20 taps total", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Shoulder-Tap-Push-up.gif", video: "https://www.youtube.com/watch?v=Hdz2S2B-g4Y" }
    ]
  },
  Friday: {
    focus: "Full body finisher day",
    structure: "EMOM style for 20 mins: 5 movements x 4 rounds.",
    exercises: [
      { name: "Thruster", plan: "8-12 reps", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Thruster.gif", video: "https://www.youtube.com/watch?v=L219ltL15zk" },
      { name: "Step-Up", plan: "10 reps/leg", image: "https://fitnessprogramer.com/wp-content/uploads/2021/05/Dumbbell-Step-up.gif", video: "https://www.youtube.com/watch?v=aajhW7DD1EA" },
      { name: "Renegade Row", plan: "8-10 reps/side", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Renegade-Row.gif", video: "https://www.youtube.com/watch?v=roCP6wCXPqo" },
      { name: "Hollow Hold", plan: "25-40 sec", image: "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hollow-Hold.gif", video: "https://www.youtube.com/watch?v=4xRpGgttca8" }
    ]
  }
};

const state = {
  activeDay: "Monday",
  timerTotal: 20 * 60,
  timerLeft: 20 * 60,
  timerId: null
};

const dom = {
  dayTabs: document.getElementById("dayTabs"),
  daySummary: document.getElementById("daySummary"),
  exerciseList: document.getElementById("exerciseList"),
  exerciseInputs: document.getElementById("exerciseInputs"),
  timerText: document.getElementById("timerText"),
  startTimer: document.getElementById("startTimer"),
  pauseTimer: document.getElementById("pauseTimer"),
  resetTimer: document.getElementById("resetTimer"),
  logForm: document.getElementById("logForm"),
  dateInput: document.getElementById("dateInput"),
  bodyWeightInput: document.getElementById("bodyWeightInput"),
  energyInput: document.getElementById("energyInput"),
  notesInput: document.getElementById("notesInput"),
  historyList: document.getElementById("historyList"),
  weeklyCount: document.getElementById("weeklyCount"),
  lastSession: document.getElementById("lastSession")
};

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function getLogs() {
  return JSON.parse(localStorage.getItem("workoutLogs") || "[]");
}

function saveLogs(logs) {
  localStorage.setItem("workoutLogs", JSON.stringify(logs));
}

function renderTabs() {
  const days = Object.keys(workouts);
  dom.dayTabs.innerHTML = days
    .map((day) => `<button class="tab ${day === state.activeDay ? "active" : ""}" data-day="${day}">${day}</button>`)
    .join("");
}

function renderDay() {
  const data = workouts[state.activeDay];
  dom.daySummary.innerHTML = `<strong>${data.focus}</strong><br>${data.structure}`;
  dom.exerciseList.innerHTML = data.exercises
    .map((exercise, i) => `
      <article class="exercise-card">
        <div class="exercise-top">
          <h3 class="exercise-name">${i + 1}. ${exercise.name}</h3>
        </div>
        <p class="exercise-plan">${exercise.plan}</p>
        <div class="media-row">
          <img src="${exercise.image}" alt="${exercise.name} demonstration">
          <a href="${exercise.video}" target="_blank" rel="noopener noreferrer">Watch quick form video</a>
        </div>
      </article>
    `).join("");

  dom.exerciseInputs.innerHTML = data.exercises
    .map((exercise, i) => `
      <div class="exercise-input-row">
        <strong>${i + 1}. ${exercise.name}</strong>
        <div class="row-2">
          <label>Reps/time achieved
            <input type="text" name="result_${i}" placeholder="e.g. 12, 11, 10">
          </label>
          <label>Weight used (kg)
            <input type="number" name="load_${i}" min="0" step="0.5" placeholder="e.g. 14">
          </label>
        </div>
      </div>
    `).join("");
}

function renderTimer() {
  const mins = String(Math.floor(state.timerLeft / 60)).padStart(2, "0");
  const secs = String(state.timerLeft % 60).padStart(2, "0");
  dom.timerText.textContent = `${mins}:${secs}`;
}

function startTimer() {
  if (state.timerId) return;
  state.timerId = setInterval(() => {
    state.timerLeft -= 1;
    if (state.timerLeft <= 0) {
      state.timerLeft = 0;
      pauseTimer();
      alert("Great work. 20 minutes done.");
    }
    renderTimer();
  }, 1000);
}

function pauseTimer() {
  if (!state.timerId) return;
  clearInterval(state.timerId);
  state.timerId = null;
}

function resetTimer() {
  pauseTimer();
  state.timerLeft = state.timerTotal;
  renderTimer();
}

function weekKey(dateString) {
  const date = new Date(dateString);
  const jan1 = new Date(date.getFullYear(), 0, 1);
  const days = Math.floor((date - jan1) / 86400000);
  const week = Math.ceil((days + jan1.getDay() + 1) / 7);
  return `${date.getFullYear()}-W${week}`;
}

function renderSummary() {
  const logs = getLogs();
  const currentWeek = weekKey(todayISO());
  const weekCount = logs.filter((log) => weekKey(log.date) === currentWeek).length;
  dom.weeklyCount.textContent = `${weekCount}/5 complete this week`;

  if (!logs.length) {
    dom.lastSession.textContent = "No session logged yet";
    return;
  }
  const latest = [...logs].sort((a, b) => b.date.localeCompare(a.date))[0];
  dom.lastSession.textContent = `Last: ${latest.day} (${latest.date})`;
}

function renderHistory() {
  const logs = getLogs().sort((a, b) => b.date.localeCompare(a.date)).slice(0, 12);
  if (!logs.length) {
    dom.historyList.innerHTML = `<p class="muted">No saved sessions yet. Do your first workout and tap "Save session".</p>`;
    return;
  }

  dom.historyList.innerHTML = logs.map((log) => `
    <article class="history-item">
      <strong>${log.date} — ${log.day}</strong>
      <div class="muted">Body weight: ${log.bodyWeight || "-"} kg | Energy: ${log.energy}/5</div>
      <div class="muted">${log.notes || "No notes."}</div>
    </article>
  `).join("");
}

function saveSession(event) {
  event.preventDefault();
  const formData = new FormData(dom.logForm);
  const exercises = workouts[state.activeDay].exercises.map((exercise, i) => ({
    name: exercise.name,
    result: String(formData.get(`result_${i}`) || "").trim(),
    loadKg: Number(formData.get(`load_${i}`) || 0)
  }));

  const logs = getLogs();
  logs.push({
    day: state.activeDay,
    date: dom.dateInput.value,
    bodyWeight: dom.bodyWeightInput.value ? Number(dom.bodyWeightInput.value) : null,
    energy: Number(dom.energyInput.value || 3),
    notes: dom.notesInput.value.trim(),
    timerSecondsLeft: state.timerLeft,
    exercises
  });
  saveLogs(logs);

  renderSummary();
  renderHistory();
  alert("Session saved.");
}

function bindEvents() {
  dom.dayTabs.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-day]");
    if (!button) return;
    state.activeDay = button.dataset.day;
    renderTabs();
    renderDay();
  });

  dom.startTimer.addEventListener("click", startTimer);
  dom.pauseTimer.addEventListener("click", pauseTimer);
  dom.resetTimer.addEventListener("click", resetTimer);
  dom.logForm.addEventListener("submit", saveSession);
}

function init() {
  dom.dateInput.value = todayISO();
  renderTabs();
  renderDay();
  renderTimer();
  renderSummary();
  renderHistory();
  bindEvents();
}

init();
