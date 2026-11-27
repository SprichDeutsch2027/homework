/* Проверка свободного ответа без ИИ: правила задания «дивана» (words/data/divan/T###.json).
   Работает в браузере (window.WRCheck) и в node (сборка прогоняет образцы ответов). */
(function (root) {
  "use strict";
  // для сравнения: строчные, умлауты → гласные, ß → ss, без апострофов и знаков
  function norm(s) {
    return String(s || "").toLowerCase().replace(/[’'`´]/g, "").replace(/ä/g, "a").replace(/ö/g, "o").replace(/ü/g, "u").replace(/ß/g, "ss")
      .replace(/[.,!?;:„“”"«»()\-–—]/g, " ").replace(/\s+/g, " ").trim();
  }
  const rx = p => new RegExp(p, "i");
  /* rule: { t: тип, need: "regex" | not: "regex" | cap: ["Wort", …] | min: n, fix, say } — по порядку; первая неудача = тип ошибки.
     opts.voice — голосовой ввод: заглавные буквы не проверяются. */
  function check(text, rules, opts) {
    opts = opts || {};
    const raw = String(text || "").trim(), n = norm(raw), words = n ? n.split(" ").length : 0;
    if (!n) return { t: "empty" };
    for (const r of rules || []) {
      if (r.t === "short") { if (words < (r.min || 2)) return { t: "short", r }; continue }
      if (r.cap) {
        if (opts.voice) continue;
        const bad = r.cap.find(w => new RegExp("(^|[^\\p{L}])" + w.toLowerCase() + "([^\\p{L}]|$)", "u").test(raw) && !new RegExp("(^|[^\\p{L}])" + w + "([^\\p{L}]|$)", "u").test(raw));
        if (bad) return { t: r.t || "cap", r, fix: bad };
        continue;
      }
      if (r.need && !rx(r.need).test(n)) return { t: r.t, r };
      if (r.not && rx(r.not).test(n)) return { t: r.t, r };
    }
    return { t: "ok" };
  }
  const api = { norm, check };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.WRCheck = api;
})(typeof window !== "undefined" ? window : this);
