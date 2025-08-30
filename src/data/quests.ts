import { ColorQuest } from '../types';

export const colorQuests: ColorQuest[] = [
  {
    color: 'red',
    name: 'Red',
    theme: 'Passion',
    challenges: [
      {
        id: 'red-1',
        title: 'Spicy Dinner Date',
        description: 'Cook a spicy meal together and share your favorite memories',
        icon: 'Flame'
      },
      {
        id: 'red-2',
        title: '60-Second Kiss',
        description: 'Share a passionate 60-second kiss without breaking contact',
        icon: 'Heart'
      },
      {
        id: 'red-3',
        title: 'Love Poetry',
        description: 'Write a passionate poem for each other and read them aloud',
        icon: 'PenTool'
      }
    ],
    pointsType: 'Spark',
    unlocked: true,
    completed: false,
    gradient: 'from-red-500 to-red-600',
    bgColor: 'rgba(239, 68, 68, 0.1)'
  },
  {
    color: 'orange',
    name: 'Orange',
    theme: 'Warmth',
    challenges: [
      {
        id: 'orange-1',
        title: 'Blanket Fort Movie Night',
        description: 'Build a cozy blanket fort and watch your favorite movie together',
        icon: 'Home'
      },
      {
        id: 'orange-2',
        title: 'Warm Surprise',
        description: 'Bring your partner their favorite warm drink unexpectedly',
        icon: 'Coffee'
      },
      {
        id: 'orange-3',
        title: '10-Minute Massage',
        description: 'Give each other a relaxing 10-minute massage',
        icon: 'Hand'
      }
    ],
    pointsType: 'Cozy',
    unlocked: false,
    completed: false,
    gradient: 'from-orange-500 to-orange-600',
    bgColor: 'rgba(249, 115, 22, 0.1)'
  },
  {
    color: 'yellow',
    name: 'Yellow',
    theme: 'Happiness',
    challenges: [
      {
        id: 'yellow-1',
        title: 'Kitchen Dance-Off',
        description: 'Have a silly dance-off in the kitchen to your favorite songs',
        icon: 'Music'
      },
      {
        id: 'yellow-2',
        title: 'Daily Gratitude',
        description: 'Share three things that made you happy today',
        icon: 'Smile'
      },
      {
        id: 'yellow-3',
        title: 'Spontaneous Picnic',
        description: 'Go on a spontaneous picnic in your favorite outdoor spot',
        icon: 'Sun'
      }
    ],
    pointsType: 'Sunshine',
    unlocked: false,
    completed: false,
    gradient: 'from-yellow-500 to-yellow-600',
    bgColor: 'rgba(234, 179, 8, 0.1)'
  },
  {
    color: 'green',
    name: 'Green',
    theme: 'Peace',
    challenges: [
      {
        id: 'green-1',
        title: 'Meditation Together',
        description: '10 minutes of meditation or mindfulness together',
        icon: 'Brain'
      },
      {
        id: 'green-2',
        title: 'Nature Walk',
        description: 'Take a quiet walk in nature without phones',
        icon: 'Trees'
      },
      {
        id: 'green-3',
        title: 'Forgiveness Practice',
        description: 'Forgive a small grievance and talk about it openly',
        icon: 'Heart'
      }
    ],
    pointsType: 'Zen',
    unlocked: false,
    completed: false,
    gradient: 'from-green-500 to-green-600',
    bgColor: 'rgba(34, 197, 94, 0.1)'
  },
  {
    color: 'blue',
    name: 'Blue',
    theme: 'Trust',
    challenges: [
      {
        id: 'blue-1',
        title: 'Secret Sharing',
        description: "Share a secret you've never told anyone",
        icon: 'Lock'
      },
      {
        id: 'blue-2',
        title: 'Surprise Day',
        description: 'Let your partner plan a surprise day for you',
        icon: 'Gift'
      },
      {
        id: 'blue-3',
        title: 'Active Listening',
        description: 'Practice active listening without interruption for 15 minutes',
        icon: 'Ear'
      }
    ],
    pointsType: 'Anchor',
    unlocked: false,
    completed: false,
    gradient: 'from-blue-500 to-blue-600',
    bgColor: 'rgba(59, 130, 246, 0.1)'
  },
  {
    color: 'indigo',
    name: 'Indigo',
    theme: 'Depth',
    challenges: [
      {
        id: 'indigo-1',
        title: 'Dream Discussion',
        description: 'Discuss your biggest dreams and aspirations',
        icon: 'Cloud'
      },
      {
        id: 'indigo-2',
        title: 'Perspective Shift',
        description: 'Talk about a book or film that changed your perspective',
        icon: 'BookOpen'
      },
      {
        id: 'indigo-3',
        title: 'Stargazing',
        description: 'Stargaze and talk about the universe and your place in it',
        icon: 'Star'
      }
    ],
    pointsType: 'Sage',
    unlocked: false,
    completed: false,
    gradient: 'from-indigo-500 to-indigo-600',
    bgColor: 'rgba(99, 102, 241, 0.1)'
  },
  {
    color: 'violet',
    name: 'Violet',
    theme: 'Mystique',
    challenges: [
      {
        id: 'violet-1',
        title: 'Past Discovery',
        description: "Learn something new about each other's past",
        icon: 'Clock'
      },
      {
        id: 'violet-2',
        title: 'Mystery Date',
        description: 'Plan a mysterious date with a secret location',
        icon: 'MapPin'
      },
      {
        id: 'violet-3',
        title: 'Riddle of Love',
        description: 'Write a riddle for your partner to solve about you',
        icon: 'HelpCircle'
      }
    ],
    pointsType: 'Enigma',
    unlocked: false,
    completed: false,
    gradient: 'from-violet-500 to-violet-600',
    bgColor: 'rgba(168, 85, 247, 0.1)'
  }
];
