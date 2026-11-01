import Icon from "./Icons.jsx";

const PIPELINE = [
  {
    icon: "list",
    color: "#8b5cf6",
    title: "1. Record",
    body: (
      <>
        A context-manager SDK wraps each step in a span. Retrieval,{" "}
        <code>faq_catalog_lookup</code> and the model call nest under one agent
        workflow automatically.
      </>
    ),
    mini: (
      <>
        <b>trace</b> › agent › retrieval · tool · llm
        <br />5 spans, each linked to its parent
      </>
    ),
  },
  {
    icon: "shield",
    color: "#f59e0b",
    title: "2. Redact",
    body: (
      <>
        Keys like <code>api_key</code> and <code>password</code>, bearer tokens
        and emails become <code>[REDACTED]</code> before anything reaches
        SQLite. It is best effort.
      </>
    ),
    mini: (
      <>
        <span className="dot" />
        <span className="dot" />
        <span className="dot r" />
        <span className="dot" />
        <br />
        api_key → <b>[REDACTED]</b>
      </>
    ),
  },
  {
    icon: "bars",
    color: "#f97316",
    title: "3. Compare",
    body: (
      <>
        Baseline and candidate prompts run on the same cases. Task success,
        groundedness, latency and cost sit side by side, and the gate decides.
      </>
    ),
    mini: (
      <>
        <div className="seg">
          <b style={{ flex: 2, background: "#ff7a45" }}>task</b>
          <b style={{ flex: 1.4, background: "#fbbf24" }}>grounded</b>
          <b style={{ flex: 1, background: "#a78bfa" }}>cost</b>
        </div>
        gate exits 1 on a regression
      </>
    ),
  },
];

const GLYPHS = {
  list: "M5 7h14M5 12h14M5 17h14",
  shield: "M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z",
  bars: "M7 19v-6M12 19V6M17 19v-10",
  code: "M8 8l-4 4 4 4M16 8l4 4-4 4",
  check: "M5 12.5l4.5 4.5L19 7.5",
  database:
    "M5 6c0-1.7 3.1-3 7-3s7 1.3 7 3-3.1 3-7 3-7-1.3-7-3zM5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6",
  arrow: "M5 12h14M13 6l6 6-6 6",
};

function Glyph({ name }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d={GLYPHS[name]} />
    </svg>
  );
}

export function Pipeline() {
  return (
    <section className="sec" id="how">
      <h2>
        Three steps.{" "}
        <span className="m">
          One <Icon name="check" color="#22c55e" /> regression trail.
        </span>
      </h2>
      <p className="lead2">
        Every run becomes one trace, and every trace is scored against the same
        expected facts.
      </p>
      <div className="steps">
        {PIPELINE.map((step) => (
          <div className="step" key={step.title}>
            <div className="ib" style={{ "--c": step.color }}>
              <Glyph name={step.icon} />
            </div>
            <h3>{step.title}</h3>
            <p>{step.body}</p>
            <div className="mini">{step.mini}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

const RESULT_CARDS = [
  {
    title: "Baseline",
    description: "The reference prompt every candidate is compared against.",
    rows: [
      ["Task", 100, "#8c8c95", "100%"],
      ["Grounded", 100, "#8c8c95", "100%"],
      ["Relevance", 100, "#8c8c95", "100%"],
      ["Cost", 100, "#8c8c95", "$0.000271"],
    ],
  },
  {
    title: "Candidate",
    description: "An intentionally regressed prompt that fails two cases.",
    rows: [
      ["Task", 50, "var(--bad)", "50%"],
      ["Grounded", 65, "var(--bad)", "65%"],
      ["Relevance", 100, "var(--bad)", "100%"],
      ["Cost", 69, "var(--bad)", "$0.000187"],
    ],
  },
  {
    title: "Gate",
    description:
      "Default limits: task success 0 points, groundedness 5 points.",
    rows: [
      ["Task", 50, "#a78bfa", "−50 pts"],
      ["Grounded", 35, "#a78bfa", "−35 pts"],
      ["Result", 100, "#a78bfa", "exit 1"],
    ],
  },
];

function ResultRow({ label, width, color, value }) {
  return (
    <div className="mr">
      <span>{label}</span>
      <div className="track">
        <div
          className="grow"
          style={{
            "--w": `${width}%`,
            "--c": color,
            animation: "none",
            width: `${width}%`,
          }}
        />
      </div>
      <b>{value}</b>
    </div>
  );
}

export function Results() {
  return (
    <section className="sec" id="results">
      <h2>
        Compared on the{" "}
        <span className="m">
          same <Icon name="bars" color="#06b6d4" /> four cases.
        </span>
      </h2>
      <p className="lead2">
        Both prompts run the traceforge-faq-v1 dataset. Figures from the bundled
        demo run:
      </p>
      <div className="rg">
        {RESULT_CARDS.map((card) => (
          <div className="rc" key={card.title}>
            <h3>{card.title}</h3>
            <p>{card.description}</p>
            <div className="tb">
              {card.rows.map(([label, width, color, value]) => (
                <ResultRow
                  key={label}
                  label={label}
                  width={width}
                  color={color}
                  value={value}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
      <p className="note">
        Honest reading: the candidate looks cheaper only because it answers
        less. Scores come from a deterministic phrase check on a synthetic
        dataset, not an LLM judge, and costs use a sample rate card, so they
        show the workflow, not real model quality.
      </p>
    </section>
  );
}

const FEATURES = [
  {
    size: "w",
    icon: "list",
    color: "#8b5cf6",
    title: "Nested spans",
    body: "Retrieval, tool and model calls become parent-linked spans with timing, tokens and estimated cost.",
    mini: (
      <>
        trace › agent workflow
        <br />› retrieve FAQ · 2.1 ms
        <br />› FAQ lookup · 0.2 ms
        <br />› generate answer · 4.4 ms
      </>
    ),
  },
  {
    size: "w",
    icon: "code",
    color: "#f97316",
    title: "Local JSON API",
    body: "Health, summary, traces and a demo rerun. Bound to 127.0.0.1 with no authentication, so keep it local.",
    mini: (
      <>
        GET /api/health
        <br />
        GET /api/summary
        <br />
        GET /api/traces
        <br />
        GET /api/traces/{"{trace_id}"}
        <br />
        POST /api/demo/rerun
      </>
    ),
  },
  {
    icon: "shield",
    color: "#f59e0b",
    title: "Best-effort redaction",
    body: "Sensitive-looking keys and tokens are masked before storage.",
    tags: ["api_key", "token", "password", "Bearer", "email"],
  },
  {
    icon: "check",
    color: "#22c55e",
    title: "Deterministic",
    body: "A fixed dataset and phrase checks give the same verdict every run.",
    tags: ["traceforge-faq-v1", "not an LLM judge"],
  },
  {
    icon: "code",
    color: "#fafafa",
    title: "Standard library",
    body: "No runtime packages to install.",
    tags: ["Python 3.11+"],
  },
  {
    size: "w",
    icon: "database",
    color: "#ec4899",
    title: "Validated SQLite storage",
    body: "A trace is saved atomically, and the store refuses malformed data before writing.",
    tags: ["duplicate span ID", "orphan span", "trace_id mismatch"],
  },
  {
    size: "w",
    icon: "bars",
    color: "#ef4444",
    title: "A gate for CI",
    body: "Compare candidate with baseline and exit with code 1 when quality drops past your limits.",
    mini: (
      <>
        gate --max-task-drop 0.25
        <br />
        exit code 1 → build blocked
      </>
    ),
  },
  {
    size: "f",
    icon: "arrow",
    color: "#22c55e",
    title: "Not in this release",
    body: "Real model calls and provider pricing, an LLM judge, authentication, production load testing, OpenTelemetry export, and trace context across thread pools are out of scope.",
    tags: [
      "model calls",
      "LLM judge",
      "authentication",
      "load benchmark",
      "OpenTelemetry",
      "thread pools",
    ],
  },
];

export function Features() {
  return (
    <section className="sec" id="features">
      <h2>
        A small system.{" "}
        <span className="m">
          Built to be <Icon name="layers" color="#8b5cf6" /> inspected.
        </span>
      </h2>
      <p className="lead2">
        The SDK, redactor, store, evaluator, gate, API and dashboard each live
        in their own module.
      </p>
      <div className="bento">
        {FEATURES.map((feature) => (
          <div className={`bc ${feature.size ?? ""}`} key={feature.title}>
            <div className="ib" style={{ "--c": feature.color }}>
              <Glyph name={feature.icon} />
            </div>
            <h3>{feature.title}</h3>
            <p>{feature.body}</p>
            {feature.tags && (
              <div className="tags">
                {feature.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
            )}
            {feature.mini && <div className="mini">{feature.mini}</div>}
          </div>
        ))}
      </div>
    </section>
  );
}

const QUICK_START = [
  {
    title: "1. Set up",
    body: "Create a virtual environment and activate it.",
    code: (
      <>
        <span className="c"># PowerShell</span>
        <br />
        py -3 -m venv .venv
        <br />
        .\.venv\Scripts\Activate.ps1
      </>
    ),
  },
  {
    title: "2. Record and serve",
    body: "Record both prompt runs, then open the dashboard on loopback.",
    code: (
      <>
        .\scripts\run.ps1 demo
        <br />
        .\scripts\run.ps1 serve
        <br />
        <span className="c"># 127.0.0.1:8000</span>
      </>
    ),
  },
  {
    title: "3. Gate the build",
    body: "Exit 1 on a regression, or allow a task-success drop.",
    code: (
      <>
        .\scripts\run.ps1 gate
        <br />
        .\scripts\run.ps1 gate \
        <br />
        {" --max-task-drop 0.25"}
      </>
    ),
  },
];

export function QuickStart() {
  return (
    <section className="sec" id="start">
      <h2>
        One minute{" "}
        <span className="m">
          to a <Icon name="bars" color="#22c55e" /> dashboard.
        </span>
      </h2>
      <p className="lead2">
        Python 3.11 or newer and nothing else. On macOS or Linux set
        PYTHONPATH=src and run python -m traceforge.cli.
      </p>
      <div className="steps qs">
        {QUICK_START.map((step) => (
          <div className="step" key={step.title}>
            <h3>{step.title}</h3>
            <p>{step.body}</p>
            <div className="code">{step.code}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

const SCOPE = [
  {
    title: "In scope",
    color: "#22c55e",
    icon: "check",
    items: [
      "Nested spans for retrieval, tool and model calls",
      "Redaction before anything reaches SQLite",
      "Two prompt versions scored on one fixed dataset",
      "A CI gate that exits 1 on a regression",
      "A local dashboard and JSON API",
    ],
  },
  {
    title: "Out of scope",
    color: "#ef4444",
    icon: "close",
    items: [
      "Real model calls or provider pricing",
      "An LLM judge or real-world accuracy claims",
      "Authentication or network-facing deployment",
      "Load benchmarks or production integration",
      "OpenTelemetry export and thread-pool context",
    ],
  },
];

export function Scope() {
  return (
    <section className="sec" id="scope">
      <h2>
        Built to <Icon name="bulb" color="#f97316" />{" "}
        <span className="m">teach.</span>
      </h2>
      <p className="lead2">
        TraceForge is for learning how agent tracing and regression testing
        work. It is not a production observability tool.
      </p>
      <div className="sc">
        {SCOPE.map((group) => (
          <div className="scc" key={group.title}>
            <div className="ib" style={{ "--c": group.color }}>
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d={
                    group.icon === "check"
                      ? "M5 12.5l4.5 4.5L19 7.5"
                      : "M6 6l12 12M18 6L6 18"
                  }
                />
              </svg>
            </div>
            <h3>{group.title}</h3>
            <ul>
              {group.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}

const FAQ = [
  [
    "Does it call a real model?",
    "No. The bundled agent is deterministic, so scores illustrate the workflow, not real model quality. Add provider timeouts, retries and secret handling before connecting a real one.",
  ],
  [
    "What is in scope?",
    "Recording nested spans, redacting before storage, scoring two prompt versions on a fixed dataset, a CI gate, a local API and a local dashboard.",
  ],
  [
    "What is not included?",
    "Model-provider adapters, an LLM judge, authentication, load testing, OpenTelemetry export and async or thread-pool context propagation.",
  ],
  [
    "Is the evaluator an LLM judge?",
    "No. It checks required phrases and word overlap, so the same inputs always give the same verdict.",
  ],
  [
    "Are the costs real?",
    "No. They come from a sample rate card of $2 per million input tokens and $8 per million output tokens.",
  ],
  [
    "Do I need to install anything?",
    "Only Python 3.11 or newer. The runtime uses the standard library, with SQLite for storage.",
  ],
  [
    "Where is my data stored?",
    "In a local SQLite file under data/generated/, which Git ignores. Demo reruns replace only traces tagged traceforge_sample_v1 and keep everything else.",
  ],
  [
    "Where are the docs?",
    "The docs folder covers architecture, schema, evaluators, CI, privacy and a walkthrough.",
  ],
  [
    "Is it ready for production?",
    "No. It is local and single-process, has no authentication, and has had no load or security testing. Keep the server on loopback.",
  ],
];

export function Faq() {
  return (
    <section className="sec" id="faq">
      <h2>
        Any <Icon name="question" color="#ec4899" />{" "}
        <span className="m">questions?</span>
      </h2>
      <div className="faq">
        {FAQ.map(([question, answer]) => (
          <details key={question}>
            <summary>{question}</summary>
            <p>{answer}</p>
          </details>
        ))}
      </div>
    </section>
  );
}
