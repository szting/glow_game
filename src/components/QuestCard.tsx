import React from 'react';
import { ColorQuest } from '../types';
import * as Icons from 'lucide-react';
import { Lock, CheckCircle } from 'lucide-react';

interface QuestCardProps {
  quest: ColorQuest;
  onSelect: () => void;
  isActive: boolean;
}

const QuestCard: React.FC<QuestCardProps> = ({ quest, onSelect, isActive }) => {
  return (
    <div
      onClick={quest.unlocked ? onSelect : undefined}
      className={`glass-card rounded-2xl p-6 transition-all duration-300 ${
        quest.unlocked 
          ? 'cursor-pointer hover:transform hover:scale-105 hover:shadow-xl' 
          : 'opacity-50 cursor-not-allowed'
      } ${isActive ? 'ring-2 ring-white/50 shadow-2xl transform scale-105' : ''}`}
      style={{
        background: quest.unlocked 
          ? `linear-gradient(135deg, ${quest.bgColor} 0%, rgba(255, 255, 255, 0.05) 100%)`
          : 'rgba(128, 128, 128, 0.1)'
      }}
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${quest.gradient} flex items-center justify-center`}>
          {quest.completed ? (
            <CheckCircle className="w-6 h-6 text-white" />
          ) : quest.unlocked ? (
            <span className="text-white font-bold text-lg">{quest.name[0]}</span>
          ) : (
            <Lock className="w-6 h-6 text-white/70" />
          )}
        </div>
        <span className="text-white/60 text-sm font-medium">{quest.pointsType} Points</span>
      </div>
      
      <h3 className="text-white font-semibold text-lg mb-2">
        {quest.name}: {quest.theme} Quests
      </h3>
      
      <p className="text-white/70 text-sm mb-4">
        {quest.unlocked 
          ? `Complete ${quest.challenges.length} challenges to unlock the ${quest.name.toLowerCase()} band`
          : 'Complete previous quests to unlock'}
      </p>
      
      {quest.unlocked && (
        <div className="space-y-2">
          {quest.challenges.slice(0, 2).map((challenge) => {
            const IconComponent = Icons[challenge.icon as keyof typeof Icons] || Icons.Circle;
            return (
              <div key={challenge.id} className="flex items-center space-x-2 text-white/60 text-xs">
                <IconComponent className="w-3 h-3" />
                <span className="truncate">{challenge.title}</span>
              </div>
            );
          })}
          {quest.challenges.length > 2 && (
            <span className="text-white/40 text-xs">+{quest.challenges.length - 2} more</span>
          )}
        </div>
      )}
    </div>
  );
};

export default QuestCard;
