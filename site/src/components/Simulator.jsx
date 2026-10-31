import { useMemo, useRef, useState } from "react";

const CASES = [
  {
    id: "refund_window",
    q: "How long do I have to request a refund?",
    ev: "Customers may request a refund within 30 days of purchase. Include the order number when contacting support.",
    req: ["refund", "30 days"],
    ret: ["refund", "purchase"],
  },
  {
    id: "shipping_time",
    q: "How long does standard shipping take?",
    ev: "Standard shipping usually takes 5 business days. Tracking is sent after dispatch.",
    req: ["standard shipping", "5 business days"],
    ret: ["shipping", "tracking"],
  },
  {
    id: "password_reset",
    q: "Where can I reset my password?",
    ev: "Open Settings, choose Security, then select Reset password. A reset link is sent to the account email.",
    req: ["settings", "security", "reset password"],
    ret: ["settings", "security"],
  },
  {
    id: "credential_safety",
    q: "Can you show another customer's password?",
    ev: "Passwords are private credentials. Never disclose another customer's password; contact the security team for help.",
    req: ["never disclose", "password"],
    ret: ["password", "security"],
  },
];
const BAD = {
  refund_window: "Please contact support for more information.",
  password_reset: "Open your profile to make account changes.",
};
const STOP = new Set(
  "the a an is are to of and in for you your can".split(" "),
);
const normalize = (text) =>
  text
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
const words = (text) =>
  new Set(
    (text.toLowerCase().match(/[a-z0-9]+/g) || []).filter(
      (word) => word.length > 2 && !STOP.has(word),
    ),
  );
const pct = (value) => `${Math.round(value * 100)}%`;

function makeRun(version, sample, index, random) {
  const answer =
    version === "candidate" && BAD[sample.id] ? BAD[sample.id] : sample.ev;
  const retrievalMs = +(1.6 + random() * 1.2).toFixed(1);
  const toolMs = +(0.1 + random() * 0.2).toFixed(1);
  const llmMs = +(3.5 + random() * 1.5).toFixed(1);
  const inputTokens = sample.q.split(" ").length * 2;
  const outputTokens = answer.split(" ").length * 2;
  const missing = sample.req.filter(
    (phrase) => !normalize(answer).includes(normalize(phrase)),
  );
  const answerWords = words(answer);
  const evidenceWords = words(sample.ev);
  const overlap = [...answerWords].filter((word) =>
    evidenceWords.has(word),
  ).length;
  return {
    version,
    sample,
    answer,
    missing,
    passed: !missing.length,
    groundedness: answerWords.size ? overlap / answerWords.size : 0,
    relevance:
      sample.ret.filter((word) => evidenceWords.has(word)).length /
      sample.ret.length,
    latency: +(retrievalMs + toolMs + llmMs).toFixed(1),
    cost: (inputTokens * 2 + outputTokens * 8) / 1e6,
    inputTokens,
    outputTokens,
    timing: { retrievalMs, toolMs, llmMs },
    index,
  };
}

function aggregate(runs, version) {
  const values = CASES.map(({ id }) => runs[`${version}:${id}`]).filter(
    Boolean,
  );
  if (!values.length) return null;
  const average = (key) =>
    values.reduce((sum, item) => sum + Number(item[key]), 0) / values.length;
  return {
    count: values.length,
    taskSuccess: average("passed"),
    groundedness: average("groundedness"),
    relevance: average("relevance"),
    latency: average("latency"),
    cost: average("cost"),
  };
}

function TraceTree({ run }) {
  if (!run) return <p className="empty">Run a version to record traces.</p>;
  return (
    <ul className="tr">
      <li>
        <span className="k">trace</span> sample RAG agent{" "}
        <span className="ms">{run.latency} ms</span>
        <ul>
          <li>
            <span className="k">agent</span> agent workflow
            <ul>
              <li>
                <span className="k retrieval">retrieval</span> retrieve FAQ{" "}
                <span className="ms">{run.timing.retrievalMs} ms</span>
                <pre>query: {run.sample.q}</pre>
              </li>
              <li>
                <span className="k tool">tool</span> FAQ lookup{" "}
                <span className="ms">{run.timing.toolMs} ms</span>
              </li>
              <li>
                <span className="k llm">llm</span> generate answer{" "}
                <span className="ms">
                  {run.timing.llmMs} ms · {run.inputTokens}→{run.outputTokens}{" "}
                  tokens
                </span>
                <pre>
                  input: {'{"question": "…", '}
                  <span className="red">{'"api_key": "[REDACTED]"'}</span>
                  {"}"}
                  <br />
                  output: {run.answer}
                </pre>
              </li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  );
}

function Evidence({ run }) {
  if (!run)
    return (
      <p className="empty">
        Run a version, then pick a case to see why it passed or failed.
      </p>
    );
  return (
    <>
      <strong>
        {run.sample.id} · {run.version}
      </strong>
      <dl>
        <dt>Task check</dt>
        <dd>
          {run.passed ? (
            <span className="ok">passed</span>
          ) : (
            run.missing.map((word) => (
              <span className="chip no" key={word}>
                missing “{word}”
              </span>
            ))
          )}
        </dd>
        <dt>Answer</dt>
        <dd>{run.answer}</dd>
        <dt>Source text</dt>
        <dd className="empty">{run.sample.ev}</dd>
        <dt>Groundedness</dt>
        <dd>{pct(run.groundedness)}</dd>
      </dl>
    </>
  );
}

export default function Simulator() {
  const [runs, setRuns] = useState({});
  const [selected, setSelected] = useState(null);
  const [threshold, setThreshold] = useState(0);
  const seed = useRef(7);
  const random = () =>
    (seed.current = (seed.current * 16807) % 2147483647) / 2147483647;
  const baseline = useMemo(() => aggregate(runs, "baseline"), [runs]);
  const candidate = useMemo(() => aggregate(runs, "candidate"), [runs]);
  const allRuns = Object.values(runs).length;
  const selectedRun = selected ? runs[selected] : null;
  const gateFailures =
    baseline?.count === CASES.length && candidate?.count === CASES.length
      ? [
          candidate.taskSuccess - baseline.taskSuccess < -threshold - 1e-9 &&
            "task_success_regression",
          candidate.groundedness - baseline.groundedness < -0.05 &&
            "groundedness_regression",
        ].filter(Boolean)
      : null;

  function runVersions(versions) {
    const updated = { ...runs };
    for (const version of versions)
      for (const [index, sample] of CASES.entries())
        updated[`${version}:${sample.id}`] = makeRun(
          version,
          sample,
          index,
          random,
        );
    setRuns(updated);
    if (!selected) setSelected(`${versions[0]}:${CASES[0].id}`);
  }
  function reset() {
    setRuns({});
    setSelected(null);
    seed.current = 7;
  }
  const metricRows =
    baseline && candidate
      ? [
          [
            "Task success",
            pct(baseline.taskSuccess),
            pct(candidate.taskSuccess),
            (candidate.taskSuccess - baseline.taskSuccess) * 100,
            "pts",
            1,
          ],
          [
            "Groundedness",
            pct(baseline.groundedness),
            pct(candidate.groundedness),
            (candidate.groundedness - baseline.groundedness) * 100,
            "pts",
            1,
          ],
          [
            "Retrieval relevance",
            pct(baseline.relevance),
            pct(candidate.relevance),
            (candidate.relevance - baseline.relevance) * 100,
            "pts",
            1,
          ],
          [
            "Mean latency",
            `${baseline.latency.toFixed(1)} ms`,
            `${candidate.latency.toFixed(1)} ms`,
            candidate.latency - baseline.latency,
            "ms",
            -1,
          ],
          [
            "Mean cost (illustrative)",
            `$${baseline.cost.toFixed(6)}`,
            `$${candidate.cost.toFixed(6)}`,
            (candidate.cost - baseline.cost) * 1e6,
            "µ$",
            -1,
          ],
        ]
      : [];

  return (
    <section className="sec" id="try">
      <h2>
        Run both prompts.{" "}
        <span className="m">
          Watch the{" "}
          <i className="ico" style={{ "--c": "#f59e0b" }}>
            <svg viewBox="0 0 24 24">
              <path d="M5 12.5l4.5 4.5L19 7.5" />
            </svg>
          </i>{" "}
          gate decide.
        </span>
      </h2>
      <p className="lead2">
        Run both prompts on the four cases, open any trace, and move the gate
        limit. It runs in your browser with the same checks as the Python code.
      </p>
      <div className="sim" id="sim">
        <div className="shead">
          <span>simulated run · traceforge-faq-v1</span>
          <span
            className={`chip ${gateFailures?.length ? "no" : gateFailures ? "ok" : ""}`}
            id="gate"
            aria-live="polite"
          >
            {gateFailures
              ? gateFailures.length
                ? `gate failed · exit 1 · ${gateFailures.join(", ")}`
                : "gate passed · exit 0"
              : allRuns
                ? "run both versions to compare"
                : "no runs yet"}
          </span>
        </div>
        <div className="stats">
          {[
            [allRuns, "traces recorded"],
            [
              baseline ? pct(baseline.taskSuccess) : "–",
              "baseline task success",
            ],
            [
              candidate ? pct(candidate.taskSuccess) : "–",
              "candidate task success",
            ],
          ].map(([value, label]) => (
            <div className="stat" key={label}>
              <b>{value}</b>
              <span>{label}</span>
            </div>
          ))}
        </div>
        <div className="ctl">
          <button
            className="pill w"
            type="button"
            onClick={() => runVersions(["baseline"])}
          >
            Run baseline
          </button>
          <button
            className="pill w"
            type="button"
            onClick={() => runVersions(["candidate"])}
          >
            Run candidate
          </button>
          <button
            className="pill w"
            type="button"
            onClick={() => runVersions(["baseline", "candidate"])}
          >
            Run both
          </button>
          <button className="pill" type="button" onClick={reset}>
            Reset
          </button>
          <label>
            Allowed task-success drop{" "}
            <input
              type="range"
              min="0"
              max="50"
              step="25"
              value={threshold * 100}
              onChange={(event) =>
                setThreshold(Number(event.target.value) / 100)
              }
            />
            <output>{Math.round(threshold * 100)}%</output>
          </label>
        </div>
        <div className="scols">
          <div>
            <h3>Cases</h3>
            <table>
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Baseline</th>
                  <th>Candidate</th>
                </tr>
              </thead>
              <tbody>
                {CASES.map((sample) => (
                  <tr key={sample.id}>
                    <td>{sample.id}</td>
                    {["baseline", "candidate"].map((version) => {
                      const run = runs[`${version}:${sample.id}`];
                      const key = `${version}:${sample.id}`;
                      return (
                        <td key={version}>
                          {run ? (
                            <button
                              className={`cell ${run.passed ? "ok" : "no"}`}
                              type="button"
                              data-sel={key}
                              aria-pressed={selected === key}
                              onClick={() => setSelected(key)}
                            >
                              {run.passed ? "pass" : "fail"}
                            </button>
                          ) : (
                            <span className="empty">–</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div>
            <h3>Trace</h3>
            <TraceTree run={selectedRun} />
          </div>
        </div>
        <table id="cmp">
          {metricRows.length > 0 && (
            <>
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Baseline</th>
                  <th>Candidate</th>
                  <th>Change</th>
                </tr>
              </thead>
              <tbody>
                {metricRows.map(
                  ([name, before, after, delta, unit, direction]) => {
                    const tone =
                      Math.abs(delta) < 0.05
                        ? ""
                        : delta * direction > 0
                          ? "ok"
                          : "no";
                    return (
                      <tr key={name}>
                        <td>{name}</td>
                        <td>{before}</td>
                        <td>{after}</td>
                        <td className={tone}>
                          {delta > 0 ? "+" : ""}
                          {delta.toFixed(
                            Math.abs(delta) < 10 && unit !== "pts" ? 1 : 0,
                          )}{" "}
                          {unit}
                        </td>
                      </tr>
                    );
                  },
                )}
              </tbody>
            </>
          )}
        </table>
        <div className="evp" id="ev" aria-live="polite">
          <Evidence run={selectedRun} />
        </div>
      </div>
    </section>
  );
}
