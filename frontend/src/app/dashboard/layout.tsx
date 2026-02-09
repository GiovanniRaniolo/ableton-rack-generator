import { Shell } from "@/components/layout/Shell";
import { ProfileSyncProvider } from "@/components/providers/ProfileSyncProvider";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProfileSyncProvider>
      <Shell>{children}</Shell>
    </ProfileSyncProvider>
  );
}
