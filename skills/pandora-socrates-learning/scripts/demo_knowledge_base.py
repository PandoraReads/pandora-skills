#!/usr/bin/env python3
"""
Example usage of the Active Recall Socrates knowledge base system
Demonstrates how to use the local database for personalized learning
"""

from knowledge_base import UserKnowledgeBase
from generate_questions import QuestionGenerator
from analyze_text import TextAnalyzer

def demo_knowledge_base():
    """Demonstrate the knowledge base functionality"""

    # Initialize knowledge base for a user
    kb = UserKnowledgeBase(user_id="demo_user")

    print("=== Active Recall Socrates Knowledge Base Demo ===\n")

    # Get user profile (initial state)
    profile = kb.get_user_profile()
    print(f"Initial User Profile:")
    print(f"  Level: {profile['level']}")
    print(f"  Total Questions: {profile['total_questions']}")
    print(f"  Accuracy Rate: {profile['accuracy_rate']:.2%}")
    print(f"  Achievement Streak: {profile['achievement_streak']}")
    print()

    # Start a session
    session_id = kb.start_session()
    print(f"Started session: {session_id}")
    print()

    # Sample text for analysis
    sample_text = """
    Active Recall is a powerful learning method that forces the brain to retrieve information from memory rather than passively absorbing it. This creates stronger neural pathways and improves long-term retention. The key principle is that the more difficult the retrieval, the stronger the memory becomes.
    """

    # Analyze text
    analyzer = TextAnalyzer()
    text_analysis = analyzer.analyze_text(sample_text)
    print(f"Text Analysis Results:")
    print(f"  Difficulty Score: {text_analysis['difficulty_score']}/10")
    print(f"  Keywords found: {len(text_analysis['keywords']['academic'])} academic words")
    print()

    # Generate questions with knowledge base integration
    question_generator = QuestionGenerator(text_analysis, kb)
    questions = question_generator.generate_questions('pre-learning')

    print("Generated Pre-Learning Questions:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q['question']} (Type: {q['type']}, Difficulty: {q['difficulty']})")
        if q.get('personalized'):
            print(f"     [Personalized based on user history]")
    print()

    # Simulate user answering questions
    print("Simulating user responses...")

    # Simulate a correct answer
    question_data = questions[0]
    kb.record_question(session_id, question_data, "some words", True)

    # Simulate an incorrect answer
    question_data2 = questions[1] if len(questions) > 1 else questions[0]
    kb.record_question(session_id, question_data2, "wrong answer", False)

    print("Recorded user answers: 1 correct, 1 incorrect")
    print()

    # Get updated profile
    updated_profile = kb.get_user_profile()
    print("Updated User Profile:")
    print(f"  Level: {updated_profile['level']}")
    print(f"  Total Questions: {updated_profile['total_questions']}")
    print(f"  Accuracy Rate: {updated_profile['accuracy_rate']:.2%}")
    print(f"  Recent Accuracy: {updated_profile['recent_accuracy']:.2%}")
    print()

    # Show error analysis
    if updated_profile['error_patterns']:
        print("Error Pattern Analysis:")
        for error_type, data in updated_profile['error_patterns'].items():
            print(f"  {error_type}: {data['count']} occurrences")
    print()

    # Get personalized recommendations
    personalized = kb.get_personalized_questions(text_analysis['difficulty_score'],
                                             ['blurt', 'prediction', 'summary'])
    print("Personalized Question Recommendations:")
    print(f"  Target Difficulty: {personalized['target_difficulty']}")
    print(f"  Focus Areas: {personalized['focus_areas']}")
    print(f"  Question Types: {personalized['question_types']}")
    print()

    # Generate review questions
    review_questions = question_generator.generate_review_questions(3)
    if review_questions:
        print("Review Questions based on past mistakes:")
        for i, q in enumerate(review_questions, 1):
            print(f"  {i}. {q['question']}")
    else:
        print("No past mistakes to review yet.")
    print()

    # Export user data
    exported_data = kb.export_user_data()
    print(f"Data exported successfully. Size: {exported_data['total_data_size']} bytes")

    # Clean up demo data (optional)
    # kb.clear_recent_data(days=0)  # Clear all data

    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_knowledge_base()