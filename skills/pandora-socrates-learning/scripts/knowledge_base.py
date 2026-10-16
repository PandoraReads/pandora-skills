#!/usr/bin/env python3
"""
Lightweight local database for Active Recall Socrates skill
Stores user learning records, error patterns, and progress tracking
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import uuid

class UserKnowledgeBase:
    """Lightweight local database for user learning data"""

    def __init__(self, user_id: str = "default", storage_dir: str = None):
        self.user_id = user_id
        self.storage_dir = storage_dir or os.path.join(os.path.expanduser("~"), ".active_recall_socrates", "data")
        self.user_file = os.path.join(self.storage_dir, f"{user_id}.json")
        self.session_file = os.path.join(self.storage_dir, "sessions.json")

        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)

        # Initialize user data if not exists
        self._init_user_data()

    def _init_user_data(self):
        """Initialize user data structure if it doesn't exist"""
        if not os.path.exists(self.user_file):
            user_data = {
                "user_id": self.user_id,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "level": "beginner",
                "total_sessions": 0,
                "total_questions": 0,
                "accuracy_rate": 0.0,
                "error_patterns": {},
                "strengths": {},
                "weaknesses": {},
                "learning_goals": [],
                "preferences": {
                    "difficulty_preference": "adaptive",
                    "question_types": ["blurting", "prediction", "summary", "construction", "mcq", "fill_blank", "translation"],
                    "language_target": "english",
                    "session_length": "medium"
                },
                "vocabulary_progress": {},
                "grammar_progress": {},
                "recent_mistakes": [],
                "achievement_streak": 0,
                "last_achievement": None
            }
            self._save_user_data(user_data)

    def _save_user_data(self, data: Dict):
        """Save user data to JSON file"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.user_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_user_data(self) -> Dict:
        """Load user data from JSON file"""
        try:
            with open(self.user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self._init_user_data()
            return self._load_user_data()

    def start_session(self, session_type: str = "learning") -> str:
        """Start a new learning session"""
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "user_id": self.user_id,
            "session_type": session_type,
            "started_at": datetime.now().isoformat(),
            "questions_asked": [],
            "answers_given": [],
            "correct_answers": 0,
            "incorrect_answers": 0,
            "difficulty_level": 0,
            "topics_covered": [],
            "errors_made": [],
            "notes": ""
        }

        # Save to sessions file
        self._save_session_data(session_data)
        return session_id

    def _save_session_data(self, session_data: Dict):
        """Save session data to sessions file"""
        sessions = self._load_all_sessions()
        sessions[session_data["session_id"]] = session_data
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)

    def _load_all_sessions(self) -> Dict:
        """Load all sessions from JSON file"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def record_question(self, session_id: str, question_data: Dict, user_answer: str, correct: bool):
        """Record a question and user's answer"""
        user_data = self._load_user_data()
        sessions = self._load_all_sessions()

        if session_id not in sessions:
            return

        session = sessions[session_id]

        # Record question
        question_record = {
            "question_text": question_data.get("question", ""),
            "question_type": question_data.get("type", "unknown"),
            "difficulty": question_data.get("difficulty", 1),
            "user_answer": user_answer,
            "correct": correct,
            "timestamp": datetime.now().isoformat(),
            "time_taken": question_data.get("time_taken", 0)
        }

        session["questions_asked"].append(question_record)
        if correct:
            session["correct_answers"] += 1
            user_data["achievement_streak"] = user_data.get("achievement_streak", 0) + 1
        else:
            session["incorrect_answers"] += 1
            user_data["achievement_streak"] = 0
            self._record_error(user_data, question_record)

        # Update user statistics
        user_data["total_sessions"] = max(user_data["total_sessions"], len(sessions))
        user_data["total_questions"] += 1

        # Calculate accuracy
        total_answered = session["correct_answers"] + session["incorrect_answers"]
        if total_answered > 0:
            session_accuracy = session["correct_answers"] / total_answered
            user_accuracy = (user_data["total_questions"] * user_data["accuracy_rate"] +
                           (1 if correct else 0)) / user_data["total_questions"]
            user_data["accuracy_rate"] = user_accuracy

        # Update level based on performance
        self._update_level(user_data)

        # Save updated data
        self._save_user_data(user_data)
        self._save_session_data(session)

    def _record_error(self, user_data: Dict, question_record: Dict):
        """Record user errors for pattern analysis"""
        error_type = self._categorize_error(question_record)

        # Update error patterns
        if error_type not in user_data["error_patterns"]:
            user_data["error_patterns"][error_type] = {
                "count": 0,
                "instances": [],
                "first_seen": datetime.now().isoformat()
            }

        error_entry = user_data["error_patterns"][error_type]
        error_entry["count"] += 1
        error_entry["instances"].append({
            "question": question_record["question_text"],
            "user_answer": question_record["user_answer"],
            "timestamp": datetime.now().isoformat()
        })

        # Keep only recent errors (last 10)
        if len(error_entry["instances"]) > 10:
            error_entry["instances"] = error_entry["instances"][-10:]

        # Update recent mistakes list
        user_data["recent_mistakes"].append({
            "error_type": error_type,
            "question": question_record["question_text"],
            "timestamp": datetime.now().isoformat()
        })

        # Keep only recent mistakes (last 20)
        if len(user_data["recent_mistakes"]) > 20:
            user_data["recent_mistakes"] = user_data["recent_mistakes"][-20:]

    def _categorize_error(self, question_record: Dict) -> str:
        """Categorize user errors for analysis"""
        question_type = question_record["question_type"]

        error_categories = {
            "vocabulary": ["fill_blank", "translation", "mcq"],
            "grammar": ["sentence_construction", "summary"],
            "comprehension": ["summary", "prediction"],
            "memory": ["blurting", "recall"],
            "application": ["construction", "mcq"]
        }

        for category, types in error_categories.items():
            if question_type in types:
                return category

        return "general"

    def _update_level(self, user_data: Dict):
        """Update user level based on performance"""
        accuracy = user_data["accuracy_rate"]
        total_questions = user_data["total_questions"]
        streak = user_data["achievement_streak"]

        # Level criteria
        level_criteria = {
            "beginner": {"accuracy": 0.5, "questions": 0},
            "elementary": {"accuracy": 0.65, "questions": 20},
            "intermediate": {"accuracy": 0.75, "questions": 50},
            "upper_intermediate": {"accuracy": 0.85, "questions": 100},
            "advanced": {"accuracy": 0.9, "questions": 200},
            "expert": {"accuracy": 0.95, "questions": 500}
        }

        current_level = user_data["level"]

        for level, criteria in level_criteria.items():
            if (accuracy >= criteria["accuracy"] and
                total_questions >= criteria["questions"] and
                level != current_level):
                user_data["level"] = level
                user_data["last_achievement"] = {
                    "achievement": f"Reached {level} level",
                    "timestamp": datetime.now().isoformat()
                }
                break

    def get_user_profile(self) -> Dict:
        """Get comprehensive user profile"""
        user_data = self._load_user_data()
        sessions = self._load_all_sessions()

        # Calculate statistics
        total_sessions = len([s for s in sessions.values() if s.get("started_at")])

        # Get recent performance (last 10 sessions)
        recent_sessions = list(sessions.values())[-10:] if len(sessions) > 10 else list(sessions.values())
        recent_accuracy = 0
        if recent_sessions:
            total_recent_questions = sum(s.get("correct_answers", 0) + s.get("incorrect_answers", 0) for s in recent_sessions)
            correct_recent = sum(s.get("correct_answers", 0) for s in recent_sessions)
            recent_accuracy = correct_recent / total_recent_questions if total_recent_questions > 0 else 0

        # Analyze strengths and weaknesses
        strengths, weaknesses = self._analyze_performance()

        return {
            "user_id": self.user_id,
            "level": user_data["level"],
            "total_sessions": total_sessions,
            "total_questions": user_data["total_questions"],
            "overall_accuracy": user_data["accuracy_rate"],
            "recent_accuracy": recent_accuracy,
            "achievement_streak": user_data["achievement_streak"],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "error_patterns": self._summarize_errors(),
            "last_updated": user_data["last_updated"],
            "preferences": user_data["preferences"],
            "learning_goals": user_data["learning_goals"]
        }

    def _analyze_performance(self) -> tuple[Dict, Dict]:
        """Analyze user performance to identify strengths and weaknesses"""
        user_data = self._load_user_data()
        sessions = self._load_all_sessions()

        # Performance by question type
        performance_by_type = {}

        for session in sessions.values():
            for question in session.get("questions_asked", []):
                q_type = question["question_type"]
                if q_type not in performance_by_type:
                    performance_by_type[q_type] = {"correct": 0, "total": 0}

                performance_by_type[q_type]["total"] += 1
                if question["correct"]:
                    performance_by_type[q_type]["correct"] += 1

        # Calculate strengths and weaknesses
        strengths = {}
        weaknesses = {}

        for q_type, stats in performance_by_type.items():
            if stats["total"] >= 5:  # Only consider types with enough samples
                accuracy = stats["correct"] / stats["total"]
                if accuracy >= 0.8:
                    strengths[q_type] = {
                        "accuracy": accuracy,
                        "attempts": stats["total"]
                    }
                elif accuracy <= 0.6:
                    weaknesses[q_type] = {
                        "accuracy": accuracy,
                        "attempts": stats["total"]
                    }

        return strengths, weaknesses

    def _summarize_errors(self) -> Dict:
        """Summarize user error patterns"""
        user_data = self._load_user_data()

        summary = {}
        for error_type, data in user_data["error_patterns"].items():
            summary[error_type] = {
                "count": data["count"],
                "recent_mistakes": len(data["instances"]),
                "first_seen": data["first_seen"]
            }

        return summary

    def get_personalized_questions(self, current_difficulty: int, question_types: List[str]) -> Dict:
        """Get personalized question recommendations"""
        user_profile = self.get_user_profile()

        # Adjust difficulty based on performance
        if user_profile["recent_accuracy"] > 0.8:
            target_difficulty = min(current_difficulty + 1, 10)
        elif user_profile["recent_accuracy"] < 0.6:
            target_difficulty = max(current_difficulty - 1, 1)
        else:
            target_difficulty = current_difficulty

        # Prioritize weak areas
        recommended_types = []

        # Add question types where user has weaknesses
        for q_type in question_types:
            if q_type in user_profile["weaknesses"]:
                recommended_types.append(q_type)

        # Add remaining question types
        for q_type in question_types:
            if q_type not in recommended_types and q_type not in user_profile["strengths"]:
                recommended_types.append(q_type)

        # Fill with remaining types
        for q_type in question_types:
            if q_type not in recommended_types:
                recommended_types.append(q_type)

        return {
            "target_difficulty": target_difficulty,
            "question_types": recommended_types,
            "focus_areas": list(user_profile["weaknesses"].keys()),
            "avoid_areas": list(user_profile["strengths"].keys())
        }

    def update_learning_goals(self, goals: List[str]):
        """Update user learning goals"""
        user_data = self._load_user_data()
        user_data["learning_goals"] = goals
        self._save_user_data(user_data)

    def get_review_questions(self, count: int = 5) -> List[Dict]:
        """Get review questions based on past mistakes"""
        user_data = self._load_user_data()
        sessions = self._load_all_sessions()

        # Collect recent mistakes
        recent_mistakes = []
        for session in sessions.values():
            for question in session.get("questions_asked", []):
                if not question["correct"]:
                    recent_mistakes.append(question)

        # Sort by timestamp and get most recent
        recent_mistakes.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return recent_mistakes[:count]

    def export_user_data(self) -> Dict:
        """Export all user data for backup or analysis"""
        user_data = self._load_user_data()
        sessions = self._load_all_sessions()

        return {
            "user_profile": user_data,
            "sessions": sessions,
            "export_date": datetime.now().isoformat(),
            "total_data_size": len(json.dumps(user_data)) + len(json.dumps(sessions))
        }

    def clear_recent_data(self, days: int = 30):
        """Clear data older than specified days"""
        user_data = self._load_user_data()
        sessions = self._load_all_sessions()

        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.isoformat()

        # Filter old sessions
        filtered_sessions = {}
        for session_id, session in sessions.items():
            if session.get("started_at", "") > cutoff_str:
                filtered_sessions[session_id] = session

        # Update recent mistakes
        user_data["recent_mistakes"] = [
            mistake for mistake in user_data["recent_mistakes"]
            if mistake.get("timestamp", "") > cutoff_str
        ]

        # Save filtered data
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_sessions, f, ensure_ascii=False, indent=2)

        self._save_user_data(user_data)