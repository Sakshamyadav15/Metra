'use client'

import { motion } from 'framer-motion'
import AppLayout from '@/components/layout/AppLayout'
import { 
  Brain, 
  Flame, 
  TrendingUp, 
  Clock, 
  Target, 
  BookOpen,
  Zap,
  ChevronRight,
  AlertCircle
} from 'lucide-react'

export default function DashboardPage() {
  return (
    <AppLayout>
      <div className="p-6 lg:p-8">
        {/* Header */}
        <div className="mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-3xl font-bold font-heading">
              Welcome back, <span className="gradient-text">Learner</span>! 👋
            </h1>
            <p className="text-muted-foreground mt-2">
              Your Learning Twin is ready to help you today
            </p>
          </motion.div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass rounded-2xl p-5"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                  <p className="text-2xl font-bold mt-1">{stat.value}</p>
                  <p className={`text-sm mt-1 ${stat.changeType === 'positive' ? 'text-success' : 'text-muted-foreground'}`}>
                    {stat.change}
                  </p>
                </div>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${stat.iconBg}`}>
                  <stat.icon className={`w-5 h-5 ${stat.iconColor}`} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Learning Twin Visualization */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2 glass rounded-2xl p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-semibold font-heading">Learning Twin Profile</h2>
                <p className="text-sm text-muted-foreground">Your cognitive state visualization</p>
              </div>
              <button className="text-sm text-primary hover:underline flex items-center gap-1">
                View Details <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            {/* Brain Visualization Placeholder */}
            <div className="relative h-64 flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-radial from-primary/20 via-transparent to-transparent" />
              <motion.div
                animate={{ 
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0]
                }}
                transition={{ 
                  duration: 4,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="relative"
              >
                <Brain className="w-32 h-32 text-primary/30" />
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-4xl font-bold gradient-text">72%</p>
                    <p className="text-sm text-muted-foreground">Mastery Score</p>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Modality Preferences */}
            <div className="mt-6 grid grid-cols-5 gap-2">
              {modalities.map((mod) => (
                <div key={mod.name} className="text-center">
                  <div 
                    className="h-20 bg-background-tertiary rounded-lg relative overflow-hidden"
                    title={`${mod.name}: ${mod.value}%`}
                  >
                    <motion.div
                      initial={{ height: 0 }}
                      animate={{ height: `${mod.value}%` }}
                      transition={{ delay: 0.5, duration: 0.8 }}
                      className={`absolute bottom-0 left-0 right-0 ${mod.color} rounded-b-lg`}
                    />
                  </div>
                  <p className="text-xs text-muted-foreground mt-2">{mod.name}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Quick Actions & Today's Goals */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            {/* Quick Actions */}
            <div className="glass rounded-2xl p-6">
              <h2 className="text-lg font-semibold font-heading mb-4">Quick Actions</h2>
              <div className="space-y-3">
                {quickActions.map((action) => (
                  <button
                    key={action.label}
                    className="w-full flex items-center gap-3 p-3 rounded-xl bg-background-tertiary hover:bg-primary/20 hover:border-primary/30 border border-transparent transition-all"
                  >
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${action.iconBg}`}>
                      <action.icon className={`w-5 h-5 ${action.iconColor}`} />
                    </div>
                    <div className="text-left">
                      <p className="font-medium">{action.label}</p>
                      <p className="text-xs text-muted-foreground">{action.description}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Misconceptions Alert */}
            <div className="glass rounded-2xl p-6 border-warning/30 border">
              <div className="flex items-center gap-3 mb-4">
                <AlertCircle className="w-5 h-5 text-warning" />
                <h2 className="text-lg font-semibold font-heading">Active Gaps</h2>
              </div>
              <div className="space-y-3">
                <div className="p-3 bg-warning/10 rounded-xl">
                  <p className="font-medium text-sm">Quadratic Formula Application</p>
                  <p className="text-xs text-muted-foreground mt-1">Confusion with negative discriminant</p>
                  <button className="text-xs text-warning mt-2 hover:underline">Fix Now →</button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Today's Learning Feed */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-6 glass rounded-2xl p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-semibold font-heading">Today's Learning Feed</h2>
              <p className="text-sm text-muted-foreground">Personalized lessons based on your LTP</p>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span>~25 mins</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {lessonFeed.map((lesson, index) => (
              <motion.div
                key={lesson.title}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="p-4 bg-background-tertiary rounded-xl hover:ring-2 ring-primary/30 transition-all cursor-pointer group"
              >
                <div className="flex items-start justify-between mb-3">
                  <span className={`text-xs px-2 py-1 rounded-full ${lesson.typeBg} ${lesson.typeColor}`}>
                    {lesson.type}
                  </span>
                  <span className="text-xs text-muted-foreground">{lesson.duration}</span>
                </div>
                <h3 className="font-medium group-hover:text-primary transition-colors">{lesson.title}</h3>
                <p className="text-sm text-muted-foreground mt-1">{lesson.subject}</p>
                <div className="mt-3 flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    {[...Array(5)].map((_, i) => (
                      <div
                        key={i}
                        className={`w-1.5 h-1.5 rounded-full ${i < lesson.difficulty ? 'bg-primary' : 'bg-muted'}`}
                      />
                    ))}
                  </div>
                  <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </AppLayout>
  )
}

const stats = [
  {
    label: 'Current Streak',
    value: '7 days',
    change: '+2 from last week',
    changeType: 'positive',
    icon: Flame,
    iconBg: 'bg-warning/20',
    iconColor: 'text-warning'
  },
  {
    label: 'Concepts Mastered',
    value: '24',
    change: '+3 this week',
    changeType: 'positive',
    icon: Target,
    iconBg: 'bg-success/20',
    iconColor: 'text-success'
  },
  {
    label: 'Study Time',
    value: '12.5h',
    change: 'This week',
    changeType: 'neutral',
    icon: Clock,
    iconBg: 'bg-primary/20',
    iconColor: 'text-primary'
  },
  {
    label: 'Learning Velocity',
    value: '1.2x',
    change: 'Above average',
    changeType: 'positive',
    icon: TrendingUp,
    iconBg: 'bg-secondary/20',
    iconColor: 'text-secondary'
  },
]

const modalities = [
  { name: 'Visual', value: 85, color: 'bg-primary' },
  { name: 'Verbal', value: 60, color: 'bg-secondary' },
  { name: 'Abstract', value: 45, color: 'bg-accent' },
  { name: 'Analogy', value: 90, color: 'bg-success' },
  { name: 'Interactive', value: 75, color: 'bg-warning' },
]

const quickActions = [
  {
    label: 'Start Learning',
    description: 'Continue your daily lessons',
    icon: BookOpen,
    iconBg: 'bg-primary/20',
    iconColor: 'text-primary'
  },
  {
    label: 'AI Chat',
    description: 'Ask questions anytime',
    icon: Zap,
    iconBg: 'bg-secondary/20',
    iconColor: 'text-secondary'
  },
  {
    label: 'Speech Practice',
    description: 'Test your understanding',
    icon: Brain,
    iconBg: 'bg-success/20',
    iconColor: 'text-success'
  },
]

const lessonFeed = [
  {
    title: 'Introduction to Calculus',
    subject: 'Mathematics',
    type: 'New',
    typeBg: 'bg-primary/20',
    typeColor: 'text-primary',
    duration: '8 min',
    difficulty: 3
  },
  {
    title: 'Newton\'s Laws Review',
    subject: 'Physics',
    type: 'Review',
    typeBg: 'bg-warning/20',
    typeColor: 'text-warning',
    duration: '5 min',
    difficulty: 2
  },
  {
    title: 'Chemical Bonding',
    subject: 'Chemistry',
    type: 'Practice',
    typeBg: 'bg-success/20',
    typeColor: 'text-success',
    duration: '12 min',
    difficulty: 4
  },
]
