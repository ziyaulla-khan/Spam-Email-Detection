# Email Spam Detection with Deep Learning

A deep learning-based email spam detection system using TensorFlow/Keras with a Gradio web interface.

## Features

- **Deep Learning Model**: CNN-based neural network for text classification
- **Gradio Interface**: User-friendly web interface for real-time spam detection
- **Text Preprocessing**: Automatic cleaning and normalization of email text
- **Easy to Use**: Simple API for training and prediction

## Model Architecture

The model uses a Convolutional Neural Network (CNN) architecture:
- Embedding layer for word representations
- Multiple 1D convolutional layers with max pooling
- Dense layers with dropout for regularization
- Sigmoid output for binary classification (spam/ham)

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Gradio Interface

Simply run the main script:
```bash
python spam_detector.py
```

This will:
- Load a pre-trained model if available, or train a new one with sample data
- Launch a Gradio web interface at `http://localhost:7860`

### Using the Interface

1. Open your browser and navigate to the URL shown in the terminal
2. Paste or type email text in the input box
3. Click "Submit" to get the spam detection result
4. The result shows:
   - Spam probability percentage
   - Ham (not spam) probability percentage
   - Final classification

### Programmatic Usage

```python
from spam_detector import SpamDetector

# Initialize detector
detector = SpamDetector()

# Load pre-trained model
detector.load_model()

# Predict spam
email_text = "Your email text here..."
prediction = detector.predict(email_text)
print(f"Spam probability: {prediction}")
```

### Training Your Own Model

```python
from spam_detector import SpamDetector

# Initialize detector
detector = SpamDetector()

# Prepare your data
texts = ["email text 1", "email text 2", ...]
labels = [1, 0, ...]  # 1 for spam, 0 for ham

# Train the model
detector.train(texts, labels, epochs=20, batch_size=32)

# Save the model
detector.save_model()
```

## Project Structure

```
.
├── spam_detector.py      # Main script with model and Gradio interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── spam_model.h5        # Saved model (created after training)
└── tokenizer.pkl        # Saved tokenizer (created after training)
```

## Model Details

- **Max Words**: 10,000 (vocabulary size)
- **Max Sequence Length**: 200 tokens
- **Embedding Dimension**: 128
- **Architecture**: CNN with 3 convolutional layers
- **Optimizer**: Adam
- **Loss Function**: Binary cross-entropy

## Text Preprocessing

The model automatically preprocesses input text by:
- Converting to lowercase
- Replacing email addresses with "emailaddr"
- Replacing URLs with "urladdr"
- Replacing numbers with "number"
- Removing special characters
- Normalizing whitespace

## Notes

- The model comes with sample training data for demonstration
- For production use, train the model with a larger, more diverse dataset
- Consider using datasets like the SpamAssassin Public Corpus or Enron Spam Dataset
- The model performance improves with more training data

## Requirements

- Python 3.8+
- TensorFlow 2.13+
- Gradio 4.0+
- NumPy 1.24+

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

