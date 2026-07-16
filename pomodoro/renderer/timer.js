// ===== DOM 元素 =====
const modeLabel = document.getElementById('mode-label');
const ringFg = document.getElementById('ring-fg');
const timerDisplay = document.getElementById('timer-display');
const dotsContainer = document.getElementById('pomodoro-dots');
const btnStart = document.getElementById('btn-start');
const btnSkip = document.getElementById('btn-skip');
const btnReset = document.getElementById('btn-reset');
const btnMinimize = document.getElementById('btn-minimize');
const btnClose = document.getElementById('btn-close');
const btnPin = document.getElementById('btn-pin');
const modeBtns = document.querySelectorAll('.mode-btn');

// ===== 常量 =====
const CIRCUMFERENCE = 2 * Math.PI * 88; // r=88

const DURATIONS = {
  work: 25 * 60,
  shortBreak: 5 * 60,
  longBreak: 15 * 60,
};

const MODE_LABELS = {
  work: '专注',
  shortBreak: '短休息',
  longBreak: '长休息',
};

// ===== 状态 =====
let state = 'idle'; // 'idle' | 'running' | 'paused'
let mode = 'work'; // 'work' | 'shortBreak' | 'longBreak'
let timeLeft = DURATIONS.work;
let totalTime = DURATIONS.work;
let pomodoroCount = 0;
let timerInterval = null;
let isPinned = false;

// ===== 初始化 =====
ringFg.style.strokeDasharray = CIRCUMFERENCE;
ringFg.style.strokeDashoffset = '0';
updateDisplay();
renderDots();

// ===== 事件监听 =====
btnStart.addEventListener('click', () => {
  if (state === 'idle' || state === 'paused') {
    startTimer();
  } else if (state === 'running') {
    pauseTimer();
  }
});

btnSkip.addEventListener('click', skipCurrent);

btnReset.addEventListener('click', resetTimer);

btnMinimize.addEventListener('click', () => {
  window.electronAPI?.minimizeWindow();
});

btnClose.addEventListener('click', () => {
  window.electronAPI?.closeWindow();
});

btnPin.addEventListener('click', () => {
  isPinned = !isPinned;
  btnPin.classList.toggle('active', isPinned);
  window.electronAPI?.toggleAlwaysOnTop();
});

// 模式切换按钮
modeBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const newMode = btn.dataset.mode;
    if (newMode && newMode !== mode) {
      switchMode(newMode);
    }
  });
});

// ===== 核心函数 =====

function startTimer() {
  state = 'running';
  updateStartButton();

  timerInterval = setInterval(() => {
    timeLeft--;

    if (timeLeft <= 0) {
      timeLeft = 0;
      updateDisplay();
      updateRing();
      clearInterval(timerInterval);
      timerInterval = null;
      onTimerComplete();
      return;
    }

    updateDisplay();
    updateRing();
  }, 1000);
}

function pauseTimer() {
  state = 'paused';
  clearInterval(timerInterval);
  timerInterval = null;
  updateStartButton();
}

function resetTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  state = 'idle';
  timeLeft = totalTime;
  updateDisplay();
  updateRing();
  updateStartButton();
}

function skipCurrent() {
  clearInterval(timerInterval);
  timerInterval = null;
  state = 'idle';

  if (mode === 'work') {
    // 跳过工作：不增加番茄计数，直接进入短休息
    switchMode('shortBreak');
  } else {
    // 跳过休息：回到工作模式
    switchMode('work');
  }
  updateStartButton();
}

function switchMode(newMode) {
  mode = newMode;
  totalTime = DURATIONS[mode];
  timeLeft = totalTime;
  state = 'idle';
  clearInterval(timerInterval);
  timerInterval = null;

  // 更新模式标签
  modeLabel.textContent = MODE_LABELS[mode];
  const isBreak = mode !== 'work';
  modeLabel.classList.toggle('break', isBreak);
  ringFg.classList.toggle('break', isBreak);

  // 更新模式选择按钮
  modeBtns.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === mode);
  });

  // 更新按钮样式
  btnStart.classList.remove('pause');
  btnSkip.classList.toggle('break-mode', isBreak);

  updateDisplay();
  updateRing();
  updateStartButton();
  renderDots();
}

function onTimerComplete() {
  playChime();
  showNotification();
  state = 'idle';

  if (mode === 'work') {
    // 工作完成，番茄 +1
    pomodoroCount++;
    renderDots();

    // 每 4 个番茄进入长休息
    if (pomodoroCount % 4 === 0) {
      switchMode('longBreak');
    } else {
      switchMode('shortBreak');
    }
  } else {
    // 休息完成，回到工作模式
    switchMode('work');
  }
}

// ===== UI 更新 =====

function updateDisplay() {
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  timerDisplay.textContent =
    String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
}

function updateRing() {
  const progress = 1 - timeLeft / totalTime;
  ringFg.style.strokeDashoffset = CIRCUMFERENCE * progress;
}

function updateStartButton() {
  if (state === 'running') {
    btnStart.textContent = '暂停';
    btnStart.classList.add('pause');
  } else {
    btnStart.textContent = '开始';
    btnStart.classList.remove('pause');
  }
}

function renderDots() {
  dotsContainer.innerHTML = '';

  // 显示当前轮次的番茄（每轮最多8个，超过后重置计数视觉）
  const displayCount = pomodoroCount % 8;
  const roundNum = Math.floor(pomodoroCount / 8);

  for (let i = 0; i < 8; i++) {
    const dot = document.createElement('div');
    dot.className = 'dot';
    if (i < displayCount) {
      dot.classList.add('filled');
    }
    dotsContainer.appendChild(dot);
  }

  // 如果超过一轮，显示轮次标记
  if (roundNum > 0) {
    const roundBadge = document.createElement('span');
    roundBadge.className = 'round-badge';
    roundBadge.textContent = `×${roundNum + 1}`;
    dotsContainer.appendChild(roundBadge);
  }
}

// ===== 音效 =====

function playChime() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();

    // 播放两音符提示音
    [523.25, 659.25].forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.3, ctx.currentTime + i * 0.18);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.18 + 0.4);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(ctx.currentTime + i * 0.18);
      osc.stop(ctx.currentTime + i * 0.18 + 0.4);
    });
  } catch (e) {
    // 忽略音频错误
  }
}

// ===== 系统通知 =====

function showNotification() {
  const title = mode === 'work'
    ? '🍅 专注完成！'
    : '☕ 休息完成！';
  const body = mode === 'work'
    ? '做得不错，休息一下吧。'
    : '休息结束，继续加油！';

  // 优先使用 Electron Notification（通过主进程）
  if (window.electronAPI?.showNotification) {
    window.electronAPI.showNotification(title, body);
  } else if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body });
  } else if ('Notification' in window && Notification.permission !== 'denied') {
    Notification.requestPermission().then(perm => {
      if (perm === 'granted') {
        new Notification(title, { body });
      }
    });
  }
}
