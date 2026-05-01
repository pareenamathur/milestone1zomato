"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Utensils, MapPin, Search, Star, DollarSign, ArrowRight, Loader2, Sparkles } from "lucide-react";

interface Recommendation {
  restaurant_name: string;
  rating: number | null;
  cuisines: string[];
  estimated_cost: string;
  explanation: string;
  rank: number;
}

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [formData, setFormData] = useState({
    location: "",
    cuisines: "",
    budget_mode: "category",
    budget_category: "medium",
    min_rating: "3.5",
    max_rating: "5.0",
    extra_preferences: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setRecommendations([]);

    try {
      const response = await fetch("/api/v1/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          location: formData.location,
          cuisines: formData.cuisines,
          budget: {
            mode: formData.budget_mode,
            category: formData.budget_category,
          },
          min_rating: parseFloat(formData.min_rating),
          max_rating: parseFloat(formData.max_rating),
          extra_preferences: formData.extra_preferences,
        }),
      });

      const data = await response.json();
      if (data.ok) {
        setRecommendations(data.recommendations);
      } else {
        alert("Error: " + (data.error || "Failed to fetch recommendations"));
      }
    } catch (err) {
      alert("Error connecting to server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 md:p-24 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-16"
      >
        <h1 className="text-5xl md:text-7xl font-bold mb-4 accent-gradient bg-clip-text text-transparent">
          Gourmet AI
        </h1>
        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto">
          Discover your next favorite meal with our intelligent restaurant recommendation engine.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        {/* Form Section */}
        <motion.div 
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-4"
        >
          <div className="glass p-8 rounded-3xl sticky top-8">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Search className="text-violet-400" /> Preferences
            </h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Location</label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4" />
                  <input
                    type="text"
                    required
                    placeholder="e.g., Delhi, Bellandur"
                    className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-4 focus:ring-2 focus:ring-violet-500 outline-none transition-all text-slate-200 placeholder:text-slate-500"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Cuisines</label>
                <div className="relative">
                  <Utensils className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4" />
                  <input
                    type="text"
                    required
                    placeholder="Italian, Chinese, etc."
                    className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-4 focus:ring-2 focus:ring-violet-500 outline-none transition-all text-slate-200 placeholder:text-slate-500"
                    value={formData.cuisines}
                    onChange={(e) => setFormData({ ...formData, cuisines: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Budget</label>
                <select
                  className="w-full bg-white/5 border border-white/10 rounded-xl py-3 px-4 focus:ring-2 focus:ring-violet-500 outline-none transition-all appearance-none text-slate-200"
                  value={formData.budget_category}
                  onChange={(e) => setFormData({ ...formData, budget_category: e.target.value })}
                >
                  <option value="low">Budget-Friendly</option>
                  <option value="medium">Mid-Range</option>
                  <option value="high">Premium / Fine Dining</option>
                </select>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <label className="text-sm font-medium text-gray-400">Min Rating</label>
                    <span className="text-violet-400 font-bold">{formData.min_rating}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="5"
                    step="0.1"
                    className="w-full accent-violet-500"
                    value={formData.min_rating}
                    onChange={(e) => setFormData({ ...formData, min_rating: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <label className="text-sm font-medium text-gray-400">Max Rating</label>
                    <span className="text-violet-400 font-bold">{formData.max_rating}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="5"
                    step="0.1"
                    className="w-full accent-violet-500"
                    value={formData.max_rating}
                    onChange={(e) => setFormData({ ...formData, max_rating: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Additional Preferences</label>
                <textarea
                  placeholder="e.g. outdoor seating, quiet place, romantic vibe..."
                  className="w-full bg-white/5 border border-white/10 rounded-xl py-4 px-4 focus:ring-2 focus:ring-violet-500 outline-none transition-all resize-none h-32 text-slate-200 placeholder:text-slate-500 leading-relaxed"
                  value={formData.extra_preferences}
                  onChange={(e) => setFormData({ ...formData, extra_preferences: e.target.value })}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-premium w-full flex items-center justify-center gap-2 group"
              >
                {loading ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <>
                    Generate Magic <Sparkles className="w-4 h-4 group-hover:scale-125 transition-transform" />
                  </>
                )}
              </button>
            </form>
          </div>
        </motion.div>

        {/* Results Section */}
        <div className="lg:col-span-8">
          <AnimatePresence mode="wait">
            {loading ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-6"
              >
                {[1, 2, 3].map((i) => (
                  <div key={i} className="glass p-8 rounded-3xl animate-pulse">
                    <div className="h-8 bg-white/5 rounded-lg w-1/3 mb-4" />
                    <div className="h-4 bg-white/5 rounded-lg w-full mb-2" />
                    <div className="h-4 bg-white/5 rounded-lg w-2/3" />
                  </div>
                ))}
              </motion.div>
            ) : recommendations.length > 0 ? (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {recommendations.map((rec, index) => (
                  <motion.div
                    key={rec.restaurant_name}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="glass p-8 rounded-3xl glass-hover group"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="flex items-center gap-3 mb-2">
                          <span className="bg-violet-500/20 text-violet-400 px-3 py-1 rounded-full text-sm font-bold border border-violet-500/30">
                            #{rec.rank}
                          </span>
                          <h3 className="text-2xl font-bold group-hover:text-violet-400 transition-colors">
                            {rec.restaurant_name}
                          </h3>
                        </div>
                        <div className="flex gap-2 flex-wrap">
                          {rec.cuisines.map((c) => (
                            <span key={c} className="text-xs text-gray-500 bg-white/5 px-2 py-1 rounded-md border border-white/5">
                              {c}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-amber-400 font-bold mb-1">
                          <Star className="w-4 h-4 fill-amber-400" /> {rec.rating || "N/A"}
                        </div>
                        <div className="flex items-center gap-1 text-emerald-400 text-sm">
                          <DollarSign className="w-4 h-4" /> {rec.estimated_cost}
                        </div>
                      </div>
                    </div>
                    <p className="text-gray-400 leading-relaxed mb-6 italic">
                      "{rec.explanation}"
                    </p>
                    <button className="flex items-center gap-2 text-sm font-semibold text-violet-400 group-hover:gap-4 transition-all">
                      View Details <ArrowRight className="w-4 h-4" />
                    </button>
                  </motion.div>
                ))}
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="glass p-16 rounded-3xl text-center flex flex-col items-center justify-center text-gray-500"
              >
                <div className="w-24 h-24 bg-white/5 rounded-full flex items-center justify-center mb-6">
                  <Utensils className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-2 text-white">No Recommendations Yet</h3>
                <p>Fill out the form on the left to discover amazing places to eat.</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </main>
  );
}
