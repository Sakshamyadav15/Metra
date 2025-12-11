import { DashboardLayout } from "@/components/DashboardLayout";
import { GlassCard } from "@/components/ui/glass-card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Sparkles, BookOpen, Lightbulb } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: { title: string; type: "student" | "academic" }[];
}

const initialMessages: Message[] = [
  {
    id: "1",
    role: "assistant",
    content: "Hello! I'm your Learning Twin assistant powered by Dual RAG technology. I can help you understand concepts by combining your learning history with academic knowledge. What would you like to learn about today?",
    timestamp: new Date(),
  },
];

const suggestedQuestions = [
  "Explain neural networks in simple terms",
  "Help me understand backpropagation",
  "What concepts should I review?",
  "Create a study plan for me",
];

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Based on your learning profile and the academic materials, here's what I found...\n\nThis is a simulated response from the Dual RAG system. In production, this would combine your personal learning context (Source A) with academic knowledge (Source B) to provide personalized explanations tailored to your understanding level.",
        timestamp: new Date(),
        sources: [
          { title: "Your Learning History", type: "student" },
          { title: "Neural Networks Fundamentals", type: "academic" },
        ],
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <DashboardLayout>
      <div className="h-full flex flex-col p-6 lg:p-8 max-w-5xl mx-auto">
        {/* Header */}
        <header className="mb-6 animate-fade-in">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <Bot className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">AI Chat</h1>
              <p className="text-sm text-muted-foreground">
                Powered by Dual RAG Technology
              </p>
            </div>
          </div>
        </header>

        {/* Chat area */}
        <GlassCard className="flex-1 flex flex-col min-h-0 p-0 overflow-hidden">
          {/* Messages */}
          <ScrollArea className="flex-1 p-6">
            <div className="space-y-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex gap-3",
                    message.role === "user" && "flex-row-reverse"
                  )}
                >
                  <Avatar className="h-8 w-8 shrink-0">
                    <AvatarFallback
                      className={cn(
                        message.role === "assistant"
                          ? "bg-primary/10 text-primary"
                          : "bg-secondary text-foreground"
                      )}
                    >
                      {message.role === "assistant" ? (
                        <Bot className="w-4 h-4" />
                      ) : (
                        <User className="w-4 h-4" />
                      )}
                    </AvatarFallback>
                  </Avatar>

                  <div
                    className={cn(
                      "flex-1 max-w-[80%]",
                      message.role === "user" && "flex flex-col items-end"
                    )}
                  >
                    <div
                      className={cn(
                        "rounded-xl px-4 py-3",
                        message.role === "assistant"
                          ? "bg-secondary"
                          : "bg-primary text-primary-foreground"
                      )}
                    >
                      <p className="text-sm whitespace-pre-wrap">
                        {message.content}
                      </p>
                    </div>

                    {message.sources && message.sources.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {message.sources.map((source, index) => (
                          <div
                            key={index}
                            className={cn(
                              "flex items-center gap-1 px-2 py-1 rounded-md text-xs",
                              source.type === "student"
                                ? "bg-accent/10 text-accent"
                                : "bg-success/10 text-success"
                            )}
                          >
                            {source.type === "student" ? (
                              <Lightbulb className="w-3 h-3" />
                            ) : (
                              <BookOpen className="w-3 h-3" />
                            )}
                            {source.title}
                          </div>
                        ))}
                      </div>
                    )}

                    <p className="text-xs text-muted-foreground mt-1">
                      {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex gap-3">
                  <Avatar className="h-8 w-8 shrink-0">
                    <AvatarFallback className="bg-primary/10 text-primary">
                      <Bot className="w-4 h-4" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-secondary rounded-xl px-4 py-3">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse" />
                      <div className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse delay-100" />
                      <div className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse delay-200" />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Suggested questions */}
          {messages.length === 1 && (
            <div className="px-6 pb-4">
              <p className="text-xs text-muted-foreground mb-2">
                <Sparkles className="w-3 h-3 inline mr-1" />
                Suggested questions
              </p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((question, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    className="text-xs"
                    onClick={() => setInput(question)}
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {/* Input area */}
          <div className="p-4 border-t border-border">
            <div className="flex gap-3">
              <Textarea
                placeholder="Ask your Learning Twin anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                className="min-h-[48px] max-h-[120px] resize-none"
                rows={1}
              />
              <Button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                size="icon"
                className="h-12 w-12 shrink-0"
              >
                <Send className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  );
}
