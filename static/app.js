const display = document.querySelector('#display');
const expression = document.querySelector('#expression');
const error = document.querySelector('#error');
const buttons = [...document.querySelectorAll('.keypad button')];
const symbols = { '+': '+', '-': '−', '*': '×', '/': '÷' };
let current = '0';
let first = null;
let operator = null;
let replace = false;
let busy = false;

function calculate(first, operator, second) {
  if (!Number.isFinite(first) || !Number.isFinite(second)) {
    throw new Error('Please enter finite numbers.');
  }
  let result;
  switch (operator) {
    case '+': result = first + second; break;
    case '-': result = first - second; break;
    case '*': result = first * second; break;
    case '/':
      if (second === 0) throw new Error('Cannot divide by zero.');
      result = first / second;
      break;
    default: throw new Error('Choose +, −, ×, or ÷.');
  }
  if (!Number.isFinite(result)) throw new Error('The result is too large.');
  return result;
}

function render() {
  display.textContent = current;
  buttons.forEach(button => {
    button.disabled = busy;
    button.classList.toggle('selected', Boolean(operator) && button.dataset.operator === operator);
  });
}

async function evaluate() {
  if (first === null || !operator || replace) return true;
  busy = true;
  render();
  const label = `${first} ${symbols[operator]} ${current}`;
  try {
    current = String(calculate(first, operator, Number(current)));
    expression.textContent = `${label} =`;
    first = null;
    operator = null;
    replace = true;
    return true;
  } catch (failure) {
    error.textContent = failure.message;
    return false;
  } finally {
    busy = false;
    render();
  }
}

async function handle(value) {
  if (busy) return;
  error.textContent = '';
  if (/^[0-9.]$/.test(value)) {
    if (replace) {
      current = '0';
      replace = false;
      if (!operator) expression.textContent = 'New calculation';
    }
    if (value === '.') {
      if (!current.includes('.')) current += '.';
    } else if (current.replace(/[-.]/g, '').length < 15) {
      current = current === '0' ? value : current === '-0' ? `-${value}` : current + value;
    }
  } else if (value === 'clear') {
    current = '0'; first = null; operator = null; replace = false;
    expression.textContent = 'Ready for liftoff';
  } else if (value === 'delete') {
    if (replace) return;
    current = current.slice(0, -1);
    if (!current || current === '-') current = '0';
  } else if (value === 'sign') {
    if (replace && operator) current = '0';
    current = current.startsWith('-') ? current.slice(1) : `-${current}`;
    replace = false;
  } else if (Object.hasOwn(symbols, value)) {
    if (!(await evaluate())) return;
    first = Number(current);
    operator = value;
    replace = true;
    expression.textContent = `${current} ${symbols[operator]}`;
  } else if (value === 'equals') {
    await evaluate();
  }
  render();
}

buttons.forEach(button => button.addEventListener('click', () => handle(button.dataset.digit ?? button.dataset.operator ?? button.dataset.action)));
document.addEventListener('keydown', event => {
  if (event.target.closest('#music-toggle')) return;
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  const aliases = { Enter: 'equals', '=': 'equals', Escape: 'clear', Backspace: 'delete', Delete: 'clear' };
  const value = aliases[event.key] ?? event.key;
  if (/^[0-9.+*/-]$/.test(value) || Object.values(aliases).includes(value)) {
    event.preventDefault();
    handle(value);
  }
});
render();

const music = document.querySelector('#background-music');
const musicToggle = document.querySelector('#music-toggle');
const musicStatus = document.querySelector('#music-status');
music.volume = 0.35;

function updateMusic() {
  musicToggle.textContent = music.paused ? 'Play music' : 'Pause music';
  musicToggle.setAttribute('aria-label', music.paused ? 'Play background music' : 'Pause background music');
  musicStatus.textContent = music.paused ? 'Music paused' : 'Now playing · on repeat';
}

async function playMusic() {
  try {
    await music.play();
  } catch (failure) {
    musicStatus.textContent = failure.name === 'NotAllowedError'
      ? 'Press Play music to start'
      : 'Music unavailable. Try refreshing the page.';
  }
}

music.addEventListener('play', updateMusic);
music.addEventListener('pause', updateMusic);
music.addEventListener('error', () => {
  musicStatus.textContent = 'Music unavailable. Try refreshing the page.';
});
musicToggle.addEventListener('click', () => {
  if (music.paused) playMusic();
  else music.pause();
});
playMusic();
