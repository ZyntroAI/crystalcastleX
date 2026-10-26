import React, { useState, useEffect } from 'react';
import { CHORES } from './data/roles.config';

const CATEGORIES = [
  { key: 'daily', label: 'Daily', emoji: '☀️', color: 'green' },
  { key: 'weekly', label: 'Weekly', emoji: '📅', color: 'blue' },
  { key: 'monthly', label: 'Monthly', emoji: '🗓️', color: 'purple' },
  { key: 'project', label: 'Project', emoji: '📦', color: 'amber' },
];

const ChoresTab = () => {
  const storageKey = 'zyntro-chores-progress';
  
  // Load saved progress
  const [progress, setProgress] = useState(() => {
    if (typeof window === 'undefined') return {};
    try {
      const saved = localStorage.getItem(storageKey);
      return saved ? JSON.parse(saved) : {};
    } catch { return {}; }
  });
  
  const [activeCat, setActiveCat] = useState('daily');

  // Auto-save progress
  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(progress));
  }, [progress]);

  const toggleItem = (id) => {
    setProgress(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const currentItems = CHORES[activeCat] || [];
  const completed = currentItems.filter(item => progress[item.id]).length;
  const total = currentItems.length;
  const percent = total ? Math.round((completed / total) * 100) : 0;

  const resetCategory = () => {
    if (window.confirm('Clear all checked items in this category?')) {
      const newProgress = { ...progress };
      currentItems.forEach(item => delete newProgress[item.id]);
      setProgress(newProgress);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-2">
          🧹 Chores & Maintenance
        </h2>
        <p className="text-gray-500 dark:text-gray-400">
          Keep your codebase, docs, and workspace healthy and organized
        </p>
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        {CATEGORIES.map(cat => (
          <button
            key={cat.key}
            onClick={() => setActiveCat(cat.key)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeCat === cat.key
                ? 'bg-blue-500 text-white shadow-md scale-105'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
            }`}
          >
            <span className="mr-1">{cat.emoji}</span>
            {cat.label}
          </button>
        ))}
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-1">
          <span className="text-gray-600 dark:text-gray-400">
            {CATEGORIES.find(c => c.key === activeCat)?.emoji} 
            {CATEGORIES.find(c => c.key === activeCat)?.label} Progress
          </span>
          <span className="font-semibold text-gray-800 dark:text-gray-200">
            {completed}/{total} • {percent}%
          </span>
        </div>
        <div className="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2.5">
          <div 
            className="bg-green-500 h-2.5 rounded-full transition-all duration-300"
            style={{ width: `${percent}%` }}
          />
        </div>
      </div>

      {/* Checklist */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 shadow-sm">
        <div className="space-y-3">
          {currentItems.map(item => (
            <label 
              key={item.id}
              className="flex items-start gap-3 py-2 cursor-pointer group"
            >
              <input
                type="checkbox"
                checked={progress[item.id] || false}
                onChange={() => toggleItem(item.id)}
                className="mt-1 h-5 w-5 rounded border-gray-300 dark:border-gray-600 
                           text-green-600 focus:ring-green-500 dark:focus:ring-green-400
                           bg-white dark:bg-gray-700"
              />
              <span className={`text-sm leading-relaxed transition-colors ${
                progress[item.id]
                  ? 'text-gray-400 dark:text-gray-500 line-through'
                  : 'text-gray-700 dark:text-gray-300'
              }`}>
                {item.text}
              </span>
            </label>
          ))}
        </div>

        {/* Actions */}
        <div className="mt-5 pt-4 border-t border-gray-100 dark:border-gray-700 flex justify-between items-center">
          <span className="text-xs text-gray-400">
            💾 Progress saved automatically
          </span>
          <button
            onClick={resetCategory}
            className="text-xs text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400 transition-colors"
          >
            🗑️ Reset Category
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChoresTab;
