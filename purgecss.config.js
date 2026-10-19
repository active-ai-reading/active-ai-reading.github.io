module.exports = {
  content: ["_site/**/*.html", "_site/**/*.js"],
  css: ["_site/assets/css/*.css"],
  output: "_site/assets/css/",
  skippedContentGlobs: ["_site/assets/**/*.html"],
  // Course classes that may appear on no page yet (e.g. the header-problems note) must survive the purge.
  safelist: { greedy: [/^header-problems/, /^write-/, /^profile-link/, /^before-after/, /^role-/, /^post-card/, /^paper-card/, /^person-/] },
};
