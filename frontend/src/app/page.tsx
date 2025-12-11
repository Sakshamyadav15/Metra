'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { 
  Brain, 
  Sparkles, 
  BookOpen, 
  Mic, 
  Shield, 
  ArrowRight,
  Zap,
  Target,
  TrendingUp
} from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden px-6 py-24 sm:py-32 lg:px-8">
        {/* Background Effects */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        </div>
        
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center justify-center gap-2 mb-6">
              <Brain className="w-10 h-10 text-primary animate-pulse" />
              <span className="text-sm font-medium text-primary/80 uppercase tracking-wider">
                Adaptive AI Learning
              </span>
            </div>
            
            <h1 className="text-5xl font-bold tracking-tight sm:text-7xl font-heading">
              <span className="gradient-text">SkillTwin</span>
            </h1>
            
            <p className="mt-4 text-xl text-primary font-medium">
              Your Personal AI Learning Companion
            </p>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              Experience next-generation learning with an AI mentor that truly understands you. 
              SkillTwin adapts to your cognitive profile, delivers personalized explanations, 
              and tracks your mastery in real-time.
            </p>
          </motion.div>
          
          <motion.div 
            className="mt-10 flex items-center justify-center gap-x-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Link
              href="/dashboard"
              className="group relative inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-primary to-secondary rounded-lg font-semibold text-background hover:shadow-glow-lg transition-all duration-300"
            >
              Start Learning
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/chat"
              className="inline-flex items-center gap-2 px-8 py-4 glass rounded-lg font-semibold text-foreground hover:bg-card/90 transition-all"
            >
              <Sparkles className="w-5 h-5" />
              Try AI Chat
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6">
        <div className="mx-auto max-w-7xl">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold font-heading sm:text-4xl">
              Powered by <span className="gradient-text">Intelligent Systems</span>
            </h2>
            <p className="mt-4 text-muted-foreground max-w-2xl mx-auto">
              Five integrated modules working together to create your perfect learning experience
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="group glass rounded-2xl p-6 hover:border-primary/30 transition-all duration-300"
              >
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${feature.iconBg}`}>
                  <feature.icon className={`w-6 h-6 ${feature.iconColor}`} />
                </div>
                <h3 className="text-xl font-semibold mb-2 font-heading">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
                <div className="mt-4 flex items-center text-sm text-primary/80">
                  <span className="font-medium">{feature.module}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6">
        <div className="mx-auto max-w-7xl">
          <div className="glass rounded-3xl p-8 md:p-12">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="text-4xl md:text-5xl font-bold gradient-text font-heading">
                    {stat.value}
                  </div>
                  <div className="mt-2 text-sm text-muted-foreground">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass rounded-3xl p-12"
          >
            <Zap className="w-12 h-12 text-primary mx-auto mb-6" />
            <h2 className="text-3xl font-bold font-heading mb-4">
              Ready to Transform Your Learning?
            </h2>
            <p className="text-muted-foreground mb-8 max-w-xl mx-auto">
              Join SkillTwin and experience personalized AI-powered education that adapts to your unique learning style.
            </p>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-primary to-secondary rounded-lg font-semibold text-background hover:shadow-glow-lg transition-all"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-border">
        <div className="mx-auto max-w-7xl flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Brain className="w-6 h-6 text-primary" />
            <span className="font-semibold">SkillTwin</span>
          </div>
          <p className="text-sm text-muted-foreground">
            Built for IITM Hackathon 2025 • Adaptive AI Personal Mentor
          </p>
        </div>
      </footer>
    </main>
  )
}

const features = [
  {
    title: "Learning Twin Profile",
    description: "An evolving cognitive model that tracks your mastered concepts, learning patterns, and preferred explanation styles.",
    icon: Brain,
    iconBg: "bg-primary/20",
    iconColor: "text-primary",
    module: "Module 3.1"
  },
  {
    title: "Dual RAG Engine",
    description: "Combines your learning history with verified academic sources for personalized, accurate explanations.",
    icon: Sparkles,
    iconBg: "bg-secondary/20",
    iconColor: "text-secondary",
    module: "Module 3.2"
  },
  {
    title: "Micro Lessons",
    description: "Auto-generated short lessons with slides, narration, and quizzes tailored to your current level.",
    icon: BookOpen,
    iconBg: "bg-accent/20",
    iconColor: "text-accent",
    module: "Module 3.3"
  },
  {
    title: "Speech Assessment",
    description: "Verbally explain concepts and receive detailed feedback on clarity, confidence, and correctness.",
    icon: Mic,
    iconBg: "bg-success/20",
    iconColor: "text-success",
    module: "Module 3.4"
  },
  {
    title: "Integrity Layer",
    description: "Deepfake-resistant verification ensures authentic assessments and secure learning.",
    icon: Shield,
    iconBg: "bg-warning/20",
    iconColor: "text-warning",
    module: "Module 3.5"
  },
  {
    title: "Adaptive Pathways",
    description: "Smart learning paths that prioritize concepts based on your goals and spaced repetition needs.",
    icon: Target,
    iconBg: "bg-pink-500/20",
    iconColor: "text-pink-500",
    module: "Learning Engine"
  },
]

const stats = [
  { value: "5", label: "Core Modules" },
  { value: "∞", label: "Personalization" },
  { value: "24/7", label: "AI Availability" },
  { value: "100%", label: "Adaptive" },
]
