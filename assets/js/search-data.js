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
        },{id: "post-what-makes-a-chain-of-thought-easy-to-learn",
        
          title: "What Makes a Chain of Thought Easy to Learn?",
        
        description: "How teacher-generated reasoning can help smaller models learn, and why the structure of a reasoning trace might matter.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/what-makes-a-chain-of-thought-easy-to-learn/";
          
        },
      },{id: "post-the-points-that-matter-about-matryoshka-suites",
        
          title: "The points that matter about Matryoshka suites.",
        
        description: "A quick recap on what you need to remember from this paper instead of re-reading everything.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/week1-The-points-that-matter/";
          
        },
      },{id: "post-rewriting-the-abstract",
        
          title: "Rewriting the abstract",
        
        description: "Why should we care about language model suites ?",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/rewriting-the-abstract-matryoshka-lm-suites/";
          
        },
      },{id: "post-reimplementing-a-speculative-decoding-throughput-test-shown-in-figure-5a",
        
          title: "Reimplementing a speculative decoding throughput test, shown in Figure 5a",
        
        description: "I implemented a speculative decoding throughput performance test, running the 500M model as a draft model and the full 3B model as the verifier, examining a speedup against a baseline",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/reimplement-cross-lingual-knowledge-pretraining/";
          
        },
      },{id: "post-a-better-figure-2",
        
          title: "A better Figure 2",
        
        description: "Figure 2 uses two ternary plots to select a model architecture, but the key tradeoff between memory and computation is hidden across separate panels",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/redo-graph-figure-2/";
          
        },
      },{id: "post-three-models-in-one-a-toy-matryoshka-suite-vs-three-separate-models",
        
          title: "Three models in one: a toy Matryoshka suite vs. three separate models",
        
        description: "One nested transformer with three exits, trained once, against three separate models of matched size. The shape of the paper&#39;s result holds at toy scale.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/matryoshka-toy/";
          
        },
      },{id: "post-literature-review-of-matryoshka-language-model-suites",
        
          title: "Literature review of Matryoshka Language Model Suites",
        
        description: "Ideas behind Matryoshka LM Suites and what it adds",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/literature-matryoshka-lm-suites/";
          
        },
      },{id: "post-a-new-way-of-speculative-decoding-and-on-policy-distillation",
        
          title: "A new way of speculative decoding and on policy distillation",
        
        description: "2 papers that expand on ideas used in the matryoshka suits paper.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/hidden-gems-matryoshka-lm-suites/";
          
        },
      },{id: "post-follow-ups-of-matryoshka-language-model-suites",
        
          title: "Follow-ups of Matryoshka Language Model Suites",
        
        description: "The nested suite was built for efficiency, but its shared backbone makes it a ready-made interpretability testbed.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/follow-ups-matryoshka-lm-suites/";
          
        },
      },{id: "post-copyediting-section-1-introduction-of-matryoshka-language-model-suites",
        
          title: "Copyediting Section 1 (Introduction) of Matryoshka Language Model Suites",
        
        description: "Removing repetition.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/copyedit-introduction-matryoshka-lm-suites/";
          
        },
      },{id: "post-lt-critique-literature-review-follow-ups-gt-of-lt-paper-gt",
        
          title: "&lt;Critique / literature review / follow-ups&gt; of &lt;paper&gt;",
        
        description: "One sentence summary of your take.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/contact-authors-cross-lingual-knowledge-pretraining/";
          
        },
      },{id: "post-the-minds-behind-matryoshka",
        
          title: "The minds behind Matryoshka",
        
        description: "The paper closely aligns with Nathan Godey’s research on efficient language model design and complements Yoav Artzi’s broader work on advancing language modeling methods.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/authors-The-minds-behind-Matryoshka/";
          
        },
      },{id: "post-literature-review-matryoshka-lm-suites",
        
          title: "Literature Review: Matryoshka LM Suites",
        
        description: "Contextualizing Matryoshka LM Suites within speculative decoding, knowledge distillation, and nested/elastic transformer architectures.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/Literature-Review/";
          
        },
      },{id: "post-visualizing-models",
        
          title: "Visualizing 🪆 Models",
        
        description: "Diagrams of the nested model suite and its junction mechanism.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/visualizing-models/";
          
        },
      },{id: "post-does-sharing-kv-cache-ruin-alignment-and-why-do-we-apply-forward-kl-divergence",
        
          title: "Does sharing KV cache ruin alignment and why do we apply forward KL-Divergence...",
        
        description: "2 papers similar to parts of the paper",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/scouting-recent-non-trending/";
          
        },
      },{id: "post-visualizing-the-core-idea-of-matryoshka-lm-suites",
        
          title: "Visualizing the core idea of Matryoshka LM Suites",
        
        description: "One figure that shows how three separate models become one nested model, and where the savings come from.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/key-visual-matryoshka-lm-suites/";
          
        },
      },{id: "post-critique-of-matryoshka-language-model-suites",
        
          title: "Critique of Matryoshka Language Model Suites",
        
        description: "Clean idea to boost efficency for training model suites, should use more extensive experiments",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/critique-matryoshka-lm-suites-achi-or/";
          
        },
      },{id: "post-how-autoregressive-and-diffusion-lms-imitate-each-other-and-why-it-is-inefficient",
        
          title: "How autoregressive and diffusion LMs imitate each other, and why it is inefficient...",
        
        description: "A claim from week 1, made easier to follow with pictures: each model type can do what the other does, and what it costs to do so.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/autoregressive-vs-diffusion/";
          
        },
      },{id: "post-matryoshka-language-model-suites-in-a-thread",
        
          title: "Matryoshka Language Model Suites in a thread",
        
        description: "Social media posts for Matryoshka Language Model Suites.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/social-matryoshka-lm-suites/";
          
        },
      },{id: "post-editing-the-methods-of-lt-paper-gt",
        
          title: "Editing the methods of &lt;paper&gt;",
        
        description: "sub-models are made of blocks",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/copyedit-matryoshka-lm-suites/";
          
        },
      },{id: "post-critique-of-matryoshka-paper-ga26",
        
          title: "critique of matryoshka paper (GA26)",
        
        description: "The narative about saving on parameters is diluted by a secondary point about cheap distiliation.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/posts/2026/critique-matryoshka-lm-suites-ga26/";
          
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
            },},{id: "people-adam-gabet",
          title: 'Adam Gabet',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/adamgabet/";
            },},{id: "people-adam-gaber",
          title: 'Adam Gaber',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/adamjaber03/";
            },},{id: "people-danielle-sprinzak",
          title: 'Danielle Sprinzak',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/daniellesprinzak/";
            },},{id: "people-ido-ravid",
          title: 'Ido Ravid',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/idoravid/";
            },},{id: "people-itamar-pitz",
          title: 'Itamar (Pitz)',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/itamarfruchter/";
            },},{id: "people-matan-bar-tov",
          title: 'Matan Bar Tov',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/matanbartov/";
            },},{id: "people-nathan-adda",
          title: 'Nathan Adda',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/nathanadda/";
            },},{id: "people-nicolas",
          title: 'Nicolas',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/nicolasrw/";
            },},{id: "people-yehoshua-rothstein",
          title: 'Yehoshua Rothstein',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/shueyr/";
            },},{id: "people-tals",
          title: 'Tals',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/tals/";
            },},{id: "people-tomer-atia",
          title: 'Tomer Atia',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/tomeratia/";
            },},{id: "people-achi-or",
          title: 'Achi-Or',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/achi-or/";
            },},{id: "people-leshem-choshen",
          title: 'Leshem Choshen',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/borgr/";
            },},{id: "people-chanoch-baranes",
          title: 'Chanoch Baranes',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/chanoch1234/";
            },},{id: "people-chen-shani",
          title: 'Chen Shani',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/chenshani-droid/";
            },},{id: "people-course-team",
          title: 'Course team',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/course-team/";
            },},{id: "people-deitch",
          title: 'Deitch',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/deamir/";
            },},{id: "people-your-name",
          title: 'Your Name',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/golombi/";
            },},{id: "people-liad-bercovitch",
          title: 'Liad Bercovitch',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/liadber/";
            },},{id: "people-niv-cohen",
          title: 'Niv Cohen',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/nivcohen-ml/";
            },},{id: "people-odedorenstein",
          title: 'Odedorenstein',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/odedorenstein/";
            },},{id: "people-ohad",
          title: 'ohad',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/ohad-agadi/";
            },},{id: "people-roey-magen",
          title: 'Roey Magen',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/roey-magen/";
            },},{id: "people-shahar-avni",
          title: 'Shahar Avni',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/shachar731945/";
            },},{id: "people-shaharossy",
          title: 'Shaharossy',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/shaharossy/";
            },},{id: "people-shani-maor",
          title: 'Shani Maor',
          description: "",
          section: "People",handler: () => {
              window.location.href = "/people/shniki/";
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
