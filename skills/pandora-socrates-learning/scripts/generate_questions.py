#!/usr/bin/env python3
"""
Question generation module for Active Recall Socrates skill
Generates different types of questions based on text analysis and user knowledge
"""

import random
from typing import List, Dict, Any, Tuple, Optional
from enum import Enum
try:
    from .analyze_text import TextAnalyzer
    from .knowledge_base import UserKnowledgeBase
except ImportError:
    from analyze_text import TextAnalyzer
    from knowledge_base import UserKnowledgeBase

class QuestionType(Enum):
    BLURTING = "blurt"
    PREDICTION = "prediction"
    SUMMARY = "summary"
    SENTENCE_CONSTRUCTION = "construction"
    MCQ = "mcq"
    FILL_BLANK = "fill_blank"
    DOUBLE_TRANSLATION = "double_translation"
    REVIEW = "review"

class QuestionGenerator:
    """Generates questions based on text analysis and user performance with interactive features"""

    def __init__(self, text_analysis: Dict, knowledge_base: Optional[UserKnowledgeBase] = None):
        self.analysis = text_analysis
        self.difficulty = text_analysis['difficulty_score']
        self.keywords = text_analysis['keywords']
        self.grammar_traps = text_analysis['grammar_traps']
        self.knowledge_base = knowledge_base

    def generate_single_question(self, phase: str, question_index: int = 0) -> Dict:
        """
        Generate a single question for specific phase and index
        """
        phase_questions = self.generate_questions(phase)

        if question_index < len(phase_questions):
            # Add interactive fields for better user experience
            question = phase_questions[question_index].copy()
            question['phase'] = phase
            question['question_number'] = question_index + 1
            question['total_questions'] = len(phase_questions)
            question['interactive'] = True

            # Add explanation guidance for the answer
            question['explanation_guidance'] = self._get_explanation_guidance(question)

            return question
        else:
            return {
                'type': 'complete',
                'message': '该阶段的所有练习已完成！',
                'phase': phase,
                'interactive': True
            }

    def generate_questions(self, phase: str, user_history: List[Dict] = None) -> List[Dict]:
        """
        Generate questions for a specific phase

        Args:
            phase: 'pre-learning', 'in-learning', 'post-learning'
            user_history: Optional history of user answers for difficulty adaptation
        """
        questions = []

        # Get personalized question recommendations if knowledge base is available
        if self.knowledge_base:
            user_profile = self.knowledge_base.get_user_profile()
            question_types = self._get_phase_question_types(phase)
            personalized = self.knowledge_base.get_personalized_questions(
                self.difficulty, question_types
            )
            self.difficulty = personalized["target_difficulty"]
        else:
            question_types = self._get_phase_question_types(phase)
            personalized = {"target_difficulty": self.difficulty, "question_types": question_types}

        if phase == 'pre-learning':
            questions = self._generate_pre_learning_questions(personalized)
        elif phase == 'in-learning':
            questions = self._generate_in_learning_questions(personalized)
        elif phase == 'post-learning':
            questions = self._generate_post_learning_questions(personalized)

        # Adjust difficulty based on user history
        if user_history:
            questions = self._adapt_difficulty(questions, user_history)

        return questions

    def _get_phase_question_types(self, phase: str) -> List[str]:
        """Get appropriate question types for each phase"""
        phase_map = {
            'pre-learning': ['blurt', 'prediction'],
            'in-learning': ['summary', 'construction'],
            'post-learning': ['mcq', 'fill_blank', 'double_translation', 'review']
        }
        return phase_map.get(phase, ['summary'])

    def generate_review_questions(self, count: int = 3) -> List[Dict]:
        """Generate review questions based on past mistakes"""
        if self.knowledge_base:
            past_mistakes = self.knowledge_base.get_review_questions(count)
            if past_mistakes:
                return self._adapt_mistakes_to_questions(past_mistakes)
        return []

    def _generate_pre_learning_questions(self, personalized: Dict) -> List[Dict]:
        """Generate pre-learning questions with personalization"""
        questions = []

        # Blurting method (always included)
        questions.append({
            'type': QuestionType.BLURTING.value,
            'question': '基于这个主题，你脑子里现存的关联词汇有哪些？请列出 5-10 个。',
            'format': 'list',
            'focus': 'prior_knowledge',
            'difficulty': 1,
            'personalized': True
        })

        # Prediction challenge if user has vocabulary weakness
        if 'vocabulary' in personalized.get('focus_areas', []):
            if self.keywords['academic'] or self.keywords['technical']:
                core_words = (self.keywords['academic'][:2] +
                             self.keywords['technical'][:2])
                if core_words:
                    questions.append({
                        'type': QuestionType.PREDICTION.value,
                        'question': f'请盲猜这些词在文章中可能的含义：{", ".join(core_words[:2])}',
                        'options': [f"含义 {i+1}" for i in range(4)],
                        'focus': 'contextual_guessing',
                        'difficulty': 2,
                        'personalized': True
                    })

        # Add question from personalized types if available
        if len(questions) < 2 and personalized.get('question_types'):
            q_type = random.choice(personalized['question_types'])
            if q_type == 'blurt':
                questions.append({
                    'type': QuestionType.BLURTING.value,
                    'question': '在开始学习前，你对这个主题有什么问题？',
                    'format': 'list',
                    'focus': 'curiosity',
                    'difficulty': 1,
                    'personalized': True
                })

        return questions

    def _generate_in_learning_questions(self, personalized: Dict) -> List[Dict]:
        """Generate in-learning questions with personalization"""
        questions = []

        # Complex sentences for construction (if not a weakness)
        if 'grammar' not in personalized.get('avoid_areas', []):
            if self.analysis['complex_sentences']:
                complex_sent = random.choice(self.analysis['complex_sentences'])
                questions.append({
                    'type': QuestionType.SENTENCE_CONSTRUCTION.value,
                    'question': f"请用以下句式结构造一个关于你 Obsidian 工作流的句子：\n\"{complex_sent['text']}\"",
                    'format': 'construction',
                    'focus': 'application',
                    'difficulty': self.difficulty - 1,
                    'personalized': True
                })

        # Grammar trap awareness for weak areas
        if self.grammar_traps and 'grammar' in personalized.get('focus_areas', []):
            trap = random.choice(self.grammar_traps)
            questions.append({
                'type': QuestionType.SUMMARY.value,
                'question': f"请用简单的英语总结文章中关于 '{trap['type']}' 的部分。",
                'format': 'summary',
                'focus': 'grammar_awareness',
                'difficulty': trap.get('difficulty', 'medium'),
                'personalized': True
            })

        # Memory-focused questions if memory is a weakness
        if 'memory' in personalized.get('focus_areas', []):
            questions.append({
                'type': QuestionType.SUMMARY.value,
                'question': '读完这段后，请用自己的话记住最关键的三个点。',
                'format': 'list',
                'focus': 'memory_retention',
                'difficulty': self.difficulty,
                'personalized': True
            })

        return questions

    def _generate_post_learning_questions(self, personalized: Dict) -> List[Dict]:
        """Generate post-learning mastery questions with personalization"""
        questions = []

        # MCQ for vocabulary if vocabulary is a weakness
        if 'vocabulary' in personalized.get('focus_areas', []):
            confusable_pairs = self._get_confusable_words()
            if confusable_pairs:
                word1, word2 = random.choice(confusable_pairs)
                questions.append({
                    'type': QuestionType.MCQ.value,
                    'question': f"在刚才的语境中，表示 '{word1}' 最合适的表达是：",
                    'options': [
                        f"A. {word1}",
                        f"B. {word2}",
                        f"C. other expression",
                        f"D. both are correct"
                    ],
                    'explanation': f"{word1} vs {word2} 的区别和用法",
                    'focus': 'vocabulary_distinction',
                    'difficulty': self.difficulty,
                    'personalized': True
                })

        # Fill in the blank for comprehension
        if self.analysis['complex_sentences']:
            sentence = random.choice(self.analysis['complex_sentences'])
            blank_word = self._select_blank_word(sentence['text'])
            questions.append({
                'type': QuestionType.FILL_BLANK.value,
                'question': f"填空：{sentence['text'].replace(blank_word, '________')}",
                'answer': blank_word,
                'hint_first_letter': blank_word[0].upper() if blank_word else '',
                'focus': 'recall',
                'difficulty': self.difficulty + 1,
                'personalized': True
            })

        # Double translation if translation is a weakness
        if self.keywords['phrasal_verbs'] and 'application' in personalized.get('focus_areas', []):
            phrasal_verb = random.choice(self.keywords['phrasal_verbs'])
            questions.append({
                'type': QuestionType.DOUBLE_TRANSLATION.value,
                'question': f"将以下中文翻译成英文：{phrasal_verb} 的意思是\"办理\"",
                'answer': phrasal_verb,
                'focus': 'translation',
                'difficulty': self.difficulty - 1,
                'personalized': True
            })

        # Review question focusing on past mistakes
        if self.grammar_traps and len(personalized.get('focus_areas', [])) > 0:
            trap = random.choice(self.grammar_traps)
            questions.append({
                'type': QuestionType.REVIEW.value,
                'question': f"回顾：为什么文章中要使用 '{trap['type']}' 的结构？",
                'format': 'explanation',
                'focus': 'review',
                'difficulty': self.difficulty,
                'personalized': True
            })

        # Add review questions from past mistakes if knowledge base is available
        if self.knowledge_base:
            review_questions = self.generate_review_questions(1)
            questions.extend(review_questions)

        return questions

    def _adapt_mistakes_to_questions(self, past_mistakes: List[Dict]) -> List[Dict]:
        """Adapt past mistakes into review questions"""
        review_questions = []

        for mistake in past_mistakes[:3]:  # Convert up to 3 mistakes to review questions
            question_type = mistake.get("question_type", "general")

            if question_type == "fill_blank":
                # Create similar fill-in-the-blank question
                review_questions.append({
                    'type': QuestionType.FILL_BLANK.value,
                    'question': f"回顾：请记住这个表达 - \"{mistake.get('question_text', '')}\"",
                    'answer': mistake.get('user_answer', ''),
                    'hint_first_letter': '',
                    'focus': 'memory',
                    'difficulty': 2,
                    'personalized': True
                })

            elif question_type == "mcq":
                # Create similar MCQ focusing on the concept
                review_questions.append({
                    'type': QuestionType.MCQ.value,
                    'question': f"回顾：关于这个概念，以下哪个说法最准确？",
                    'options': ['A. 正确概念', 'B. 常见误解', 'C. 部分正确', 'D. 不相关'],
                    'focus': 'comprehension',
                    'difficulty': 3,
                    'personalized': True
                })

            else:
                # Create general review question
                review_questions.append({
                    'type': QuestionType.REVIEW.value,
                    'question': f"回顾：你之前在这个问题上的回答是什么？现在怎么理解？",
                    'format': 'explanation',
                    'focus': 'reflection',
                    'difficulty': 2,
                    'personalized': True
                })

            break  # Only create one review question for now

        return review_questions

    def _adapt_difficulty(self, questions: List[Dict], user_history: List[Dict]) -> List[Dict]:
        """Adjust question difficulty based on user performance"""
        correct_count = sum(1 for h in user_history if h.get('correct', False))
        total_count = len(user_history)

        if total_count > 0:
            accuracy = correct_count / total_count

            # Increase difficulty if doing well
            if accuracy > 0.8:
                for q in questions:
                    if q.get('difficulty'):
                        q['difficulty'] = min(q['difficulty'] + 1, 10)

            # Decrease difficulty if struggling
            elif accuracy < 0.5:
                for q in questions:
                    if q.get('difficulty'):
                        q['difficulty'] = max(q['difficulty'] - 1, 1)

        return questions

    def _get_confusable_words(self) -> List[Tuple[str, str]]:
        """Get pairs of frequently confused words"""
        return [
            ('affect', 'effect'),
            ('accept', 'except'),
            ('among', 'between'),
            ('few', 'less'),
            ('raise', 'rise'),
            ('lie', 'lay'),
            ('beside', 'besides'),
            ('complement', 'compliment')
        ]

    def _select_blank_word(self, sentence: str) -> str:
        """Select an appropriate word to blank out"""
        words = sentence.split()
        # Prefer verbs and important words
        for word in words:
            if len(word) > 3 and not word.startswith(('http', 'www', '.com')):
                return word.lower()

        return random.choice(words).lower()

    def _get_explanation_guidance(self, question: Dict) -> str:
        """Provide guidance for how to answer and what to explain"""
        guidance_map = {
            'blurt': '列出你能想到的词汇，不需要考虑是否正确，激活相关知识网络即可。',
            'prediction': '基于你的直觉猜测，不需要查词典。重点是预测能力。',
            'summary': '用简洁的语言总结核心观点，不超过规定的字数。',
            'construction': '模仿句式结构，但内容要符合你的实际情况。',
            'mcq': '不仅要选择答案，还要解释为什么选择这个答案。',
            'fill_blank': '根据上下文推断，注意时态和语法。',
            'double_translation': '既要准确翻译，又要理解文化差异。',
            'review': '回顾你的学习过程，思考为什么会出现错误。'
        }

        question_type = question.get('type', 'general')
        return guidance_map.get(question_type, '请仔细思考后给出你的答案。')

    def evaluate_answer(self, question: Dict, user_answer: str) -> Dict:
        """
        Evaluate user's answer and provide detailed feedback
        """
        result = {
            'user_answer': user_answer,
            'evaluation': '',
            'feedback': '',
            'suggestion': '',
            'score': 0,
            'next_question': None,
            'completed': False
        }

        # Simple evaluation based on question type
        if question['type'] == 'fill_blank':
            answer = question.get('answer', '')
            if answer.lower() == user_answer.lower():
                result['evaluation'] = '✅ 正确！'
                result['feedback'] = '你准确回忆起了正确的表达。'
                result['score'] = 100
            else:
                result['evaluation'] = '❌ 不完全正确'
                result['feedback'] = f'正确答案是：{answer}'
                result['suggestion'] = '注意记忆关键词汇，特别是动词和形容词。'
                result['score'] = 0

        elif question['type'] == 'mcq':
            # Simple MCQ evaluation
            result['evaluation'] = '📝 请检查你的答案'
            result['feedback'] = '选择后需要解释理由。'
            result['score'] = 50  # Partial score for selection

        else:
            # Open-ended questions need quality evaluation
            result = self._evaluate_open_answer(question, user_answer)

        return result

    def _evaluate_open_answer(self, question: Dict, user_answer: str) -> Dict:
        """Evaluate open-ended answers"""
        result = {
            'user_answer': user_answer,
            'evaluation': '',
            'feedback': '',
            'suggestion': '',
            'score': 0,
            'next_question': None,
            'completed': False
        }

        # Simple scoring based on answer quality
        answer_length = len(user_answer.strip())

        if answer_length < 10:
            result['evaluation'] = '⚠️ 答案过简'
            result['feedback'] = '答案过于简短，可能缺乏深度思考。'
            result['suggestion'] = '尝试提供更多细节和解释。'
            result['score'] = 30
        elif answer_length > 50:
            result['evaluation'] = '📝 内容丰富'
            result['feedback'] = '回答内容比较丰富，但可以考虑更加精炼。'
            result['score'] = 80
        else:
            result['evaluation'] = '✅ 回答良好'
            result['feedback'] = '回答基本完整，有思考过程。'
            result['score'] = 70

        return result
