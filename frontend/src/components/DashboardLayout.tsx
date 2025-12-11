import {
  Home,
  Brain,
  MessageSquare,
  BookOpen,
  Mic,
  ClipboardCheck,
  Calendar,
  Settings,
  User,
  LogOut,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { NavLink } from "@/components/NavLink";

const navItems = [
  { icon: Home, label: "Dashboard", href: "/" },
  { icon: Brain, label: "Learning Profile", href: "/profile" },
  { icon: MessageSquare, label: "AI Chat", href: "/chat" },
  { icon: BookOpen, label: "Lessons", href: "/lessons" },
  { icon: Mic, label: "Speech Studio", href: "/speech" },
  { icon: ClipboardCheck, label: "Assessments", href: "/assessments" },
  { icon: Calendar, label: "Learning Path", href: "/path" },
];

const bottomItems = [
  { icon: Settings, label: "Settings", href: "/settings" },
  { icon: User, label: "Profile", href: "/account" },
];

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside
        className={cn(
          "flex flex-col border-r border-border bg-card transition-all duration-300",
          collapsed ? "w-[70px]" : "w-[260px]"
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-border">
          {!collapsed && (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                <Brain className="w-5 h-5 text-primary" />
              </div>
              <span className="font-semibold text-foreground">SkillTwin</span>
            </div>
          )}
          {collapsed && (
            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center mx-auto">
              <Brain className="w-5 h-5 text-primary" />
            </div>
          )}
          <Button
            variant="ghost"
            size="icon"
            className={cn("h-8 w-8", collapsed && "absolute right-[-12px] z-10 bg-card border border-border rounded-full")}
            onClick={() => setCollapsed(!collapsed)}
          >
            {collapsed ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <ChevronLeft className="w-4 h-4" />
            )}
          </Button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200",
                "text-muted-foreground hover:text-foreground hover:bg-secondary",
                collapsed && "justify-center"
              )}
              activeClassName="bg-primary/10 text-primary"
            >
              <item.icon className="w-5 h-5 shrink-0" />
              {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* Bottom items */}
        <div className="p-3 space-y-1 border-t border-border">
          {bottomItems.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200",
                "text-muted-foreground hover:text-foreground hover:bg-secondary",
                collapsed && "justify-center"
              )}
              activeClassName="bg-primary/10 text-primary"
            >
              <item.icon className="w-5 h-5 shrink-0" />
              {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
            </NavLink>
          ))}
          <button
            className={cn(
              "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 w-full",
              "text-muted-foreground hover:text-destructive hover:bg-destructive/10",
              collapsed && "justify-center"
            )}
          >
            <LogOut className="w-5 h-5 shrink-0" />
            {!collapsed && <span className="text-sm font-medium">Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
