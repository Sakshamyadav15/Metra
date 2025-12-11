'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import AppLayout from '@/components/layout/AppLayout'
import { 
  Send, 
  Mic, 
  Sparkles, 
  BookOpen,
  ThumbsUp,
  ThumbsDown,
  Copy,
  RotateCcw,
  ChevronDown
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
  timestamp: Date
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hello! I'm your SkillTwin AI mentor. I have access to your Learning Twin Profile and can provide personalized explanations based on your learning style. What would you like to learn about today?",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Based on your learning profile, I can see you prefer **visual explanations** with **analogies**. Let me explain this concept in a way that works best for you.\n\n${getExampleResponse(input)}`,
        sources: ['Textbook: Mathematics Fundamentals', 'Previous Session Notes'],
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1500)
  }

  return (
    <AppLayout>
      <div className="h-screen flex flex-col">
        {/* Header */}
        <div className="h-16 border-b border-border flex items-center justify-between px-6 bg-background-secondary/50 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-background" />
            </div>
            <div>
              <h1 className="font-semibold">SkillTwin AI</h1>
              <p className="text-xs text-muted-foreground">Dual RAG Personalized Reasoning</p>
            </div>
          </div>
          <button className="p-2 rounded-lg hover:bg-muted/50 transition-colors">
            <RotateCcw className="w-5 h-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className={cn(
                  "flex gap-4",
                  message.role === 'user' ? "justify-end" : "justify-start"
                )}
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center flex-shrink-0">
                    <Sparkles className="w-4 h-4 text-background" />
                  </div>
                )}
                
                <div className={cn(
                  "max-w-2xl",
                  message.role === 'user' ? "order-first" : ""
                )}>
                  <div className={cn(
                    "rounded-2xl p-4",
                    message.role === 'user' 
                      ? "bg-primary text-background ml-auto" 
                      : "glass"
                  )}>
                    <p className="whitespace-pre-wrap">{message.content}</p>
                    
                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-4 pt-3 border-t border-white/10">
                        <p className="text-xs text-muted-foreground mb-2 flex items-center gap-1">
                          <BookOpen className="w-3 h-3" /> Sources
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {message.sources.map((source, i) => (
                            <span 
                              key={i} 
                              className="text-xs px-2 py-1 bg-background-tertiary rounded-full"
                            >
                              {source}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  {/* Actions for assistant messages */}
                  {message.role === 'assistant' && (
                    <div className="flex items-center gap-2 mt-2 ml-2">
                      <button className="p-1.5 rounded-lg hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
                        <ThumbsUp className="w-4 h-4" />
                      </button>
                      <button className="p-1.5 rounded-lg hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
                        <ThumbsDown className="w-4 h-4" />
                      </button>
                      <button className="p-1.5 rounded-lg hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>

                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-lg bg-secondary flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-semibold text-white">You</span>
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Loading indicator */}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-4"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-background animate-pulse" />
              </div>
              <div className="glass rounded-2xl p-4">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions */}
        <div className="px-6 pb-4">
          <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {suggestedQuestions.map((question, i) => (
              <button
                key={i}
                onClick={() => setInput(question)}
                className="flex-shrink-0 text-sm px-4 py-2 glass rounded-full hover:border-primary/30 transition-all"
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="p-6 pt-0">
          <div className="glass rounded-2xl p-2 flex items-center gap-2">
            <button 
              type="button"
              className="p-3 rounded-xl hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground"
            >
              <Mic className="w-5 h-5" />
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything... I'll personalize the answer for you"
              className="flex-1 bg-transparent border-none outline-none text-foreground placeholder:text-muted-foreground"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="p-3 rounded-xl bg-primary text-background hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <p className="text-xs text-muted-foreground text-center mt-2">
            Powered by Dual RAG • Your learning history + Verified sources
          </p>
        </form>
      </div>
    </AppLayout>
  )
}

const suggestedQuestions = [
  "Explain quadratic equations",
  "What's the difference between speed and velocity?",
  "Help me understand photosynthesis",
  "Review my recent misconceptions"
]

function getExampleResponse(input: string): string {
  const responses: Record<string, string> = {
    default: `Great question! Let me break this down for you:

**Key Concept:**
Think of this like building blocks - each piece connects to the next in a logical way.

**Visual Analogy:**
Imagine you're organizing a library. Just like how books are categorized by genre, then author, this concept follows a similar hierarchical structure.

**Step by Step:**
1. First, understand the foundation
2. Then, see how components interact
3. Finally, apply to real scenarios

Would you like me to dive deeper into any specific part? I can also show you some practice problems tailored to your current level.`
  }

  return responses.default
}
