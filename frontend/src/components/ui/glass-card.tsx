import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export function GlassCard({ children, className, hover = false, onClick }: GlassCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        "rounded-xl p-6 glass",
        hover && "glass-hover cursor-pointer",
        className
      )}
    >
      {children}
    </div>
  );
}

interface ActionCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  onClick?: () => void;
  variant?: "default" | "primary" | "accent" | "success";
  className?: string;
}

export function ActionCard({
  icon: Icon,
  title,
  description,
  onClick,
  variant = "default",
  className,
}: ActionCardProps) {
  const iconWrapperClasses = {
    default: "bg-secondary text-foreground",
    primary: "bg-primary/10 text-primary",
    accent: "bg-accent/10 text-accent",
    success: "bg-success/10 text-success",
  };

  return (
    <GlassCard hover onClick={onClick} className={cn("group", className)}>
      <div className="flex items-start gap-4">
        <div
          className={cn(
            "p-3 rounded-lg transition-all duration-200 group-hover:scale-105",
            iconWrapperClasses[variant]
          )}
        >
          <Icon className="w-6 h-6" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
            {title}
          </h3>
          <p className="text-sm text-muted-foreground mt-1">{description}</p>
        </div>
      </div>
    </GlassCard>
  );
}

interface StatCardProps {
  value: string;
  label: string;
  icon?: LucideIcon;
  trend?: { value: number; positive: boolean };
  className?: string;
}

export function StatCard({ value, label, icon: Icon, trend, className }: StatCardProps) {
  return (
    <GlassCard className={cn("relative overflow-hidden", className)}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-2xl font-bold text-foreground">{value}</p>
          <p className="text-sm text-muted-foreground mt-1">{label}</p>
          {trend && (
            <p
              className={cn(
                "text-xs mt-2 font-medium",
                trend.positive ? "text-success" : "text-destructive"
              )}
            >
              {trend.positive ? "+" : "-"}{trend.value}%
            </p>
          )}
        </div>
        {Icon && (
          <div className="p-3 rounded-lg bg-secondary">
            <Icon className="w-6 h-6 text-muted-foreground" />
          </div>
        )}
      </div>
    </GlassCard>
  );
}
