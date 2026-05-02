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
    <main className="min-h-screen p-6 md:p-12 lg:p-24 max-w-7xl mx-auto relative">
      {/* Premium Header */}
      <motion.div 
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="text-center mb-20 relative"
      >
        <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-xs font-bold tracking-widest uppercase">
          AI-Powered Discovery
        </div>
        <h1 className="text-6xl md:text-8xl font-black mb-6 accent-gradient bg-clip-text text-transparent tracking-tight">
          Gourmet AI
        </h1>
        <p className="text-slate-400 text-lg md:text-2xl max-w-3xl mx-auto leading-relaxed font-light">
          Experience the future of dining. Intelligent recommendations tailored to your unique palate.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 relative">
        {/* Advanced Form Section */}
        <motion.div 
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="lg:col-span-4"
        >
          <div className="glass p-10 rounded-[2.5rem] sticky top-12 border-white/5 shadow-2xl">
            <h2 className="text-3xl font-bold mb-8 flex items-center gap-3 text-white">
              <Sparkles className="text-fuchsia-400 w-7 h-7" /> Preferences
            </h2>
            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="space-y-3">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Location</label>
                <div className="relative group">
                  <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5 group-focus-within:text-violet-400 transition-colors" />
                  <input
                    type="text"
                    required
                    placeholder="e.g., Delhi, Bellandur"
                    className="w-full bg-slate-950/40 border border-white/10 rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-violet-500/40 focus:border-violet-500/50 outline-none transition-all text-slate-200 placeholder:text-slate-600 text-lg"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-3">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Cuisines</label>
                <div className="relative group">
                  <Utensils className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5 group-focus-within:text-violet-400 transition-colors" />
                  <input
                    type="text"
                    required
                    placeholder="Italian, Chinese, etc."
                    className="w-full bg-slate-950/40 border border-white/10 rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-violet-500/40 focus:border-violet-500/50 outline-none transition-all text-slate-200 placeholder:text-slate-600 text-lg"
                    value={formData.cuisines}
                    onChange={(e) => setFormData({ ...formData, cuisines: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-3">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Budget Experience</label>
                <div className="relative">
                  <DollarSign className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                  <select
                    className="w-full bg-slate-950/40 border border-white/10 rounded-2xl py-4 pl-12 pr-10 focus:ring-2 focus:ring-violet-500/40 outline-none transition-all appearance-none text-slate-200 text-lg cursor-pointer"
                    value={formData.budget_category}
                    onChange={(e) => setFormData({ ...formData, budget_category: e.target.value })}
                  >
                    <option value="low">Budget-Friendly</option>
                    <option value="medium">Mid-Range Casual</option>
                    <option value="high">Premium Fine Dining</option>
                  </select>
                </div>
              </div>

              <div className="space-y-6 pt-4">
                <div className="space-y-4">
                  <div className="flex justify-between items-end">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Rating Spectrum</label>
                    <div className="flex items-center gap-2 text-violet-400 font-black text-xl">
                      <span>{formData.min_rating}</span>
                      <span className="text-slate-700 text-sm">-</span>
                      <span>{formData.max_rating}</span>
                    </div>
                  </div>
                  <div className="space-y-4 px-2">
                    <input
                      type="range"
                      min="0"
                      max="5"
                      step="0.1"
                      className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-violet-500"
                      value={formData.min_rating}
                      onChange={(e) => setFormData({ ...formData, min_rating: e.target.value })}
                    />
                    <input
                      type="range"
                      min="0"
                      max="5"
                      step="0.1"
                      className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-fuchsia-500"
                      value={formData.max_rating}
                      onChange={(e) => setFormData({ ...formData, max_rating: e.target.value })}
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Personal Vibes</label>
                <textarea
                  placeholder="e.g. rooftop seating, quiet for dates, craft cocktails..."
                  className="w-full bg-slate-950/40 border border-white/10 rounded-2xl py-5 px-5 focus:ring-2 focus:ring-violet-500/40 outline-none transition-all resize-none h-40 text-slate-200 placeholder:text-slate-600 text-lg leading-relaxed"
                  value={formData.extra_preferences}
                  onChange={(e) => setFormData({ ...formData, extra_preferences: e.target.value })}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-premium w-full flex items-center justify-center gap-3 group text-xl tracking-wide"
              >
                {loading ? (
                  <Loader2 className="animate-spin w-6 h-6" />
                ) : (
                  <>
                    Find Matches <Sparkles className="w-5 h-5 group-hover:rotate-12 transition-transform" />
                  </>
                )}
              </button>
            </form>
          </div>
        </motion.div>

        {/* Results Dynamic Section */}
        <div className="lg:col-span-8">
          <AnimatePresence mode="wait">
            {loading ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="grid grid-cols-1 gap-8"
              >
                {[1, 2, 3].map((i) => (
                  <div key={i} className="glass p-12 rounded-[2.5rem] animate-pulse relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full animate-[shimmer_2s_infinite]" />
                    <div className="h-10 bg-white/5 rounded-2xl w-1/3 mb-6" />
                    <div className="h-4 bg-white/5 rounded-lg w-full mb-3" />
                    <div className="h-4 bg-white/5 rounded-lg w-2/3" />
                  </div>
                ))}
              </motion.div>
            ) : recommendations.length > 0 ? (
              <motion.div
                key="results"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="grid grid-cols-1 gap-8"
              >
                {recommendations.map((rec, index) => (
                  <motion.div
                    key={rec.restaurant_name}
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.15, ease: "easeOut" }}
                    className="glass p-10 rounded-[2.5rem] glass-hover group relative overflow-hidden"
                  >
                    <div className="flex flex-col md:flex-row justify-between items-start gap-6">
                      <div className="flex-1">
                        <div className="flex items-center gap-4 mb-4">
                          <span className="flex items-center justify-center w-12 h-12 rounded-2xl bg-violet-500/20 text-violet-400 text-xl font-black border border-violet-500/30">
                            {rec.rank}
                          </span>
                          <h3 className="text-3xl md:text-4xl font-bold text-white group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-violet-400 transition-all duration-500">
                            {rec.restaurant_name}
                          </h3>
                        </div>
                        <div className="flex gap-2 flex-wrap mb-6">
                          {rec.cuisines.map((c) => (
                            <span key={c} className="text-xs font-bold uppercase tracking-widest text-slate-400 bg-slate-950/60 px-3 py-1.5 rounded-xl border border-white/5">
                              {c}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="flex md:flex-col items-center md:items-end gap-6 md:gap-2">
                        <div className="flex items-center gap-2 text-amber-400 font-black text-2xl">
                          <Star className="w-6 h-6 fill-amber-400" /> {rec.rating || "N/A"}
                        </div>
                        <div className="flex items-center gap-1.5 text-emerald-400 font-bold text-lg">
                          <DollarSign className="w-5 h-5" /> {rec.estimated_cost}
                        </div>
                      </div>
                    </div>
                    <div className="mt-8 p-6 rounded-2xl bg-slate-950/40 border border-white/5 relative">
                      <div className="absolute -top-3 -left-1 text-4xl text-violet-500/30 font-serif">“</div>
                      <p className="text-slate-300 text-lg leading-relaxed font-light italic">
                        {rec.explanation}
                      </p>
                    </div>
                    <div className="mt-8 flex justify-end">
                      <button className="flex items-center gap-2 text-sm font-bold text-violet-400 uppercase tracking-widest hover:text-white transition-colors group/btn">
                        Explore Venue <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-2 transition-transform" />
                      </button>
                    </div>
                  </motion.div>
                ))}
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass p-24 rounded-[3rem] text-center flex flex-col items-center justify-center border-dashed border-white/5"
              >
                <div className="w-32 h-32 bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 rounded-full flex items-center justify-center mb-8 relative">
                  <div className="absolute inset-0 bg-violet-500/20 blur-2xl rounded-full animate-pulse" />
                  <Utensils className="w-16 h-16 text-violet-400 relative" />
                </div>
                <h3 className="text-3xl font-bold mb-4 text-white">Culinary Awaits</h3>
                <p className="text-slate-500 text-lg max-w-sm font-light">Your perfect dining experience is just a few preferences away.</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </main>
  );
}
