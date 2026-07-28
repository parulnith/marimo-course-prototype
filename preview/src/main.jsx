import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import ModuleOne from "../../course/modules/01-interactive-environments.mdx";
import "../styles.css";

const moduleOneImages = import.meta.glob("../../course/images/module-1/*", {
  eager: true,
  query: "?url",
  import: "default",
});

function resolveModuleOneImage(src) {
  const filename = src?.split("/").at(-1);
  const match = Object.entries(moduleOneImages).find(([path]) => path.endsWith(`/${filename}`));
  return match?.[1] || src;
}

const lessons = [
  ["top", "Why Interactive Programming Environments Matter for AI and ML", null, 1],
  ["drawbacks-of-traditional-notebooks", "Drawbacks of Traditional Notebooks", null, 2],
  ["hidden-state", "Hidden State", "nested"],
  ["out-of-order-execution", "Out-of-Order Execution", "nested"],
  ["a-better-alternative-reactive-notebooks", "A Better Alternative: Reactive Notebooks", null, 3],
  ["marimo-a-reactive-notebook", "marimo: A Reactive Notebook", null, 4],
  ["hands-on-with-marimo", "Hands On with marimo", null, 5],
];

const moduleGroups = [
  "2. Reproducibility and Trustworthy AI",
  "3. Interactivity and AI Discovery",
  "4. AI Coding Agents for AI and ML",
  "5. From Interactive Work to Reusable Systems",
];

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
  return <aside className="try-it"><div className="try-label"><span>✦</span> Try it</div><div>{children}</div></aside>;
}

function Quiz({ question, options, answer, insights = [], courseSections = [] }) {
  const [selected, setSelected] = useState(null);
  const hasCorrectAnswer = Number.isInteger(answer);
  const isCorrect = selected === answer;
  return (
    <section className="quiz" aria-labelledby="quiz-question">
      <p className="quiz-label">Check your understanding</p>
      <h3 id="quiz-question">{question}</h3>
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
            ? "Correct. The code changed, but the old outputs remained visible."
            : "Not quite. The example showed code and outputs that no longer agreed. Try again."}
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
  const isEmbedded = notebook?.endsWith(".html") || /^https?:\/\//.test(notebook || "");
  const embedUrl = notebook?.startsWith("/")
    ? `${import.meta.env.BASE_URL}${notebook.slice(1)}`
    : notebook;
  const requestedOpenUrl = openUrl || notebook;
  const openNotebookUrl = requestedOpenUrl?.startsWith("/")
    ? `${import.meta.env.BASE_URL}${requestedOpenUrl.slice(1)}`
    : requestedOpenUrl;
  return (
    <div className={`notebook ${isEmbedded ? "notebook-embedded" : ""}`} data-notebook={notebook}>
      <div className="notebook-bar">
        <div><i></i><i></i><i></i></div>
        <span>{title || "marimo notebook"}</span>
        <a href={openNotebookUrl} target="_blank" rel="noreferrer">Open notebook ↗</a>
      </div>
      {isEmbedded
        ? <iframe src={embedUrl} title={title || "Interactive marimo notebook"} loading="lazy" />
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
  img: ({ src, ...props }) => <img src={resolveModuleOneImage(src)} {...props} />,
  pre: CodeBlock,
  Callout,
  TryIt,
  Quiz,
  DemoPlaceholder,
  MarimoEmbed,
};

function Sidebar({ open, setOpen }) {
  const [active, setActive] = useState("top");
  useEffect(() => {
    const targets = lessons.map(([id]) => document.getElementById(id)).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).at(-1);
      if (visible) setActive(visible.target.id);
    }, { rootMargin: "-15% 0px -70% 0px" });
    targets.forEach((target) => observer.observe(target));
    return () => observer.disconnect();
  }, []);
  return <aside className={`sidebar ${open ? "open" : ""}`} id="courseSidebar"><div className="sidebar-inner"><p className="overline">The Modern AI and ML Development Stack</p><div className="progress"><span /></div><p className="progress-label">1 of 5 modules</p><nav className="course-outline" aria-label="Course lessons"><div className="module-group"><p>1. Why Interactive Environments Matter</p><ol>{lessons.map(([id, title, level, number]) => <li className={level === "nested" ? "nested-lesson" : ""} key={id}><a className={active === id ? "current" : ""} href={`#${id}`} onClick={() => setOpen(false)}><span>{level === "nested" ? "↳" : number}</span>{title}</a></li>)}</ol></div>{moduleGroups.map((title) => <div className="module-group future-group" key={title}><p>{title}</p></div>)}</nav></div></aside>;
}

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  return <><header className="site-header"><a className="brand" href="#top" aria-label="marimo course preview"><img src="https://marimo.io/logotype-wide.svg" alt="marimo" /></a><nav><a className="active" href="#top">Learn</a><a href="https://docs.marimo.io" target="_blank" rel="noreferrer">Docs ↗</a></nav></header><div className="mobile-course-bar"><button onClick={() => setMenuOpen(!menuOpen)} aria-expanded={menuOpen} aria-controls="courseSidebar"><span>Module 1 of 5</span><span>{menuOpen ? "×" : "☰"}</span></button></div><div className="page-shell"><Sidebar open={menuOpen} setOpen={setMenuOpen} /><main><article className="mdx-content" id="course"><div className="lesson-meta"><span>Module 01</span><span>15 min</span></div><ModuleOne components={mdxComponents} /><nav className="lesson-nav"><span></span><a href="#future"><small>Next module</small><strong>Reproducibility and Trustworthy AI →</strong></a></nav></article></main></div></>;
}

createRoot(document.getElementById("root")).render(<App />);
