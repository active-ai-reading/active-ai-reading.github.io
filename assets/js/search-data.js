// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-home",
    title: "home",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-papers",
          title: "papers",
          description: "Every paper the course has read, with everything the class wrote about it.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/papers/";
          },
        },{id: "nav-posts",
          title: "posts",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/posts/index.html";
          },
        },{id: "nav-roles",
          title: "roles",
          description: "The tasks you can take on for each paper. Pick one every week.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/roles/";
          },
        },{id: "nav-guides",
          title: "guides",
          description: "One living guide per role, written and passed on by the people who held it.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/guides/";
          },
        },{id: "nav-schedule",
          title: "schedule",
          description: "What we read each week, and who is doing what.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/schedule/";
          },
        },{id: "nav-people",
          title: "people",
          description: "Everyone writing for Active AI Reading.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/people/";
          },
        },{id: "nav-how-to-post",
          title: "how to post",
          description: "Join, add yourself, claim a task, and publish your first post in about 10 minutes.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/guide/";
          },
        },{id: "post-matryoshka-language-model-suites-in-a-thread",
        
          title: "Matryoshka Language Model Suites in a thread",
        
        description: "Social media posts for Matryoshka Language Model Suites.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/social-matryoshka-lm-suites/";
          
        },
      },{id: "post-critique-of-matryoshka-paper-ga26",
        
          title: "critique of matryoshka paper (GA26)",
        
        description: "The narative about saving on parameters is diluted by a secondary point about cheap distiliation.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/critique-matryoshka-language-model-suites/";
          
        },
      },{id: "post-week-0-in-one-page-tokens-keep-knowledge-apart",
        
          title: "Week 0 in one page: tokens keep knowledge apart",
        
        description: "The paper, what we learned, and everything the class wrote about it, in a five-minute read.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/week-1-in-one-page/";
          
        },
      },{id: "post-three-things-to-remember-and-where-the-paper-hides-them",
        
          title: "Three things to remember, and where the paper hides them",
        
        description: "The points most readers should leave with, and how the paper could make them harder to miss.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/three-things-to-remember/";
          
        },
      },{id: "post-the-paper-in-four-feeds",
        
          title: "The paper in four feeds",
        
        description: "Posts for X, Bluesky, Mastodon and LinkedIn, and why each one is written differently.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/the-paper-in-four-feeds/";
          
        },
      },{id: "post-the-core-idea-in-one-picture",
        
          title: "The core idea in one picture",
        
        description: "Same sentence, same model, different token IDs, and the knowledge stops flowing. A diagram of the three setups.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/the-core-idea-in-one-picture/";
          
        },
      },{id: "post-rewriting-the-abstract-lead-with-the-surprise",
        
          title: "Rewriting the abstract: lead with the surprise",
        
        description: "The paper&#39;s most striking result is buried in sentence six. Here is a version that starts with it.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/rewriting-the-abstract/";
          
        },
      },{id: "post-reimplementing-cleq-what-does-12-6-actually-mean",
        
          title: "Reimplementing CLeq: what does 12.6% actually mean?",
        
        description: "I simulated the paper&#39;s measurement with a known amount of transfer. The metric is right at 0% and 100%, and generous in between.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/reimplementing-cleq/";
          
        },
      },{id: "post-where-this-paper-comes-from-a-literature-map",
        
          title: "Where this paper comes from: a literature map",
        
        description: "The four lines of work it builds on, and the one it argues with.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/literature-map/";
          
        },
      },{id: "post-five-follow-ups-worth-doing",
        
          title: "Five follow-ups worth doing",
        
        description: "Concrete next experiments, from a weekend project to a thesis chapter, and why each is worth the time.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/follow-ups-worth-doing/";
          
        },
      },{id: "post-fictive-facts-how-to-know-exactly-what-a-model-saw",
        
          title: "Fictive facts: how to know exactly what a model saw",
        
        description: "A five-minute lesson on the trick that makes controlled knowledge experiments in pretraining possible.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/fictive-facts/";
          
        },
      },{id: "post-critique-a-clean-diagnosis-a-partial-cure",
        
          title: "Critique: a clean diagnosis, a partial cure",
        
        description: "Strengths, weaknesses, what would have made it stronger, and a verdict.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/critique/";
          
        },
      },{id: "post-a-better-figure-2-the-threshold-the-bar-chart-hides",
        
          title: "A better Figure 2: the threshold the bar chart hides",
        
        description: "The paper&#39;s key soft-mapping result is a curve with a cliff. Drawn as bars, the cliff disappears.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/a-better-figure-2/";
          
        },
      },{id: "guides-the-chill-guide",
          title: 'The chill guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/chill/";
            },},{id: "guides-the-coding-guide",
          title: 'The coding guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/coding/";
            },},{id: "guides-the-communication-guide",
          title: 'The communication guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/communication/";
            },},{id: "guides-the-learning-to-learn-guide",
          title: 'The learning-to-learn guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/learning/";
            },},{id: "guides-the-research-skills-guide",
          title: 'The research skills guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/research/";
            },},{id: "guides-the-paper-scouting-guide",
          title: 'The paper scouting guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/scouting/";
            },},{id: "guides-the-visualization-guide",
          title: 'The visualization guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/visualization/";
            },},{id: "guides-the-writing-guide",
          title: 'The writing guide',
          description: "",
          section: "Guides",handler: () => {
              window.location.href = "/guides/writing/";
            },},{id: "papers-why-pretraining-fails-to-share-cross-lingual-knowledge",
          title: 'Why Pretraining Fails to Share Cross-Lingual Knowledge',
          description: "",
          section: "Papers",handler: () => {
              window.location.href = "/papers/cross-lingual-knowledge-pretraining/";
            },},{id: "papers-matryoshka-language-model-suites",
          title: 'Matryoshka Language Model Suites',
          description: "",
          section: "Papers",handler: () => {
              window.location.href = "/papers/matryoshka-lm-suites/";
            },},{id: "papers-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-approach",
          title: 'Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach',
          description: "",
          section: "Papers",handler: () => {
              window.location.href = "/papers/recurrent-depth-latent-reasoning/";
            },},{id: "people-adam-gaber",
          title: 'Adam Gaber',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/adamjaber03/";
            },},{id: "people-matan-bar-tov",
          title: 'Matan Bar Tov',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/matanbartov/";
            },},{id: "people-yehoshua",
          title: 'Yehoshua',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/shueyr/";
            },},{id: "people-leshem-choshen",
          title: 'Leshem Choshen',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/borgr/";
            },},{id: "people-course-team",
          title: 'Course team',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/course-team/";
            },},{id: "people-ohad",
          title: 'ohad',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/ohad-agadi/";
            },},{id: "showcase-a-post-with-formatting-and-links",
          title: 'a post with formatting and links',
          description: "march &amp; april, looking forward to summer",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/formatting-and-links/";
            },},{id: "showcase-a-post-with-images",
          title: 'a post with images',
          description: "this is what included images could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/images/";
            },},{id: "showcase-a-post-with-code",
          title: 'a post with code',
          description: "an example of a blog post with some code",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/code/";
            },},{id: "showcase-a-post-with-math",
          title: 'a post with math',
          description: "an example of a blog post with some math",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/math/";
            },},{id: "showcase-a-post-with-disqus-comments",
          title: 'a post with disqus comments',
          description: "an example of a blog post with disqus comments",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/disqus-comments/";
            },},{id: "showcase-a-post-with-twitter",
          title: 'a post with twitter',
          description: "an example of a blog post with twitter",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/twitter/";
            },},{id: "showcase-a-distill-style-blog-post",
          title: 'a distill-style blog post',
          description: "an example of a distill-style blog post and main elements",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/distill/";
            },},{id: "showcase-a-post-with-diagrams",
          title: 'a post with diagrams',
          description: "an example of a blog post with diagrams",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/diagrams/";
            },},{id: "showcase-a-post-with-redirect",
          title: 'a post with redirect',
          description: "you can also redirect to assets like pdf",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/redirect/";
            },},{id: "showcase-a-post-with-giscus-comments",
          title: 'a post with giscus comments',
          description: "an example of a blog post with giscus comments",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/giscus-comments/";
            },},{id: "showcase-a-post-with-table-of-contents",
          title: 'a post with table of contents',
          description: "an example of a blog post with table of contents",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/table-of-contents/";
            },},{id: "showcase-displaying-beautiful-tables-with-bootstrap-tables",
          title: 'displaying beautiful tables with Bootstrap Tables',
          description: "an example of how to use Bootstrap Tables",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/tables/";
            },},{id: "showcase-a-post-with-videos",
          title: 'a post with videos',
          description: "this is what included videos could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/videos/";
            },},{id: "showcase-a-post-with-audios",
          title: 'a post with audios',
          description: "this is what included audios could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/audios/";
            },},{id: "showcase-a-post-with-table-of-contents-on-a-sidebar",
          title: 'a post with table of contents on a sidebar',
          description: "an example of a blog post with table of contents on a sidebar",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/sidebar-table-of-contents/";
            },},{id: "showcase-a-post-with-custom-blockquotes",
          title: 'a post with custom blockquotes',
          description: "an example of a blog post with custom blockquotes",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/custom-blockquotes/";
            },},{id: "showcase-a-post-with-jupyter-notebook",
          title: 'a post with jupyter notebook',
          description: "an example of a blog post with jupyter notebook",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/jupyter-notebook/";
            },},{id: "showcase-a-post-with-bibliography",
          title: 'a post with bibliography',
          description: "an example of a blog post with bibliography",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/post-bibliography/";
            },},{id: "showcase-a-post-with-tikzjax",
          title: 'a post with TikZJax',
          description: "this is what included TikZ code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/tikzjax/";
            },},{id: "showcase-a-post-with-chart-js",
          title: 'a post with chart.js',
          description: "this is what included chart.js code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/chartjs/";
            },},{id: "showcase-a-post-with-echarts",
          title: 'a post with echarts',
          description: "this is what included echarts code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/echarts/";
            },},{id: "showcase-a-post-with-geojson",
          title: 'a post with geojson',
          description: "this is what included geojson code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/geojson-map/";
            },},{id: "showcase-a-post-with-vega-lite",
          title: 'a post with vega lite',
          description: "this is what included vega lite code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/vega-lite/";
            },},{id: "showcase-a-post-with-advanced-image-components",
          title: 'a post with advanced image components',
          description: "this is what advanced image components could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/advanced-images/";
            },},{id: "showcase-a-post-with-code-diff",
          title: 'a post with code diff',
          description: "this is how you can display code diffs",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/code-diff/";
            },},{id: "showcase-a-post-with-pseudo-code",
          title: 'a post with pseudo code',
          description: "this is what included pseudo code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/pseudocode/";
            },},{id: "showcase-a-post-that-can-be-cited",
          title: 'a post that can be cited',
          description: "this is what a post that can be cited looks like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/post-citation/";
            },},{id: "showcase-a-post-with-typograms",
          title: 'a post with typograms',
          description: "this is what included typograms code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/typograms/";
            },},{id: "showcase-a-post-with-tabs",
          title: 'a post with tabs',
          description: "this is what included tabs in a post could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/tabs/";
            },},{id: "showcase-a-post-with-image-galleries",
          title: 'a post with image galleries',
          description: "this is what included image galleries could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/photo-gallery/";
            },},{id: "showcase-a-post-with-plotly-js",
          title: 'a post with plotly.js',
          description: "this is what included plotly.js code could look like",
          section: "Showcase",handler: () => {
              window.location.href = "/showcase/plotly/";
            },},{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/active-ai-reading", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
