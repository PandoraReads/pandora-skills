#!/usr/bin/env python3
"""
Lightweight text analysis module for Active Recall Socrates skill
Analyzes text to extract keywords, grammar patterns, and logical structures
"""

import re
import string
from typing import Dict, List, Tuple, Set
from collections import defaultdict

class TextAnalyzer:
    """Analyzes input text to identify learning elements"""

    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must',
            'shall', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'them', 'their', 'what', 'which', 'who', 'when', 'where',
            'why', 'how', 'all', 'each', 'every', 'some', 'any', 'few', 'more',
            'most', 'other', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among'
        }

    def analyze_text(self, text: str) -> Dict:
        """
        Perform deep analysis of text content

        Returns:
            Dict containing: keywords, grammar_traps, logical_nodes, difficulty_score
        """
        words = self._clean_and_tokenize(text)

        analysis = {
            'keywords': self._extract_keywords(words),
            'grammar_traps': self._identify_grammar_patterns(text),
            'logical_nodes': self._find_logical_structure(text),
            'difficulty_score': self._calculate_difficulty(text, words),
            'complex_sentences': self._find_complex_sentences(text),
            'vocabulary_levels': self._analyze_vocabulary(words)
        }

        return analysis

    def _clean_and_tokenize(self, text: str) -> List[str]:
        """Clean and tokenize text"""
        # Remove punctuation and convert to lowercase
        text = text.lower()
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        words = text.split()
        # Remove stop words
        return [word for word in words if word not in self.stop_words and len(word) > 2]

    def _extract_keywords(self, words: List[str]) -> Dict[str, List[str]]:
        """Extract keywords by category"""
        keywords = {
            'academic': [],
            'technical': [],
            'frequent': [],
            'phrasal_verbs': []
        }

        for word in words:
            # Academic words (longer, less common)
            if len(word) > 8:
                keywords['academic'].append(word)

            # Frequent words in learning contexts
            if word in ['learning', 'process', 'method', 'theory', 'concept',
                       'practice', 'skill', 'ability', 'system', 'approach']:
                keywords['frequent'].append(word)

            # Technical indicators (capitalized in original would be caught here)
            if any(char.isdigit() for char in word):
                keywords['technical'].append(word)

        # Remove duplicates
        for category in keywords:
            keywords[category] = list(set(keywords[category]))

        return keywords

    def _identify_grammar_patterns(self, text: str) -> List[Dict]:
        """Identify potential grammar trouble spots"""
        traps = []

        # Check for passive voice patterns
        passive_patterns = [
            r'\b(is|are|was|were) \w+ (by|to)\b',
            r'\b(have been|has been|had been) \w+\b',
            r'\b(am|is|are) being \w+\b'
        ]

        for pattern in passive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                traps.append({
                    'type': 'passive_voice',
                    'description': 'Passive voice detected',
                    'difficulty': 'medium'
                })

        # Check for complex prepositional phrases
        prep_count = len(re.findall(r'\b(in|on|at|to|for|with|by|from|up|about|into|through|during|before|after)\s+\w+', text, re.IGNORECASE))
        if prep_count > 10:
            traps.append({
                'type': 'complex_prepositions',
                'description': 'Many prepositional phrases detected',
                'difficulty': 'high'
            })

        # Check for modal verbs
        modals = re.findall(r'\b(can|could|should|would|will|might|may|must|shall)\s+\w+', text, re.IGNORECASE)
        if len(modals) > 5:
            traps.append({
                'type': 'multiple_modals',
                'description': 'Frequent modal verb usage',
                'difficulty': 'medium'
            })

        return traps

    def _find_logical_structure(self, text: str) -> Dict[str, List[str]]:
        """Identify logical connectors and relationships"""
        logical_nodes = {
            'cause_effect': [],
            'contrast': [],
            'addition': [],
            'conclusion': []
        }

        logical_patterns = {
            'cause_effect': ['because', 'since', 'therefore', 'as a result', 'due to'],
            'contrast': ['however', 'although', 'despite', 'on the other hand', 'yet'],
            'addition': ['furthermore', 'moreover', 'additionally', 'also', 'besides'],
            'conclusion': ['in conclusion', 'to summarize', 'overall', 'finally', 'thus']
        }

        text_lower = text.lower()
        for category, patterns in logical_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    logical_nodes[category].append(pattern)

        return logical_nodes

    def _calculate_difficulty(self, text: str, words: List[str]) -> int:
        """Calculate text difficulty score 1-10"""
        score = 1

        # Word length complexity
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        if avg_word_length > 7:
            score += 3
        elif avg_word_length > 5:
            score += 1

        # Sentence complexity
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(sent.split()) for sent in sentences) / len(sentences) if sentences else 0
        if avg_sentence_length > 25:
            score += 3
        elif avg_sentence_length > 15:
            score += 1

        # Vocabulary variety
        unique_words = len(set(words))
        if unique_words > 200:
            score += 2
        elif unique_words > 100:
            score += 1

        # Complex sentence structures
        long_sentences = [s for s in sentences if len(s.split()) > 20]
        if len(long_sentences) > len(sentences) * 0.3:
            score += 1

        return min(score, 10)

    def _find_complex_sentences(self, text: str) -> List[Dict]:
        """Find sentences with complex structures"""
        complex = []
        sentences = re.split(r'[.!?]+', text)

        for sent in sentences:
            if len(sent.split()) > 15:  # Long sentences
                clauses = self._count_clauses(sent)
                if clauses > 2:
                    complex.append({
                        'text': sent.strip(),
                        'clauses': clauses,
                        'difficulty': 'complex' if clauses > 3 else 'moderate'
                    })

        return complex

    def _count_clauses(self, sentence: str) -> int:
        """Count number of clauses in a sentence"""
        # Simple count of verbs as proxy for clauses
        verb_count = len(re.findall(r'\b\w+ing\b|\b\w+ed\b|\b\w+s\b', sentence, re.IGNORECASE))
        return max(1, verb_count)

    def _analyze_vocabulary(self, words: List[str]) -> Dict[str, float]:
        """Analyze vocabulary difficulty distribution"""
        word_freq = defaultdict(int)

        for word in words:
            word_freq[word] += 1

        # Calculate frequency percentages
        total_words = len(words)
        if total_words == 0:
            return {'frequent_percentage': 0, 'rare_percentage': 0}

        frequent_words = sum(1 for word, freq in word_freq.items() if freq / total_words > 0.05)
        rare_words = sum(1 for word, freq in word_freq.items() if freq / total_words < 0.01)

        return {
            'frequent_percentage': frequent_words / len(word_freq) * 100,
            'rare_percentage': rare_words / len(word_freq) * 100
        }