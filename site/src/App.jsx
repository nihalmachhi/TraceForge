import { useEffect, useState } from "react";
import ReferenceLayout from "./ReferenceLayout.jsx";
import "./styles.css";

export default function App() {
  const [active, setActive] = useState(0);
  const [paused, setPaused] = useState(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );
  const [holding, setHolding] = useState(false);

  useEffect(() => {
    if (paused || holding) return undefined;
    const timer = window.setInterval(
      () => setActive((index) => (index + 1) % 5),
      7000,
    );
    return () => window.clearInterval(timer);
  }, [paused, holding]);

  useEffect(() => {
    const targets = [
      document.getElementById("win"),
      document.getElementById("tl"),
    ].filter(Boolean);
    const pause = () => setHolding(true);
    const resume = () => setHolding(false);
    const visibility = () => setHolding(document.hidden);
    targets.forEach((target) => {
      target.addEventListener("mouseenter", pause);
      target.addEventListener("mouseleave", resume);
      target.addEventListener("focusin", pause);
      target.addEventListener("focusout", resume);
    });
    document.addEventListener("visibilitychange", visibility);
    return () => {
      targets.forEach((target) => {
        target.removeEventListener("mouseenter", pause);
        target.removeEventListener("mouseleave", resume);
        target.removeEventListener("focusin", pause);
        target.removeEventListener("focusout", resume);
      });
      document.removeEventListener("visibilitychange", visibility);
    };
  }, []);

  useEffect(() => {
    const callout = document.querySelector(".rv-wrap");
    if (!callout || !("IntersectionObserver" in window)) return undefined;
    callout.classList.add("arm");
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          callout.classList.add("in");
          observer.disconnect();
        }
      },
      { threshold: 0.25 },
    );
    observer.observe(callout);
    return () => observer.disconnect();
  }, []);

  return (
    <ReferenceLayout
      active={active}
      setActive={setActive}
      paused={paused}
      holding={holding}
      onToggle={() => setPaused((value) => !value)}
    />
  );
}
