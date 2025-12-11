import { DashboardLayout } from "@/components/DashboardLayout";
import { GlassCard } from "@/components/ui/glass-card";
import { ProgressRing } from "@/components/ui/progress-ring";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Brain, BookOpen, Clock, Target, TrendingUp, AlertCircle } from "lucide-react";

const concepts = [
  { name: "Neural Networks", mastery: 85, lastReviewed: "2 days ago", status: "strong" },
  { name: "Backpropagation", mastery: 72, lastReviewed: "1 day ago", status: "learning" },
  { name: "Gradient Descent", mastery: 45, lastReviewed: "5 days ago", status: "needs-review" },
  { name: "Activation Functions", mastery: 90, lastReviewed: "3 days ago", status: "strong" },
  { name: "Loss Functions", mastery: 60, lastReviewed: "4 days ago", status: "learning" },
];

const misconceptions = [
  { topic: "Backpropagation", issue: "Confusing chain rule application", severity: "medium" },
  { topic: "Gradient Descent", issue: "Learning rate interpretation", severity: "high" },
];

const learningStats = {
  totalHours: 42,
  conceptsLearned: 28,
  currentStreak: 23,
  averageRetention: 78,
};

export default function Profile() {
  return (
    <DashboardLayout>
      <div className="p-6 lg:p-8 max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8 animate-fade-in">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <Brain className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Learning Profile</h1>
              <p className="text-sm text-muted-foreground">
                Your Learning Twin's cognitive state
              </p>
            </div>
          </div>
        </header>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8 animate-fade-in delay-100">
          <GlassCard className="text-center">
            <Clock className="w-6 h-6 text-primary mx-auto mb-2" />
            <p className="text-2xl font-bold text-foreground">{learningStats.totalHours}h</p>
            <p className="text-xs text-muted-foreground">Total Learning</p>
          </GlassCard>
          <GlassCard className="text-center">
            <BookOpen className="w-6 h-6 text-accent mx-auto mb-2" />
            <p className="text-2xl font-bold text-foreground">{learningStats.conceptsLearned}</p>
            <p className="text-xs text-muted-foreground">Concepts Learned</p>
          </GlassCard>
          <GlassCard className="text-center">
            <Target className="w-6 h-6 text-success mx-auto mb-2" />
            <p className="text-2xl font-bold text-foreground">{learningStats.currentStreak}</p>
            <p className="text-xs text-muted-foreground">Day Streak</p>
          </GlassCard>
          <GlassCard className="text-center">
            <TrendingUp className="w-6 h-6 text-warning mx-auto mb-2" />
            <p className="text-2xl font-bold text-foreground">{learningStats.averageRetention}%</p>
            <p className="text-xs text-muted-foreground">Retention Rate</p>
          </GlassCard>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main content */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="concepts" className="animate-fade-in delay-200">
              <TabsList className="mb-4">
                <TabsTrigger value="concepts">Concept Mastery</TabsTrigger>
                <TabsTrigger value="misconceptions">Misconceptions</TabsTrigger>
              </TabsList>

              <TabsContent value="concepts">
                <GlassCard>
                  <div className="space-y-4">
                    {concepts.map((concept, index) => (
                      <div
                        key={index}
                        className="flex items-center gap-4 p-3 rounded-lg bg-secondary/50"
                      >
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-medium text-foreground">{concept.name}</h4>
                            <Badge
                              variant={
                                concept.status === "strong"
                                  ? "success"
                                  : concept.status === "learning"
                                  ? "default"
                                  : "warning"
                              }
                            >
                              {concept.status === "strong"
                                ? "Strong"
                                : concept.status === "learning"
                                ? "Learning"
                                : "Review"}
                            </Badge>
                          </div>
                          <Progress value={concept.mastery} className="h-2 mb-1" />
                          <p className="text-xs text-muted-foreground">
                            {concept.mastery}% mastery • Last reviewed: {concept.lastReviewed}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </GlassCard>
              </TabsContent>

              <TabsContent value="misconceptions">
                <GlassCard>
                  <div className="space-y-4">
                    {misconceptions.map((item, index) => (
                      <div
                        key={index}
                        className="flex items-start gap-3 p-3 rounded-lg bg-destructive/5 border border-destructive/10"
                      >
                        <AlertCircle className="w-5 h-5 text-destructive shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-foreground">{item.topic}</h4>
                          <p className="text-sm text-muted-foreground">{item.issue}</p>
                          <Badge
                            variant={item.severity === "high" ? "destructive" : "warning"}
                            className="mt-2"
                          >
                            {item.severity} priority
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </GlassCard>
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar */}
          <div className="space-y-6 animate-fade-in delay-300">
            <GlassCard>
              <h3 className="font-semibold text-foreground mb-4">Overall Mastery</h3>
              <div className="flex justify-center">
                <ProgressRing
                  progress={learningStats.averageRetention}
                  label={`${learningStats.averageRetention}%`}
                  sublabel="Average"
                  color="primary"
                  size={140}
                />
              </div>
            </GlassCard>

            <GlassCard>
              <h3 className="font-semibold text-foreground mb-4">Next Review</h3>
              <div className="space-y-3">
                {concepts
                  .filter((c) => c.status === "needs-review")
                  .map((concept, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-2 rounded-lg bg-secondary/50"
                    >
                      <span className="text-sm text-foreground">{concept.name}</span>
                      <Badge variant="outline">{concept.mastery}%</Badge>
                    </div>
                  ))}
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
