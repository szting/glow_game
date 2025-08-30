export interface Challenge {
  id: string;
  title: string;
  description: string;
  icon: string;
}

export interface ColorQuest {
  color: string;
  name: string;
  theme: string;
  challenges: Challenge[];
  pointsType: string;
  unlocked: boolean;
  completed: boolean;
  gradient: string;
  bgColor: string;
}

export interface UserProfile {
  id: string;
  name: string;
  partner?: string;
  avatar?: string;
  joinedDate: Date;
}

export interface CoupleProfile {
  id: string;
  users: UserProfile[];
  rainbowProgress: RainbowProgress;
  points: Points;
  streak: number;
  lastActivityDate: Date;
  completedChallenges: string[];
  currentQuest?: string;
}

export interface RainbowProgress {
  red: boolean;
  orange: boolean;
  yellow: boolean;
  green: boolean;
  blue: boolean;
  indigo: boolean;
  violet: boolean;
}

export interface Points {
  spark: number;
  cozy: number;
  sunshine: number;
  zen: number;
  anchor: number;
  sage: number;
  enigma: number;
}
