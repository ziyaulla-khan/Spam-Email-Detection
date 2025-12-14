"""Test script to diagnose spam detection model"""
from spam_detector import detector
import numpy as np

# Test cases
test_cases = [
    ("Hi, how are you? Let's meet for coffee.", 0),  # Should be ham
    ("Congratulations! You've won $1,000,000!", 1),  # Should be spam
    ("Meeting scheduled for tomorrow at 2 PM.", 0),  # Should be ham
    ("URGENT: Your account will be suspended!", 1),  # Should be spam
    ("Thank you for your email. I'll get back to you soon.", 0),  # Should be ham
    ("Free iPhone! Click here now!", 1),  # Should be spam
]

print("=" * 70)
print("Testing Spam Detection Model")
print("=" * 70)
print(f"Model trained: {detector.is_trained}\n")

if detector.is_trained:
    for text, expected_label in test_cases:
        pred = detector.predict(text)
        if isinstance(pred, str):
            print(f"Error: {pred}")
            break
        spam_prob = float(pred)
        predicted_label = 1 if spam_prob > 0.5 else 0
        status = "✅" if predicted_label == expected_label else "❌"
        
        print(f"{status} Text: {text[:50]}...")
        print(f"   Expected: {'SPAM' if expected_label == 1 else 'HAM'}")
        print(f"   Predicted: {'SPAM' if predicted_label == 1 else 'HAM'} (Probability: {spam_prob:.4f})")
        print()
else:
    print("Model is not trained!")

