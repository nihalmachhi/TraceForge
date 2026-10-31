import Simulator from "./components/Simulator.jsx";
import TourSlide, { TourTabs } from "./components/Tour.jsx";

export default function ReferenceLayout({
  active,
  setActive,
  paused,
  onToggle,
}) {
  return (
    <>
      {" "}
      <div className={"wrap"}>
        {" "}
        <nav className={"top"} aria-label={"Main"}>
          {" "}
          <a className={"brand"} href={"#top"}>
            <svg
              width={"22"}
              height={"22"}
              viewBox={"0 0 22 22"}
              aria-hidden={"true"}
            >
              <rect
                x={"2"}
                y={"3"}
                width={"18"}
                height={"3.4"}
                rx={"1.7"}
                fill={"#f4f4f5"}
              ></rect>
              <rect
                x={"6"}
                y={"9.3"}
                width={"14"}
                height={"3.4"}
                rx={"1.7"}
                fill={"#8c8c95"}
              ></rect>
              <rect
                x={"10"}
                y={"15.6"}
                width={"10"}
                height={"3.4"}
                rx={"1.7"}
                fill={"#ff7a45"}
              ></rect>
            </svg>
            {"TraceForge"}
          </a>{" "}
          <div className={"links"}>
            <a href={"#how"}>{"Pipeline"}</a>
            <a href={"#try"}>{"Try it"}</a>
            <a href={"#results"}>{"Results"}</a>
            <a href={"#features"}>{"Features"}</a>
            <a href={"#start"}>{"Quick start"}</a>
            <a href={"#faq"}>{"FAQ"}</a>
          </div>{" "}
          <div className={"sp"}>
            <a
              className={"pill"}
              href={"https://github.com/nihalmachhi/TraceForge"}
            >
              {"GitHub"}
            </a>
            <a className={"pill w"} href={"#start"}>
              {"Run it locally"}
            </a>
          </div>{" "}
        </nav>{" "}
        <header
          className={`hero ${paused || holding ? "hold" : ""}`}
          id={"top"}
        >
          {" "}
          <h1>{"Know which prompt change broke your agent."}</h1>{" "}
          <p>
            {
              "TraceForge records every step an agent takes, redacts what shouldn’t be stored, scores two prompt versions on the same cases, and fails your build when quality drops."
            }
          </p>{" "}
          <div className={"cta"}>
            <a className={"pill w"} href={"#start"}>
              {"Run it locally"}
            </a>
            <a
              className={"pill"}
              href={"https://github.com/nihalmachhi/TraceForge"}
            >
              {"View on GitHub"}
            </a>
          </div>{" "}
          <div className={"tabs"}>
            <TourTabs active={active} onChange={setActive} />
            <button
              className={"ctrl"}
              type={"button"}
              aria-label={
                paused
                  ? "Resume the automatic tour"
                  : "Pause the automatic tour"
              }
              title={paused ? "Resume" : "Pause"}
              onClick={onToggle}
            >
              {paused ? "▶" : "❚❚"}
            </button>
          </div>{" "}
          <div className={"win"} id={"win"} style={{ textAlign: "left" }}>
            {" "}
            <aside className={"side"} aria-hidden={"true"}>
              {" "}
              <div className={"dots"}>
                <i></i>
                <i></i>
                <i></i>
              </div>{" "}
              <div className={"it on"}>
                {"Compare "}
                <span>{"2"}</span>
              </div>
              <div className={"it"}>
                {"Traces "}
                <span>{"8"}</span>
              </div>
              <div className={"it"}>
                {"Cases "}
                <span>{"4"}</span>
              </div>
              <div className={"it"}>
                {"Gate "}
                <span className={"no"}>{"fail"}</span>
              </div>{" "}
              <h4>{"Prompt versions"}</h4>
              <div className={"it f"} style={{ "--c": "var(--ok)" }}>
                {"baseline"}
              </div>
              <div className={"it f"} style={{ "--c": "var(--bad)" }}>
                {"candidate"}
              </div>{" "}
              <h4>{"Dataset"}</h4>
              <div className={"it f"} style={{ "--c": "#62626b" }}>
                {"traceforge-faq-v1"}
              </div>{" "}
            </aside>{" "}
            <div
              className={"main"}
              id={"main"}
              role={"tabpanel"}
              aria-live={"off"}
            >
              <TourSlide active={active} />
            </div>{" "}
          </div>{" "}
        </header>{" "}
        <section className={"sec"} id={"how"}>
          {" "}
          <h2>
            {"Three steps. "}
            <span className={"m"}>
              {"One "}
              <i className={"ico"} style={{ "--c": "#22c55e" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M5 12.5l4.5 4.5L19 7.5"}></path>
                </svg>
              </i>
              {" regression trail."}
            </span>
          </h2>{" "}
          <p className={"lead2"}>
            {
              "Every run becomes one trace, and every trace is scored against the same expected facts."
            }
          </p>{" "}
          <div className={"steps"}>
            {" "}
            <div className={"step"}>
              <div className={"ib"} style={{ "--c": "#8b5cf6" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M5 7h14M5 12h14M5 17h14"}></path>
                </svg>
              </div>
              <h3>{"1. Record"}</h3>
              <p>
                {"A context-manager SDK wraps each step in a span. Retrieval, "}
                <code>{"faq_catalog_lookup"}</code>
                {
                  " and the model call nest under one agent workflow automatically."
                }
              </p>
              <div className={"mini"}>
                <b>{"trace"}</b>
                {" › agent › retrieval · tool · llm"}
                <br />
                {"5 spans, each linked to its parent"}
              </div>
            </div>{" "}
            <div className={"step"}>
              <div className={"ib"} style={{ "--c": "#f59e0b" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"}></path>
                </svg>
              </div>
              <h3>{"2. Redact"}</h3>
              <p>
                {"Keys like "}
                <code>{"api_key"}</code>
                {" and "}
                <code>{"password"}</code>
                {", bearer tokens and emails become "}
                <code>{"[REDACTED]"}</code>
                {" before anything reaches SQLite. It is best effort."}
              </p>
              <div className={"mini"}>
                <span className={"dot"}></span>
                <span className={"dot"}></span>
                <span className={"dot r"}></span>
                <span className={"dot"}></span>
                <br />
                {"api_key → "}
                <b>{"[REDACTED]"}</b>
              </div>
            </div>{" "}
            <div className={"step"}>
              <div className={"ib"} style={{ "--c": "#f97316" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M7 19v-6M12 19V6M17 19v-10"}></path>
                </svg>
              </div>
              <h3>{"3. Compare"}</h3>
              <p>
                {
                  "Baseline and candidate prompts run on the same cases. Task success, groundedness, latency and cost sit side by side, and the gate decides."
                }
              </p>
              <div className={"mini"}>
                <div className={"seg"}>
                  <b style={{ flex: "2", background: "#ff7a45" }}>{"task"}</b>
                  <b style={{ flex: "1.4", background: "#fbbf24" }}>
                    {"grounded"}
                  </b>
                  <b style={{ flex: "1", background: "#a78bfa" }}>{"cost"}</b>
                </div>
                {"gate exits 1 on a regression"}
              </div>
            </div>{" "}
          </div>{" "}
        </section>{" "}
        <Simulator />{" "}
        <section className={"sec"} id={"results"}>
          {" "}
          <h2>
            {"Compared on the "}
            <span className={"m"}>
              {"same "}
              <i className={"ico"} style={{ "--c": "#06b6d4" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M7 19v-6M12 19V6M17 19v-10"}></path>
                </svg>
              </i>
              {" four cases."}
            </span>
          </h2>{" "}
          <p className={"lead2"}>
            {
              "Both prompts run the traceforge-faq-v1 dataset. Figures from the bundled demo run:"
            }
          </p>{" "}
          <div className={"rg"}>
            {" "}
            <div className={"rc"}>
              <h3>{"Baseline"}</h3>
              <p>
                {"The reference prompt every candidate is compared against."}
              </p>
              <div className={"tb"}>
                <div className={"mr"}>
                  <span>{"Task"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "100%",
                        "--c": "#8c8c95",
                        animation: "none",
                        width: "100%",
                      }}
                    ></div>
                  </div>
                  <b>{"100%"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Grounded"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "100%",
                        "--c": "#8c8c95",
                        animation: "none",
                        width: "100%",
                      }}
                    ></div>
                  </div>
                  <b>{"100%"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Relevance"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "100%",
                        "--c": "#8c8c95",
                        animation: "none",
                        width: "100%",
                      }}
                    ></div>
                  </div>
                  <b>{"100%"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Cost"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "100%",
                        "--c": "#8c8c95",
                        animation: "none",
                        width: "100%",
                      }}
                    ></div>
                  </div>
                  <b>{"$0.000271"}</b>
                </div>
              </div>
            </div>{" "}
            <div className={"rc"}>
              <h3>{"Candidate"}</h3>
              <p>{"An intentionally regressed prompt that fails two cases."}</p>
              <div className={"tb"}>
                <div className={"mr"}>
                  <span>{"Task"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "50%",
                        "--c": "var(--bad)",
                        animation: "none",
                        width: "50%",
                      }}
                    ></div>
                  </div>
                  <b>{"50%"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Grounded"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "65%",
                        "--c": "var(--bad)",
                        animation: "none",
                        width: "65%",
                      }}
                    ></div>
                  </div>
                  <b>{"65%"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Relevance"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "100%",
                        "--c": "var(--bad)",
                        animation: "none",
                        width: "100%",
                      }}
                    ></div>
                  </div>
                  <b>{"100%"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Cost"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "69%",
                        "--c": "var(--bad)",
                        animation: "none",
                        width: "69%",
                      }}
                    ></div>
                  </div>
                  <b>{"$0.000187"}</b>
                </div>
              </div>
            </div>{" "}
            <div className={"rc"}>
              <h3>{"Gate"}</h3>
              <p>
                {
                  "Default limits: task success 0 points, groundedness 5 points."
                }
              </p>
              <div className={"tb"}>
                <div className={"mr"}>
                  <span>{"Task"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "50%",
                        "--c": "#a78bfa",
                        animation: "none",
                        width: "50%",
                      }}
                    ></div>
                  </div>
                  <b>{"−50 pts"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Grounded"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "35%",
                        "--c": "#a78bfa",
                        animation: "none",
                        width: "35%",
                      }}
                    ></div>
                  </div>
                  <b>{"−35 pts"}</b>
                </div>
                <div className={"mr"}>
                  <span>{"Result"}</span>
                  <div className={"track"}>
                    <div
                      className={"grow"}
                      style={{
                        "--w": "100%",
                        "--c": "#a78bfa",
                        animation: "none",
                        width: "100%",
                      }}
                    ></div>
                  </div>
                  <b>{"exit 1"}</b>
                </div>
              </div>
            </div>{" "}
          </div>{" "}
          <p className={"note"}>
            {
              "Honest reading: the candidate looks cheaper only because it answers less. Scores come from a deterministic phrase check on a synthetic dataset, not an LLM judge, and costs use a sample rate card, so they show the workflow, not real model quality."
            }
          </p>{" "}
        </section>{" "}
        <section className={"sec"} id={"features"}>
          {" "}
          <h2>
            {"A small system. "}
            <span className={"m"}>
              {"Built to be "}
              <i className={"ico"} style={{ "--c": "#8b5cf6" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path
                    d={
                      "M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12v9M12 12L4 7.5"
                    }
                  ></path>
                </svg>
              </i>
              {" inspected."}
            </span>
          </h2>{" "}
          <p className={"lead2"}>
            {
              "The SDK, redactor, store, evaluator, gate, API and dashboard each live in their own module."
            }
          </p>{" "}
          <div className={"bento"}>
            {" "}
            <div className={"bc w"}>
              <div className={"ib"} style={{ "--c": "#8b5cf6" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M5 7h14M5 12h14M5 17h14"}></path>
                </svg>
              </div>
              <h3>{"Nested spans"}</h3>
              <p>
                {
                  "Retrieval, tool and model calls become parent-linked spans with timing, tokens and estimated cost."
                }
              </p>
              <div className={"mini"}>
                {"trace › agent workflow"}
                <br />
                {" › retrieve FAQ · 2.1 ms"}
                <br />
                {" › FAQ lookup · 0.2 ms"}
                <br />
                {" › generate answer · 4.4 ms"}
              </div>
            </div>{" "}
            <div className={"bc w"}>
              <div className={"ib"} style={{ "--c": "#f97316" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M8 8l-4 4 4 4M16 8l4 4-4 4"}></path>
                </svg>
              </div>
              <h3>{"Local JSON API"}</h3>
              <p>
                {
                  "Health, summary, traces and a demo rerun. Bound to 127.0.0.1 with no authentication, so keep it local."
                }
              </p>
              <div className={"mini"}>
                {"GET /api/health"}
                <br />
                {"GET /api/summary"}
                <br />
                {"GET /api/traces"}
                <br />
                {"GET /api/traces/{trace_id}"}
                <br />
                {"POST /api/demo/rerun"}
              </div>
            </div>{" "}
            <div className={"bc "}>
              <div className={"ib"} style={{ "--c": "#f59e0b" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"}></path>
                </svg>
              </div>
              <h3>{"Best-effort redaction"}</h3>
              <p>
                {"Sensitive-looking keys and tokens are masked before storage."}
              </p>
              <div className={"tags"}>
                <span>{"api_key"}</span>
                <span>{"token"}</span>
                <span>{"password"}</span>
                <span>{"Bearer"}</span>
                <span>{"email"}</span>
              </div>
            </div>{" "}
            <div className={"bc "}>
              <div className={"ib"} style={{ "--c": "#22c55e" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M5 12.5l4.5 4.5L19 7.5"}></path>
                </svg>
              </div>
              <h3>{"Deterministic"}</h3>
              <p>
                {
                  "A fixed dataset and phrase checks give the same verdict every run."
                }
              </p>
              <div className={"tags"}>
                <span>{"traceforge-faq-v1"}</span>
                <span>{"not an LLM judge"}</span>
              </div>
            </div>{" "}
            <div className={"bc "}>
              <div className={"ib"} style={{ "--c": "#fafafa" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M8 8l-4 4 4 4M16 8l4 4-4 4"}></path>
                </svg>
              </div>
              <h3>{"Standard library"}</h3>
              <p>{"No runtime packages to install."}</p>
              <div className={"tags"}>
                <span>{"Python 3.11+"}</span>
              </div>
            </div>{" "}
            <div className={"bc w"}>
              <div className={"ib"} style={{ "--c": "#ec4899" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path
                    d={
                      "M5 6c0-1.7 3.1-3 7-3s7 1.3 7 3-3.1 3-7 3-7-1.3-7-3zM5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6"
                    }
                  ></path>
                </svg>
              </div>
              <h3>{"Validated SQLite storage"}</h3>
              <p>
                {
                  "A trace is saved atomically, and the store refuses malformed data before writing."
                }
              </p>
              <div className={"tags"}>
                <span>{"duplicate span ID"}</span>
                <span>{"orphan span"}</span>
                <span>{"trace_id mismatch"}</span>
              </div>
            </div>{" "}
            <div className={"bc w"}>
              <div className={"ib"} style={{ "--c": "#ef4444" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M7 19v-6M12 19V6M17 19v-10"}></path>
                </svg>
              </div>
              <h3>{"A gate for CI"}</h3>
              <p>
                {
                  "Compare candidate with baseline and exit with code 1 when quality drops past your limits."
                }
              </p>
              <div className={"mini"}>
                {"gate --max-task-drop 0.25"}
                <br />
                {"exit code 1 → build blocked"}
              </div>
            </div>{" "}
            <div className={"bc f"}>
              <div className={"ib"} style={{ "--c": "#22c55e" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M5 12h14M13 6l6 6-6 6"}></path>
                </svg>
              </div>
              <h3>{"Not in this release"}</h3>
              <p>
                {
                  "Real model calls and provider pricing, an LLM judge, authentication, production load testing, OpenTelemetry export, and trace context across thread pools are out of scope."
                }
              </p>
              <div className={"tags"}>
                <span>{"model calls"}</span>
                <span>{"LLM judge"}</span>
                <span>{"authentication"}</span>
                <span>{"load benchmark"}</span>
                <span>{"OpenTelemetry"}</span>
                <span>{"thread pools"}</span>
              </div>
            </div>{" "}
          </div>{" "}
        </section>{" "}
        <section className={"sec"} id={"start"}>
          {" "}
          <h2>
            {"One minute "}
            <span className={"m"}>
              {"to a "}
              <i className={"ico"} style={{ "--c": "#22c55e" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M7 19v-6M12 19V6M17 19v-10"}></path>
                </svg>
              </i>
              {" dashboard."}
            </span>
          </h2>{" "}
          <p className={"lead2"}>
            {
              "Python 3.11 or newer and nothing else. On macOS or Linux set PYTHONPATH=src and run python -m traceforge.cli."
            }
          </p>{" "}
          <div className={"steps qs"}>
            {" "}
            <div className={"step"}>
              <h3>{"1. Set up"}</h3>
              <p>{"Create a virtual environment and activate it."}</p>
              <div className={"code"}>
                <span className={"c"}>{"# PowerShell"}</span>
                <br />
                {"py -3 -m venv .venv"}
                <br />
                {".\\.venv\\Scripts\\Activate.ps1"}
              </div>
            </div>{" "}
            <div className={"step"}>
              <h3>{"2. Record and serve"}</h3>
              <p>
                {
                  "Record both prompt runs, then open the dashboard on loopback."
                }
              </p>
              <div className={"code"}>
                {".\\scripts\\run.ps1 demo"}
                <br />
                {".\\scripts\\run.ps1 serve"}
                <br />
                <span className={"c"}>{"# 127.0.0.1:8000"}</span>
              </div>
            </div>{" "}
            <div className={"step"}>
              <h3>{"3. Gate the build"}</h3>
              <p>{"Exit 1 on a regression, or allow a task-success drop."}</p>
              <div className={"code"}>
                {".\\scripts\\run.ps1 gate"}
                <br />
                {".\\scripts\\run.ps1 gate \\"}
                <br />
                {" --max-task-drop 0.25"}
              </div>
            </div>{" "}
          </div>{" "}
        </section>{" "}
        <section className={"sec"} id={"scope"}>
          {" "}
          <h2>
            {"Built to "}
            <i className={"ico"} style={{ "--c": "#f97316" }}>
              <svg viewBox={"0 0 24 24"}>
                <path
                  d={
                    "M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z"
                  }
                ></path>
              </svg>
            </i>{" "}
            <span className={"m"}>{"teach."}</span>
          </h2>{" "}
          <p className={"lead2"}>
            {
              "TraceForge is for learning how agent tracing and regression testing work. It is not a production observability tool."
            }
          </p>{" "}
          <div className={"sc"}>
            {" "}
            <div className={"scc"}>
              <div className={"ib"} style={{ "--c": "#22c55e" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M5 12.5l4.5 4.5L19 7.5"}></path>
                </svg>
              </div>
              <h3>{"In scope"}</h3>
              <ul>
                <li>{"Nested spans for retrieval, tool and model calls"}</li>
                <li>{"Redaction before anything reaches SQLite"}</li>
                <li>{"Two prompt versions scored on one fixed dataset"}</li>
                <li>{"A CI gate that exits 1 on a regression"}</li>
                <li>{"A local dashboard and JSON API"}</li>
              </ul>
            </div>{" "}
            <div className={"scc"}>
              <div className={"ib"} style={{ "--c": "#ef4444" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M6 6l12 12M18 6L6 18"}></path>
                </svg>
              </div>
              <h3>{"Out of scope"}</h3>
              <ul>
                <li>{"Real model calls or provider pricing"}</li>
                <li>{"An LLM judge or real-world accuracy claims"}</li>
                <li>{"Authentication or network-facing deployment"}</li>
                <li>{"Load benchmarks or production integration"}</li>
                <li>{"OpenTelemetry export and thread-pool context"}</li>
              </ul>
            </div>{" "}
          </div>{" "}
        </section>{" "}
        <section className={"sec"} id={"faq"}>
          {" "}
          <h2>
            {"Any "}
            <i className={"ico"} style={{ "--c": "#ec4899" }}>
              <svg viewBox={"0 0 24 24"}>
                <path
                  d={"M9.5 9a2.6 2.6 0 115 .6c0 1.8-2.5 2.2-2.5 4M12 17.5h.01"}
                ></path>
              </svg>
            </i>{" "}
            <span className={"m"}>{"questions?"}</span>
          </h2>{" "}
          <div className={"faq"}>
            <details>
              <summary>{"Does it call a real model?"}</summary>
              <p>
                {
                  "No. The bundled agent is deterministic, so scores illustrate the workflow, not real model quality. Add provider timeouts, retries and secret handling before connecting a real one."
                }
              </p>
            </details>
            <details>
              <summary>{"What is in scope?"}</summary>
              <p>
                {
                  "Recording nested spans, redacting before storage, scoring two prompt versions on a fixed dataset, a CI gate, a local API and a local dashboard."
                }
              </p>
            </details>
            <details>
              <summary>{"What is not included?"}</summary>
              <p>
                {
                  "Model-provider adapters, an LLM judge, authentication, load testing, OpenTelemetry export and async or thread-pool context propagation."
                }
              </p>
            </details>
            <details>
              <summary>{"Is the evaluator an LLM judge?"}</summary>
              <p>
                {
                  "No. It checks required phrases and word overlap, so the same inputs always give the same verdict."
                }
              </p>
            </details>
            <details>
              <summary>{"Are the costs real?"}</summary>
              <p>
                {
                  "No. They come from a sample rate card of $2 per million input tokens and $8 per million output tokens."
                }
              </p>
            </details>
            <details>
              <summary>{"Do I need to install anything?"}</summary>
              <p>
                {
                  "Only Python 3.11 or newer. The runtime uses the standard library, with SQLite for storage."
                }
              </p>
            </details>
            <details>
              <summary>{"Where is my data stored?"}</summary>
              <p>
                {
                  "In a local SQLite file under data/generated/, which Git ignores. Demo reruns replace only traces tagged traceforge_sample_v1 and keep everything else."
                }
              </p>
            </details>
            <details>
              <summary>{"Where are the docs?"}</summary>
              <p>
                {
                  "The docs folder covers architecture, schema, evaluators, CI, privacy and a walkthrough."
                }
              </p>
            </details>
            <details>
              <summary>{"Is it ready for production?"}</summary>
              <p>
                {
                  "No. It is local and single-process, has no authentication, and has had no load or security testing. Keep the server on loopback."
                }
              </p>
            </details>
          </div>{" "}
        </section>{" "}
        <section className={"cta2 rv-wrap"} aria-label={"Get started"}>
          {" "}
          <div className={"rv archw"} style={{ "--r": "0" }}>
            <svg
              className={"flow arch"}
              viewBox={"0 0 964 90"}
              role={"img"}
              aria-label={
                "TraceForge pipeline: fixed task cases, deterministic demo agent, nested spans, redaction, SQLite trace store, comparison, dashboard and regression gate"
              }
            >
              <path className={"fl"} d={"M112 45H142"}></path>
              <path className={"fl"} d={"M254 45H284"}></path>
              <path className={"fl"} d={"M396 45H426"}></path>
              <path className={"fl"} d={"M538 45H568"}></path>
              <path className={"fl"} d={"M680 45H710"}></path>
              <path className={"fl"} d={"M822 45H852"}></path>
              <g className={"gn st"} style={{ "--d": "0.0s" }}>
                <rect
                  x={"0"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"56.0"} y={"42.0"}>
                    {"Fixed task"}
                  </tspan>
                  <tspan x={"56.0"} y={"55.0"}>
                    {"cases"}
                  </tspan>
                </text>
              </g>
              <g className={"gn st"} style={{ "--d": "0.9s" }}>
                <rect
                  x={"142"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"198.0"} y={"42.0"}>
                    {"Deterministic"}
                  </tspan>
                  <tspan x={"198.0"} y={"55.0"}>
                    {"demo agent"}
                  </tspan>
                </text>
              </g>
              <g className={"gn st"} style={{ "--d": "1.8s" }}>
                <rect
                  x={"284"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"340.0"} y={"35.5"}>
                    {"Nested"}
                  </tspan>
                  <tspan x={"340.0"} y={"48.5"}>
                    {"retrieval, tool,"}
                  </tspan>
                  <tspan x={"340.0"} y={"61.5"}>
                    {"and model spans"}
                  </tspan>
                </text>
              </g>
              <g className={"gn st"} style={{ "--d": "2.7s" }}>
                <rect
                  x={"426"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"482.0"} y={"35.5"}>
                    {"Redact"}
                  </tspan>
                  <tspan x={"482.0"} y={"48.5"}>
                    {"sensitive-"}
                  </tspan>
                  <tspan x={"482.0"} y={"61.5"}>
                    {"looking values"}
                  </tspan>
                </text>
              </g>
              <g className={"gn st"} style={{ "--d": "3.6s" }}>
                <rect
                  x={"568"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"624.0"} y={"42.0"}>
                    {"SQLite trace"}
                  </tspan>
                  <tspan x={"624.0"} y={"55.0"}>
                    {"store"}
                  </tspan>
                </text>
              </g>
              <g className={"gn st"} style={{ "--d": "4.5s" }}>
                <rect
                  x={"710"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"766.0"} y={"35.5"}>
                    {"Task, quality,"}
                  </tspan>
                  <tspan x={"766.0"} y={"48.5"}>
                    {"and cost"}
                  </tspan>
                  <tspan x={"766.0"} y={"61.5"}>
                    {"comparison"}
                  </tspan>
                </text>
              </g>
              <g className={"gn st last"} style={{ "--d": "5.4s" }}>
                <rect
                  x={"852"}
                  y={"12.0"}
                  width={"112"}
                  height={"66"}
                  rx={"9"}
                ></rect>
                <text textAnchor={"middle"}>
                  <tspan x={"908.0"} y={"42.0"}>
                    {"Dashboard and"}
                  </tspan>
                  <tspan x={"908.0"} y={"55.0"}>
                    {"regression gate"}
                  </tspan>
                </text>
              </g>
              <circle r={"3.2"} fill={"#f4f4f5"}>
                <animateMotion
                  dur={"6.3s"}
                  repeatCount={"indefinite"}
                  path={"M0 45H964"}
                ></animateMotion>
              </circle>
            </svg>
          </div>{" "}
          <h2 className={"rv"} style={{ "--r": "1" }}>
            {"Run it."}
            <br />
            <span className={"m"}>
              {"Watch it get "}
              <i className={"ico pulse"} style={{ "--c": "#ef4444" }}>
                <svg viewBox={"0 0 24 24"}>
                  <path d={"M12 8v5M12 17h.01"}></path>
                </svg>
              </i>
              {" caught."}
            </span>
          </h2>{" "}
          <div className={"btns rv"} style={{ "--r": "2" }}>
            <a
              className={"pill w"}
              href={"https://github.com/nihalmachhi/TraceForge"}
            >
              {"View on GitHub"}
            </a>
            <a className={"pill"} href={"#try"}>
              {"Back to the simulator"}
            </a>
          </div>{" "}
        </section>{" "}
      </div>{" "}
      <footer className={"wrap"}>
        <div className={"foot"}>
          <div className={"fcols"}>
            <div>
              <a className={"brand"} href={"#top"}>
                {"TraceForge"}
              </a>
              <p className={"tg"}>
                {
                  "A local, synthetic tracer and regression tester for AI agents."
                }
              </p>
            </div>{" "}
            <div>
              <h5>{"Product"}</h5>
              <ul>
                <li>
                  <a href={"#top"}>{"Overview"}</a>
                </li>
                <li>
                  <a href={"#how"}>{"Pipeline"}</a>
                </li>
                <li>
                  <a href={"#try"}>{"Simulator"}</a>
                </li>
                <li>
                  <a href={"#results"}>{"Results"}</a>
                </li>
              </ul>
            </div>{" "}
            <div>
              <h5>{"Run it"}</h5>
              <ul>
                <li>
                  <a href={"#features"}>{"Features"}</a>
                </li>
                <li>
                  <a href={"#start"}>{"Quick start"}</a>
                </li>
                <li>
                  <a href={"#faq"}>{"FAQ"}</a>
                </li>
              </ul>
            </div>{" "}
            <div>
              <h5>{"Source"}</h5>
              <ul>
                <li>
                  <a href={"https://github.com/nihalmachhi/TraceForge"}>
                    {"GitHub"}
                  </a>
                </li>
                <li>
                  <a
                    href={
                      "https://github.com/nihalmachhi/TraceForge/tree/main/docs"
                    }
                  >
                    {"Docs"}
                  </a>
                </li>
                <li>
                  <a
                    href={
                      "https://github.com/nihalmachhi/TraceForge/tree/main/src/traceforge"
                    }
                  >
                    {"Source code"}
                  </a>
                </li>
                <li>
                  <a href={"https://github.com/nihalmachhi/TraceForge/issues"}>
                    {"Issues"}
                  </a>
                </li>
              </ul>
            </div>
          </div>{" "}
          <div className={"fbot"}>
            <span>
              {
                "Synthetic demo. Scores, costs and latencies are illustrative, not real model quality or provider pricing."
              }
            </span>
            <span>{"Python · SQLite · JSON"}</span>
          </div>
          <div className={"mark"} aria-hidden={"true"}>
            {"TraceForge"}
          </div>
        </div>
      </footer>{" "}
    </>
  );
}
