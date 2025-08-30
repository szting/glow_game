import React from 'react';
import { Heart, Users, Sparkles } from 'lucide-react';

interface HeaderProps {
  userName: string;
  partnerName?: string;
}

const Header: React.FC<HeaderProps> = ({ userName, partnerName }) => {
  return (
    <header className="glass-dark border-b border-white/10 sticky top-0 z-40">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full rainbow-gradient flex items-center justify-center">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gradient">Chromance</h1>
              <p className="text-white/60 text-xs">Level up your love</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="glass rounded-full px-4 py-2 flex items-center space-x-2">
              <Users className="w-4 h-4 text-white/60" />
              <span className="text-white text-sm font-medium">
                {userName} {partnerName && `& ${partnerName}`}
              </span>
            </div>
            
            <button className="glass rounded-full p-2 hover:bg-white/10 transition-colors">
              <Sparkles className="w-5 h-5 text-white/80" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
