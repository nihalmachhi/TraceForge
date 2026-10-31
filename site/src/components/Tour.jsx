const samples = [
  "refund_window",
  "shipping_time",
  "password_reset",
  "credential_safety",
];

export function TourTabs({ active, onChange }) {
  return (
    <div
      className="tl"
      role="tablist"
      aria-label="What TraceForge does"
      id="tl"
    >
      {["Record", "Redact", "Evaluate", "Compare", "Gate"].map(
        (name, index) => (
          <button
            className="tab"
            type="button"
            role="tab"
            aria-selected={active === index}
            key={name}
            onClick={() => onChange(index)}
          >
            {name}
            <i className="bar" />
          </button>
        ),
      )}
    </div>
  );
}

function Span({ kind, label, detail = "", depth = 0, index }) {
  return (
    <div className="sp-r rise" style={{ "--i": index, marginLeft: depth * 22 }}>
      <span className={`k ${kind}`}>{kind}</span>
      {label}
      <span className="ms">{detail}</span>
    </div>
  );
}
function Record() {
  return (
    <>
      <p className="tx rise">
        One request becomes one trace. Each step is a span linked to its parent,
        so you can see where the time and tokens went.
      </p>
      <Span kind="trace" label="sample RAG agent" detail="6.9 ms" index={1} />
      <Span kind="agent" label="agent workflow" depth={1} index={2} />
      <Span
        kind="retrieval"
        label="retrieve FAQ"
        detail="2.1 ms"
        depth={2}
        index={3}
      />
      <Span
        kind="tool"
        label="FAQ lookup"
        detail="0.2 ms"
        depth={2}
        index={4}
      />
      <Span
        kind="llm"
        label="generate answer"
        detail="4.4 ms"
        depth={2}
        index={5}
      />
    </>
  );
}
function Redact() {
  const data = [
    ["question", '"How long do I have to request a refund?"'],
    ["api_key", '"tf_demo_fake_secret"', "[REDACTED]"],
    ["authorization", '"Bearer eyJhbGciOiJI…"', "[REDACTED]"],
    ["note", '"reach me at dana@example.com"', '"reach me at [REDACTED]"'],
  ];
  return (
    <>
      <p className="tx rise">
        Sensitive-looking values are replaced before anything reaches SQLite.
        Watch the captured values turn into what is stored.
      </p>
      {data.map(([key, value, masked], index) => (
        <div className="rw rise" style={{ "--i": index + 1 }} key={key}>
          <span>{key}</span>
          {masked ? (
            <span className="v" style={{ "--i": index + 1 }}>
              <s>{value}</s>
              <b>{masked}</b>
            </span>
          ) : (
            <span>{value}</span>
          )}
        </div>
      ))}
    </>
  );
}
function Evaluate() {
  const pct = [20, 100, 40, 100];
  return (
    <>
      <p className="tx rise">
        Each answer must contain the facts the case requires. The bar shows how
        much of the answer is grounded in the retrieved text.
      </p>
      <table>
        <thead>
          <tr>
            <th>Case</th>
            <th>Baseline</th>
            <th>Candidate</th>
            <th>Grounded</th>
          </tr>
        </thead>
        <tbody>
          {samples.map((id, index) => (
            <tr className="rise" style={{ "--i": index + 1 }} key={id}>
              <td>{id}</td>
              <td className="ok">pass</td>
              <td className={index % 2 ? "ok" : "no"}>
                {index % 2 ? "pass" : "fail"}
              </td>
              <td>
                <div className="track">
                  <div
                    className="grow"
                    style={{
                      "--w": `${pct[index]}%`,
                      "--c": index % 2 ? "var(--ok)" : "var(--bad)",
                      "--i": index + 1,
                    }}
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
function Metric({
  index,
  name,
  baseline,
  candidate,
  before,
  after,
  change,
  bad = false,
}) {
  return (
    <div className="m rise" style={{ "--i": index }}>
      <div>
        <span>{name}</span>
        <span className={bad ? "no" : "ok"}>{change}</span>
      </div>
      {[before, after].map((width, n) => (
        <div className="track" key={n}>
          <div
            className="grow"
            style={{
              "--w": `${width}%`,
              "--c": n && bad ? "var(--bad)" : "#62626b",
              "--i": index + n,
            }}
          />
        </div>
      ))}
      <small>
        baseline {baseline} · candidate {candidate}
      </small>
    </div>
  );
}
function Compare() {
  return (
    <>
      <Metric
        index={1}
        name="Task success"
        baseline="100%"
        candidate="50%"
        before={100}
        after={50}
        change="−50 pts"
        bad
      />
      <Metric
        index={3}
        name="Groundedness"
        baseline="100%"
        candidate="65%"
        before={100}
        after={65}
        change="−35 pts"
        bad
      />
      <Metric
        index={5}
        name="Retrieval relevance"
        baseline="100%"
        candidate="100%"
        before={100}
        after={100}
        change="no change"
      />
      <Metric
        index={7}
        name="Mean cost (illustrative)"
        baseline="$0.000271"
        candidate="$0.000187"
        before={100}
        after={69}
        change="−31%"
      />
    </>
  );
}
function Gate() {
  return (
    <div className="term">
      <div className="rise">
        <span className="c">$</span> .\scripts\run.ps1 gate
      </div>
      <div className="rise" style={{ "--i": 2 }}>
        {'{ "passed": '}
        <span className="no">false</span>,
      </div>
      <div className="rise" style={{ "--i": 3 }}>
        {'  "failures": ["task_success_regression",'}
      </div>
      <div className="rise" style={{ "--i": 3 }}>
        {'    "groundedness_regression"] }'}
      </div>
      <div className="rise no" style={{ "--i": 4 }}>
        exit code 1
      </div>
      <div className="rise" style={{ "--i": 6, marginTop: 10 }}>
        <span className="c">$</span> .\scripts\run.ps1 gate --max-task-drop 0.5
      </div>
      <div className="rise" style={{ "--i": 8 }}>
        {'{ "failures": ["groundedness_regression"] }'}
      </div>
      <div className="rise no" style={{ "--i": 9 }}>
        exit code 1
      </div>
    </div>
  );
}

const panels = [
  [
    "refund_window · candidate",
    "Trace recorded in 6.9 ms",
    Record,
    <>
      <h4 className="rise">Totals</h4>
      <ul className="lst">
        <li className="rise" style={{ "--i": 1 }}>
          Spans <b style={{ float: "right" }}>5</b>
        </li>
        <li className="rise" style={{ "--i": 2 }}>
          Tokens in → out <b style={{ float: "right" }}>9 → 8</b>
        </li>
        <li className="rise" style={{ "--i": 3 }}>
          Estimated cost <b style={{ float: "right" }}>$0.000187</b>
        </li>
      </ul>
      <p
        className="tx rise"
        style={{ "--i": 4, color: "var(--mu)", fontSize: ".84rem" }}
      >
        Parents are tracked with context-local state, so there are no IDs to
        pass around.
      </p>
    </>,
  ],
  [
    "Redaction before storage",
    "Applied to every input, output and attribute",
    Redact,
    <>
      <h4 className="rise">What it catches</h4>
      <ul className="lst">
        <li className="rise" style={{ "--i": 1 }}>
          <b>Keys</b> api_key, token, secret, password
        </li>
        <li className="rise" style={{ "--i": 2 }}>
          <b>Tokens</b> Bearer and sk- values in text
        </li>
        <li className="rise" style={{ "--i": 3 }}>
          <b>Emails</b> and key=value strings
        </li>
      </ul>
      <p
        className="tx rise"
        style={{ "--i": 4, color: "var(--mu)", fontSize: ".84rem" }}
      >
        Best effort. It cannot promise to find arbitrary personal data.
      </p>
    </>,
  ],
  [
    "Same four cases, both prompts",
    "traceforge-faq-v1 · deterministic checks",
    Evaluate,
    <>
      <h4 className="rise">Why refund_window failed</h4>
      <p
        className="tx rise"
        style={{ "--i": 1, fontSize: ".86rem", color: "var(--mu)" }}
      >
        “Please contact support for more information.”
      </p>
      <span className="chip no rise" style={{ "--i": 2 }}>
        missing “refund”
      </span>
      <span className="chip no rise" style={{ "--i": 3 }}>
        missing “30 days”
      </span>
    </>,
  ],
  [
    "Baseline against candidate",
    "Grey is the baseline, colour is the candidate",
    Compare,
    <>
      <h4 className="rise">Regressed cases</h4>
      <span className="chip no rise" style={{ "--i": 1 }}>
        refund_window
      </span>
      <span className="chip no rise" style={{ "--i": 2 }}>
        password_reset
      </span>
      <p
        className="tx rise"
        style={{ "--i": 3, color: "var(--mu)", fontSize: ".84rem" }}
      >
        Both passed with the baseline prompt and fail with the candidate.
      </p>
    </>,
  ],
  [
    "Fail the build on a regression",
    "Exit code 1 stops the CI step",
    Gate,
    <>
      <h4 className="rise">Thresholds</h4>
      <ul className="lst">
        <li className="rise" style={{ "--i": 1 }}>
          <b>Task success</b> may drop 0 points
        </li>
        <li className="rise" style={{ "--i": 2 }}>
          <b>Groundedness</b> may drop 5 points
        </li>
      </ul>
      <p
        className="tx rise"
        style={{ "--i": 3, color: "var(--mu)", fontSize: ".84rem" }}
      >
        Loosen the task limit with --max-task-drop. Each limit is checked on its
        own.
      </p>
    </>,
  ],
];

export default function TourSlide({ active }) {
  const [title, subtitle, Main, aside] = panels[active];
  return (
    <div className="body" id="body">
      <div className="col cv">
        <h3>{title}</h3>
        <div className="sub">{subtitle}</div>
        <Main />
      </div>
      <div className="col cv">{aside}</div>
    </div>
  );
}
