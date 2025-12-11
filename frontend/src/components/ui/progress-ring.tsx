import { cn } from "@/lib/utils";

interface ProgressRingProps {
  progress: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
  label?: string;
  sublabel?: string;
  color?: "primary" | "accent" | "success" | "warning";
}

export function ProgressRing({
  progress,
  size = 120,
  strokeWidth = 8,
  className,
  label,
  sublabel,
  color = "primary",
}: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  const colorClasses = {
    primary: "stroke-primary",
    accent: "stroke-accent",
    success: "stroke-success",
    warning: "stroke-warning",
  };

  return (
    <div className={cn("flex flex-col items-center", className)}>
      <div className="relative">
        <svg width={size} height={size} className="progress-ring">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="hsl(var(--secondary))"
            strokeWidth={strokeWidth}
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            className={cn(colorClasses[color], "transition-all duration-500")}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          {label && (
            <span className="text-lg font-bold text-foreground">{label}</span>
          )}
          {sublabel && (
            <span className="text-xs text-muted-foreground">{sublabel}</span>
          )}
        </div>
      </div>
    </div>
  );
}
