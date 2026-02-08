import { Navbar } from "@/components/landing/Navbar";
import { HeroSection } from "@/components/landing/HeroSection";
import { ProblemSection } from "@/components/landing/ProblemSection";
import { SocialProof } from "@/components/landing/SocialProof";
import { TechSpecs } from "@/components/landing/TechSpecs";
import { PricingSection } from "@/components/landing/PricingSection";
import { Footer } from "@/components/landing/Footer";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0A0A0B] text-white selection:bg-accent-primary/30 font-sans">
      <Navbar />
      <main>
        <HeroSection />
        <SocialProof />
        <ProblemSection />
        <TechSpecs />
        <PricingSection />
      </main>
      <Footer />
    </div>
  );
}
