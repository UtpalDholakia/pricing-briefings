/* Decisions page: click choices, then send them all to Claude as one GitHub issue (AGENTS.md section 14).
   Choices are kept in this browser until sent, so nothing is lost if the page is closed. */
(function () {
  var REPO = "UtpalDholakia/pricing-briefings";
  var KEY = "pb-decisions-v1";
  var SENT = "pb-decisions-sent-v1";
  var state = load(KEY) || {};
  var sent = load(SENT) || {};

  function load(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function id(box) { return box.dataset.kind + ":" + box.dataset.ref; }
  function boxes() { return Array.prototype.slice.call(document.querySelectorAll(".decide")); }

  function paint(box) {
    var s = state[id(box)];
    box.querySelectorAll(".dz").forEach(function (b) { b.classList.toggle("on", !!s && s.v === b.dataset.v); });
    var note = box.querySelector(".dz-note");
    if (s && s.note) { note.hidden = false; note.value = s.note; }
    var needs = s && box.querySelector('.dz.on[data-note="required"]') && !(s.note || "").trim();
    note.classList.toggle("need", !!needs);
    if (needs) { note.hidden = false; note.placeholder = s.v === "Published" ? "Paste the Substack URL" : "Say what to change (required)"; }
    var row = box.closest("tr");
    if (row) {
      row.classList.toggle("dz-chosen", !!s);
      row.classList.toggle("dz-sent", !s && !!sent[id(box)]);
    }
  }

  function bar() {
    var keys = Object.keys(state);
    var missing = keys.filter(function (k) {
      var b = document.querySelector('.decide[data-kind="' + k.split(":")[0] + '"][data-ref="' + k.slice(k.indexOf(":") + 1) + '"]');
      return b && b.querySelector('.dz.on[data-note="required"]') && !(state[k].note || "").trim();
    });
    var el = document.getElementById("dz-bar");
    el.hidden = keys.length === 0;
    document.getElementById("dz-count").textContent = keys.length + (keys.length === 1 ? " decision" : " decisions") + " chosen";
    document.getElementById("dz-warn").textContent = missing.length ? missing.length + " still need a note" : "";
    document.getElementById("dz-send").disabled = missing.length > 0;
  }

  function choose(box, v) {
    var k = id(box);
    if (state[k] && state[k].v === v) { delete state[k]; }
    else { state[k] = { v: v, note: (state[k] && state[k].note) || "", title: box.dataset.title }; }
    save(KEY, state); paint(box); bar();
    var on = box.querySelector(".dz.on");
    if (on && on.dataset.note === "required") box.querySelector(".dz-note").focus();
  }

  function body(compact) {
    var keys = Object.keys(state);
    var today = new Date().toISOString().slice(0, 10);
    var lines = ["**" + keys.length + " decisions** from the Decisions page, " + today + ". Claude applies them in its next daily run and closes this issue.", ""];
    if (!compact) {
      keys.forEach(function (k) {
        var s = state[k];
        lines.push("- **" + s.v + "**: " + (s.title || k) + (s.note ? " (note: " + s.note + ")" : ""));
      });
      lines.push("");
    }
    lines.push("```decisions");
    keys.forEach(function (k) {
      var s = state[k];
      lines.push([k.split(":")[0], k.slice(k.indexOf(":") + 1), s.v, (s.note || "").replace(/[|\n]/g, " ")].join(" | ").replace(/ \| $/, ""));
    });
    lines.push("```");
    return lines.join("\n");
  }

  function copy(text) {
    try { if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(text); return true; } } catch (e) {}
    try {
      var t = document.createElement("textarea"); t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select(); var ok = document.execCommand("copy"); document.body.removeChild(t); return ok;
    } catch (e) { return false; }
  }

  function showText(text) {
    var box = document.getElementById("dz-text");
    box.hidden = false; box.querySelector("textarea").value = text; box.querySelector("textarea").select();
  }

  function send() {
    var n = Object.keys(state).length;
    var title = "Decisions " + new Date().toISOString().slice(0, 10) + " (" + n + ")";
    var url = "https://github.com/" + REPO + "/issues/new?labels=decisions&title=" + encodeURIComponent(title) + "&body=";
    var full = url + encodeURIComponent(body(false));
    if (full.length > 7800) full = url + encodeURIComponent(body(true));   // drop the readable list, keep the decisions
    if (full.length > 7800) {                                                // still too long for one link: copy and paste
      var text = body(true);
      var copied = copy(text);
      full = url + encodeURIComponent("Paste the decisions here (they were copied when you clicked Send).");
      showText(text);
      alert((copied ? "Your decisions were copied. " : "Copy the decisions from the box on the page. ") +
            "On the GitHub page, paste them into the description box, then click Submit.");
    }
    window.open(full, "_blank", "noopener");
    Object.keys(state).forEach(function (k) { sent[k] = new Date().toISOString().slice(0, 10); });
    save(SENT, sent);
    state = {}; save(KEY, state);
    boxes().forEach(paint); bar();
    document.getElementById("dz-done").hidden = false;
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest(".dz");
    if (b) { choose(b.closest(".decide"), b.dataset.v); return; }
    var t = e.target.closest(".dz-note-toggle");
    if (t) { var n = t.parentNode.querySelector(".dz-note"); n.hidden = !n.hidden; if (!n.hidden) n.focus(); return; }
    var all = e.target.closest(".dz-accept-all");
    if (all) {
      all.closest("section").querySelectorAll(".decide").forEach(function (box) {
        var star = box.querySelector(".dz.star");
        if (star && !state[id(box)] && star.dataset.note !== "required") {
          state[id(box)] = { v: star.dataset.v, note: "", title: box.dataset.title };
          paint(box);
        }
      });
      save(KEY, state); bar(); return;
    }
    if (e.target.id === "dz-send") send();
    if (e.target.id === "dz-copy") { var t = body(false); if (copy(t)) { e.target.textContent = "Copied"; setTimeout(function () { e.target.textContent = "Copy as text"; }, 1500); } else { showText(t); } }
    if (e.target.id === "dz-clear" && confirm("Clear all the choices you have made on this page?")) { state = {}; save(KEY, state); boxes().forEach(paint); bar(); }
  });
  document.addEventListener("input", function (e) {
    if (!e.target.classList.contains("dz-note")) return;
    var box = e.target.closest(".decide"), k = id(box);
    if (!state[k]) return;
    state[k].note = e.target.value; save(KEY, state);
    e.target.classList.toggle("need", !!box.querySelector('.dz.on[data-note="required"]') && !e.target.value.trim());
    bar();
  });

  boxes().forEach(paint); bar();

  // Show batches already sent and waiting for Claude (public issues; no sign-in needed).
  try {
    fetch("https://api.github.com/repos/" + REPO + "/issues?labels=decisions&state=open")
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (list) {
        if (!list.length) return;
        var el = document.getElementById("dz-pending");
        el.hidden = false;
        el.innerHTML = list.length + (list.length === 1 ? " batch" : " batches") + " of decisions sent and waiting for Claude's next run: " +
          list.map(function (i) { return '<a href="' + i.html_url + '">' + i.title.replace(/</g, "&lt;") + "</a>"; }).join(", ") + ".";
      })
      .catch(function () {});
  } catch (e) {}
})();
