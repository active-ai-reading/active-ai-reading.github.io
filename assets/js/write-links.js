// One-click "Write" links.
// A link like <a class="write-link" data-role="research" data-task="critique" data-paper="...">
// opens GitHub's editor with a new post already named, dated and filled from templates/<role>.md.
// <a class="profile-link"> does the same for a profile in _people/.
// Without data-paper, the paper of the current week (from _data/schedule.yml) is used.
(function () {
  const cfg = window.AAR_WRITE;
  if (!cfg) return;
  const MONTHS = { jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5, jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11 };

  function weekStart(text) {
    const m = /(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})/.exec(text || "");
    return m ? new Date(+m[3], MONTHS[m[2].toLowerCase()], +m[1]) : null;
  }

  function currentPaper() {
    const today = new Date();
    let pick = null;
    for (const w of cfg.schedule) {
      if (!w.paper) continue;
      const start = weekStart(w.date);
      if (!pick) pick = w.paper; // before the course starts: the first paper
      if (start && start <= today) pick = w.paper;
    }
    return pick || "paper-id";
  }

  function today() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  }

  async function template(name) {
    const r = await fetch(`https://raw.githubusercontent.com/${cfg.repo}/main/templates/${name}.md`);
    if (!r.ok) throw new Error("template not found");
    return r.text();
  }

  function editorUrl(path, text) {
    return `https://github.com/${cfg.repo}/new/main?filename=${encodeURIComponent(path)}&value=${encodeURIComponent(text)}`;
  }

  async function openPost(a) {
    const role = a.dataset.role;
    const task = a.dataset.task;
    const paper = a.dataset.paper || currentPaper();
    let text = await template(role);
    text = text
      .split("\n")
      .filter((l) => !/^# Copy to /.test(l))
      .join("\n")
      .replace(/^paper:.*$/m, `paper: ${paper}`)
      .replace(/^task:.*$/m, `task: ${task}`);
    location.href = editorUrl(`_posts/${today()}-${task}-${paper}.md`, text);
  }

  async function openProfile() {
    const text = (await template("person"))
      .split("\n")
      .filter((l) => !/^# (Copy this file|The filename must)/.test(l))
      .join("\n");
    location.href = editorUrl("_people/your-github-username.md", text);
  }

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.write-link, a.profile-link");
    if (!a) return;
    e.preventDefault();
    (a.classList.contains("profile-link") ? openProfile() : openPost(a)).catch(() => {
      location.href = a.href; // fall back to the templates folder
    });
  });
})();

// A <select class="write-select"> of "role/task" values drives the Write link next to it.
document.addEventListener("change", (e) => {
  const s = e.target.closest("select.write-select");
  if (!s) return;
  const a = s.parentElement.querySelector("a.write-link");
  const [role, task] = s.value.split("/");
  a.dataset.role = role;
  a.dataset.task = task;
});
