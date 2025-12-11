import { cn } from "@/lib/utils";
import { GlassCard } from "@/components/ui/glass-card";
import { Flame, Zap, Trophy, Star } from "lucide-react";

interface StreakCounterProps {
  days: number;
  className?: string;
}

export function StreakCounter({ days, className }: StreakCounterProps) {
  return (
    <GlassCard className={cn("", className)}>
      <div className="flex items-center gap-4">
        <div className="p-3 rounded-xl bg-warning/10">
          <Flame className="w-8 h-8 text-warning" />
        </div>
        <div className="flex-1">
          <p className="text-2xl font-bold text-foreground">{days} Days</p>
          <p className="text-sm text-muted-foreground">Learning Streak</p>
        </div>
      </div>

      {/* Weekly progress */}
      <div className="mt-4 pt-4 border-t border-border">
        <p className="text-xs text-muted-foreground mb-3">This Week</p>
        <div className="flex gap-2">
          {["M", "T", "W", "T", "F", "S", "S"].map((day, index) => (
            <div key={index} className="flex flex-col items-center gap-1.5 flex-1">
              <div
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium transition-colors",
                  index < 5
                    ? "bg-success/20 text-success"
                    : index === 5
                    ? "bg-warning/20 text-warning"
                    : "bg-secondary text-muted-foreground"
                )}
              >
                {index < 6 ? "✓" : day}
              </div>
              <span className="text-xs text-muted-foreground">{day}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements */}
      <div className="flex items-center gap-2 mt-4 pt-4 border-t border-border">
        <span className="text-xs text-muted-foreground">Achievements:</span>
        <div className="flex gap-1">
          {days >= 7 && (
            <div className="p-1.5 rounded-full bg-success/10" title="7-day streak">
              <Zap className="w-3 h-3 text-success" />
            </div>
          )}
          {days >= 30 && (
            <div className="p-1.5 rounded-full bg-primary/10" title="30-day streak">
              <Trophy className="w-3 h-3 text-primary" />
            </div>
          )}
          {days >= 100 && (
            <div className="p-1.5 rounded-full bg-accent/10" title="100-day streak">
              <Star className="w-3 h-3 text-accent" />
            </div>
          )}
        </div>
      </div>
    </GlassCard>
  );
}
