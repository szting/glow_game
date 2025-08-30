import React from 'react';
import { RainbowProgress } from '../types';

interface RainbowProps {
  progress: RainbowProgress;
  onColorClick: (color: string) => void;
}

const Rainbow: React.FC<RainbowProps> = ({ progress, onColorClick }) => {
  const colors = [
    { name: 'red', active: progress.red, gradient: 'from-red-400 to-red-600' },
    { name: 'orange', active: progress.orange, gradient: 'from-orange-400 to-orange-600' },
    { name: 'yellow', active: progress.yellow, gradient: 'from-yellow-400 to-yellow-600' },
    { name: 'green', active: progress.green, gradient: 'from-green-400 to-green-600' },
    { name: 'blue', active: progress.blue, gradient: 'from-blue-400 to-blue-600' },
    { name: 'indigo', active: progress.indigo, gradient: 'from-indigo-400 to-indigo-600' },
    { name: 'violet', active: progress.violet, gradient: 'from-violet-400 to-violet-600' }
  ];

  return (
    <div className="relative w-full max-w-md mx-auto">
      <div className="glass-card rounded-3xl p-8 shadow-2xl">
        <div className="space-y-3">
          {colors.map((color, index) => (
            <button
              key={color.name}
              onClick={() => onColorClick(color.name)}
              className={`w-full h-12 rounded-full transition-all duration-500 transform hover:scale-105 ${
                color.active
                  ? `bg-gradient-to-r ${color.gradient} shadow-lg`
                  : 'bg-gray-300/30 backdrop-blur-sm'
              }`}
              style={{
                animation: color.active ? `pulse 2s infinite` : 'none',
                animationDelay: `${index * 0.1}s`
              }}
            >
              <span className="sr-only">{color.name} band</span>
            </button>
          ))}
        </div>
        <div className="mt-6 text-center">
          <p className="text-white/80 text-sm font-medium">
            {Object.values(progress).filter(Boolean).length} / 7 Colors Unlocked
          </p>
        </div>
      </div>
    </div>
  );
};

export default Rainbow;
