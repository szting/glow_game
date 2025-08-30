import React from 'react';
import { Trophy, Flame, Target, Calendar } from 'lucide-react';
import { CoupleProfile } from '../types';

interface StatsCardProps {
  profile: CoupleProfile;
}

const StatsCard: React.FC<StatsCardProps> = ({ profile }) => {
  const totalPoints = Object.values(profile.points).reduce((sum, points) => sum + points, 0);
  const completedColors = Object.values(profile.rainbowProgress).filter(Boolean).length;

  return (
    <div className="glass-card rounded-2xl p-6 shadow-xl">
      <h3 className="text-white font-semibold text-lg mb-4">Your Journey</h3>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="glass rounded-xl p-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center">
              <Trophy className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white/60 text-xs">Total Points</p>
              <p className="text-white font-bold text-xl">{totalPoints}</p>
            </div>
          </div>
        </div>
        
        <div className="glass rounded-xl p-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center">
              <Flame className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white/60 text-xs">Streak</p>
              <p className="text-white font-bold text-xl">{profile.streak} days</p>
            </div>
          </div>
        </div>
        
        <div className="glass rounded-xl p-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center">
              <Target className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white/60 text-xs">Challenges</p>
              <p className="text-white font-bold text-xl">{profile.completedChallenges.length}</p>
            </div>
          </div>
        </div>
        
        <div className="glass rounded-xl p-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full rainbow-gradient flex items-center justify-center">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white/60 text-xs">Colors</p>
              <p className="text-white font-bold text-xl">{completedColors}/7</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 space-y-3">
        <h4 className="text-white/80 text-sm font-medium">Points Breakdown</h4>
        {Object.entries(profile.points).map(([type, value]) => (
          value > 0 && (
            <div key={type} className="flex items-center justify-between">
              <span className="text-white/60 text-sm capitalize">{type}</span>
              <span className="text-white font-medium">{value}</span>
            </div>
          )
        ))}
      </div>
    </div>
  );
};

export default StatsCard;
