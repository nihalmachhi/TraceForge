import Icon from "./Icons.jsx";
import { Brand } from "./SiteHeader.jsx";

const GITHUB_URL = "https://github.com/nihalmachhi/TraceForge";

const ARCH_NODES = [
  { x: 0, delay: "0.0s", lines: ["Fixed task", "cases"] },
  { x: 142, delay: "0.9s", lines: ["Deterministic", "demo agent"] },
  {
    x: 284,
    delay: "1.8s",
    lines: ["Nested", "retrieval, tool,", "and model spans"],
  },
  { x: 426, delay: "2.7s", lines: ["Redact", "sensitive-", "looking values"] },
  { x: 568, delay: "3.6s", lines: ["SQLite trace", "store"] },
  {
    x: 710,
    delay: "4.5s",
    lines: ["Task, quality,", "and cost", "comparison"],
  },
  {
    x: 852,
    delay: "5.4s",
    lines: ["Dashboard and", "regression gate"],
    last: true,
  },
];

const ARCH_LINKS = [112, 254, 396, 538, 680, 822];

function Architecture() {
  return (
    <svg
      className="flow arch"
      viewBox="0 0 964 90"
      role="img"
      aria-label="TraceForge pipeline: fixed task cases, deterministic demo agent, nested spans, redaction, SQLite trace store, comparison, dashboard and regression gate"
    >
      {ARCH_LINKS.map((x) => (
        <path className="fl" d={`M${x} 45H${x + 30}`} key={x} />
      ))}
      {ARCH_NODES.map((node) => {
        const lineHeight = 13;
        const startY = 45 - ((node.lines.length - 1) * lineHeight) / 2 + 3.5;
        return (
          <g
            className={`gn st${node.last ? " last" : ""}`}
            style={{ "--d": node.delay }}
            key={node.x}
          >
            <rect x={node.x} y="12.0" width="112" height="66" rx="9" />
            <text textAnchor="middle">
              {node.lines.map((line, index) => (
                <tspan
                  x={node.x + 56}
                  y={startY + index * lineHeight}
                  key={line}
                >
                  {line}
                </tspan>
              ))}
            </text>
          </g>
        );
      })}
      <circle r="3.2" fill="#f4f4f5">
        <animateMotion dur="6.3s" repeatCount="indefinite" path="M0 45H964" />
      </circle>
    </svg>
  );
}

export function ClosingCta() {
  return (
    <section className="cta2 rv-wrap" aria-label="Get started">
      <div className="rv archw" style={{ "--r": "0" }}>
        <Architecture />
      </div>
      <h2 className="rv" style={{ "--r": "1" }}>
        Run it.
        <br />
        <span className="m">
          Watch it get <Icon name="alert" color="#ef4444" pulse /> caught.
        </span>
      </h2>
      <div className="btns rv" style={{ "--r": "2" }}>
        <a className="pill w" href={GITHUB_URL}>
          View on GitHub
        </a>
        <a className="pill" href="#try">
          Back to the simulator
        </a>
      </div>
    </section>
  );
}

export default function SiteFooter() {
  return (
    <footer className="wrap">
      <div className="foot">
        <div className="fcols">
          <div>
            <Brand />
            <p className="tg">
              A local, synthetic tracer and regression tester for AI agents.
            </p>
          </div>
          <div>
            <h5>Product</h5>
            <ul>
              <li>
                <a href="#top">Overview</a>
              </li>
              <li>
                <a href="#how">Pipeline</a>
              </li>
              <li>
                <a href="#try">Simulator</a>
              </li>
              <li>
                <a href="#results">Results</a>
              </li>
            </ul>
          </div>
          <div>
            <h5>Run it</h5>
            <ul>
              <li>
                <a href="#features">Features</a>
              </li>
              <li>
                <a href="#start">Quick start</a>
              </li>
              <li>
                <a href="#faq">FAQ</a>
              </li>
            </ul>
          </div>
          <div>
            <h5>Source</h5>
            <ul>
              <li>
                <a href={GITHUB_URL}>GitHub</a>
              </li>
              <li>
                <a href={`${GITHUB_URL}/tree/main/docs`}>Docs</a>
              </li>
              <li>
                <a href={`${GITHUB_URL}/tree/main/src/traceforge`}>
                  Source code
                </a>
              </li>
              <li>
                <a href={`${GITHUB_URL}/issues`}>Issues</a>
              </li>
            </ul>
          </div>
        </div>
        <div className="fbot">
          <span>
            Synthetic demo. Scores, costs and latencies are illustrative, not
            real model quality or provider pricing.
          </span>
          <span>Python · SQLite · JSON</span>
        </div>
        <div className="mark" aria-hidden="true">
          TraceForge
        </div>
      </div>
    </footer>
  );
}
