import { Navbar } from "@/components/landing/Navbar";
import { HeroSection } from "@/components/landing/HeroSection";
import { Showcase } from "@/components/landing/Showcase";
import { ProblemSection } from "@/components/landing/ProblemSection";
import { TechSpecs } from "@/components/landing/TechSpecs";
import { FinalCTA } from "@/components/landing/FinalCTA";
import { Footer } from "@/components/landing/Footer";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0A0A0B] text-white selection:bg-brand-primary/30 font-sans">
      <Navbar />
      <main>
        <HeroSection />
        <ProblemSection />
        <TechSpecs />
        <Showcase />
        <FinalCTA />
      </main>
      <Footer />
    </div>
  );
}
