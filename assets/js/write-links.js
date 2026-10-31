// One-click "Write" links.
// A link like <a class="write-link" data-role="research" data-task="critique" data-paper="...">
// opens GitHub's editor with a new post already named, dated and filled from templates/<role>.md.
// <a class="profile-link"> does the same for a profile in _people/.
// Without data-paper, the paper of the upcoming meeting (from _data/schedule.yml) is used.
(function () {
  const cfg = window.AAR_WRITE;
  if (!cfg) return;
  // A week's class day: course_start (the Sunday of week first_week_number) plus 7 days a week plus class_day.
  function classDate(week) {
    const [y, m, d] = cfg.courseStart.split("-").map(Number);
    return new Date(y, m - 1, d + 7 * (week - (cfg.firstWeek || 0)) + (cfg.classDay || 0));
  }

  // The upcoming meeting's paper: the first week whose class day is today or later
  // (so from the day after class it already points at the next week). After the last class: the last paper.
  function currentPaper() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    let pick = null;
    for (const w of cfg.schedule) {
      if (!w.paper) continue;
      pick = w.paper;
      if (classDate(w.week) >= today) return w.paper;
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
