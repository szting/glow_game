import React, { useState } from 'react';
import { X, CheckCircle } from 'lucide-react';
import { ColorQuest, Challenge } from '../types';
import * as Icons from 'lucide-react';

interface ChallengeModalProps {
  quest: ColorQuest;
  onClose: () => void;
  onComplete: (challengeId: string) => void;
  completedChallenges: string[];
}

const ChallengeModal: React.FC<ChallengeModalProps> = ({ 
  quest, 
  onClose, 
  onComplete,
  completedChallenges 
}) => {
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);

  const handleComplete = (challengeId: string) => {
    onComplete(challengeId);
    setSelectedChallenge(null);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      
      <div className="glass-card relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl p-8 shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-6 right-6 text-white/60 hover:text-white transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
        
        <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${quest.gradient} flex items-center justify-center mb-6 mx-auto`}>
          <span className="text-white font-bold text-3xl">{quest.name[0]}</span>
        </div>
        
        <h2 className="text-3xl font-bold text-white text-center mb-2">
          {quest.name}: {quest.theme} Quests
        </h2>
        
        <p className="text-white/70 text-center mb-8">
          Complete these challenges to unlock the {quest.name.toLowerCase()} band and earn {quest.pointsType} points
        </p>
        
        <div className="space-y-4">
          {quest.challenges.map((challenge) => {
            const IconComponent = Icons[challenge.icon as keyof typeof Icons] || Icons.Circle;
            const isCompleted = completedChallenges.includes(challenge.id);
            
            return (
              <div
                key={challenge.id}
                className={`glass rounded-xl p-6 transition-all duration-300 ${
                  isCompleted 
                    ? 'opacity-70' 
                    : 'hover:shadow-lg hover:transform hover:scale-[1.02] cursor-pointer'
                }`}
                onClick={() => !isCompleted && setSelectedChallenge(challenge)}
              >
                <div className="flex items-start space-x-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${
                    isCompleted 
                      ? 'bg-green-500/20' 
                      : 'bg-white/10'
                  }`}>
                    {isCompleted ? (
                      <CheckCircle className="w-6 h-6 text-green-400" />
                    ) : (
                      <IconComponent className="w-6 h-6 text-white/80" />
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <h3 className={`font-semibold text-lg mb-1 ${
                      isCompleted ? 'text-white/50 line-through' : 'text-white'
                    }`}>
                      {challenge.title}
                    </h3>
                    <p className="text-white/60 text-sm">{challenge.description}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        
        {selectedChallenge && (
          <div className="mt-6 p-6 glass rounded-xl">
            <h4 className="text-white font-semibold mb-3">Ready to complete "{selectedChallenge.title}"?</h4>
            <div className="flex space-x-3">
              <button
                onClick={() => handleComplete(selectedChallenge.id)}
                className="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-6 rounded-xl font-medium hover:shadow-lg transition-all duration-300 hover:transform hover:scale-105"
              >
                Mark as Complete
              </button>
              <button
                onClick={() => setSelectedChallenge(null)}
                className="flex-1 glass text-white/80 py-3 px-6 rounded-xl font-medium hover:bg-white/10 transition-all duration-300"
              >
                Not Yet
              </button>
            </div>
          </div>
        )}
        
        <div className="mt-8 text-center">
          <div className="inline-flex items-center space-x-2 text-white/60">
            <span className="text-2xl font-bold text-white">
              {completedChallenges.filter(id => quest.challenges.some(c => c.id === id)).length}
            </span>
            <span>/</span>
            <span>{quest.challenges.length}</span>
            <span>Completed</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChallengeModal;
