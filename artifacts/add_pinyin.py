from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = s.replace('/* 隐藏类 */', '''/* 拼音题卡：声调用于展示，输入使用普通字母 */
        .char-card.pinyin-card { flex-direction: column; gap: 8px; font-size: 3.8rem; }
        .pinyin-word { font-size: 2.6rem; line-height: 1.1; }
        .pinyin-label { font-size: 1.7rem; line-height: 1.2; letter-spacing: 2px; }
        .pinyin-input { font-size: 1rem; color: #596275; letter-spacing: 3px; }
        .mode-dynamic .pinyin-card { width: 160px; height: 160px; border-radius: 30px; }
        .mode-dynamic .pinyin-word { font-size: 2rem; }
        .mode-dynamic .pinyin-label { font-size: 1.4rem; }
        @media (max-width: 480px) {
            .modal-card { padding: 20px; box-sizing: border-box; }
            .toggle-btn { font-size: 12px; }
        }
        /* 隐藏类 */''')
s = s.replace('<button class="toggle-btn" onclick="setDiff(\'mixed\')">混合</button>', '<button class="toggle-btn" onclick="setDiff(\'mixed\')">混合</button>\n                    <button class="toggle-btn" onclick="setDiff(\'pinyin\')">拼音</button>')
s = s.replace('colors: [', '''pinyin: [
                { word: '妈', label: 'mā', keys: 'MA' },
                { word: '爸', label: 'bà', keys: 'BA' },
                { word: '米', label: 'mǐ', keys: 'MI' },
                { word: '大', label: 'dà', keys: 'DA' },
                { word: '小', label: 'xiǎo', keys: 'XIAO' },
                { word: '山', label: 'shān', keys: 'SHAN' },
                { word: '水', label: 'shuǐ', keys: 'SHUI' },
                { word: '火', label: 'huǒ', keys: 'HUO' },
                { word: '木', label: 'mù', keys: 'MU' },
                { word: '日', label: 'rì', keys: 'RI' },
                { word: '月', label: 'yuè', keys: 'YUE' },
                { word: '人', label: 'rén', keys: 'REN' },
                { word: '口', label: 'kǒu', keys: 'KOU' },
                { word: '手', label: 'shǒu', keys: 'SHOU' },
                { word: '牛', label: 'niú', keys: 'NIU' },
                { word: '马', label: 'mǎ', keys: 'MA' },
                { word: '猫', label: 'māo', keys: 'MAO' },
                { word: '狗', label: 'gǒu', keys: 'GOU' },
                { word: '鸟', label: 'niǎo', keys: 'NIAO' },
                { word: '鱼', label: 'yú', keys: 'YU' },
                { word: '绿', label: 'lǜ', keys: 'LV' }
            ],
            colors: [''')
s = s.replace("fallY: 0", "fallY: 0,\n            typed: '',\n            item: null,\n            answered: false")
s = s.replace('fall: null };', 'fall: null, next: null };')
s = s.replace('// 重置卡片样式', "clearTimeout(timers.next);\n            timers.next = null;\n            // 重置卡片样式")
s = s.replace('state.char = pool.charAt(Math.floor(Math.random() * pool.length));\n            els.card.textContent = state.char;', '''state.typed = '';
            state.answered = false;
            if (state.diff === 'pinyin') {
                state.item = pool[Math.floor(Math.random() * pool.length)];
                state.char = state.item.keys;
                els.card.classList.add('pinyin-card');
                renderPinyin();
            } else {
                state.item = null;
                state.char = pool.charAt(Math.floor(Math.random() * pool.length));
                els.card.textContent = state.char;
            }''')
s = s.replace("els.card.style.left = (Math.random() * (window.innerWidth - 120)) + 60 + 'px';", "els.card.style.left = Math.random() * Math.max(0, window.innerWidth - cardSize()) + 'px';")
s = s.replace('speak(state.char);', "speak(state.item ? state.item.word : state.char);")
s = s.replace('const x = Math.random() * (window.innerWidth - 200) + 100;\n            const y = Math.random() * (window.innerHeight - 250) + 100;', '''const size = cardSize();
            const x = Math.random() * Math.max(0, window.innerWidth - size);
            const top = Math.min(90, Math.max(0, window.innerHeight - size));
            const y = top + Math.random() * Math.max(0, window.innerHeight - size - top - 50);''')
s = s.replace('        function check(key) {\n            if(key === state.char) {', '''        function cardSize() { return state.diff === 'pinyin' ? 160 : 120; }

        function renderPinyin() {
            els.card.replaceChildren();
            const values = [state.item.word, state.item.label,
                state.typed.toLowerCase() + '＿'.repeat(state.char.length - state.typed.length)];
            ['pinyin-word', 'pinyin-label', 'pinyin-input'].forEach((className, i) => {
                const span = document.createElement('span');
                span.className = className;
                span.textContent = values[i];
                els.card.appendChild(span);
            });
        }

        function check(key) {
            if (!state.active || state.answered) return;
            if (state.diff === 'pinyin') {
                if (key === 'Backspace') {
                    state.typed = state.typed.slice(0, -1);
                    renderPinyin();
                    return;
                }
                if (!/^[A-Z]$/.test(key)) return;
                if (key !== state.char[state.typed.length]) {
                    playTone(200, 0.2, 'sawtooth');
                    return;
                }
                state.typed += key;
                renderPinyin();
                if (state.typed !== state.char) return;
            }
            if(state.diff === 'pinyin' || key === state.char) {
                state.answered = true;
                if(timers.mole) clearInterval(timers.mole);
                if(timers.fall) cancelAnimationFrame(timers.fall);''')
s = s.replace('else setTimeout(spawn, 300);', 'else timers.next = setTimeout(spawn, 300);')
s = s.replace("            els.menu.classList.add('hidden');\n            spawn();", '''            if (state.diff === 'pinyin') els.hint.textContent = '依次输入拼音字母，退格可修改；ü 用 v，声调不用输入（请切换英文键盘）';
            els.container.classList.remove('mode-dynamic');
            els.menu.classList.add('hidden');
            spawn();''')
s = s.replace("            if(!state.active) return;\n            if(e.key.length === 1) check(e.key.toUpperCase());", '''            if(!state.active || e.repeat || e.isComposing || e.ctrlKey || e.altKey || e.metaKey) return;
            if (state.diff === 'pinyin' && e.key === 'Backspace') {
                e.preventDefault();
                check('Backspace');
            } else if (/^[a-z0-9]$/i.test(e.key)) {
                e.preventDefault();
                check(e.key.toUpperCase());
            }''')
p.write_text(s, encoding='utf-8')
