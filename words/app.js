/* Wortreise — тренажёр слов курса «10 Stufen». Статическая страница: данные в data/, прогресс в localStorage. */
"use strict";
const CFG = {
  endpoint: "https://script.google.com/macros/s/AKfycbyZrV1bz35yxbLZMEaNNCXC7BvaMmYV6dFYiTEX8qKbhrqB3rgSpaUmAg2FnjohKwxO/exec",
  token: "61319aa1a62c", lang: "de-DE", v: 1
};
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const app = () => $("#app");
const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const strip = s => String(s || "").replace(/<[^>]+>/g, "");
const today = () => Math.floor((Date.now() - new Date().getTimezoneOffset() * 6e4) / 864e5);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a };
const pad = n => String(n).padStart(3, "0");
const normW = w => String(w).trim().toLowerCase().replace("(pl.)", "").trim().replace(/^(der|die|das|sich)\s+/, "");
const cmp = s => String(s).toLowerCase().replace(/ß/g, "ss").replace(/[.,!?;:„“"«»()]/g, "").replace(/\s+/g, " ").trim();

/* ---------- Тексты интерфейса ---------- */
const UI = {
  uk: {
    hello: "Привіт! Це Wortreise — подорож словами курсу «10 Stufen».", who: "Як тебе звати?", lang: "Мова підказок", create: "Почати",
    profiles: "Хто вчиться?", newp: "Новий учень", choose: "Обери свого героя", chooseSub: "Ти проходиш теми курсу як цей герой: його друзі, його місто, його історія.",
    start: "З чого почати?", fromStart: "З теми 1", fromN: "З теми №", go: "Далі", map: "Карта", review: "Повторити", diary: "Щоденник", me: "Профіль",
    soon: "скоро", lock: "закрито", topic: "Тема", stufe: "Ступінь", startEp: "Почати епізод", cont: "Далі", check: "Перевірити", next: "Далі",
    steps: ["Вхід", "Знайомство", "Тренування", "Повторення", "Опиши сцену", "Підсумок"], diff: "Складність лексики в цій темі",
    keep: "далі так само", newWords: "нових слів", revWords: "на повторення", chest: "Скриня", chestTxt: n => `Ще ${n} слів теми — за них додатковий досвід.`,
    openChest: "Відкрити скриню", right: "Правильно!", wrong: "Не зовсім.", correct: "Правильна відповідь:", you: "Ти", tap: "показати переклад",
    type: "Напиши слово", know: "Я вже знаю це слово", found: "Знайдено", extra: "зайвих натискань", sceneCloud: "Знайди слова цієї теми (натискай)",
    sceneBuild: "Збери речення про сцену", sceneChoose: "Яке речення з цієї теми?", done: "Епізод пройдено!", score: "з першої спроби", xp: "досвіду",
    send: "Надіслати викладачу", sending: "Надсилаю…", sent: "Надіслано ✓", sendFail: "Не вдалося надіслати. Скопіюй звіт і надішли в месенджері.",
    toMap: "На карту", nextTopic: "Наступна тема", returned: n => `повернулося з теми ${n}`, due: n => `Чекають повторення: ${n}`,
    blocked: "Багато слів чекають повторення — спочатку повторимо, потім нова тема.", noDue: "Зараз нічого повторювати. Чудово!",
    reviewDone: "Повторення завершено", diaryEmpty: "Тут з’являться записи після кожного епізоду.", backup: "Резервна копія",
    exp: "Зберегти файл прогресу", imp: "Відновити з файлу", hw: "Імпорт з домашнього тесту", hwTxt: "Встав блок профілю з листа (рядки «Слова розминки з помилкою», «Слова на повторення»).",
    hwBtn: "Додати слова на повторення", hwOk: n => `Додано на повторення: ${n}`, remind: "Давно не зберігав копію прогресу. Збережи файл — так прогрес не загубиться.",
    friends: "Друзі", badges: "Нагороди", words: "Слова", learned: "вивчено", inSrs: "у повторенні", streak: "днів поспіль", topics: "тем пройдено",
    suggestEasy: "Два епізоди поспіль були важкими. Зробити легше?", suggestHard: "Два епізоди поспіль майже без помилок. Спробувати складніше?", yes: "Так", no: "Ні",
    fest: n => `Свято в кварталі: велике повторення тем ${n - 24}–${n}`, exam: s => `Іспит ступеня ${s}`, examPass: "Іспит складено!", examFail: "Ще трохи — потрібно 80 %. Спробуй ще раз.",
    switchHero: "Змінити героя", switchUser: "Змінити учня", del: "Видалити профіль", delQ: "Видалити прогрес цього учня на цьому пристрої?",
    article: "Який артикль?", listen: "Послухай слово", def: "Тлумачення", odd: "Яке слово не з цієї теми?", newType: "Новий тип завдання",
    intro: "Знайомство зі словами", skipShow: "До тренування", empty: "Для цієї теми тексти ще пишуться.", hero: "Герой", place: "Місце",
    back: "Назад", lvl: "рівень слова", choosePlace: "Тема, з якої почати (як на уроці):", diffShort: { easy: "↓", hard: "↑", harder: "↑↑" },
    report: "Звіт", copy: "Скопіювати", copied: "Скопійовано", hwLink: "Слова з домашнього тесту додано на повторення.", ofTopic: "тема",
    nameNeed: "Напиши ім’я.", exists: "Такий учень уже є на цьому пристрої — відкриваю його профіль.",
    go: "Продовжити", goReview: "Повторити слова", goSoon: "Нові теми скоро", home: "Головна", more: "Ще",
    regT: "Реєстрація", regSub: "Вкажіть ім’я та e-mail. Викладач схвалить доступ — і на пошту прийде лист.",
    email: "E-mail", regBtn: "Надіслати заявку", haveAcc: "Вже зареєстровані? Увійти", loginT: "Вхід",
    loginSub: "Ім’я та e-mail — такі самі, як у заявці.", loginBtn: "Увійти", waitT: "Заявку надіслано ✓",
    waitTxt: "Коли викладач схвалить доступ, на пошту прийде лист. Тоді натисніть кнопку нижче.", check2: "Перевірити",
    notYet: "Ще не схвалено. Спробуйте трохи пізніше.", rejected: "Доступ не схвалено. Напишіть викладачеві.",
    net: "Немає зв’язку з сервером. Спробуйте ще раз.", oldServer: "Реєстрація ще не ввімкнена на сервері. Напишіть викладачеві.",
    notFound: "Заявку з таким іменем і e-mail не знайдено.", emailBad: "Перевірте e-mail.", change: "Змінити дані",
    sendingReg: "Надсилаю…", lvlWords: "слів вивчено", ofAll: "з 750"
  },
  ru: {
    hello: "Привет! Это Wortreise — путешествие по словам курса «10 Stufen».", who: "Как тебя зовут?", lang: "Язык подсказок", create: "Начать",
    profiles: "Кто учится?", newp: "Новый ученик", choose: "Выбери своего героя", chooseSub: "Ты проходишь темы курса как этот герой: его друзья, его город, его история.",
    start: "С чего начать?", fromStart: "С темы 1", fromN: "С темы №", go: "Дальше", map: "Карта", review: "Повторить", diary: "Дневник", me: "Профиль",
    soon: "скоро", lock: "закрыто", topic: "Тема", stufe: "Ступень", startEp: "Начать эпизод", cont: "Дальше", check: "Проверить", next: "Дальше",
    steps: ["Вход", "Знакомство", "Тренировка", "Повторение", "Опиши сцену", "Итог"], diff: "Сложность лексики в этой теме",
    keep: "дальше так же", newWords: "новых слов", revWords: "на повторение", chest: "Сундук", chestTxt: n => `Ещё ${n} слов темы — за них дополнительный опыт.`,
    openChest: "Открыть сундук", right: "Правильно!", wrong: "Не совсем.", correct: "Правильный ответ:", you: "Ты", tap: "показать перевод",
    type: "Напиши слово", know: "Я уже знаю это слово", found: "Найдено", extra: "лишних нажатий", sceneCloud: "Найди слова этой темы (нажимай)",
    sceneBuild: "Собери предложение о сцене", sceneChoose: "Какое предложение из этой темы?", done: "Эпизод пройден!", score: "с первой попытки", xp: "опыта",
    send: "Отправить преподавателю", sending: "Отправляю…", sent: "Отправлено ✓", sendFail: "Не удалось отправить. Скопируй отчёт и отправь в мессенджере.",
    toMap: "На карту", nextTopic: "Следующая тема", returned: n => `вернулось из темы ${n}`, due: n => `Ждут повторения: ${n}`,
    blocked: "Много слов ждут повторения — сначала повторим, потом новая тема.", noDue: "Сейчас нечего повторять. Отлично!",
    reviewDone: "Повторение завершено", diaryEmpty: "Здесь появятся записи после каждого эпизода.", backup: "Резервная копия",
    exp: "Сохранить файл прогресса", imp: "Восстановить из файла", hw: "Импорт из домашнего теста", hwTxt: "Вставь блок профиля из письма (строки «Слова разминки с ошибкой», «Слова на повторение»).",
    hwBtn: "Добавить слова на повторение", hwOk: n => `Добавлено на повторение: ${n}`, remind: "Давно не сохранял копию прогресса. Сохрани файл — так прогресс не потеряется.",
    friends: "Друзья", badges: "Награды", words: "Слова", learned: "выучено", inSrs: "в повторении", streak: "дней подряд", topics: "тем пройдено",
    suggestEasy: "Два эпизода подряд были трудными. Сделать легче?", suggestHard: "Два эпизода подряд почти без ошибок. Попробовать сложнее?", yes: "Да", no: "Нет",
    fest: n => `Праздник в квартале: большое повторение тем ${n - 24}–${n}`, exam: s => `Экзамен ступени ${s}`, examPass: "Экзамен сдан!", examFail: "Ещё немного — нужно 80 %. Попробуй ещё раз.",
    switchHero: "Сменить героя", switchUser: "Сменить ученика", del: "Удалить профиль", delQ: "Удалить прогресс этого ученика на этом устройстве?",
    article: "Какой артикль?", listen: "Послушай слово", def: "Толкование", odd: "Какое слово не из этой темы?", newType: "Новый тип задания",
    intro: "Знакомство со словами", skipShow: "К тренировке", empty: "Для этой темы тексты ещё пишутся.", hero: "Герой", place: "Место",
    back: "Назад", lvl: "уровень слова", choosePlace: "Тема, с которой начать (как на уроке):", diffShort: { easy: "↓", hard: "↑", harder: "↑↑" },
    report: "Отчёт", copy: "Скопировать", copied: "Скопировано", hwLink: "Слова из домашнего теста добавлены на повторение.", ofTopic: "тема",
    nameNeed: "Напиши имя.", exists: "Такой ученик уже есть на этом устройстве — открываю его профиль.",
    go: "Продолжить", goReview: "Повторить слова", goSoon: "Новые темы скоро", home: "Главная", more: "Ещё",
    regT: "Регистрация", regSub: "Укажите имя и e-mail. Преподаватель одобрит доступ — и на почту придёт письмо.",
    email: "E-mail", regBtn: "Отправить заявку", haveAcc: "Уже зарегистрированы? Войти", loginT: "Вход",
    loginSub: "Имя и e-mail — такие же, как в заявке.", loginBtn: "Войти", waitT: "Заявка отправлена ✓",
    waitTxt: "Когда преподаватель одобрит доступ, на почту придёт письмо. Тогда нажмите кнопку ниже.", check2: "Проверить",
    notYet: "Ещё не одобрено. Попробуйте чуть позже.", rejected: "Доступ не одобрен. Напишите преподавателю.",
    net: "Нет связи с сервером. Попробуйте ещё раз.", oldServer: "Регистрация ещё не включена на сервере. Напишите преподавателю.",
    notFound: "Заявка с таким именем и e-mail не найдена.", emailBad: "Проверьте e-mail.", change: "Изменить данные",
    sendingReg: "Отправляю…", lvlWords: "слов выучено", ofAll: "из 750"
  }
};
let L = "uk", U = UI.uk;

/* ---------- Данные ---------- */
const D = { meta: null, heroes: null, st: null, topics: {}, lex: {}, index: null };
async function getJSON(p) { const r = await fetch(p, { cache: "no-cache" }); if (!r.ok) throw new Error(p + " " + r.status); return r.json() }
async function boot() {
  [D.meta, D.heroes, D.st] = await Promise.all(["data/meta.json", "data/heroes.json", "data/stufen.json"].map(getJSON));
  D.byId = {}; D.meta.topics.forEach(t => D.byId[t.id] = t);
  window.addEventListener("hashchange", route); route(); recheck();
}
async function topic(id) {
  if (D.topics[id]) return D.topics[id];
  const t = await getJSON(`data/topics/T${pad(id)}.json`); D.topics[id] = t;
  t.words.forEach(w => { if (w.tr && w.first === id && !D.lex[w.k]) D.lex[w.k] = Object.assign({ t: id }, w) });
  return t;
}
async function lexOf(t) { // загрузить темы, где у слов этой темы есть тексты
  const need = [...new Set(t.words.filter(w => w.first !== t.id).map(w => w.first))].filter(id => D.byId[id] && D.byId[id].ready);
  await Promise.all(need.map(topic));
}
const word = k => D.lex[k];
const hero = () => D.heroes.heroes.find(h => h.key === P.hero);
const chr = k => D.heroes.chars[k];
const gform = s => String(s || "").replace(/\{([^}|]*)\|([^}]*)\}/g, (m, a, b) => (hero() && hero().g === "f") ? b : a);

/* ---------- Профиль ученика ---------- */
let P = null;
const PK = n => "wr_" + n;
function profiles() { try { return JSON.parse(localStorage.getItem("wr_profiles") || "[]") } catch (e) { return [] } }
function saveProfiles(a) { try { localStorage.setItem("wr_profiles", JSON.stringify(a)) } catch (e) { } }
function load(name) { try { const p = JSON.parse(localStorage.getItem(PK(name)) || "null"); return p } catch (e) { return null } }
function save() { if (!P) return; try { localStorage.setItem(PK(P.name), JSON.stringify(P)); localStorage.setItem("wr_cur", P.name) } catch (e) { toast("localStorage: " + e.message) } }
function newProfile(name, l1) {
  return { v: CFG.v, name, l1, hero: null, start: 1, cur: 1, shift: 0, t: {}, srs: {}, def: {}, xp: 0, ep: 0, diary: [], badges: [], fr: {}, nt: {}, hw: [],
    days: [], streak: 0, scores: [], made: Date.now(), lastExport: Date.now(), sent: 0, log: [] };
}
function useProfile(p) { P = p; L = P.l1 || "uk"; U = UI[L]; document.documentElement.lang = L }

/* ---------- Профиль сложности ---------- */
function profIdx(t) { const ps = D.st.profiles; let i = ps.findIndex(p => p.niveau === t.niveau); return i < 0 ? 0 : i }
function diffOf(tid) { const r = P.t[tid]; if (r && r.d) return r.d; const k = ["easy", "course", "hard", "harder"][Math.max(0, Math.min(3, 1 + (P.shift || 0)))]; return k }
function prof(t, dk) {
  const ps = D.st.profiles, sh = D.st.diff.find(d => d.key === dk).shift, i = Math.max(0, Math.min(ps.length - 1, profIdx(t) + sh));
  const types = []; for (let j = 0; j <= i; j++) types.push(...ps[j].add);
  const p = Object.assign({}, ps[i], { i, types, dk });
  if (dk === "easy") { p.l1 = "always"; p.opts = Math.max(2, ps[Math.max(0, profIdx(t))].opts - 1) }
  if (dk === "hard" && p.l1 !== "dict" && p.l1 !== "def") p.l1 = "tap";
  return p;
}
const RANK = { de2l1: 1, img2de: 1, audio: 2, l12de: 2, article: 2, me: 3, spell: 3, odd: 3, def2de: 4, cloze: 4, mecloze: 5 };

/* ---------- Интервальное повторение ---------- */
function isDue(s) { if (!s || s.b < 1) return false; const B = D.st.box[s.b]; return (today() - s.d >= B.d) || (P.ep - s.e >= B.e) }
function overdue(s) { const B = D.st.box[s.b]; return Math.max(today() - s.d - B.d, (P.ep - s.e - B.e)) }
function dueList() { return Object.entries(P.srs).filter(([k, s]) => s.b < 5 && isDue(s)).map(([k]) => k) }
function grade(k, ok, t) {
  const s = P.srs[k] || (P.srs[k] = { t: (word(k) || {}).t || t, b: 0, d: today(), e: P.ep, n: 0, f: 0 });
  if (ok) { s.b = Math.min(5, s.b + 1); s.n++ } else { s.b = 1; s.f++ }
  s.d = today(); s.e = P.ep;
}
function learnNew(k, okAll, t) { const s = P.srs[k] || (P.srs[k] = { t: (word(k) || {}).t || t, b: 0, d: today(), e: P.ep, n: 0, f: 0 }); s.b = Math.max(s.b, 1); if (!okAll) s.b = 1; s.d = today(); s.e = P.ep; delete P.def[k] }

/* ---------- Варианты ответов ---------- */
function similar(a, b) { const x = cmp(a), y = cmp(b); return x === y || x.includes(y) || y.includes(x) }
function distractors(it, n, mode, pi) {
  const all = Object.values(D.lex).filter(c => c.k !== it.k && c.tr && !similar(c.tr[L], it.tr[L]) && cmp(c.w) !== cmp(it.w));
  let pool = all.filter(c => c.pos === it.pos);
  if (pool.length < n * 2) pool = all;
  const len = x => mode === "l1" ? x.tr[L].length : x.w.length, L0 = len(it);
  const pref = c => pi <= 2 ? (c.t !== it.t ? 0 : 6) : (c.t === it.t ? 0 : 4);
  pool = pool.map(c => [Math.abs(len(c) - L0) + pref(c) + Math.random() * 5, c]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
  const out = []; for (const c of pool) { if (out.length >= n) break; if (out.some(o => similar(o.tr[L], c.tr[L]) || cmp(o.w) === cmp(c.w))) continue; out.push(c) }
  return out;
}
const artOf = w => (w.match(/^(der|die|das)\s/) || [])[1];
const bare = w => w.replace(/^(der|die|das)\s+/, "").replace(/\s*\(pl\.\)/, "");
const uParts = s => [...String(s).matchAll(/<u>(.*?)<\/u>/g)].map(m => m[1]);
const blank = s => String(s).replace(/<u>.*?<\/u>/g, "<b class='gap'>＿＿＿</b>");

/* ---------- Карточки ---------- */
function canType(type, it, p) {
  switch (type) {
    case "img2de": return !!it.img;
    case "article": return it.pos === "n" && !!artOf(it.w);
    case "spell": return bare(it.w).length >= 3 && bare(it.w).length <= 16;
    case "cloze": return uParts(it.ex.de).length === 1 && uParts(it.ex.de)[0].length <= 24;
    case "mecloze": return uParts(it.me.de).length === 1 && uParts(it.me.de)[0].length <= 24;
    case "def2de": return !!it.def;
    case "me": return !!it.me;
    case "audio": return canSay;
    default: return true;
  }
}
function pickType(it, p, want, ep) {
  // want: "rec" — узнавание; "hard" — самый трудный разрешённый; "prod" — L1→DE; "me" — реплика
  const ok = t => p.types.includes(t) && canType(t, it, p);
  const hi = p.l1 === "def" || p.l1 === "dict";
  if (want === "rec") { if (ok("img2de") && Math.random() < .5) return "img2de"; if (hi) return ok("def2de") ? "def2de" : (ok("me") ? "me" : "de2l1"); return "de2l1" }
  if (want === "prod") { if (hi) return ok("cloze") ? "cloze" : "me"; return ok("audio") && Math.random() < .3 ? "audio" : "l12de" }
  if (want === "me") { if (ok("mecloze") && Math.random() < .6) return "mecloze"; if (ok("me")) return "me"; return "l12de" }
  let c = p.types.filter(t => ok(t) && t !== "de2l1" && t !== "odd");
  if (ep) c = c.filter(t => !(ep.introUsed && (P.nt[t] || 0) < 5 && ep.introType !== t) || (P.nt[t] || 0) >= 5);
  if (!c.length) return "l12de";
  c.sort((a, b) => RANK[b] - RANK[a]);
  const top = c.slice(0, 3), t = top[Math.random() < .55 ? 0 : Math.floor(Math.random() * top.length)];
  if (ep && (P.nt[t] || 0) < 5) { if (ep.introUsed && ep.introType !== t) return c.find(x => (P.nt[x] || 0) >= 5) || "l12de"; ep.introUsed = true; ep.introType = t }
  return t;
}
function makeCard(type, it, p) {
  const n = Math.max(2, p.opts) - 1, c = { type, k: it.k, it, subAfter: true };
  if (type === "de2l1") { c.q = `<span class="de">${esc(it.w)}</span>`; c.say = it.w; const ds = distractors(it, n, "l1", p.i); c.opts = shuffle([it, ...ds]).map(x => ({ label: x.tr[L], sub: x.w, ok: x.k === it.k })) }
  else if (type === "l12de" || type === "img2de" || type === "audio" || type === "def2de") {
    if (type === "l12de") c.q = `<span class="tr">${esc(it.tr[L])}</span>`;
    if (type === "img2de") c.q = `<img class="pic" src="${it.img}" alt="">`;
    if (type === "audio") { c.q = `<button class="say big" data-say="${esc(it.w)}">🔊 ${U.listen}</button>`; c.auto = it.w }
    if (type === "def2de") c.q = `<span class="sent">${esc(it.def)}</span>`;
    const ds = distractors(it, n, "de", p.i); c.opts = shuffle([it, ...ds]).map(x => ({ label: x.w, sub: type === "audio" ? "" : x.tr[L], ok: x.k === it.k, say: x.w }));
    c.subAfter = true;
  }
  else if (type === "article") { const a = artOf(it.w); c.q = `<span class="de">${esc(bare(it.w))}</span>`; c.opts = ["der", "die", "das"].map(x => ({ label: x, ok: x === a })); c.say = bare(it.w) }
  else if (type === "me") { c.q = `<span class="sent">${U.you}: ${gform(blank(it.me.de))}</span>`; c.ctx = "me"; const ds = distractors(it, n, "de", p.i); c.opts = shuffle([it, ...ds]).map(x => ({ label: x.w, sub: x.tr[L], ok: x.k === it.k })); c.subAfter = true }
  else if (type === "cloze" || type === "mecloze") {
    const src = type === "cloze" ? it.ex : it.me, ans = uParts(src.de)[0];
    c.q = `<span class="sent">${type === "mecloze" ? U.you + ": " : ""}${gform(blank(src.de))}</span>`; c.input = ans; c.ctx = type === "cloze" ? "ex" : "me";
    c.hint = (p.l1 === "dict" ? "" : `<div class="tr">${esc(gform(src[L]))}</div>`) + `<small class="mute">${esc(ans[0])}…  (${esc(it.w)})</small>`;
  }
  else if (type === "spell") { const w = bare(it.w); c.q = `<span class="tr">${esc(it.tr[L])}</span>${artOf(it.w) ? ` <small class="mute">(${artOf(it.w)} …)</small>` : ""}`; c.spell = w }
  return c;
}
function makeOdd(t, p) {
  const own = shuffle(t.words.filter(w => word(w.k) && w.first === t.id)).slice(0, 3).map(w => word(w.k));
  const far = shuffle(Object.values(D.lex).filter(x => Math.abs(x.t - t.id) > 10)).slice(0, 1);
  if (own.length < 3 || !far.length) return null;
  return { type: "odd", k: null, it: far[0], q: U.odd, opts: shuffle([...own, far[0]]).map(x => ({ label: x.w, sub: x.tr[L], ok: x === far[0] })), subAfter: true };
}

/* ---------- Отрисовка карточки ---------- */
let canSay = !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
function say(t) {
  if (!canSay || !t) return;
  try { const v = speechSynthesis.getVoices().find(x => x.lang.toLowerCase().startsWith("de")); speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(strip(t)); u.lang = CFG.lang; if (v) u.voice = v; u.rate = .9; speechSynthesis.speak(u) } catch (e) { }
}
document.addEventListener("click", e => { const b = e.target.closest("[data-say]"); if (b) { e.preventDefault(); e.stopPropagation(); say(b.dataset.say) } }, true);
const sayBtn = t => canSay ? `<button class="say" data-say="${esc(strip(t))}" title="🔊">🔊</button>` : "";
function trShown(p) { return p.l1 === "always" || p.l1 === "after" }
function exampleHTML(it, p, which) {
  const src = which === "me" ? it.me : it.ex, pre = which === "me" ? `<b>${U.you}:</b> ` : "";
  const tr = p.l1 === "dict" ? `<details><summary class="mute">${U.tap}</summary><div class="tr">${esc(gform(src[L]))}</div></details>`
    : (p.l1 === "tap" || p.l1 === "def") ? `<details><summary class="mute">${U.tap}</summary><div class="tr">${esc(gform(src[L]))}</div></details>` : `<div class="tr">${esc(gform(src[L]))}</div>`;
  return `<div>${pre}${gform(src.de)} ${sayBtn(gform(src.de))}</div>${tr}`;
}
function cardHTML(c, p, meta) {
  const nm = D.st.names[c.type], nw = !!nm && (P.nt[c.type] || 0) < 5 && c.type !== "de2l1" && c.type !== "l12de";
  let h = `<div class="card"><div class="kind">${nm ? nm[L] : ""}${nw ? ` <span class="new">${U.newType}</span>` : ""}<span style="flex:1"></span>${meta || ""}</div>`;
  h += `<div class="q ${c.type === "me" || c.type === "cloze" || c.type === "mecloze" || c.type === "def2de" ? "sent" : ""}">${c.q} ${c.say ? sayBtn(c.say) : ""}</div>`;
  if (c.hint) h += `<div style="margin:-6px 0 10px">${c.hint}</div>`;
  if (c.opts) h += `<div class="opts">${c.opts.map((o, i) => `<button class="opt" data-i="${i}">${esc(o.label)}${o.sub && !c.subAfter ? `<small>${esc(o.sub)}</small>` : ""}</button>`).join("")}</div>`;
  if (c.input != null) h += `<div class="row"><input type="text" id="inp" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" placeholder="${U.type}"><button class="main" id="chk">${U.check}</button></div>`;
  if (c.spell) h += `<div class="slot" id="slot"></div><div class="tiles" id="tiles">${shuffle([...c.spell]).map((ch, i) => `<button data-ch="${esc(ch)}">${ch === " " ? "␣" : esc(ch)}</button>`).join("")}</div><div class="row"><button id="bs">⌫</button><button class="main" id="chk">${U.check}</button></div>`;
  h += `<div id="fb"></div></div>`;
  return h;
}
function feedback(c, ok, p) {
  const it = c.it; if (!it) return "";
  let h = `<div class="fb"><div class="verdict ${ok ? "ok" : "bad"}">${ok ? U.right : U.wrong}</div>`;
  if (!ok) h += `<div>${U.correct} <b>${esc(c.input != null ? c.input : c.spell ? c.spell : it.w)}</b>${c.input != null && c.input !== it.w ? ` <small class="mute">(${esc(it.w)})</small>` : ""}</div>`;
  h += `<div style="margin:4px 0"><span class="de">${esc(it.w)}</span> ${sayBtn(it.w)} — <span class="tr">${esc(it.tr[L])}</span></div>`;
  if (it.def && p.i >= 8) h += `<div class="mute"><small>${U.def}:</small> ${esc(it.def)}</div>`;
  h += `<div style="margin-top:6px">${exampleHTML(it, Object.assign({}, p, { l1: p.l1 === "always" || p.l1 === "after" ? "always" : p.l1 }), c.ctx === "me" ? "me" : "ex")}</div>`;
  return h + `</div>`;
}
/* Показ карточки; resolve({ok}) по первой попытке */
function runCard(host, c, p, meta) {
  return new Promise(res => {
    host.innerHTML = cardHTML(c, p, meta); try { if (localStorage.getItem('wr_debug')) window.__card = c } catch (e) { }
    if (c.auto) setTimeout(() => say(c.auto), 250);
    if (P.nt[c.type] == null) P.nt[c.type] = 0;
    const done = ok => {
      P.nt[c.type] = (P.nt[c.type] || 0) + 1;
      $("#fb").innerHTML = feedback(c, ok, p) + `<div class="row" style="margin-top:10px"><button class="main" id="nx">${U.next}</button></div>`;
      if (c.it) say(c.it.w);
      const nx = $("#nx"); nx.focus(); nx.onclick = () => res({ ok });
    };
    if (c.opts) $$(".opt").forEach(b => b.onclick = () => {
      if (host.dataset.answered) return; host.dataset.answered = 1;
      const o = c.opts[+b.dataset.i];
      $$(".opt").forEach((x, i) => { x.disabled = true; const oo = c.opts[i]; if (oo.ok) x.classList.add("ok"); if (c.subAfter && oo.sub) x.insertAdjacentHTML("beforeend", `<small>${esc(oo.sub)}</small>`) });
      if (!o.ok) b.classList.add("bad");
      done(o.ok);
    });
    if (c.input != null) {
      const inp = $("#inp"); inp.focus();
      const go = () => { if (host.dataset.answered || !inp.value.trim()) return; host.dataset.answered = 1; inp.disabled = true; $("#chk").disabled = true; done(cmp(inp.value) === cmp(c.input)) };
      $("#chk").onclick = go; inp.onkeydown = e => { if (e.key === "Enter") go() };
    }
    if (c.spell) {
      let s = ""; const slot = $("#slot"), used = [];
      $$("#tiles button").forEach(b => b.onclick = () => { if (b.disabled) return; s += b.dataset.ch; used.push(b); b.disabled = true; slot.textContent = s });
      $("#bs").onclick = () => { if (!used.length) return; const b = used.pop(); b.disabled = false; s = s.slice(0, -1); slot.textContent = s };
      $("#chk").onclick = () => { if (host.dataset.answered || !s) return; host.dataset.answered = 1; $$("#tiles button,#bs,#chk").forEach(b => b.disabled = true); done(s === c.spell) };
    }
    delete host.dataset.answered;
  });
}
/* Очередь карточек: первая попытка — в балл, ошибка возвращается в конце */
async function runDeck(host, cards, p, onEach) {
  const q = cards.slice(), first = new Map(); let i = 0;
  while (q.length) {
    const c = q.shift(); i++;
    const meta = `<small>${i <= cards.length ? i + "/" + cards.length : "↻ " + (q.length + 1)}</small>`;
    const r = await runCard(host, c, p, meta);
    if (!first.has(c)) { first.set(c, r.ok); onEach && onEach(c, r.ok) }
    if (!r.ok) { const again = c.opts ? Object.assign({}, c, { opts: shuffle(c.opts) }) : Object.assign({}, c); first.set(again, false); q.push(again) }
    save();
  }
  const res = cards.map(c => first.get(c));
  return { ok: res.filter(Boolean).length, all: cards.length, bad: cards.filter(c => first.get(c) === false).map(c => c.it && c.it.w).filter(Boolean) };
}

/* ---------- Маршруты ---------- */
function toast(t) { const d = document.createElement("div"); d.className = "toast"; d.textContent = t; document.body.appendChild(d); setTimeout(() => d.remove(), 3200) }
function head() {
  if (!P) return `<header class="top"><a class="brand" href="#/">Wort<b>reise</b></a><span class="sp"></span><a class="chip" href="../">Sprich Deutsch</a></header>`;
  return `<header class="top"><a class="brand" href="#/">Wort<b>reise</b></a><span class="sp"></span><span class="chip">⭐ ${P.xp}</span>${P.streak > 1 ? `<span class="chip">🔥 ${P.streak}</span>` : ""}<a class="chip home" href="#/" title="${U.home}">⌂</a></header>`;
}
function route() {
  if (window.speechSynthesis) try { speechSynthesis.cancel() } catch (e) { }
  const hsh = location.hash.replace(/^#/, "") || "/", [path, qs] = hsh.split("?"), parts = path.split("/").filter(Boolean);
  const q = new URLSearchParams(qs || "");
  if (!P) { const cur = localStorage.getItem("wr_cur"), p = cur && load(cur); if (p) useProfile(p) }
  if (parts[0] === "new") { P = null; return viewRegister() }
  if (parts[0] === "login") { P = null; return viewLogin() }
  if (!P) return pending() ? viewWaiting() : profiles().length && parts[0] !== "reg" ? viewProfiles() : viewRegister();
  if (!P.reg || P.reg.status !== "approved") return P.reg && P.reg.status === "rejected" ? viewBlocked() : viewRegister(P.name, P.l1);
  if (q.get("review")) { importWords(q.get("review").split(",")); toast(U.hwLink); history.replaceState(null, "", "#/" + parts.join("/")) }
  if (!P.hero || parts[0] === "hero") return viewHero();
  if (parts[0] === "t") return viewTopic(+parts[1]);
  if (parts[0] === "review") return viewReview(parts[1], +parts[2]);
  if (parts[0] === "diary") return viewDiary();
  if (parts[0] === "me") return viewMe();
  if (parts[0] === "users") { P = null; localStorage.removeItem("wr_cur"); return viewProfiles() }
  if (parts[0] === "map") return viewMap();
  return viewHome();
}
function viewProfiles() {
  const ps = profiles();
  app().innerHTML = head() + `<h1>${UI.uk.hello}</h1><p class="mute">${UI.ru.hello}</p>
  ${ps.length ? `<h2>${U.profiles}</h2><div class="row">${ps.map(n => `<button data-p="${esc(n)}">👤 ${esc(n)}</button>`).join("")}</div>` : ""}
  <div class="row" style="margin-top:14px"><a class="btn" href="#/new">＋ ${U.newp}</a></div>`;
  $$("[data-p]").forEach(b => b.onclick = () => { const p = load(b.dataset.p); if (p) { useProfile(p); save(); location.hash = "#/"; route() } });
}
function viewNew() {
  app().innerHTML = head() + `<div class="box"><h1>Wortreise</h1><label>${UI.uk.who} / ${UI.ru.who}<input type="text" id="nm" maxlength="40" autocomplete="off"></label>
  <p style="margin:12px 0 4px">${UI.uk.lang} / ${UI.ru.lang}</p><div class="row"><button class="on" data-l="uk">Українська</button><button data-l="ru">Русский</button></div>
  <p id="msg" class="mute"></p><button class="main" id="go">${UI.uk.create} / ${UI.ru.create}</button></div>`;
  let l1 = "uk"; $$("[data-l]").forEach(b => b.onclick = () => { l1 = b.dataset.l; $$("[data-l]").forEach(x => x.classList.toggle("main", x === b)) }); $("[data-l=uk]").classList.add("main");
  $("#go").onclick = () => {
    const n = $("#nm").value.trim(); if (!n) { $("#msg").textContent = UI[l1].nameNeed; return }
    const ps = profiles(); let p = load(n);
    if (p) toast(UI[l1].exists); else { p = newProfile(n, l1); ps.push(n); saveProfiles(ps) }
    useProfile(p); save(); location.hash = p.hero ? "#/map" : "#/hero";
  };
}
function viewHero() {
  const hs = D.heroes.heroes;
  app().innerHTML = head() + `<h1>${U.choose}</h1><p class="mute">${U.chooseSub}</p><div class="heroes">${hs.map(h => { const c = chr(h.key); return `<button class="hero ${P.hero === h.key ? "sel" : ""}" data-h="${h.key}"><span class="em">${h.emoji}</span><b>${esc(c[L])}</b><small>${esc(c.role[L])}</small><small>${esc(h.lineName[L])} · ${esc(h.place[L])}</small></button>` }).join("")}</div>
  ${Object.keys(P.t).length ? "" : `<div class="box" style="margin-top:14px"><h3>${U.start}</h3><div class="row"><label style="flex:1">${U.choosePlace}<input type="number" id="st" min="1" max="750" value="${P.start || 1}"></label></div></div>`}`;
  $$("[data-h]").forEach(b => b.onclick = () => {
    P.hero = b.dataset.h; const st = $("#st");
    if (st) { const n = Math.max(1, Math.min(750, +st.value || 1)); P.start = n; P.cur = n; for (let i = 1; i < n; i++) P.t[i] = { st: "skip" } }
    save(); location.hash = "#/";
  });
}
const tStatus = id => { const r = P.t[id]; if (r && r.st === "done") return "done"; if (r && r.st === "skip") return "skip"; if (id === P.cur) return "cur"; return id < P.cur ? "open" : "lock" };
function viewMap() {
  const st = +(sessionStorage.getItem("wr_stufe") || Math.ceil(P.cur / 75)), due = dueList().length, s0 = (st - 1) * 75;
  let h = head() + `<div class="tabs">${[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => `<button data-s="${n}" class="${n === st ? "on" : ""}">${U.stufe} ${n}</button>`).join("")}</div>`;
  const cur = D.byId[P.cur];
  if (cur) h += `<div class="box"><div class="row"><div style="flex:1"><small class="mute">${U.topic} ${cur.id} · ${cur.niveau}</small><div class="de">${esc(cur.name)}</div></div>
   ${due > 60 ? `<a class="btn main" href="#/review">${U.review} (${due})</a>` : `<a class="btn main" href="#/t/${cur.id}">▶ ${U.startEp}</a>`}</div>${due > 60 ? `<p class="hint">${U.blocked}</p>` : due ? `<p class="mute" style="margin:8px 0 0">${U.due(due)} · <a href="#/review">${U.review}</a></p>` : ""}</div>`;
  for (let ch = 0; ch < 3; ch++) {
    const a = s0 + ch * 25 + 1, b = a + 24, hl = D.heroes.heroes[(a - 1) / 25 % 25 | 0];
    h += `<h2>${a}–${b}</h2><div class="grid">`;
    for (let id = a; id <= b; id++) {
      const t = D.byId[id], s = tStatus(id), r = P.t[id] || {};
      const cls = !t.ready ? "soon" : s === "lock" ? "lock" : s;
      const mark = s === "done" ? `✓${r.d && r.d !== "course" ? U.diffShort[r.d] : ""}` : s === "cur" ? "▶" : s === "lock" ? "🔒" : s === "skip" ? "·" : "";
      h += `<button class="tile ${cls}" data-t="${id}"><span class="st">${mark}</span><span class="no">${id}</span><span>${esc(t.name.split(":")[0])}</span>${!t.ready ? `<small class="mute">${U.soon}</small>` : s === "done" && r.s != null ? `<small class="mute">${r.s}%</small>` : ""}</button>`;
    }
    const fd = P.t["f" + b];
    h += `<button class="tile fest ${tStatus(b) === "done" || P.t[b] ? "" : "lock"}" data-f="${b}"><span class="st">${fd ? "🎉" : "🎈"}</span><span class="no">🎪</span><span>${U.fest(b).split(":")[0]}</span></button>`;
    if (ch === 2) h += `<button class="tile fest ${P.t[b] && P.t[b].st === "done" ? "" : "lock"}" data-x="${st}"><span class="st">${P.t["x" + st] ? "🏅" : "📝"}</span><span class="no">🎓</span><span>${U.exam(st)}</span></button>`;
    h += `</div>`;
  }
  app().innerHTML = h;
  $$("[data-s]").forEach(b => b.onclick = () => { sessionStorage.setItem("wr_stufe", b.dataset.s); viewMap() });
  $$("[data-t]").forEach(b => b.onclick = () => { const id = +b.dataset.t, s = tStatus(id); if (!D.byId[id].ready) return toast(U.empty); if (s === "lock") return toast(U.lock); location.hash = "#/t/" + id });
  $$("[data-f]").forEach(b => b.onclick = () => { if (b.classList.contains("lock")) return toast(U.lock); location.hash = "#/review/fest/" + b.dataset.f });
  $$("[data-x]").forEach(b => b.onclick = () => { if (b.classList.contains("lock")) return toast(U.lock); location.hash = "#/review/exam/" + b.dataset.x });
  if (Date.now() - (P.lastExport || 0) > 7 * 864e5 && Object.keys(P.srs).length > 30) { P.lastExport = Date.now() - 5 * 864e5; save(); toast(U.remind) }
}

/* ---------- Эпизод ---------- */
function stepsBar(n) { return `<div class="steps">${U.steps.map((s, i) => `<i class="${i < n ? "done" : i === n ? "on" : ""}" title="${s}"></i>`).join("")}</div>` }
const FIRST_OF = { "A2": 51, "B1": 101, "B2-C1": 151, "Schrift": 101, "Haupt": 151, "Basis": 1, "A1": 1 };
function plan(t, dk) {
  const set = t.sets[dk] || t.sets.course, W = t.words, have = i => W[i] && word(W[i].k);
  const uniq = a => { const s = new Set(); return a.filter(i => have(i) && !s.has(W[i].k) && s.add(W[i].k)) };
  const core = uniq(set.core), quick = uniq(set.quick || []), chest = uniq(set.chest || []);
  const known = k => P.srs[k] && P.srs[k].b >= 1;
  const nw = core.filter(i => !known(W[i].k)).map(i => W[i].k), rv = core.filter(i => known(W[i].k)).map(i => W[i].k);
  const qk = quick.filter(i => !nw.includes(W[i].k)).map(i => W[i].k);
  const back = Object.entries(P.def).filter(([k, d]) => d.due <= t.id && word(k) && !known(k) && !nw.includes(k)).sort((a, b) => a[1].due - b[1].due).slice(0, 4).map(([k]) => k);
  return { nw, rv, qk, back, chest: chest.map(i => W[i].k).filter(k => !known(k) && !nw.includes(k)) };
}
function reviewSet(t, p, extra, n) {
  const due = dueList().filter(k => word(k) && !extra.includes(k));
  const hw = P.hw.filter(k => due.includes(k));
  const od = due.filter(k => !hw.includes(k)).sort((a, b) => overdue(P.srs[b]) - overdue(P.srs[a]));
  const line = t ? od.filter(k => D.byId[P.srs[k].t] && D.byId[P.srs[k].t].line === t.line) : [];
  const order = [...hw, ...od.slice(0, Math.ceil(n * .6)), ...line, ...od];
  const out = [], seenT = {};
  for (const k of order) { if (out.length >= n) break; if (out.includes(k)) continue; const tt = P.srs[k].t; if ((seenT[tt] || 0) >= Math.max(3, n / 4)) continue; seenT[tt] = (seenT[tt] || 0) + 1; out.push(k) }
  for (const k of order) { if (out.length >= n) break; if (!out.includes(k)) out.push(k) }
  if (out.length < n) { const weak = Object.entries(P.srs).filter(([k, s]) => word(k) && !out.includes(k) && !extra.includes(k) && s.b < 5).sort((a, b) => a[1].b - b[1].b || a[1].d - b[1].d).map(([k]) => k); out.push(...weak.slice(0, Math.min(n - out.length, 3))) }
  return out;
}
async function ensureDueLoaded(keys) { const ids = [...new Set(keys.map(k => P.srs[k] && P.srs[k].t).filter(Boolean))].filter(id => D.byId[id] && D.byId[id].ready); await Promise.all(ids.map(topic)) }
async function viewTopic(id) {
  const m = D.byId[id]; if (!m || !m.ready) { location.hash = "#/map"; return toast(U.empty) }
  app().innerHTML = head() + `<p class="mute">…</p>`;
  const t = await topic(id); await lexOf(t); await ensureDueLoaded(Object.keys(P.srs));
  await preloadNeighbours(id);
  const E = { t, dk: diffOf(id), res: [], xp: 0, t0: Date.now(), introUsed: false, newOk: {} };
  intro(E);
}
async function preloadNeighbours(id) { // для неверных вариантов — соседние готовые темы
  const ready = D.meta.topics.filter(x => x.ready).map(x => x.id), near = ready.filter(x => x !== id).sort((a, b) => Math.abs(a - id) - Math.abs(b - id)).slice(0, 3);
  const far = ready.filter(x => Math.abs(x - id) > 10); if (far.length) near.push(far[Math.floor(Math.random() * far.length)]);
  await Promise.all(near.map(topic));
}
function intro(E) {
  const t = E.t, h = hero(), p = prof(t, E.dk), pl = plan(t, E.dk), ent = (t.entry || {})[P.hero] || {}, host = t.host;
  const hostC = host && chr(host.who), due = dueList().length;
  app().innerHTML = head() + stepsBar(0) + `<div class="box scene"><small class="mute">${U.topic} ${t.id} · ${U.stufe} ${t.stufe} · ${t.niveau}</small><h1>${esc(t.name)}</h1>
   <p>${esc(gform((t.scene || {})[L] || ""))}</p>${ent[L] ? `<p><b>${esc(chr(P.hero)[L])}:</b> ${esc(gform(ent[L]))}</p>` : ""}
   ${host ? `<div class="host"><b>${esc(hostC ? hostC[L] : host.who)}:</b> <span class="de">${host.de}</span> ${sayBtn(host.de)}<div class="tr">${esc(gform(host[L]))}</div></div>` : ""}</div>
   <div class="sticky"><button class="main big" id="go">▶ ${U.startEp}</button></div>
   <details class="box diffbox"><summary>${U.diff}: <b>${D.st.diff.find(d => d.key === E.dk)[L]}</b></summary><div class="diff" style="margin-top:10px">${D.st.diff.map(d => `<button data-d="${d.key}" class="${d.key === E.dk ? "on" : ""}">${d[L]}</button>`).join("")}</div>
   <label class="row mute" style="margin-top:8px"><input type="checkbox" id="keep" ${P.shift === D.st.diff.find(d => d.key === E.dk).shift && P.shift !== 0 ? "checked" : ""}> ${U.keep}</label>
   <p class="mute" style="margin:8px 0 0">${pl.nw.length + pl.back.length} ${U.newWords} · ${pl.rv.length + pl.qk.length + Math.min(due, p.review)} ${U.revWords}${pl.chest.length ? ` · ${U.chest}: ${pl.chest.length}` : ""}</p></details>`;
  $$("[data-d]").forEach(b => b.onclick = () => { E.dk = b.dataset.d; P.t[t.id] = Object.assign(P.t[t.id] || {}, { d: E.dk }); if ($("#keep").checked) P.shift = D.st.diff.find(d => d.key === E.dk).shift; save(); intro(E); const db = $(".diffbox"); if (db) db.open = true });
  $("#keep").onchange = e => { P.shift = e.target.checked ? D.st.diff.find(d => d.key === E.dk).shift : 0; save() };
  $("#go").onclick = () => { if (host) say(host.de); E.plan = plan(t, E.dk); showStep(E) };
}
async function showStep(E) {
  const t = E.t, p = prof(t, E.dk), list = [...E.plan.nw, ...E.plan.back];
  if (!list.length) return trainStep(E);
  let i = 0;
  const draw = () => {
    const it = word(list[i]), back = E.plan.back.includes(list[i]) ? `<small class="badge">${U.returned(it.t)}</small>` : "";
    app().innerHTML = head() + stepsBar(1) + `<div class="card"><div class="kind">${U.intro} · ${i + 1}/${list.length} ${back}<span style="flex:1"></span><small class="mute">${it.lvl}</small></div>
    ${it.img ? `<img class="pic" src="${it.img}" alt="">` : ""}
    <div class="q">${esc(it.w)} ${sayBtn(it.w)}</div>
    ${p.l1 === "def" || p.l1 === "dict" ? (it.def ? `<p>${esc(it.def)}</p>` : "") + `<details><summary class="mute">${U.tap}</summary><p class="tr">${esc(it.tr[L])}</p></details>` : p.l1 === "tap" ? `<details open><summary class="mute">${U.tap}</summary><p class="tr">${esc(it.tr[L])}</p></details>` : `<p class="tr" style="font-size:20px;margin-top:-6px">${esc(it.tr[L])}</p>`}
    <div class="fb">${exampleHTML(it, p, "ex")}<div style="margin-top:8px">${exampleHTML(it, p, "me")}</div></div>
    <div class="row" style="margin-top:12px"><button class="main" id="nx">${U.next}</button>${i > 0 ? `<button id="pv">${U.back}</button>` : ""}<span style="flex:1"></span><button class="ghost" id="sk"><small>${U.skipShow}</small></button></div></div>`;
    setTimeout(() => say(it.w), 200);
    $("#nx").onclick = () => { i++; i < list.length ? draw() : trainStep(E) };
    if ($("#pv")) $("#pv").onclick = () => { i--; draw() };
    $("#sk").onclick = () => trainStep(E);
  };
  draw();
}
async function trainStep(E) {
  const t = E.t, p = prof(t, E.dk), list = [...E.plan.nw, ...E.plan.back];
  app().innerHTML = head() + stepsBar(2) + `<div id="host"></div>`;
  if (list.length) {
    const a = shuffle(list).map(k => makeCard(pickType(word(k), p, "rec", E), word(k), p));
    const b = shuffle(list).map(k => makeCard(pickType(word(k), p, "hard", E), word(k), p));
    const cards = [...a.slice(0, Math.ceil(a.length / 2)), ...b.slice(0, Math.ceil(b.length / 2)), ...a.slice(Math.ceil(a.length / 2)), ...b.slice(Math.ceil(b.length / 2))];
    if (p.types.includes("odd")) { const o = makeOdd(t, p); if (o) cards.push(o) }
    const r = await runDeck($("#host"), cards, p, (c, ok) => { if (c.k) E.newOk[c.k] = (E.newOk[c.k] !== false) && ok });
    E.res.push(Object.assign({ step: "train" }, r));
    list.forEach(k => learnNew(k, E.newOk[k] !== false, t.id));
  }
  // невзятые слова уходят в отложенные
  const W = t.words, taken = new Set(list), inC = new Set((t.sets.course.core || []).map(i => W[i] && W[i].k));
  const later = (k, due) => { if (!word(k) || taken.has(k) || (P.srs[k] && P.srs[k].b >= 1)) return; const d = P.def[k]; if (!d || d.due > due) P.def[k] = { t: t.id, due } };
  if (E.dk === "easy") inC.forEach(k => later(k, t.id + 10));
  (t.deferred || []).forEach(i => { const w = W[i]; if (!w) return; later(w.k, Math.max(t.id + 10, FIRST_OF[w.lvl] || t.id + 10)) });
  P.ep++; const r = P.t[t.id] = Object.assign(P.t[t.id] || {}, { d: E.dk }); r.st = r.st === "done" ? "done" : "part"; save();
  reviewStep(E);
}
function reviewCards(keys, p) {
  return keys.map(k => { const s = P.srs[k] || { b: 1 }, it = word(k), want = s.b <= 1 ? "rec" : s.b === 2 ? "prod" : s.b === 4 ? "me" : "hard"; return makeCard(pickType(it, p, want, null), it, p) });
}
async function reviewStep(E) {
  const t = E.t, p = prof(t, E.dk), extra = [...E.plan.nw, ...E.plan.back];
  const keys = [...new Set([...E.plan.rv, ...E.plan.qk.slice(0, 8), ...reviewSet(t, p, extra.concat(E.plan.rv, E.plan.qk), p.review)])].filter(k => word(k));
  if (!keys.length) return sceneStep(E);
  app().innerHTML = head() + stepsBar(3) + `<div id="host"></div>`;
  const r = await runDeck($("#host"), reviewCards(keys, p), p, (c, ok) => { if (c.k) { grade(c.k, ok, t.id); if (ok) P.hw = P.hw.filter(x => x !== c.k) } });
  E.res.push(Object.assign({ step: "review" }, r));
  sceneStep(E);
}
async function sceneStep(E) {
  const t = E.t, p = prof(t, E.dk);
  const own = shuffle(t.words.filter(w => w.first === t.id && word(w.k) && (P.srs[w.k] || {}).b >= 1).map(w => word(w.k)));
  let far = shuffle(Object.values(D.lex).filter(x => Math.abs(x.t - t.id) > 8 && D.byId[x.t] && D.byId[x.t].line !== t.line));
  const easyFar = far.filter(x => ["A1", "A2", "Basis", "CORE"].includes(x.lvl)); if (p.i <= 3 && easyFar.length >= 8) far = easyFar;
  app().innerHTML = head() + stepsBar(4) + `<div id="host"></div>`;
  const host = $("#host");
  if (p.scene === "cloud" || !own.length) {
    const fit = own.slice(0, 7), bad = far.slice(0, Math.max(5, 12 - fit.length));
    if (!fit.length || !bad.length) return finish(E);
    const chips = shuffle([...fit.map(x => [x, 1]), ...bad.map(x => [x, 0])]);
    let found = 0, wrong = 0;
    host.innerHTML = `<div class="card"><div class="kind">${U.steps[4]}</div><p>${esc(gform((t.scene || {})[L] || ""))}</p><h3>${U.sceneCloud}</h3><div class="cloud">${chips.map(([x], i) => `<button data-i="${i}">${esc(x.w)}</button>`).join("")}</div><p class="mute" id="cnt"></p><div id="fb"></div></div>`;
    const upd = () => $("#cnt").textContent = `${U.found}: ${found}/${fit.length} · ${U.extra}: ${wrong}`; upd();
    await new Promise(res => $$(".cloud button").forEach(b => b.onclick = () => {
      if (b.disabled) return; const [x, ok] = chips[+b.dataset.i]; b.disabled = true; b.classList.add(ok ? "ok" : "bad"); b.insertAdjacentHTML("beforeend", `<small>${esc(x.tr[L])}</small>`); say(x.w);
      if (ok) { found++; $("#fb").innerHTML = `<div class="fb">${gform(x.ex.de)} ${sayBtn(gform(x.ex.de))}<div class="tr">${esc(gform(x.ex[L]))}</div></div>` } else wrong++;
      upd(); if (found === fit.length) { $("#fb").insertAdjacentHTML("beforeend", `<div class="row" style="margin-top:10px"><button class="main" id="nx">${U.next}</button></div>`); $("#nx").onclick = res }
    }));
    E.scene = { found, all: fit.length, wrong };
  } else if (p.scene === "build") {
    const cand = own.filter(x => { const n = strip(gform(x.ex.de)).split(/\s+/).length; return n >= 3 && n <= 12 });
    const x = cand[0] || own[0], words = strip(gform(x.ex.de)).split(/\s+/);
    let built = [];
    host.innerHTML = `<div class="card"><div class="kind">${U.steps[4]}</div><p class="mute">${esc(gform((t.scene || {})[L] || ""))}</p><h3>${U.sceneBuild}</h3>${p.l1 !== "dict" ? `<p class="tr">${esc(gform(x.ex[L]))}</p>` : ""}
     <div class="slot" id="slot"></div><div class="tiles" id="tiles">${shuffle(words.map((w, i) => [w, i])).map(([w, i]) => `<button data-w="${esc(w)}">${esc(w)}</button>`).join("")}</div><div class="row"><button id="bs">⌫</button><button class="main" id="chk">${U.check}</button></div><div id="fb"></div></div>`;
    const used = [];
    $$("#tiles button").forEach(b => b.onclick = () => { if (b.disabled) return; built.push(b.dataset.w); used.push(b); b.disabled = true; $("#slot").textContent = built.join(" ") });
    $("#bs").onclick = () => { if (!used.length) return; used.pop().disabled = false; built.pop(); $("#slot").textContent = built.join(" ") };
    await new Promise(res => $("#chk").onclick = () => {
      const ok = cmp(built.join(" ")) === cmp(words.join(" ")); $$("#tiles button,#bs,#chk").forEach(b => b.disabled = true);
      $("#fb").innerHTML = `<div class="fb"><div class="verdict ${ok ? "ok" : "bad"}">${ok ? U.right : U.wrong}</div>${gform(x.ex.de)} ${sayBtn(gform(x.ex.de))}<div class="tr">${esc(gform(x.ex[L]))}</div></div><div class="row" style="margin-top:10px"><button class="main" id="nx">${U.next}</button></div>`;
      say(gform(x.ex.de)); E.scene = { found: ok ? 1 : 0, all: 1, wrong: ok ? 0 : 1 }; $("#nx").onclick = res;
    });
  } else {
    const x = own[0], ds = far.slice(0, 2);
    const opts = shuffle([x, ...ds]).map(y => ({ label: strip(gform(y.ex.de)), ok: y === x }));
    const c = { type: "scene", it: x, q: `<span class="sent">${esc(gform((t.scene || {})[L] || t.name))}</span>`, opts };
    const r = await runCard(host, c, p, ""); E.scene = { found: r.ok ? 1 : 0, all: 1, wrong: r.ok ? 0 : 1 };
  }
  finish(E);
}
function streakUpd() { const d = today(); if (P.days[P.days.length - 1] === d) return; P.streak = (P.days[P.days.length - 1] === d - 1) ? P.streak + 1 : 1; P.days.push(d); P.days = P.days.slice(-60) }
function badge(id, txt) { if (!P.badges.find(b => b.id === id)) { P.badges.push({ id, txt, at: Date.now() }); toast("🏅 " + txt) } }
function checkBadges() {
  const done = Object.values(P.t).filter(r => r.st === "done").length, learned = Object.values(P.srs).filter(s => s.b >= 3).length;
  if (done >= 1) badge("first", L === "uk" ? "Перший епізод" : "Первый эпизод");
  [10, 25, 50, 75, 150, 300, 750].forEach(n => done >= n && badge("t" + n, `${n} ${U.topics}`));
  [100, 500, 1000, 2500, 5000].forEach(n => learned >= n && badge("w" + n, `${n} ${U.learned}`));
  [7, 30, 100].forEach(n => P.streak >= n && badge("s" + n, `🔥 ${n} ${U.streak}`));
}
function finish(E) {
  const t = E.t, dd = D.st.diff.find(d => d.key === E.dk), ok = E.res.reduce((a, r) => a + r.ok, 0), all = E.res.reduce((a, r) => a + r.all, 0);
  const pc = all ? Math.round(ok * 100 / all) : 100, xp = Math.round((ok * D.st.xp.card + (E.scene ? E.scene.found * D.st.xp.first : 0) + D.st.xp.episode) * dd.xp);
  P.xp += xp; streakUpd();
  const r = P.t[t.id] = Object.assign(P.t[t.id] || {}, { st: "done", d: E.dk, s: pc, at: Date.now(), x: (P.t[t.id] || {}).x ? P.t[t.id].x + xp : xp });
  if (t.id >= P.cur) { P.cur = t.id + 1; while (P.t[P.cur] && P.t[P.cur].st === "done") P.cur++ }
  (t.cast || []).filter(k => k !== P.hero && chr(k)).forEach(k => P.fr[k] = (P.fr[k] || 0) + 1);
  const bad = [...new Set(E.res.flatMap(r => r.bad))];
  const ent = ((t.entry || {})[P.hero] || {})[L] || "";
  P.diary.unshift({ id: t.id, at: Date.now(), d: E.dk, s: pc, txt: gform(ent), nw: [...E.plan.nw, ...E.plan.back].map(k => word(k).w), bad });
  P.diary = P.diary.slice(0, 400);
  P.scores.push(pc); P.scores = P.scores.slice(-6);
  P.log.push({ id: t.id, name: t.name, at: Date.now(), d: E.dk, s: pc, ok, all, nw: E.plan.nw.length + E.plan.back.length, bad, min: Math.round((Date.now() - E.t0) / 6e4), scene: E.scene });
  P.log = P.log.slice(-200);
  checkBadges(); save();
  const s2 = P.scores.slice(-2), sug = s2.length === 2 && s2.every(x => x < 60) && E.dk !== "easy" ? "easy" : s2.length === 2 && s2.every(x => x > 95) && E.dk !== "harder" ? "up" : null;
  const nextId = t.id + 1, nx = D.byId[nextId];
  app().innerHTML = head() + stepsBar(5) + `<div class="box"><h1>🎉 ${U.done}</h1><div class="stat"><div><b>${pc}%</b>${U.score}</div><div><b>+${xp}</b>${U.xp}</div><div><b>${E.plan.nw.length + E.plan.back.length}</b>${U.newWords}</div></div>
   ${ent ? `<p style="margin-top:12px">📔 ${esc(gform(ent))}</p>` : ""}${bad.length ? `<p class="mute">${U.wrong} ${bad.map(esc).join(", ")}</p>` : ""}</div>
   ${sug ? `<div class="box hint">${sug === "easy" ? U.suggestEasy : U.suggestHard} <button id="sgY">${U.yes}</button> <button id="sgN">${U.no}</button></div>` : ""}
   <a class="btn main big" href="${nextAction().href}">${U.next} ▶</a>
   ${E.plan.chest.length ? `<div class="box" style="margin-top:16px"><h3>🧰 ${U.chest}</h3><p>${U.chestTxt(E.plan.chest.length)}</p><button id="chest">${U.openChest}</button></div>` : ""}
   <p class="links"><a href="#/">${U.home}</a></p>`;
  if ($("#sgY")) { $("#sgY").onclick = () => { const order = ["easy", "course", "hard", "harder"], i = order.indexOf(E.dk); const nk = sug === "easy" ? order[Math.max(0, i - 1)] : order[Math.min(3, i + 1)]; P.shift = D.st.diff.find(d => d.key === nk).shift; P.scores = []; save(); $("#sgY").parentNode.remove() }; $("#sgN").onclick = () => { P.scores = []; save(); $("#sgN").parentNode.remove() } }
  if ($("#chest")) $("#chest").onclick = () => chestRun(E);

}
async function chestRun(E) {
  const t = E.t, p = prof(t, E.dk), list = E.plan.chest.slice(0, 12);
  app().innerHTML = head() + `<h2>🧰 ${U.chest}</h2><div id="host"></div>`;
  const host = $("#host");
  for (let i = 0; i < list.length; i++) {
    const it = word(list[i]);
    host.innerHTML = `<div class="card"><div class="kind">${U.chest} · ${i + 1}/${list.length}<span style="flex:1"></span><small class="mute">${it.lvl}</small></div>${it.img ? `<img class="pic" src="${it.img}" alt="">` : ""}<div class="q">${esc(it.w)} ${sayBtn(it.w)}</div><p class="tr" style="font-size:19px">${esc(it.tr[L])}</p><div class="fb">${exampleHTML(it, Object.assign({}, p, { l1: "always" }), "ex")}</div><div class="row" style="margin-top:10px"><button class="main" id="nx">${U.next}</button></div></div>`;
    say(it.w); await new Promise(r => $("#nx").onclick = r);
  }
  const r = await runDeck(host, shuffle(list).map(k => makeCard(pickType(word(k), p, "rec", null), word(k), p)), p, (c, ok) => { if (c.k) learnNew(c.k, ok, t.id) });
  const xp = Math.round(r.ok * D.st.xp.chest * D.st.diff.find(d => d.key === E.dk).xp); P.xp += xp; badge("chest", L === "uk" ? "Відкрита скриня" : "Открытый сундук"); save();
  E.plan.chest = E.plan.chest.slice(12);
  host.innerHTML = `<div class="box"><h2>🧰 +${xp} ${U.xp}</h2><p>${r.ok}/${r.all} ${U.score}</p><a class="btn main big" href="${nextAction().href}">${U.next} ▶</a></div>`;
}

/* ---------- Повторение отдельно, праздник, экзамен ---------- */
async function viewReview(kind, n) {
  app().innerHTML = head() + `<p class="mute">…</p>`;
  const curT = D.byId[Math.min(750, P.cur)] || D.byId[1], t = await topic(curT.ready ? curT.id : 1).catch(() => null);
  await ensureDueLoaded(Object.keys(P.srs));
  const p = prof(t || curT, diffOf(curT.id)); let keys, title, need = 0;
  if (kind === "fest") { title = U.fest(n); keys = shuffle(Object.keys(P.srs).filter(k => word(k) && P.srs[k].t > n - 25 && P.srs[k].t <= n)).slice(0, 30) }
  else if (kind === "exam") { title = U.exam(n); need = 80; keys = shuffle(Object.keys(P.srs).filter(k => word(k) && Math.ceil(P.srs[k].t / 75) === n)).slice(0, 40) }
  else { title = U.review; keys = reviewSet(t, p, [], Math.max(p.review, 20)) }
  if (!keys.length) { app().innerHTML = head() + `<div class="box"><h2>${title}</h2><p>${U.noDue}</p><a class="btn main big" href="#/">${U.home}</a></div>`; return }
  app().innerHTML = head() + `<h2>${title}</h2><div id="host"></div>`;
  const cards = kind === "exam" ? keys.map(k => makeCard(pickType(word(k), p, "hard", null), word(k), p)) : reviewCards(keys, p);
  const r = await runDeck($("#host"), cards, p, (c, ok) => { if (c.k) { grade(c.k, ok); if (ok) P.hw = P.hw.filter(x => x !== c.k) } });
  const pc = Math.round(r.ok * 100 / r.all), xp = r.ok * D.st.xp.review; P.xp += xp; streakUpd();
  let msg = "";
  if (kind === "fest") { P.t["f" + n] = { s: pc, at: Date.now() }; badge("f" + n, title.split(":")[0] + " " + n) }
  if (kind === "exam") { if (pc >= need) { P.t["x" + n] = { s: pc, at: Date.now() }; badge("x" + n, U.exam(n)); msg = U.examPass } else msg = U.examFail }
  P.log.push({ id: kind || "review", name: title, at: Date.now(), s: pc, ok: r.ok, all: r.all, bad: r.bad, nw: 0 }); P.log = P.log.slice(-200);
  checkBadges(); save();
  $("#host").innerHTML = `<div class="box"><h2>${U.reviewDone}</h2><div class="stat"><div><b>${pc}%</b>${U.score}</div><div><b>+${xp}</b>${U.xp}</div></div>${msg ? `<p><b>${msg}</b></p>` : ""}${r.bad.length ? `<p class="mute">${U.wrong} ${r.bad.map(esc).join(", ")}</p>` : ""}
   <a class="btn main big" href="${nextAction().href}">${U.next} ▶</a></div>`;
}

/* ---------- Дневник и профиль ---------- */
function viewDiary() {
  app().innerHTML = head() + `<h1>📔 ${U.diary}</h1>` + (P.diary.length ? `<ul class="list">${P.diary.map(d => `<li><small class="mute">${new Date(d.at).toLocaleDateString()} · ${U.topic} ${d.id} · ${d.s}%${d.d && d.d !== "course" ? " " + U.diffShort[d.d] : ""}</small><div><b>${esc((D.byId[d.id] || {}).name || "")}</b></div>${d.txt ? `<div>${esc(d.txt)}</div>` : ""}<small class="mute">${(d.nw || []).map(esc).join(" · ")}</small></li>`).join("")}</ul>` : `<p class="mute">${U.diaryEmpty}</p>`);
}
function viewMe() {
  const s = Object.values(P.srs), done = Object.values(P.t).filter(r => r.st === "done").length;
  const fr = Object.entries(P.fr).sort((a, b) => b[1] - a[1]).slice(0, 12);
  app().innerHTML = head() + `<h1>👤 ${esc(P.name)}</h1><div class="stat"><div><b>${done}</b>${U.topics}</div><div><b>${s.filter(x => x.b >= 3).length}</b>${U.learned}</div><div><b>${s.length}</b>${U.inSrs}</div><div><b>${P.streak}</b>${U.streak}</div><div><b>${P.xp}</b>${U.xp}</div></div>
  ${fr.length ? `<h2>${U.friends}</h2><div>${fr.map(([k, n]) => `<div class="row" style="margin:4px 0"><span style="width:150px">${esc(chr(k)[L])}</span><div class="bar" style="flex:1"><i style="width:${Math.min(100, n * 5)}%"></i></div><small>${n}</small></div>`).join("")}</div>` : ""}
  ${P.badges.length ? `<h2>${U.badges}</h2><div>${P.badges.map(b => `<span class="badge">🏅 ${esc(b.txt)}</span>`).join("")}</div>` : ""}
  <h2>${U.hw}</h2><p class="mute">${U.hwTxt}</p><textarea id="hwt"></textarea><div class="row" style="margin-top:6px"><button id="hwb">${U.hwBtn}</button></div>
  <h2>${U.backup}</h2><div class="row"><button id="exp">💾 ${U.exp}</button><label class="btn">📂 ${U.imp}<input type="file" id="imp" accept=".json" hidden></label></div>
  <h2>⚙️</h2><div class="row"><a class="btn" href="#/hero">${U.switchHero}</a><button id="lang">${L === "uk" ? "Русский" : "Українська"}</button><button id="usr">${U.switchUser}</button><button id="del">${U.del}</button></div>
  <p class="mute" style="margin-top:20px"><a href="../">Sprich Deutsch · домашні завдання</a></p>`;
  $("#hwb").onclick = async () => { const n = await importHW($("#hwt").value); toast(U.hwOk(n)) };
  $("#exp").onclick = () => { const b = new Blob([JSON.stringify(P)], { type: "application/json" }), a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = `wortreise_${P.name.replace(/[^\p{L}\p{N}]+/gu, "_")}_${new Date().toISOString().slice(0, 10)}.json`; a.click(); P.lastExport = Date.now(); save() };
  $("#imp").onchange = e => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { try { const p = JSON.parse(r.result); if (!p.name || !p.srs) throw 0; const ps = profiles(); if (!ps.includes(p.name)) { ps.push(p.name); saveProfiles(ps) } useProfile(p); save(); toast("✓"); route() } catch (x) { toast("✗ JSON") } }; r.readAsText(f) };
  $("#lang").onclick = () => { P.l1 = L === "uk" ? "ru" : "uk"; useProfile(P); save(); viewMe() };
  $("#usr").onclick = () => { location.hash = "#/users" };
  $("#del").onclick = () => { if (!confirm(U.delQ)) return; localStorage.removeItem(PK(P.name)); saveProfiles(profiles().filter(n => n !== P.name)); localStorage.removeItem("wr_cur"); P = null; location.hash = "#/"; route() };
}
async function importWords(ws) {
  if (!D.index) D.index = await getJSON("data/index.json");
  let n = 0;
  for (const w of ws) { const k = normW(decodeURIComponent(w)); const tid = D.index[k]; if (!tid || !D.byId[tid] || !D.byId[tid].ready) continue; const s = P.srs[k] || (P.srs[k] = { t: tid, b: 1, d: 0, e: -99, n: 0, f: 0 }); s.b = 1; s.d = 0; s.e = -99; if (!P.hw.includes(k)) P.hw.push(k); n++ }
  save(); return n;
}
function importHW(txt) {
  const ws = []; String(txt).split(/\n/).forEach(l => { const m = l.match(/(Слова (?:разминки с ошибкой|розминки з помилкою|на повторення|на повторение))\s*:\s*(.+)$/i); if (m && m[2].trim() !== "—") ws.push(...m[2].split(",").map(x => x.trim()).filter(Boolean)) });
  return importWords(ws);
}

/* ---------- Регистрация: заявка → одобрение преподавателем (письмо) → доступ ---------- */
function jsonp(u) {
  return new Promise((ok, no) => {
    const cb = "cb" + Math.random().toString(36).slice(2), s = document.createElement("script");
    const tm = setTimeout(() => { delete window[cb]; s.remove(); no(new Error("timeout")) }, 10000);
    window[cb] = r => { clearTimeout(tm); delete window[cb]; s.remove(); ok(r) };
    s.onerror = () => { clearTimeout(tm); delete window[cb]; s.remove(); no(new Error("net")) };
    s.src = u + (u.includes("?") ? "&" : "?") + "callback=" + cb; document.head.appendChild(s);
  });
}
const api = q => jsonp(CFG.endpoint + "?" + q);
function pending() { try { return JSON.parse(localStorage.getItem("wr_pending") || "null") } catch (e) { return null } }
function setPending(x) { try { x ? localStorage.setItem("wr_pending", JSON.stringify(x)) : localStorage.removeItem("wr_pending") } catch (e) { } }
const rid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 10);
function langBtns(l1) {
  return `<div class="seg">${[["uk", "Українська"], ["ru", "Русский"]].map(([k, n]) => `<button type="button" data-l="${k}" class="${k === l1 ? "on" : ""}">${n}</button>`).join("")}</div>`;
}
function bindLang(cb) { $$("[data-l]").forEach(b => b.onclick = () => { $$("[data-l]").forEach(x => x.classList.toggle("on", x === b)); cb(b.dataset.l) }) }
function welcome() { return `<div class="welcome"><div class="logo">Wort<b>reise</b></div><p class="mute">${UI.uk.hello}<br>${UI.ru.hello}</p></div>` }

function viewRegister(name, l1) {
  l1 = l1 || L || "uk"; const T = () => UI[l1];
  const draw = () => {
    app().innerHTML = welcome() + `<div class="box form"><h1>${T().regT}</h1><p class="mute">${T().regSub}</p>
     <label>${T().who}<input type="text" id="nm" maxlength="40" autocomplete="name" value="${esc(name || "")}"></label>
     <label>${T().email}<input type="email" id="em" maxlength="80" autocomplete="email" inputmode="email"></label>
     <p class="lbl">${T().lang}</p>${langBtns(l1)}
     <p id="msg" class="msg"></p><button class="main big" id="go">${T().regBtn}</button>
     <p class="links"><a href="#/login">${T().haveAcc}</a>${profiles().length ? ` · <a href="#/users">${T().profiles}</a>` : ""}</p></div>`;
    bindLang(k => { name = $("#nm").value; const em = $("#em").value; l1 = k; draw(); $("#em").value = em });
    $("#go").onclick = async () => {
      const n = $("#nm").value.trim(), em = $("#em").value.trim(), msg = $("#msg");
      if (!n) { msg.textContent = T().nameNeed; return }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) { msg.textContent = T().emailBad; return }
      const r = { rid: rid(), name: n, email: em, l1, at: Date.now() };
      $("#go").disabled = true; msg.textContent = T().sendingReg;
      try { await fetch(CFG.endpoint, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify({ token: CFG.token, type: "register", rid: r.rid, name: n, email: em, l1 }) }) }
      catch (e) { $("#go").disabled = false; msg.textContent = T().net; return }
      for (let i = 0; i < 6; i++) {
        await new Promise(z => setTimeout(z, i ? 2000 : 1200));
        try {
          const x = await api("reg=" + encodeURIComponent(r.rid));
          if (x.v !== 6) { $("#go").disabled = false; msg.textContent = T().oldServer; return }
          if (x.status !== "unknown") { setPending(r); location.hash = "#/"; route(); return }
        } catch (e) { }
      }
      $("#go").disabled = false; msg.textContent = T().net;
    };
  };
  draw();
}
function viewLogin() {
  let l1 = L || "uk"; const T = () => UI[l1];
  const draw = () => {
    app().innerHTML = welcome() + `<div class="box form"><h1>${T().loginT}</h1><p class="mute">${T().loginSub}</p>
     <label>${T().who}<input type="text" id="nm" maxlength="40" autocomplete="name"></label>
     <label>${T().email}<input type="email" id="em" maxlength="80" autocomplete="email" inputmode="email"></label>
     <p id="msg" class="msg"></p><button class="main big" id="go">${T().loginBtn}</button>
     <p class="links"><a href="#/new">${T().regT}</a></p></div>`;
    $("#go").onclick = async () => {
      const n = $("#nm").value.trim(), em = $("#em").value.trim(), msg = $("#msg");
      if (!n || !em) { msg.textContent = T().nameNeed; return }
      $("#go").disabled = true; msg.textContent = "…";
      let x; try { x = await api("login=" + encodeURIComponent(em) + "&name=" + encodeURIComponent(n)) } catch (e) { $("#go").disabled = false; msg.textContent = T().net; return }
      $("#go").disabled = false;
      if (x.v !== 6) { msg.textContent = T().oldServer; return }
      if (x.status === "approved") return grant({ rid: x.rid, name: n, email: em, l1: x.l1 === "ru" ? "ru" : "uk" });
      if (x.status === "pending") { setPending({ rid: x.rid, name: n, email: em, l1: x.l1 === "ru" ? "ru" : "uk", at: Date.now() }); location.hash = "#/"; return route() }
      msg.textContent = x.status === "rejected" ? T().rejected : T().notFound;
    };
  };
  draw();
}
function grant(r) {
  const ps = profiles(); let p = load(r.name);
  if (!p) { p = newProfile(r.name, r.l1); ps.push(r.name); saveProfiles(ps) }
  p.reg = { rid: r.rid, email: r.email, status: "approved", at: Date.now() };
  useProfile(p); save(); setPending(null); location.hash = "#/hero"; route();
}
async function viewWaiting() {
  const r = pending(), T = UI[r.l1 || "uk"];
  app().innerHTML = welcome() + `<div class="box form center"><div class="big-ico">✉️</div><h1>${T.waitT}</h1><p>${esc(r.name)} · ${esc(r.email)}</p>
   <p class="mute">${T.waitTxt}</p><p id="msg" class="msg"></p><button class="main big" id="go">${T.check2}</button>
   <p class="links"><a href="#" id="chg">${T.change}</a></p></div>`;
  const check = async quiet => {
    const msg = $("#msg"); if (!quiet) msg.textContent = "…";
    try {
      const x = await api("reg=" + encodeURIComponent(r.rid));
      if (x.status === "approved") return grant(r);
      msg.textContent = x.status === "rejected" ? T.rejected : quiet ? "" : T.notYet;
    } catch (e) { if (!quiet) msg.textContent = T.net }
  };
  $("#go").onclick = () => check(false);
  $("#chg").onclick = e => { e.preventDefault(); setPending(null); location.hash = "#/new"; route() };
  check(true);
}
function viewBlocked() {
  app().innerHTML = welcome() + `<div class="box form center"><h1>Wortreise</h1><p>${U.rejected}</p><p class="links"><a href="#/users">${U.switchUser}</a></p></div>`;
}
let rechecked = false;
async function recheck() {   // раз за сеанс: доступ могли отозвать
  if (rechecked || !P || !P.reg || !P.reg.rid) return; rechecked = true;
  try { const x = await api("reg=" + encodeURIComponent(P.reg.rid)); if (x.v === 6 && x.status === "rejected") { P.reg.status = "rejected"; save(); route() } } catch (e) { }
}

/* ---------- Главная: одна кнопка ---------- */
function nextAction() {
  const due = dueList().length, cur = D.byId[Math.min(750, P.cur)];
  if (due > 60) return { href: "#/review", label: U.goReview, sub: U.due(due), ico: "🔁" };
  if (cur && cur.ready) return { href: "#/t/" + cur.id, label: U.go, sub: `${U.topic} ${cur.id} · ${cur.name}`, ico: "▶" };
  if (due > 0) return { href: "#/review", label: U.goReview, sub: U.due(due), ico: "🔁" };
  return { href: "#/", label: U.goSoon, sub: "", ico: "⏳", off: true };
}
function viewHome() {
  const h = hero(), c = chr(h.key), a = nextAction(), done = Object.values(P.t).filter(r => r.st === "done").length;
  const learned = Object.values(P.srs).filter(x => x.b >= 3).length, due = dueList().length, pc = Math.round(done * 100 / 750);
  app().innerHTML = head() + `<div class="homecard"><div class="avatar">${h.emoji}</div><div><div class="hname">${esc(c[L])}</div><small class="mute">${esc(h.lineName[L])} · ${esc(h.place[L])}</small></div></div>
   <a class="btn main huge ${a.off ? "off" : ""}" href="${a.href}"><span class="ico">${a.ico}</span><span><b>${a.label}</b>${a.sub ? `<small>${esc(a.sub)}</small>` : ""}</span></a>
   <div class="progress"><div class="bar"><i style="width:${Math.max(2, pc)}%"></i></div><small class="mute">${done} ${U.ofAll} · ${learned} ${U.lvlWords}</small></div>
   <nav class="quick"><a href="#/map">🗺️<span>${U.map}</span></a><a href="#/review">🔁<span>${U.review}${due ? ` (${due})` : ""}</span></a><a href="#/diary">📔<span>${U.diary}</span></a><a href="#/me">👤<span>${U.me}</span></a></nav>`;
  if (Date.now() - (P.lastExport || 0) > 7 * 864e5 && Object.keys(P.srs).length > 30) { P.lastExport = Date.now() - 5 * 864e5; save(); toast(U.remind) }
}

boot().catch(e => { app().innerHTML = `<div class="box"><h2>⚠️</h2><p>${esc(e.message)}</p></div>` });
