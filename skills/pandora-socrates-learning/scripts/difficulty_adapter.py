#!/usr/bin/env python3
"""
Difficulty adaptation module for Active Recall Socrates skill
Tracks user performance and adjusts question difficulty accordingly
"""

from typing import List, Dict, Any
from enum import Enum

class Performance(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class DifficultyAdapter:
    """Manages difficulty adaptation based on user performance"""

    def __init__(self, initial_difficulty: int = 5):
        self.current_difficulty = initial_difficulty
        self.performance_history = []
        self.streak_count = 0
        self.adjustment_threshold = 3  # Adjust after 3 questions

    def record_answer(self, question: Dict, user_answer: str, correct: bool) -> Dict:
        """
        Record user's answer and update difficulty

        Args:
            question: The question that was answered
            user_answer: User's response
            correct: Whether the answer was correct

        Returns:
            Dict containing performance metrics and adjustment decisions
        """
        performance = {
            'question_type': question.get('type', 'unknown'),
            'difficulty': question.get('difficulty', self.current_difficulty),
            'user_answer': user_answer,
            'correct': correct,
            'timestamp': self._get_timestamp()
        }

        self.performance_history.append(performance)
        self._update_streak(correct)
        self._maybe_adjust_difficulty()

        return {
            'performance': performance,
            'current_difficulty': self.current_difficulty,
            'streak': self.streak_count,
            'adjustment_made': len(self.performance_history) % self.adjustment_threshold == 0
        }

    def _update_streak(self, correct: bool):
        """Update consecutive correct/incorrect streak"""
        if correct:
            self.streak_count += 1
        else:
            self.streak_count = -1  # Negative streak for incorrect answers

    def _maybe_adjust_difficulty(self):
        """Adjust difficulty based on performance patterns"""
        if len(self.performance_history) < self.adjustment_threshold:
            return

        recent_performance = self.performance_history[-self.adjustment_threshold:]
        correct_count = sum(1 for p in recent_performance if p['correct'])
        accuracy = correct_count / len(recent_performance)

        # Increase difficulty if performing well
        if accuracy >= 0.8 and self.streak_count >= 2:
            self.current_difficulty = min(self.current_difficulty + 1, 10)
            self.streak_count = 0  # Reset after adjustment
            return {'action': 'increase', 'reason': 'high accuracy'}

        # Decrease difficulty if struggling
        elif accuracy <= 0.4 or self.streak_count <= -2:
            self.current_difficulty = max(self.current_difficulty - 1, 1)
            self.streak_count = 0  # Reset after adjustment
            return {'action': 'decrease', 'reason': 'low accuracy or poor streak'}

        return {'action': 'maintain', 'reason': 'balanced performance'}

    def get_performance_summary(self) -> Dict:
        """Get summary of recent performance"""
        if not self.performance_history:
            return {'status': 'no_data'}

        recent = self.performance_history[-10:]  # Last 10 questions
        correct = sum(1 for p in recent if p['correct'])
        accuracy = correct / len(recent)

        return {
            'total_questions': len(recent),
            'correct_answers': correct,
            'accuracy': accuracy,
            'current_difficulty': self.current_difficulty,
            'difficulty_trend': self._get_trend(),
            'recommendation': self._get_recommendation(accuracy)
        }

    def _get_trend(self) -> str:
        """Analyze performance trend"""
        if len(self.performance_history) < 5:
            return 'insufficient_data'

        recent = self.performance_history[-5:]
        correct = sum(1 for p in recent if p['correct'])

        if correct >= 4:
            return 'improving'
        elif correct <= 1:
            return 'declining'
        else:
            return 'stable'

    def _get_recommendation(self, accuracy: float) -> str:
        """Get learning recommendation based on performance"""
        if accuracy >= 0.8:
            return "Try more challenging material or increase difficulty"
        elif accuracy >= 0.6:
            return "Maintain current difficulty level"
        elif accuracy >= 0.4:
            return "Review basic concepts before continuing"
        else:
            return "Go back to fundamentals and build confidence"

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()