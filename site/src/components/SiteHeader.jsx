import TourSlide, { TourTabs } from "./Tour.jsx";

const LINKS = [
  ["#how", "Pipeline"],
  ["#try", "Try it"],
  ["#results", "Results"],
  ["#features", "Features"],
  ["#start", "Quick start"],
  ["#faq", "FAQ"],
];

const GITHUB_URL = "https://github.com/nihalmachhi/TraceForge";

const ICON_URL = `${import.meta.env.BASE_URL}icon.png`;

export function Brand({ withIcon = true }) {
  return (
    <a className="brand" href="#top">
      {withIcon && (
        <img
          className="brand-icon"
          src={ICON_URL}
          alt=""
          width="22"
          height="22"
        />
      )}
      TraceForge
    </a>
  );
}

export default function SiteHeader({
  active,
  setActive,
  paused,
  holding,
  onToggle,
  report,
}) {
  const caseCount = report?.versions?.baseline?.case_count ?? 4;
  const taskDelta = report?.comparison?.task_success_delta ?? -0.5;
  const groundednessDelta = report?.comparison?.groundedness_delta ?? -0.35;
  const gateFailed = taskDelta < 0 || groundednessDelta < -0.05;

  return (
    <>
      <nav className="top" aria-label="Main">
        <Brand />
        <div className="links">
          {LINKS.map(([href, label]) => (
            <a href={href} key={href}>
              {label}
            </a>
          ))}
        </div>
        <div className="sp">
          <a className="pill" href={GITHUB_URL}>
            GitHub
          </a>
          <a className="pill w" href="#start">
            Run it locally
          </a>
        </div>
      </nav>

      <header className={`hero ${paused || holding ? "hold" : ""}`} id="top">
        <h1>Know which prompt change broke your agent.</h1>
        <p>
          TraceForge records every step an agent takes, redacts what shouldn’t
          be stored, scores two prompt versions on the same cases, and fails
          your build when quality drops.
        </p>
        <div className="cta">
          <a className="pill w" href="#start">
            Run it locally
          </a>
          <a className="pill" href={GITHUB_URL}>
            View on GitHub
          </a>
        </div>

        <div className="tabs">
          <TourTabs active={active} onChange={setActive} />
          <button
            className="ctrl"
            type="button"
            aria-label={
              paused ? "Resume the automatic tour" : "Pause the automatic tour"
            }
            title={paused ? "Resume" : "Pause"}
            onClick={onToggle}
          >
            {paused ? "▶" : "❚❚"}
          </button>
        </div>

        <div className="win" id="win" style={{ textAlign: "left" }}>
          <aside className="side" aria-hidden="true">
            <div className="dots">
              <i />
              <i />
              <i />
            </div>
            <div className="it on">
              Compare <span>2</span>
            </div>
            <div className="it">
              Traces <span>8</span>
            </div>
            <div className="it">
              Cases <span>{caseCount}</span>
            </div>
            <div className="it">
              Gate{" "}
              <span className={gateFailed ? "no" : ""}>
                {gateFailed ? "fail" : "pass"}
              </span>
            </div>
            <h4>Prompt versions</h4>
            <div className="it f" style={{ "--c": "var(--ok)" }}>
              baseline
            </div>
            <div className="it f" style={{ "--c": "var(--bad)" }}>
              candidate
            </div>
            <h4>Dataset</h4>
            <div className="it f" style={{ "--c": "#62626b" }}>
              traceforge-faq-v1
            </div>
          </aside>
          <div className="main" id="main" role="tabpanel" aria-live="off">
            <TourSlide active={active} />
          </div>
        </div>
      </header>
    </>
  );
}
