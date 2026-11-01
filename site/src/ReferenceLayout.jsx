import Simulator from "./components/Simulator.jsx";
import SiteFooter, { ClosingCta } from "./components/SiteFooter.jsx";
import SiteHeader from "./components/SiteHeader.jsx";
import {
  Faq,
  Features,
  Pipeline,
  QuickStart,
  Results,
  Scope,
} from "./components/Sections.jsx";

export default function ReferenceLayout({
  active,
  setActive,
  paused,
  holding,
  onToggle,
  report,
}) {
  return (
    <>
      <div className="wrap">
        <SiteHeader
          active={active}
          setActive={setActive}
          paused={paused}
          holding={holding}
          onToggle={onToggle}
          report={report}
        />
        <Pipeline />
        <Simulator />
        <Results />
        <Features />
        <QuickStart />
        <Scope />
        <Faq />
        <ClosingCta />
      </div>
      <SiteFooter />
    </>
  );
}
