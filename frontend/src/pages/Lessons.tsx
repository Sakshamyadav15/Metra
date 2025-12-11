import { DashboardLayout } from "@/components/DashboardLayout";
import { GlassCard } from "@/components/ui/glass-card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { 
  BookOpen, 
  Play, 
  Clock, 
  CheckCircle2, 
  Lock,
  ChevronRight 
} from "lucide-react";

const lessons = [
  {
    id: "1",
    module: "Introduction to Machine Learning",
    lessons: [
      { title: "What is Machine Learning?", duration: "15 min", completed: true },
      { title: "Types of Learning", duration: "12 min", completed: true },
      { title: "Setting Up Your Environment", duration: "20 min", completed: false, progress: 60 },
    ],
    progress: 70,
  },
  {
    id: "2",
    module: "Neural Networks Fundamentals",
    lessons: [
      { title: "Introduction to Neural Networks", duration: "18 min", completed: false },
      { title: "Activation Functions", duration: "15 min", completed: false },
      { title: "Forward Propagation", duration: "22 min", completed: false },
    ],
    progress: 0,
    locked: false,
  },
  {
    id: "3",
    module: "Deep Learning Advanced",
    lessons: [
      { title: "Convolutional Neural Networks", duration: "25 min", completed: false },
      { title: "Recurrent Neural Networks", duration: "28 min", completed: false },
      { title: "Transformers Architecture", duration: "30 min", completed: false },
    ],
    progress: 0,
    locked: true,
  },
];

export default function Lessons() {
  return (
    <DashboardLayout>
      <div className="p-6 lg:p-8 max-w-5xl mx-auto">
        {/* Header */}
        <header className="mb-8 animate-fade-in">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <BookOpen className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Lessons</h1>
              <p className="text-sm text-muted-foreground">
                Your personalized learning curriculum
              </p>
            </div>
          </div>
        </header>

        {/* Lessons list */}
        <div className="space-y-6">
          {lessons.map((module, moduleIndex) => (
            <GlassCard 
              key={module.id} 
              className={`animate-fade-in delay-${moduleIndex * 100} ${module.locked ? 'opacity-60' : ''}`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  {module.locked ? (
                    <div className="p-2 rounded-lg bg-muted">
                      <Lock className="w-5 h-5 text-muted-foreground" />
                    </div>
                  ) : module.progress === 100 ? (
                    <div className="p-2 rounded-lg bg-success/10">
                      <CheckCircle2 className="w-5 h-5 text-success" />
                    </div>
                  ) : (
                    <div className="p-2 rounded-lg bg-primary/10">
                      <BookOpen className="w-5 h-5 text-primary" />
                    </div>
                  )}
                  <div>
                    <h2 className="font-semibold text-foreground">{module.module}</h2>
                    <p className="text-sm text-muted-foreground">
                      {module.lessons.length} lessons
                    </p>
                  </div>
                </div>
                <Badge variant={module.locked ? "outline" : module.progress > 0 ? "default" : "secondary"}>
                  {module.locked ? "Locked" : `${module.progress}% complete`}
                </Badge>
              </div>

              {!module.locked && (
                <>
                  <Progress value={module.progress} className="h-1.5 mb-4" />
                  
                  <div className="space-y-2">
                    {module.lessons.map((lesson, lessonIndex) => (
                      <div
                        key={lessonIndex}
                        className="flex items-center justify-between p-3 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors cursor-pointer"
                      >
                        <div className="flex items-center gap-3">
                          {lesson.completed ? (
                            <CheckCircle2 className="w-5 h-5 text-success" />
                          ) : (
                            <Play className="w-5 h-5 text-muted-foreground" />
                          )}
                          <div>
                            <p className={`text-sm ${lesson.completed ? 'text-muted-foreground line-through' : 'text-foreground'}`}>
                              {lesson.title}
                            </p>
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Clock className="w-3 h-3" />
                              {lesson.duration}
                            </div>
                          </div>
                        </div>
                        <ChevronRight className="w-4 h-4 text-muted-foreground" />
                      </div>
                    ))}
                  </div>
                </>
              )}

              {!module.locked && module.progress < 100 && (
                <Button className="w-full mt-4 gap-2">
                  <Play className="w-4 h-4" />
                  {module.progress > 0 ? "Continue Learning" : "Start Module"}
                </Button>
              )}
            </GlassCard>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}
