import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Rainbow from './components/Rainbow';
import QuestCard from './components/QuestCard';
import ChallengeModal from './components/ChallengeModal';
import StatsCard from './components/StatsCard';
import RewardModal from './components/RewardModal';
import { colorQuests } from './data/quests';
import { CoupleProfile, ColorQuest } from './types';

function App() {
  const [profile, setProfile] = useState<CoupleProfile>({
    id: '1',
    users: [
      { id: '1', name: 'Alex', joinedDate: new Date() },
      { id: '2', name: 'Jordan', joinedDate: new Date() }
    ],
    rainbowProgress: {
      red: false,
      orange: false,
      yellow: false,
      green: false,
      blue: false,
      indigo: false,
      violet: false
    },
    points: {
      spark: 0,
      cozy: 0,
      sunshine: 0,
      zen: 0,
      anchor: 0,
      sage: 0,
      enigma: 0
    },
    streak: 0,
    lastActivityDate: new Date(),
    completedChallenges: []
  });

  const [quests, setQuests] = useState<ColorQuest[]>(colorQuests);
  const [selectedQuest, setSelectedQuest] = useState<ColorQuest | null>(null);
  const [showReward, setShowReward] = useState(false);

  useEffect(() => {
    // Check if all colors are unlocked
    const allColorsUnlocked = Object.values(profile.rainbowProgress).every(Boolean);
    if (allColorsUnlocked && profile.completedChallenges.length > 0) {
      setShowReward(true);
    }
  }, [profile.rainbowProgress, profile.completedChallenges]);

  const handleColorClick = (color: string) => {
    const quest = quests.find(q => q.color === color && q.unlocked);
    if (quest) {
      setSelectedQuest(quest);
    }
  };

  const handleChallengeComplete = (challengeId: string) => {
    if (!selectedQuest) return;

    const updatedProfile = { ...profile };
    updatedProfile.completedChallenges.push(challengeId);

    // Check if all challenges in the quest are completed
    const questChallengeIds = selectedQuest.challenges.map(c => c.id);
    const allQuestChallengesCompleted = questChallengeIds.every(id => 
      updatedProfile.completedChallenges.includes(id)
    );

    if (allQuestChallengesCompleted) {
      // Update rainbow progress
      updatedProfile.rainbowProgress[selectedQuest.color as keyof typeof updatedProfile.rainbowProgress] = true;
      
      // Add points
      const pointsType = selectedQuest.pointsType.toLowerCase() as keyof typeof updatedProfile.points;
      updatedProfile.points[pointsType] += 100;

      // Unlock next quest
      const currentIndex = quests.findIndex(q => q.color === selectedQuest.color);
      if (currentIndex < quests.length - 1) {
        const updatedQuests = [...quests];
        updatedQuests[currentIndex + 1].unlocked = true;
        setQuests(updatedQuests);
      }

      // Mark quest as completed
      const updatedQuests = [...quests];
      updatedQuests[currentIndex].completed = true;
      setQuests(updatedQuests);
    } else {
      // Add partial points
      const pointsType = selectedQuest.pointsType.toLowerCase() as keyof typeof updatedProfile.points;
      updatedProfile.points[pointsType] += 25;
    }

    // Update streak
    const today = new Date();
    const lastActivity = new Date(updatedProfile.lastActivityDate);
    const daysDiff = Math.floor((today.getTime() - lastActivity.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysDiff === 0) {
      // Same day, no streak change
    } else if (daysDiff === 1) {
      updatedProfile.streak += 1;
    } else {
      updatedProfile.streak = 1;
    }
    
    updatedProfile.lastActivityDate = today;
    setProfile(updatedProfile);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="fixed inset-0 bg-[url('https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=1920')] bg-cover bg-center opacity-10" />
      
      <div className="relative z-10">
        <Header 
          userName={profile.users[0]?.name || 'User'} 
          partnerName={profile.users[1]?.name}
        />
        
        <main className="container mx-auto px-4 py-8">
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Rainbow Progress */}
            <div className="lg:col-span-1">
              <div className="sticky top-24 space-y-6">
                <Rainbow 
                  progress={profile.rainbowProgress} 
                  onColorClick={handleColorClick}
                />
                <StatsCard profile={profile} />
              </div>
            </div>
            
            {/* Quest Cards */}
            <div className="lg:col-span-2">
              <div className="mb-6">
                <h2 className="text-3xl font-bold text-white mb-2">Color Quests</h2>
                <p className="text-white/70">Complete challenges to paint your rainbow of love</p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                {quests.map((quest) => (
                  <QuestCard
                    key={quest.color}
                    quest={quest}
                    onSelect={() => setSelectedQuest(quest)}
                    isActive={selectedQuest?.color === quest.color}
                  />
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
      
      {selectedQuest && (
        <ChallengeModal
          quest={selectedQuest}
          onClose={() => setSelectedQuest(null)}
          onComplete={handleChallengeComplete}
          completedChallenges={profile.completedChallenges}
        />
      )}
      
      <RewardModal 
        show={showReward} 
        onClose={() => setShowReward(false)} 
      />
      
      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.8;
          }
        }
        
        @keyframes bounce-in {
          0% {
            transform: scale(0.9);
            opacity: 0;
          }
          50% {
            transform: scale(1.05);
          }
          100% {
            transform: scale(1);
            opacity: 1;
          }
        }
        
        .animate-bounce-in {
          animation: bounce-in 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}

export default App;
