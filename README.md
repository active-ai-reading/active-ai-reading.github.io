# Active AI Reading

**The site:** https://active-ai-reading.github.io

A course where we read AI papers actively: we rewrite them, critique them, redraw their figures, rerun their code, trace their ideas and tell the world about them. This repository *is* the course blog, and **everyone in the course can change everything in it**. No approvals: save, and the site rebuilds itself in a few minutes.

## Start here (10 minutes)

1. **Join:** comment on the pinned [**Join here**](../../issues) issue. Someone already in the course will add you, so accept the email invite.
2. **Add yourself:** copy [`templates/person.md`](templates/person.md) to `_people/<your-github-username>.md` and fill it in.
3. **Take a role:** pick a task on the [roles page](https://active-ai-reading.github.io/roles/), add yourself in the sign-up sheet (Google Sheet, linked on the [schedule page](https://active-ai-reading.github.io/schedule/)), and read that role's [guide](https://active-ai-reading.github.io/guides/).
4. **Write:** copy your role's template from [`templates/`](templates/) to `_posts/YYYY-MM-DD-short-title.md`, fill in the header, write.
5. **Publish:** commit to `main`. Watch the [Actions tab](../../actions): green ✓ means it's live.

The full guide, with how to cite, add images, make charts and change the design, is on the site: **[how to post](https://active-ai-reading.github.io/guide/)**. The fastest way to learn is to open one of the [example posts](_posts/) and copy it.

## Passing it on

What one week learns, the next week inherits.

- **Handoff notes:** after class, spend 5 minutes on `handoffs/week-NN/<github-username>-<role>.md`: what you tried, what failed, one tip. Raw is fine. (Chill needs no handoff.) See [handoffs/README.md](handoffs/README.md).
- **Role guides:** each role has a living guide ([on the site](https://active-ai-reading.github.io/guides/), files in [`_guides/`](_guides/)). When you take a role, read its guide and the last handoffs for that role, move whatever is worth keeping into the guide, then do your task.
- Mid-semester we reread every guide as a newcomer would and cut it back to what actually helps.

## Where things are

| You want to... | Edit |
| --- | --- |
| Write a post | `_posts/YYYY-MM-DD-title.md` (start from `templates/`) |
| Add a paper | `_papers/<paper-id>.md` (start from `templates/paper.md`) |
| Your profile | `_people/<github-username>.md` |
| Take a role this week | the sign-up Google Sheet (linked on the schedule page) |
| The weeks and their papers (read / upcoming meeting / after that / planned) | `_data/schedule.yml` only: the schedule page and the sign-up sheet's *Papers* tab both read it |
| Role guides | `_guides/<role>.md` |
| Handoff notes | `handoffs/week-NN/<github-username>-<role>.md` |
| Add, rename or change roles and tasks | `_data/roles.yml` first, then the matching row in the sheet's *Rules* tab (its *On the site?* column shows which) |
| Add a reference | `_bibliography/references.bib` |
| Images | `assets/img/posts/<post-name>/` |
| Change the look | `_sass/_course.scss`, `_sass/_variables.scss`, `_layouts/`, `_includes/course/` |
| Site title, menu, settings, first class (`course_start`) and Sundays without class (`no_class`) | `_config.yml` |
| See every theme feature | `_showcase/` (rendered at [/showcase/](https://active-ai-reading.github.io/showcase/)) |

Editing options: the github.com web editor (press <kbd>.</kbd> on the repo page), a **Codespace** (Code → Codespaces → Create; it opens with a live site preview), or locally with `docker compose up` → http://localhost:8080.

## House rules

- Edit your own posts freely; fix typos anywhere; ask before rewriting someone else's post.
- `git pull --rebase` before `git push`. Never force-push to `main`.
- Big design changes: try them in a Codespace first and mention them in [Discussions](../../discussions).
- Everything is public and [CC BY 4.0](LICENSE-content.md). Critique the work, not the people.

---

## For instructors: one-time setup

Do this once before the course. About 15 minutes.

1. **Create a free GitHub organization** named `active-ai-reading` (github.com → your avatar → *Your organizations* → *New organization* → Free). A different name works too: then update `url` and `github_repo` in `_config.yml` and the links in this README.
2. **Create the repository** `active-ai-reading.github.io` in the organization (public), and push this folder to its `main` branch. That name gives the site the short address `https://active-ai-reading.github.io`. (Any other repo name works too: set `baseurl: /<repo-name>` in `_config.yml`.)
3. **Allow the deploy workflow to push:** repo *Settings → Actions → General → Workflow permissions → Read and write permissions*.
4. **Wait for the first build** (Actions tab, about 5 minutes). It creates a `gh-pages` branch. Then: *Settings → Pages → Build and deployment → Source: Deploy from a branch → `gh-pages` / root*.
5. **Let students add each other:**
   - Create a team `students` (org → *Teams → New team*) and give it **Admin** on the repository (repo *Settings → Collaborators and teams*).
   - Org *Settings → Member privileges*: allow **repository administrators to invite outside collaborators**; under *Repository deletion and transfer*, **turn off** members' ability to delete or transfer repositories.
   - Repo *Settings → Rules → Rulesets → New branch ruleset* for `main`: enable only **Block force pushes** and **Restrict deletions**. (No review requirements.)
   - Note: students join as repository admins (that's what lets anyone add the next person). Admins can change repo settings, so these guards protect against accidents, not against someone determined. Every change stays in the history either way.
6. **Turn on Discussions** (repo *Settings → General → Features → Discussions*).
7. **Open and pin the join issue.** Use the text in [`docs/join-issue.md`](docs/join-issue.md), then click *Pin issue*. Its link is the one link you share with the class.
8. **Optional, comments under posts:** install [giscus](https://giscus.app) on the repo, copy the `repo_id` and `category_id` it gives you into `_config.yml` → `giscus:`, and set `giscus_comments: true` in the `defaults:` for posts.
9. **Optional, a custom domain:** *Settings → Pages → Custom domain*, and update `url` in `_config.yml`.

Then add your profile (`_people/borgr.md` is a stub), check the schedule, and share the join-issue link.

### Maintenance notes

- The site is built with [al-folio](https://github.com/alshedivat/al-folio) **v0.16.3**, chosen because all its layouts and styles live in this repo (the v1 line moves them into gems), so students can edit everything. The original al-folio docs are in [`docs/al-folio/`](docs/al-folio/).
- The example posts are marked `example: true` and authored by `course-team`. Keep them as the reference for week 0, or delete them later.
- Code is MIT (from al-folio, see [LICENSE](LICENSE)); content is CC BY 4.0 (see [LICENSE-content.md](LICENSE-content.md)).
