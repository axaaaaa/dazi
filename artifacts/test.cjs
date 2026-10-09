const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
const source = fs.readFileSync(process.argv[2], 'utf8');
const script = source.match(/<script>([\s\S]*?)<\/script>/)[1];
function element() {
  return { style: { setProperty() {} }, classList: { add() {}, remove() {} },
    children: [], appendChild(x) { this.children.push(x); }, replaceChildren() { this.children = []; },
    getBoundingClientRect() { return { left: 0, top: 0, width: 180, height: 180 }; }, remove() {} };
}
const nodes = {};
const handlers = {};
let pending = [];
const synth = { cancel() {}, speak() {}, getVoices() { return []; } };
const ctx = vm.createContext({
  document: { getElementById(id) { return nodes[id] ||= element(); }, createElement: element,
    body: element(), addEventListener(name, fn) { handlers[name] = fn; } },
  window: { innerWidth: 800, innerHeight: 600, speechSynthesis: synth },
  speechSynthesis: synth, SpeechSynthesisUtterance: function(t) { this.text = t; },
  setTimeout(fn) { pending.push(fn); return pending.length; }, clearTimeout() {},
  setInterval() { return 1; }, clearInterval() {}, requestAnimationFrame() { return 1; }, cancelAnimationFrame() {}
});
vm.runInContext(script, ctx);
const run = code => vm.runInContext(code, ctx);
run("state.active = true; state.char = 'A'; check('A'); check('A')");
const score = run('state.score');
const hasPinyin = run('Array.isArray(config.pinyin)');
if (!hasPinyin) {
  assert.equal(score, 2);
  console.log('BASELINE: pinyin=false; repeated-answer score=2; PASS');
} else {
  assert.equal(score, 1);
  for (const mode of ['static', 'mole', 'fall']) {
    run(`state.diff = 'pinyin'; startGame('${mode}'); state.item = config.pinyin[4]; state.char = state.item.keys; state.typed = ''; renderPinyin(); check('X'); check('Z');`);
    assert.equal(run('state.typed'), 'X');
    assert.equal(run('state.score'), 0);
    run("check('Backspace')");
    assert.equal(run('state.typed'), '');
    run("check('X'); check('I'); check('A'); check('O'); check('O')");
    assert.equal(run('state.score'), 1);
    assert.equal(run('state.typed'), 'XIAO');
  }
  run("state.item = config.pinyin[20]; state.char = 'LV'; state.typed = ''; state.answered = false; check('L'); check('V')");
  assert.equal(run('state.score'), 2);
  run("state.answered = false; state.typed = ''");
  handlers.keydown({ key: 'l', repeat: true });
  assert.equal(run('state.typed'), '');
  handlers.keydown({ key: 'l', isComposing: true });
  assert.equal(run('state.typed'), '');
  for (const diff of ['letters', 'numbers', 'mixed']) {
    run(`state.diff = '${diff}'; startGame('static'); check(state.char); check(state.char)`);
    assert.equal(run('state.score'), 1);
  }
  console.log('MODIFIED: pinyin=21; modes=3 PASS; sequential/wrong/backspace/umlaut/repeat/IME PASS; legacy=3 PASS; repeated-answer score=1; PASS');
}
