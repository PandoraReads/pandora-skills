#!/usr/bin/env python3
"""
Interactive learning session manager for Active Recall Socrates skill
Handles phase selection, question presentation, and feedback loops
"""

import json
from typing import Dict, List, Optional, Any
try:
    from .generate_questions import QuestionGenerator
    from .knowledge_base import UserKnowledgeBase
except ImportError:
    from generate_questions import QuestionGenerator
    from knowledge_base import UserKnowledgeBase

class InteractiveSession:
    """Manages interactive learning sessions with user selection and feedback"""

    def __init__(self, text_analysis: Dict, user_id: str = "default"):
        self.text_analysis = text_analysis
        self.user_id = user_id
        self.current_phase = None
        self.current_question_index = 0
        self.question_generator = QuestionGenerator(
            text_analysis,
            UserKnowledgeBase(user_id) if user_id != "default" else None
        )
        self.session_complete = False
        self.phase_scores = {}

    def start_session(self) -> Dict:
        """Initialize the learning session with phase selection"""
        return {
            'type': 'phase_selection',
            'title': '🎯 欢迎使用 Active Recall Socrates！',
            'message': '首先，请选择你想要开始的学习阶段：',
            'options': [
                {
                    'id': 'pre-learning',
                    'emoji': '🎯',
                    'title': '预学习激活',
                    'description': '激活已有知识，为新内容做准备'
                },
                {
                    'id': 'in-learning',
                    'emoji': '📚',
                    'title': '学习中提取',
                    'description': '深入理解文本，提取核心信息'
                },
                {
                    'id': 'post-learning',
                    'emoji': '🏆',
                    'title': '学习后掌握',
                    'description': '检验学习效果，巩固记忆'
                },
                {
                    'id': 'error-review',
                    'emoji': '🔄',
                    'title': '错误回顾',
                    'description': '针对性练习，弥补薄弱环节'
                }
            ],
            'instruction': '请输入数字 1-4 选择阶段，或输入 "quit" 退出'
        }

    def confirm_phase(self, phase_id: str) -> Dict:
        """Get confirmation before starting a phase"""
        phase_names = {
            'pre-learning': '预学习激活',
            'in-learning': '学习中提取',
            'post-learning': '学习后掌握',
            'error-review': '错误回顾'
        }

        phase_descriptions = {
            'pre-learning': [
                '激活相关知识网络',
                '建立学习预期',
                '提高后续学习效率'
            ],
            'in-learning': [
                '深入理解文本内容',
                '提取关键信息',
                '培养分析能力'
            ],
            'post-learning': [
                '检验学习效果',
                '巩固记忆内容',
                '应用所学知识'
            ],
            'error-review': [
                '针对性强化练习',
                '弥补知识漏洞',
                '避免重复错误'
            ]
        }

        return {
            'type': 'phase_confirmation',
            'phase': phase_id,
            'title': f'🔄 {phase_names[phase_id]}',
            'message': f'我建议先进行{phase_names[phase_id]}，这将帮助你：',
            'benefits': phase_descriptions[phase_id],
            'question': f'你想要继续{phase_names[phase_id]}吗？(yes/no)',
            'options': ['yes', 'no']
        }

    def get_next_question(self, phase: Optional[str] = None) -> Dict:
        """Get the next question for the current phase"""
        if phase:
            self.current_phase = phase
            self.current_question_index = 0

        if not self.current_phase:
            return {
                'type': 'error',
                'message': '请先选择一个学习阶段'
            }

        # Get single question for interactive presentation
        question = self.question_generator.generate_single_question(
            self.current_phase,
            self.current_question_index
        )

        if question['type'] == 'complete':
            self.session_complete = True
            return {
                'type': 'phase_complete',
                'phase': self.current_phase,
                'message': '该阶段的所有练习已完成！'
            }

        # Format the question for presentation
        formatted_question = {
            'type': 'question',
            'phase': self.current_phase,
            'question_number': question['question_number'],
            'total_questions': question['total_questions'],
            'question': question['question'],
            'format': question.get('format', 'text'),
            'guidance': question['explanation_guidance'],
            'interactive': True,
            'options': question.get('options', []),
            'hint': question.get('hint_first_letter', ''),
            'instruction': '请仔细思考后给出你的答案'
        }

        return formatted_question

    def process_answer(self, user_answer: str) -> Dict:
        """Process user's answer and provide feedback"""
        if not self.current_phase:
            return {
                'type': 'error',
                'message': '没有找到当前的学习阶段'
            }

        # Get the current question for evaluation
        question = self.question_generator.generate_single_question(
            self.current_phase,
            self.current_question_index
        )

        # Evaluate the answer
        evaluation = self.question_generator.evaluate_answer(question, user_answer)

        # Update knowledge base if available
        if self.question_generator.knowledge_base:
            self.question_generator.knowledge_base.record_question(
                self.current_phase,
                question,
                user_answer,
                evaluation
            )

        # Determine next action
        next_action = self._determine_next_action(evaluation)

        # Format feedback
        feedback = {
            'type': 'feedback',
            'phase': self.current_phase,
            'question_number': self.current_question_index + 1,
            'user_answer': user_answer,
            'evaluation': evaluation['evaluation'],
            'feedback': evaluation['feedback'],
            'suggestion': evaluation['suggestion'],
            'score': evaluation['score'],
            'next_action': next_action,
            'interactive': True
        }

        # Update question index if moving to next question
        if next_action == 'next':
            self.current_question_index += 1

        return feedback

    def _determine_next_action(self, evaluation: Dict) -> str:
        """Determine the next action based on evaluation"""
        if evaluation['score'] >= 80:
            return 'excellent'
        elif evaluation['score'] >= 60:
            return 'good'
        elif evaluation['score'] >= 40:
            return 'okay'
        else:
            return 'review'

    def continue_or_exit(self) -> Dict:
        """Ask user whether to continue with next question or exit"""
        if self.session_complete:
            return {
                'type': 'session_complete',
                'message': '本次学习会话已完成！你想要开始新的阶段吗？',
                'options': ['new_phase', 'exit']
            }

        if self.current_question_index >= 3:  # Limit questions per session
            return {
                'type': 'session_complete',
                'message': '本阶段练习已完成！你想要：',
                'options': ['next_phase', 'new_phase', 'exit']
            }

        return {
            'type': 'continue',
            'message': '准备好继续下一题吗？',
            'options': ['continue', 'new_phase', 'exit']
        }

    def switch_phase(self, new_phase: str) -> Dict:
        """Switch to a different learning phase"""
        if new_phase == self.current_phase:
            return {
                'type': 'error',
                'message': '已经在当前阶段了'
            }

        self.current_phase = new_phase
        self.current_question_index = 0

        return {
            'type': 'phase_switched',
            'message': f'已切换到 {self._get_phase_name(new_phase)}',
            'next_question': self.get_next_question(new_phase)
        }

    def _get_phase_name(self, phase: str) -> str:
        """Get readable phase name"""
        names = {
            'pre-learning': '预学习激活',
            'in-learning': '学习中提取',
            'post-learning': '学习后掌握',
            'error-review': '错误回顾'
        }
        return names.get(phase, phase)

    def get_session_summary(self) -> Dict:
        """Get summary of the current session"""
        return {
            'type': 'summary',
            'current_phase': self.current_phase,
            'current_question': self.current_question_index + 1,
            'session_complete': self.session_complete,
            'phase_scores': self.phase_scores,
            'message': '学习会话总结'
        }
