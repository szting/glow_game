import React from 'react';
import { Trophy, Star, Gift, X } from 'lucide-react';

interface RewardModalProps {
  show: boolean;
  onClose: () => void;
}

const RewardModal: React.FC<RewardModalProps> = ({ show, onClose }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      
      <div className="glass-card relative w-full max-w-md rounded-3xl p-8 shadow-2xl animate-bounce-in">
        <button
          onClick={onClose}
          className="absolute top-6 right-6 text-white/60 hover:text-white transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
        
        <div className="text-center">
          <div className="w-24 h-24 mx-auto mb-6 rounded-full rainbow-gradient flex items-center justify-center animate-pulse">
            <Trophy className="w-12 h-12 text-white" />
          </div>
          
          <h2 className="text-3xl font-bold text-white mb-4">
            🌈 Rainbow Complete! 🌈
          </h2>
          
          <p className="text-white/80 mb-6">
            Congratulations! You've unlocked all seven colors of your relationship rainbow!
          </p>
          
          <div className="glass rounded-xl p-6 mb-6">
            <h3 className="text-white font-semibold mb-4">Your Pot of Gold Reward</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Gift className="w-5 h-5 text-yellow-400" />
                <span className="text-white/80">Special Date Night Coupon</span>
              </div>
              <div className="flex items-center space-x-3">
                <Star className="w-5 h-5 text-yellow-400" />
                <span className="text-white/80">Rainbow Master Badge</span>
              </div>
              <div className="flex items-center space-x-3">
                <Trophy className="w-5 h-5 text-yellow-400" />
                <span className="text-white/80">1000 Bonus Points</span>
              </div>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-6 rounded-xl font-medium hover:shadow-lg transition-all duration-300 hover:transform hover:scale-105"
          >
            Claim Rewards
          </button>
        </div>
      </div>
    </div>
  );
};

export default RewardModal;
