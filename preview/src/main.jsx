import { useEffect, useId, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import ModuleOne from "../../course/modules/01-interactive-environments.mdx";
import ModuleTwo from "../../course/modules/02-reproducibility.mdx";
import ModuleThree from "../../course/modules/03-interactivity.mdx";
import ModuleFour from "../../course/modules/04-ai-coding-agents.mdx";
import ModuleFive from "../../course/modules/05-reusable-systems.mdx";
import "../styles.css";

const courseImages = import.meta.glob("../../course/images/**/*", {
  eager: true,
  query: "?url",
  import: "default",
});

function resolveCourseImage(src) {
  const filename = src?.split("/").at(-1);
  const match = Object.entries(courseImages).find(([path]) => path.endsWith(`/${filename}`));
  return match?.[1] || src;
}

const modules = {
  1: {
    number: 1,
    title: "Why Interactive Environments Matter",
    duration: "15 min",
    Content: ModuleOne,
    lessons: [
      ["drawbacks-of-traditional-notebooks", "Drawbacks of Traditional Notebooks", null, 1],
      ["hidden-state", "Hidden State", "nested"],
      ["out-of-order-execution", "Out-of-Order Execution", "nested"],
      ["a-better-alternative-reactive-notebooks", "A Better Alternative: Reactive Notebooks", null, 2],
      ["marimo-a-reactive-notebook", "marimo: A Reactive Notebook", null, 3],
      ["getting-started-with-marimo", "Getting started with marimo", null, 4],
      ["check-your-understanding", "Quiz", null, 5],
    ],
  },
  2: {
    number: 2,
    title: "Reproducibility and Trustworthy AI",
    duration: "20 min",
    Content: ModuleTwo,
    lessons: [
      ["the-it-works-on-my-machine-problem", 'The "It Works on My Machine" Problem', null, 1],
      ["what-causes-environment-drift", "What Causes Environment Drift", null, 2],
      ["reproducible-environments-with-marimo", "Reproducible Environments with marimo", null, 3],
      ["clean-and-reviewable-git-diffs", "Clean and Reviewable Git Diffs", null, 4],
      ["using-one-notebook-across-environments", "Using One Notebook Across Environments", null, 5],
      ["check-your-understanding", "Quiz", null, 6],
    ],
  },
  3: {
    number: 3,
    title: "Why Interactivity Accelerates AI Discovery",
    duration: "20 min",
    Content: ModuleThree,
    lessons: [
      ["1-inspect-and-edit-data", "Inspect the data", null, 1],
      ["2-explore-data-visually", "Explore data visually", null, 2],
      ["3-train-and-evaluate-models", "Train and evaluate models", null, 3],
      ["4-debug-errors-interactively", "Debug errors interactively", null, 4],
      ["5-create-your-own-widgets", "Create your own widgets", null, 5],
      ["check-your-understanding", "Quiz", null, 6],
    ],
  },
  4: {
    number: 4,
    title: "AI Coding Agents for AI and ML",
    duration: "15 min",
    Content: ModuleFour,
    lessons: [
      ["1-generate-and-edit-with-the-ai-assistant", "Generate and edit with the AI assistant", null, 1],
      ["2-using-the-chat-panel", "Using the Chat panel", null, 2],
      ["3-work-with-a-coding-agent-using-marimo-pair", "Work with marimo pair", null, 3],
      ["4-review-ai-generated-work", "Review AI-generated work", null, 4],
      ["check-your-understanding", "Quiz", null, 5],
    ],
  },
  5: {
    number: 5,
    title: "From Prototype to Production",
    duration: "20 min",
    Content: ModuleFive,
    lessons: [
      ["1-start-with-a-notebook", "Start with a notebook", null, 1],
      ["2-run-a-marimo-notebook-as-a-script", "Turn your notebook into a script", null, 2],
      ["3-publish-the-classifier-as-a-web-app", "Turn your notebook into a web app", null, 3],
      ["4-export-and-share-a-report", "Share your work as an artifact", null, 4],
      ["5-reuse-the-classifier-in-another-notebook", "Reuse your notebook as a Python module", null, 5],
      ["6-the-complete-classifier", "Bring it all together", null, 6],
      ["check-your-understanding", "Quiz", null, 7],
    ],
  },
};

const futureModules = [];

const devNotebookCacheKey = Date.now();

function moduleHref(number, section = "top") {
  return `${window.location.pathname}?module=${number}#${section}`;
}

function slugify(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  async function copy() {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }
  return (
    <button className={`copy-code ${copied ? "copied" : ""}`} type="button" onClick={copy} aria-label={copied ? "Copied" : "Copy code"} title={copied ? "Copied" : "Copy"}>
      <svg aria-hidden="true" viewBox="0 0 24 24">
        {copied ? <path d="m5 12 4 4L19 6" /> : <><rect x="9" y="9" width="10" height="10" rx="2" /><path d="M15 9V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" /></>}
      </svg>
    </button>
  );
}

function CodeBlock({ children }) {
  const code = children?.props?.children ?? "";
  const language = children?.props?.className?.replace("language-", "") || "code";
  return <div className="code-block"><div className="code-toolbar"><span className="code-label">{language}</span><CopyButton text={String(code).trimEnd()} /></div><pre>{children}</pre></div>;
}

function Callout({ title, children }) {
  return <aside className={title === "Coming from Jupyter" ? "callout neutral" : "callout"}><div><strong>{title}</strong><div>{children}</div></div></aside>;
}

function TryIt({ children }) {
  return <aside className="try-it"><div className="try-label"><span>✦</span> Try it</div><div className="try-content">{children}</div></aside>;
}

function SetupTab({ children }) {
  return children;
}

function ImageComparison({ leftImage, leftLabel, rightImage, rightLabel }) {
  return (
    <div className="image-comparison" aria-label="Version comparison">
      <figure className="comparison-card comparison-success">
        <figcaption><span aria-hidden="true">✓</span>{leftLabel}</figcaption>
        <img src={resolveCourseImage(leftImage)} alt="" />
      </figure>
      <figure className="comparison-card comparison-error">
        <figcaption><span aria-hidden="true">×</span>{rightLabel}</figcaption>
        <img src={resolveCourseImage(rightImage)} alt="" />
      </figure>
    </div>
  );
}

function ImagePlaceholder({ title, description }) {
  return (
    <div className="visual-placeholder" role="img" aria-label={`${title}. ${description}`}>
      <strong>{title}</strong>
      <span>{description}</span>
      <small>Image placeholder</small>
    </div>
  );
}

function TweetEmbed({ url }) {
  const containerRef = useRef(null);

  useEffect(() => {
    const renderTweet = () => window.twttr?.widgets?.load(containerRef.current);
    if (window.twttr?.widgets) {
      renderTweet();
      return;
    }

    let script = document.getElementById("twitter-widgets");
    if (!script) {
      script = document.createElement("script");
      script.id = "twitter-widgets";
      script.src = "https://platform.twitter.com/widgets.js";
      script.async = true;
      document.body.appendChild(script);
    }
    script.addEventListener("load", renderTweet);
    return () => script.removeEventListener("load", renderTweet);
  }, [url]);

  return (
    <div className="tweet-embed" ref={containerRef}>
      <blockquote className="twitter-tweet" data-theme="light" data-dnt="true" data-align="center">
        <p>ML pipelines should not be Jupyter notebooks.</p>
        <span>Shreya Shankar</span>
        <a href={url} target="_blank" rel="noreferrer">View the original post on X</a>
      </blockquote>
    </div>
  );
}

function SetupTabs({ children }) {
  const [active, setActive] = useState(0);
  const tabs = (Array.isArray(children) ? children : [children]).filter(Boolean);
  const tabId = useId();
  return (
    <div className="setup-tabs">
      <div className="setup-tab-list" role="tablist" aria-label="Choose how to use marimo">
        {tabs.map((tab, index) => (
          <button
            id={`${tabId}-tab-${index}`}
            aria-controls={`${tabId}-panel-${index}`}
            aria-selected={active === index}
            className={active === index ? "active" : ""}
            key={tab.props.label}
            onClick={() => setActive(index)}
            role="tab"
            type="button"
          >
            {tab.props.label}
          </button>
        ))}
      </div>
      <div
        aria-labelledby={`${tabId}-tab-${active}`}
        className="setup-tab-panel"
        id={`${tabId}-panel-${active}`}
        role="tabpanel"
      >
        {tabs[active]?.props.children}
      </div>
    </div>
  );
}

function Quiz({ question, options, answer, insights = [], courseSections = [], correctFeedback, incorrectFeedback }) {
  const [selected, setSelected] = useState(null);
  const questionId = useId();
  const hasCorrectAnswer = Number.isInteger(answer);
  const isCorrect = selected === answer;
  return (
    <section className="quiz" aria-labelledby={questionId}>
      <h3 id={questionId}>{question}</h3>
      <div className="quiz-options">
        {options.map((option, index) => (
          <button
            className={selected === index ? (hasCorrectAnswer ? (isCorrect ? "correct" : "incorrect") : "selected") : ""}
            type="button"
            key={option}
            onClick={() => setSelected(index)}
            aria-pressed={selected === index}
          >
            <span>{String.fromCharCode(65 + index)}</span>
            {option}
          </button>
        ))}
      </div>
      {selected !== null && hasCorrectAnswer && (
        <p className={`quiz-feedback ${isCorrect ? "correct" : "incorrect"}`} role="status">
          {isCorrect
            ? correctFeedback || "Correct. The code changed, but the old outputs remained visible."
            : incorrectFeedback || "Not quite. The example showed code and outputs that no longer agreed. Try again."}
        </p>
      )}
      {selected !== null && !hasCorrectAnswer && (
        <div className="poll-response" role="status">
          <p className="quiz-feedback selected">{insights[selected]}</p>
          <div className="course-pointer">
            <strong>Where this course covers it</strong>
            <span>{courseSections[selected]}</span>
          </div>
        </div>
      )}
    </section>
  );
}

function DemoPlaceholder({ title }) {
  return <div className="demo-card"><div className="demo-head"><div><span className="badge">Jupyter demo</span><h3>{title}</h3></div><span className="placeholder-pill">Visual placeholder</span></div><div className="steps"><div><span>1</span><p>Run with<br /><strong>b = 2</strong></p></div><i>→</i><div><span>2</span><p>Change to<br /><strong>b = 11</strong></p></div><i>→</i><div><span>3</span><p>Delete cell<br /><strong>b stays 11</strong></p></div><i>→</i><div className="warning"><span>4</span><p>Result<br /><strong>a + b = 12</strong></p></div></div></div>;
}

function MarimoEmbed({ title, notebook, openUrl }) {
  const isEmbedded = /\.html(?:[?#]|$)/.test(notebook || "") || /^https?:\/\//.test(notebook || "");
  const resolvedEmbedUrl = notebook?.startsWith("/")
    ? `${import.meta.env.BASE_URL}${notebook.slice(1)}`
    : notebook;
  const embedUrl = import.meta.env.DEV && notebook?.startsWith("/")
    ? `${resolvedEmbedUrl}${resolvedEmbedUrl.includes("?") ? "&" : "?"}dev=${devNotebookCacheKey}`
    : resolvedEmbedUrl;
  const requestedOpenUrl = openUrl || notebook;
  const openNotebookUrl = requestedOpenUrl?.startsWith("/")
    ? `${import.meta.env.BASE_URL}${requestedOpenUrl.slice(1)}`
    : requestedOpenUrl;
  const openLabel = openNotebookUrl?.includes("molab.marimo.io") ? "Open in molab" : "Open notebook";
  return (
    <div className={`notebook ${isEmbedded ? "notebook-embedded" : ""}`} data-notebook={notebook}>
      <div className="notebook-bar">
        {openUrl && <a href={openNotebookUrl} target="_blank" rel="noreferrer">{openLabel} ↗</a>}
      </div>
      {isEmbedded
        ? <iframe
            src={embedUrl}
            title={title || "Interactive marimo notebook"}
            sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
            allow="microphone"
            allowFullScreen
            loading="lazy"
          />
        : <div className="notebook-body"><span className="badge green">Interactive notebook</span><h3>{title}</h3><p>The live marimo notebook will appear here when its hosted URL is available.</p></div>}
    </div>
  );
}

const mdxComponents = {
  h1: (props) => <h1 id="top" {...props} />,
  h2: ({ children, ...props }) => <h2 id={slugify(children)} {...props}>{children}</h2>,
  h3: ({ children, ...props }) => <h3 id={slugify(children)} {...props}>{children}</h3>,
  p: ({ children, ...props }) => {
    const text = typeof children === "string" ? children : "";
    const id = text.startsWith("Outputs can also become stale") ? "stale-outputs" : undefined;
    return <p id={id} {...props}>{children}</p>;
  },
  img: ({ src, ...props }) => <img src={resolveCourseImage(src)} {...props} />,
  pre: CodeBlock,
  Callout,
  TryIt,
  SetupTabs,
  SetupTab,
  ImageComparison,
  ImagePlaceholder,
  TweetEmbed,
  Quiz,
  DemoPlaceholder,
  MarimoEmbed,
};

function Sidebar({ module, open, setOpen }) {
  const sidebarParams = new URLSearchParams(window.location.search);
  const [active, setActive] = useState(module.lessons[0]?.[0] || "top");
  const [outlineOpen, setOutlineOpen] = useState(() => sidebarParams.get("outline") === "1");
  const [expandedModule, setExpandedModule] = useState(() => Number(sidebarParams.get("expanded")) || null);
  useEffect(() => {
    setActive(module.lessons[0]?.[0] || "top");
    const targets = module.lessons.map(([id]) => document.getElementById(id)).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).at(-1);
      if (visible) setActive(visible.target.id);
    }, { rootMargin: "-15% 0px -70% 0px" });
    targets.forEach((target) => observer.observe(target));
    return () => observer.disconnect();
  }, [module]);
  return <aside className={`sidebar ${open ? "open" : ""}`} id="courseSidebar"><div className="sidebar-inner"><div className="course-title"><a href={window.location.pathname}>marimo for AI and ML Development</a><button type="button" onClick={() => setOutlineOpen(!outlineOpen)} aria-label={outlineOpen ? "Collapse course contents" : "Expand course contents"} aria-expanded={outlineOpen} aria-controls="courseOutline">{outlineOpen ? "−" : "+"}</button></div>{outlineOpen && <><div className="progress"><span style={{ width: `${module.number * 20}%` }} /></div><p className="progress-label">{module.number} of 5 modules</p><nav className="course-outline" id="courseOutline" aria-label="Course lessons">{Object.values(modules).map((item) => <div className={`module-group ${expandedModule === item.number ? "" : "collapsed-group"}`} key={item.number}><p><a className="module-link" href={`${window.location.pathname}?module=${item.number}&outline=1&expanded=${item.number}`} onClick={() => setExpandedModule(item.number)}>{item.number}. {item.title}</a></p>{expandedModule === item.number && item.number === module.number && <ol>{item.lessons.map(([id, title, level, number]) => <li className={level === "nested" ? "nested-lesson" : ""} key={id}><a className={active === id ? "current" : ""} href={`#${id}`} onClick={() => setOpen(false)}><span>{level === "nested" ? "↳" : number}</span>{title}</a></li>)}</ol>}</div>)}{futureModules.map((title) => <div className="module-group future-group" key={title}><p>{title}</p></div>)}</nav></>}</div></aside>;
}

function CourseHome() {
  return <article className="course-home" id="course">
    <p className="course-kicker">marimo course</p>
    <h1>marimo for AI and ML Development</h1>
    <p className="course-subtitle">Enable reactive execution and predictable AI workflows.</p>
    <p className="course-author">Parul Pandey</p>
    <div className="course-actions">
      <a className="course-start" href={`${window.location.pathname}?module=1&outline=1&expanded=1`}>Start the course</a>
    </div>
    <section className="course-outcomes">
      <h2>What you will learn and how you can apply it</h2>
      <ul>
        <li>See how reactive execution and clear dependencies prevent common reproducibility problems in notebooks.</li>
        <li>Build and share AI and ML experiments that use the same environment and dependencies.</li>
        <li>Explore data and evaluate models with interactive controls and visualizations.</li>
        <li>Use AI coding agents while you prototype, debug models, and improve an ML workflow.</li>
        <li>Turn one marimo notebook into a script, web app, shareable artifact, or Python module without rewriting the code.</li>
      </ul>
    </section>
  </article>;
}

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const requestedModule = Number(new URLSearchParams(window.location.search).get("module"));
  const isCourseHome = !requestedModule || !modules[requestedModule];
  const module = modules[requestedModule] || modules[1];
  const Content = module.Content;
  const previous = modules[module.number - 1];
  const next = modules[module.number + 1];
  return <><header className="site-header"><a className="brand" href="https://marimo.io" target="_blank" rel="noreferrer" aria-label="Visit marimo"><img src="https://marimo.io/logotype-wide.svg" alt="marimo" /></a><nav><a href="https://docs.marimo.io" target="_blank" rel="noreferrer">Docs ↗</a></nav></header><div className="mobile-course-bar"><button onClick={() => setMenuOpen(!menuOpen)} aria-expanded={menuOpen} aria-controls="courseSidebar"><span>{isCourseHome ? "Course contents" : `Module ${module.number} of 5`}</span><span>{menuOpen ? "×" : "☰"}</span></button></div><div className="page-shell"><Sidebar module={module} open={menuOpen} setOpen={setMenuOpen} /><main>{isCourseHome ? <CourseHome /> : <article className="mdx-content" id="course"><div className="lesson-meta"><span>Module {String(module.number).padStart(2, "0")}</span><span>{module.duration}</span></div><Content components={mdxComponents} /><nav className={`lesson-nav ${previous ? "has-previous" : ""}`}>{previous ? <a className="previous" href={moduleHref(previous.number)}><small>Previous module</small><strong>← {previous.title}</strong></a> : <span />}{next && <a className="next" href={moduleHref(next.number)}><small>Next module</small><strong>{next.title} →</strong></a>}</nav></article>}</main></div></>;
}

createRoot(document.getElementById("root")).render(<App />);
