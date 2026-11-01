const PATHS = {
  check: "M5 12.5l4.5 4.5L19 7.5",
  shield: "M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z",
  bars: "M7 19v-6M12 19V6M17 19v-10",
  layers: "M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12v9M12 12L4 7.5",
  code: "M8 8l-4 4 4 4M16 8l4 4-4 4",
  database:
    "M5 6c0-1.7 3.1-3 7-3s7 1.3 7 3-3.1 3-7 3-7-1.3-7-3zM5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6",
  arrow: "M5 12h14M13 6l6 6-6 6",
  bulb: "M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z",
  close: "M6 6l12 12M18 6L6 18",
  question: "M9.5 9a2.6 2.6 0 115 .6c0 1.8-2.5 2.2-2.5 4M12 17.5h.01",
  alert: "M12 8v5M12 17h.01",
  list: "M5 7h14M5 12h14M5 17h14",
};

export default function Icon({
  name,
  color = "#8b5cf6",
  pulse = false,
  className = "ico",
}) {
  return (
    <i
      className={`${className}${pulse ? " pulse" : ""}`}
      style={{ "--c": color }}
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d={PATHS[name]} />
      </svg>
    </i>
  );
}
