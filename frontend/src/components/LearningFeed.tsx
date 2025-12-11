import { cn } from "@/lib/utils";
import { GlassCard } from "@/components/ui/glass-card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Play, CheckCircle2, Clock, FileText, Dumbbell, Headphones } from "lucide-react";

interface Lesson {
  id: string;
  title: string;
  duration: string;
  type: "video" | "practice" | "reading" | "audio";
  completed?: boolean;
  progress?: number;
}

interface LearningFeedProps {
  lessons: Lesson[];
  onLessonClick?: (id: string) => void;
  className?: string;
}

const typeIcons = {
  video: Play,
  practice: Dumbbell,
  reading: FileText,
  audio: Headphones,
};

const typeLabels = {
  video: "Video",
  practice: "Practice",
  reading: "Reading",
  audio: "Audio",
};

export function LearningFeed({ lessons, onLessonClick, className }: LearningFeedProps) {
  return (
    <div className={cn("space-y-3", className)}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-foreground">Today's Lessons</h3>
        <Badge variant="secondary">{lessons.length} items</Badge>
      </div>

      {lessons.map((lesson) => {
        const Icon = typeIcons[lesson.type];
        
        return (
          <div
            key={lesson.id}
            onClick={() => onLessonClick?.(lesson.id)}
            className={cn(
              "p-4 rounded-lg border border-border bg-card/50 transition-all duration-200 cursor-pointer",
              "hover:bg-card hover:border-primary/20",
              lesson.completed && "opacity-75"
            )}
          >
            <div className="flex items-start gap-3">
              <div
                className={cn(
                  "p-2 rounded-lg",
                  lesson.completed
                    ? "bg-success/10"
                    : "bg-secondary"
                )}
              >
                {lesson.completed ? (
                  <CheckCircle2 className="w-5 h-5 text-success" />
                ) : (
                  <Icon className="w-5 h-5 text-muted-foreground" />
                )}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <h4
                    className={cn(
                      "font-medium text-foreground",
                      lesson.completed && "line-through text-muted-foreground"
                    )}
                  >
                    {lesson.title}
                  </h4>
                  <Badge variant="outline" className="shrink-0 text-xs">
                    {typeLabels[lesson.type]}
                  </Badge>
                </div>
                
                <div className="flex items-center gap-3 mt-2">
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Clock className="w-3 h-3" />
                    {lesson.duration}
                  </div>
                  
                  {lesson.progress !== undefined && !lesson.completed && (
                    <div className="flex items-center gap-2 flex-1">
                      <Progress value={lesson.progress} className="h-1.5 flex-1" />
                      <span className="text-xs text-muted-foreground">
                        {lesson.progress}%
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
