import { DashboardLayout } from "@/components/DashboardLayout";
import { LearningTwinVisualization } from "@/components/LearningTwinVisualization";
import { ProgressRing } from "@/components/ui/progress-ring";
import { ActionCard, StatCard } from "@/components/ui/glass-card";
import { StreakCounter } from "@/components/StreakCounter";
import { LearningFeed } from "@/components/LearningFeed";
import { Button } from "@/components/ui/button";
import {
  Play,
  Mic,
  ClipboardCheck,
  TrendingUp,
  Clock,
  Target,
  Sparkles,
  ArrowRight,
} from "lucide-react";

const todaysLessons = [
  {
    id: "1",
    title: "Introduction to Neural Networks",
    duration: "12 min",
    type: "video" as const,
    completed: true,
  },
  {
    id: "2",
    title: "Practice: Backpropagation Basics",
    duration: "8 min",
    type: "practice" as const,
    completed: false,
    progress: 45,
  },
  {
    id: "3",
    title: "Understanding Gradient Descent",
    duration: "15 min",
    type: "reading" as const,
    completed: false,
  },
  {
    id: "4",
    title: "Neural Network Architecture Deep Dive",
    duration: "20 min",
    type: "audio" as const,
    completed: false,
  },
];

export default function Index() {
  return (
    <DashboardLayout>
      <div className="p-6 lg:p-8 max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8 animate-fade-in">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl lg:text-4xl font-bold text-foreground">
                Welcome back, <span className="text-primary">Alex</span>
              </h1>
              <p className="text-muted-foreground mt-2">
                Ready to continue your learning journey? You're doing great!
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline" className="gap-2">
                <Sparkles className="w-4 h-4" />
                AI Insights
              </Button>
              <Button className="gap-2">
                <Play className="w-4 h-4" />
                Resume Learning
              </Button>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main content - 2 columns */}
          <div className="lg:col-span-2 space-y-6">
            {/* Learning Twin Visualization */}
            <div className="animate-fade-in delay-100">
              <LearningTwinVisualization
                cognitiveState="active"
                masteryLevel={72}
                className="w-full"
              />
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 animate-fade-in delay-200">
              <ActionCard
                icon={Play}
                title="Start Lesson"
                description="Continue where you left off"
                variant="primary"
              />
              <ActionCard
                icon={Mic}
                title="Practice Speaking"
                description="Improve pronunciation"
                variant="accent"
              />
              <ActionCard
                icon={ClipboardCheck}
                title="Take Assessment"
                description="Test your knowledge"
                variant="success"
              />
            </div>

            {/* Learning Feed */}
            <div className="glass rounded-xl p-6 animate-fade-in delay-300">
              <LearningFeed
                lessons={todaysLessons}
                onLessonClick={(id) => console.log("Clicked lesson:", id)}
              />
            </div>
          </div>

          {/* Sidebar - 1 column */}
          <div className="space-y-6">
            {/* Progress Rings */}
            <div className="glass rounded-xl p-6 animate-fade-in delay-100">
              <h3 className="font-semibold text-foreground mb-6">
                Mastery Progress
              </h3>
              <div className="flex flex-wrap justify-center gap-4">
                <ProgressRing
                  progress={72}
                  label="72%"
                  sublabel="Overall"
                  color="primary"
                />
                <ProgressRing
                  progress={85}
                  label="85%"
                  sublabel="This Week"
                  color="accent"
                  size={100}
                />
                <ProgressRing
                  progress={94}
                  label="94%"
                  sublabel="Retention"
                  color="success"
                  size={100}
                />
              </div>
            </div>

            {/* Streak Counter */}
            <div className="animate-fade-in delay-200">
              <StreakCounter days={23} />
            </div>

            {/* Stats */}
            <div className="space-y-4 animate-fade-in delay-300">
              <StatCard
                value="4.2h"
                label="Learning Time This Week"
                icon={Clock}
                trend={{ value: 12, positive: true }}
              />
              <StatCard
                value="18"
                label="Concepts Mastered"
                icon={Target}
                trend={{ value: 8, positive: true }}
              />
              <StatCard
                value="+15%"
                label="Learning Velocity"
                icon={TrendingUp}
              />
            </div>

            {/* CTA */}
            <div className="glass rounded-xl p-6 border-primary/20 animate-fade-in delay-400">
              <h4 className="font-semibold text-foreground mb-2">
                Unlock AI Chat
              </h4>
              <p className="text-sm text-muted-foreground mb-4">
                Get personalized answers from your Learning Twin with dual RAG technology.
              </p>
              <Button variant="accent" className="w-full gap-2">
                Try AI Chat
                <ArrowRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
