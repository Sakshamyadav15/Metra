import { cn } from "@/lib/utils";
import { Brain, Activity } from "lucide-react";
import { GlassCard } from "@/components/ui/glass-card";

interface LearningTwinVisualizationProps {
  cognitiveState?: "learning" | "processing" | "resting" | "active";
  masteryLevel?: number;
  className?: string;
}

export function LearningTwinVisualization({
  cognitiveState = "active",
  masteryLevel = 72,
  className,
}: LearningTwinVisualizationProps) {
  const stateLabels = {
    learning: "Learning Mode",
    processing: "Processing Knowledge",
    resting: "Consolidating Memory",
    active: "Ready to Learn",
  };

  const stateColors = {
    learning: "bg-primary/20 border-primary/30",
    processing: "bg-accent/20 border-accent/30",
    resting: "bg-muted border-muted",
    active: "bg-success/20 border-success/30",
  };

  const stateIndicatorColors = {
    learning: "bg-primary",
    processing: "bg-accent",
    resting: "bg-muted-foreground",
    active: "bg-success",
  };

  return (
    <GlassCard className={cn("relative overflow-hidden", className)}>
      <div className="flex flex-col items-center py-6">
        {/* Main visualization */}
        <div className="relative">
          {/* Outer ring */}
          <div
            className={cn(
              "w-32 h-32 rounded-full border-2 flex items-center justify-center transition-all duration-500",
              stateColors[cognitiveState]
            )}
          >
            {/* Inner circle with brain icon */}
            <div className="w-24 h-24 rounded-full bg-card flex items-center justify-center shadow-inner">
              <Brain className="w-12 h-12 text-primary" />
            </div>
          </div>

          {/* Mastery indicator */}
          <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-card px-3 py-1 rounded-full border border-border shadow-sm">
            <span className="text-sm font-semibold text-foreground">{masteryLevel}%</span>
          </div>
        </div>

        {/* State label */}
        <div className="text-center mt-6">
          <h3 className="font-semibold text-lg text-foreground mb-1">
            Your Learning Twin
          </h3>
          <div className="flex items-center gap-2 justify-center">
            <div
              className={cn(
                "w-2 h-2 rounded-full",
                stateIndicatorColors[cognitiveState]
              )}
            />
            <span className="text-sm text-muted-foreground">
              {stateLabels[cognitiveState]}
            </span>
          </div>
        </div>

        {/* Stats row */}
        <div className="flex items-center gap-6 mt-6 pt-4 border-t border-border w-full justify-center">
          <div className="text-center">
            <div className="flex items-center gap-1 justify-center text-muted-foreground">
              <Activity className="w-4 h-4" />
              <span className="text-xs">Activity</span>
            </div>
            <p className="text-lg font-semibold text-foreground mt-1">High</p>
          </div>
          <div className="w-px h-10 bg-border" />
          <div className="text-center">
            <div className="flex items-center gap-1 justify-center text-muted-foreground">
              <Brain className="w-4 h-4" />
              <span className="text-xs">Focus</span>
            </div>
            <p className="text-lg font-semibold text-foreground mt-1">94%</p>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
