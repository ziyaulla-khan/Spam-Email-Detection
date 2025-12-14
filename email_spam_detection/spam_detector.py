import numpy as np
import pickle
import re
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Conv1D, MaxPooling1D, GlobalMaxPooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.utils.class_weight import compute_class_weight
from sklearn.utils import shuffle
import gradio as gr
import os

class SpamDetector:
    def __init__(self, max_words=10000, max_len=200):
        self.max_words = max_words
        self.max_len = max_len
        self.tokenizer = None
        self.model = None
        self.is_trained = False
        
    def preprocess_text(self, text):
        """Clean and preprocess email text"""
        # Convert to lowercase
        text = text.lower()
        # Remove email addresses
        text = re.sub(r'\S+@\S+', 'emailaddr', text)
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', 'urladdr', text)
        # Remove numbers
        text = re.sub(r'\d+', 'number', text)
        # Remove special characters except basic punctuation
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def build_model(self):
        """Build the deep learning model"""
        model = Sequential([
            Embedding(self.max_words, 128, input_length=self.max_len),
            Conv1D(128, 5, activation='relu'),
            MaxPooling1D(5),
            Conv1D(128, 5, activation='relu'),
            MaxPooling1D(5),
            Conv1D(128, 5, activation='relu'),
            GlobalMaxPooling1D(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, texts, labels, epochs=10, batch_size=32, validation_split=0.2):
        """Train the spam detection model"""
        # Shuffle data before processing
        from sklearn.utils import shuffle
        texts, labels = shuffle(texts, labels, random_state=42)
        
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Create tokenizer and fit on texts
        self.tokenizer = Tokenizer(num_words=self.max_words, oov_token='<OOV>')
        self.tokenizer.fit_on_texts(processed_texts)
        
        # Convert texts to sequences
        sequences = self.tokenizer.texts_to_sequences(processed_texts)
        X = pad_sequences(sequences, maxlen=self.max_len)
        y = np.array(labels)
        
        # Calculate class weights for imbalanced data
        class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
        class_weight_dict = {0: class_weights[0], 1: class_weights[1]}
        print(f"Class weights: {class_weight_dict}")
        
        # Build model
        self.model = self.build_model()
        
        # Callbacks - use loss for early stopping as it's more stable
        early_stopping = EarlyStopping(
            monitor='val_loss', 
            patience=10, 
            restore_best_weights=True,
            mode='min',
            verbose=1
        )
        model_checkpoint = ModelCheckpoint(
            'best_spam_model.keras', 
            save_best_only=True, 
            monitor='val_loss',
            mode='min',
            verbose=1
        )
        
        # Train model with class weights and shuffle
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stopping, model_checkpoint],
            class_weight=class_weight_dict,
            shuffle=True,
            verbose=1
        )
        
        self.is_trained = True
        return history
    
    def predict(self, text):
        """Predict if email is spam or not"""
        if not self.is_trained or self.model is None or self.tokenizer is None:
            return "Model not trained yet. Please train the model first."
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Convert to sequence
        sequence = self.tokenizer.texts_to_sequences([processed_text])
        X = pad_sequences(sequence, maxlen=self.max_len)
        
        # Predict
        prediction = self.model.predict(X, verbose=0)[0][0]
        
        return prediction
    
    def save_model(self, model_path='spam_model.keras', tokenizer_path='tokenizer.pkl'):
        """Save the trained model and tokenizer"""
        if self.model:
            self.model.save(model_path)
        if self.tokenizer:
            with open(tokenizer_path, 'wb') as f:
                pickle.dump(self.tokenizer, f)
    
    def load_model(self, model_path='spam_model.keras', tokenizer_path='tokenizer.pkl'):
        """Load a trained model and tokenizer"""
        # Try .keras format first, then fallback to .h5 for backward compatibility
        keras_path = model_path
        h5_path = model_path.replace('.keras', '.h5')
        
        # Check for .keras file first
        if os.path.exists(keras_path) and os.path.exists(tokenizer_path):
            try:
                self.model = load_model(keras_path)
                with open(tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                self.is_trained = True
                return True
            except Exception as e:
                print(f"Warning: Could not load .keras model: {e}")
        
        # Fallback to .h5 format
        if os.path.exists(h5_path) and os.path.exists(tokenizer_path):
            try:
                self.model = load_model(h5_path)
                with open(tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                self.is_trained = True
                print("⚠️  Loaded legacy .h5 model. Consider retraining to use .keras format.")
                return True
            except Exception as e:
                print(f"Warning: Could not load .h5 model: {e}")
        
        return False

# Initialize the spam detector
detector = SpamDetector()

# Try to load existing model, otherwise create sample data
print("=" * 60)
print("Initializing Email Spam Detection System...")
print("=" * 60)

if not detector.load_model():
    print("\n⚠️  No pre-trained model found. Creating sample training data...")
    
    # Expanded spam and ham emails for training (more diverse examples)
    spam_samples = [
        "Congratulations! You've won $1,000,000! Click here to claim your prize now!",
        "URGENT: Your account will be suspended. Verify your information immediately!",
        "Limited time offer! Buy now and get 90% off! Don't miss this opportunity!",
        "You have been selected for a free gift card. Enter your details to claim!",
        "Make money fast! Work from home and earn $5000 per week. No experience needed!",
        "Your payment failed. Update your credit card information now to avoid service interruption.",
        "Free iPhone! Just click this link and complete a short survey to receive your free phone!",
        "Act now! Your subscription expires in 24 hours. Renew now to continue service.",
        "You've inherited $500,000! Contact us immediately to claim your inheritance!",
        "Hot singles in your area want to meet you! Click here to see who's interested!",
        "Your package delivery failed. Click here to reschedule and avoid return to sender.",
        "Bank account alert: Suspicious activity detected. Verify your account immediately.",
        "Get rich quick! Invest in cryptocurrency and watch your money grow 10x in days!",
        "Free trial ending soon! Your credit card will be charged $99.99 unless you cancel.",
        "You've won a luxury vacation! Claim your all-expenses-paid trip to the Bahamas now!",
        "Important: Your email storage is full. Upgrade now to avoid losing messages.",
        "Exclusive deal for you! 50% off all products. Use code SAVE50 at checkout.",
        "Your social media account has been compromised. Reset your password immediately!",
        "Make $1000 a day from home! No skills required. Start earning money today!",
        "Your order has been confirmed. Click here to track your shipment status.",
        "WINNER! You have been selected to receive a brand new car! Claim now!",
        "URGENT ACTION REQUIRED: Your PayPal account needs verification immediately!",
        "Get instant cash! No credit check required. Apply now and get approved today!",
        "You have unclaimed money waiting! Click here to claim your $5000 reward!",
        "Special promotion: Buy one get ten free! Limited stock available now!",
        "Your computer has been infected! Download our antivirus software immediately!",
        "You've been chosen! Enter our exclusive lottery and win millions!",
        "Warning: Your Netflix account will be deleted. Verify your payment method now!",
        "Earn money by clicking ads! Make $200 per day working from home!",
        "Your Amazon Prime membership is expiring. Renew now to avoid cancellation!",
        "Congratulations! You've won a free cruise! Book your trip today!",
        "Your bank account has been locked. Click here to unlock it immediately!",
        "Get prescription drugs without a doctor! Order now and save 90%!",
        "You have 24 hours to claim your prize! Don't miss this opportunity!",
        "Your email has been hacked! Change your password immediately by clicking here!",
        "Free money! No strings attached. Just provide your bank details!",
        "Your credit score needs attention. Sign up now for our premium service!",
        "You've won the lottery! Claim your $10 million prize now!",
        "URGENT: Your account will be closed. Verify your identity immediately!",
        "Get instant loans! No questions asked. Apply now and get money today!",
    ]
    
    ham_samples = [
        "Hi, just wanted to check in and see how you're doing. Let's catch up soon!",
        "Meeting scheduled for tomorrow at 2 PM in the conference room. Please confirm attendance.",
        "Thank you for your application. We'll review it and get back to you within a week.",
        "The quarterly report is ready for review. Please find it attached to this email.",
        "Reminder: Team lunch this Friday at 12:30 PM. Please RSVP by Thursday.",
        "I wanted to follow up on our conversation from yesterday. Can we schedule a call?",
        "The project deadline has been extended to next Friday. Please update your timeline accordingly.",
        "Happy birthday! Hope you have a wonderful day filled with joy and celebration.",
        "Please find the document you requested attached. Let me know if you need any changes.",
        "The software update has been completed successfully. All systems are running normally.",
        "I'm writing to confirm our appointment for next Tuesday at 10 AM. See you then!",
        "Thank you for your feedback. We appreciate your input and will take it into consideration.",
        "The budget proposal has been approved. We can proceed with the project as planned.",
        "I hope this email finds you well. I wanted to discuss the upcoming project with you.",
        "The training session has been rescheduled to next week. New date and time to follow.",
        "Congratulations on completing the certification! Your hard work has paid off.",
        "Please review the attached contract and let me know if you have any questions.",
        "I wanted to thank you for your help with the presentation. It went really well!",
        "The office will be closed next Monday for a holiday. Please plan accordingly.",
        "I'm looking forward to our collaboration on this project. Let's make it a success!",
        "Hi John, I hope you're doing well. I wanted to discuss the project timeline with you.",
        "The meeting has been moved to next Wednesday at 3 PM. Please update your calendar.",
        "Thank you for your patience. I'll have the report ready by end of day tomorrow.",
        "I wanted to share some good news about the project. Can we schedule a brief call?",
        "Please find attached the presentation slides for tomorrow's meeting.",
        "I hope you had a great weekend. Let's touch base about the upcoming deadline.",
        "The client has approved the proposal. We can move forward with the next phase.",
        "I wanted to follow up on the email I sent last week. Have you had a chance to review it?",
        "The conference call is scheduled for Friday at 10 AM. Dial-in details are attached.",
        "Thank you for your quick response. I appreciate your help with this matter.",
        "I'm writing to introduce myself. I'll be working with you on the new project.",
        "The document has been updated based on your feedback. Please review when you have a moment.",
        "I wanted to confirm that I received your email. I'll get back to you by end of week.",
        "The team meeting has been canceled. We'll reschedule for next week.",
        "Thank you for your interest in our company. We'll be in touch soon.",
        "I hope this message finds you well. I wanted to discuss a potential collaboration.",
        "The invoice has been processed and payment should be received within 5 business days.",
        "I wanted to thank you for attending yesterday's meeting. Your input was very valuable.",
        "Please let me know if you have any questions about the proposal. I'm happy to discuss.",
        "I'm reaching out to schedule a follow-up meeting. What time works best for you?",
    ]
    
    # Combine and label data
    all_texts = spam_samples + ham_samples
    all_labels = [1] * len(spam_samples) + [0] * len(ham_samples)
    
    # Train the model
    print(f"\n🔄 Training model with {len(all_texts)} samples ({len(spam_samples)} spam, {len(ham_samples)} ham)...")
    print("This may take a few minutes. Please wait...\n")
    detector.train(all_texts, all_labels, epochs=50, batch_size=16, validation_split=0.2)
    detector.save_model()
    print("\n✅ Model trained and saved successfully!")
else:
    print("\n✅ Pre-trained model loaded successfully!")

def predict_spam(email_text):
    """Gradio prediction function"""
    if not email_text or email_text.strip() == "":
        return "Please enter an email text to analyze."
    
    prediction = detector.predict(email_text)
    
    if isinstance(prediction, str):
        return prediction
    
    spam_probability = float(prediction)
    ham_probability = 1 - spam_probability
    
    result = f"""
    **Spam Probability:** {spam_probability:.2%}
    **Ham (Not Spam) Probability:** {ham_probability:.2%}
    
    **Classification:** {'🚨 SPAM' if spam_probability > 0.5 else '✅ NOT SPAM'}
    """
    
    return result

# Create Gradio interface
def create_interface():
    interface = gr.Interface(
        fn=predict_spam,
        inputs=gr.Textbox(
            label="Email Text",
            placeholder="Enter the email content here to check if it's spam...",
            lines=10
        ),
        outputs=gr.Markdown(label="Spam Detection Result"),
        title="📧 Email Spam Detection",
        description="""
        This tool uses a deep learning model (CNN-based) to detect spam emails.
        Simply paste the email content in the text box below and click 'Submit' to analyze.
        
        The model analyzes the text and provides:
        - Spam probability percentage
        - Ham (not spam) probability percentage
        - Final classification result
        """,
        examples=[
            ["Congratulations! You've won $1,000,000! Click here to claim your prize now!"],
            ["Hi, just wanted to check in and see how you're doing. Let's catch up soon!"],
            ["URGENT: Your account will be suspended. Verify your information immediately!"],
            ["Meeting scheduled for tomorrow at 2 PM in the conference room. Please confirm attendance."],
        ]
    )
    return interface

if __name__ == "__main__":
    # Verify model is ready
    if not detector.is_trained:
        print("\n❌ Error: Model is not trained. Cannot start interface.")
        exit(1)
    
    print("\n" + "=" * 60)
    print("🚀 Starting Gradio Web Interface...")
    print("=" * 60)
    print("\n📝 The interface will open in your browser automatically.")
    print("🌐 If it doesn't open, navigate to: http://127.0.0.1:7860")
    print("\n⏹️  Press Ctrl+C to stop the server\n")
    
    # Launch Gradio interface
    try:
        interface = create_interface()
        interface.launch(
            share=False, 
            server_name="127.0.0.1", 
            server_port=7860, 
            theme=gr.themes.Soft(),
            inbrowser=True,
            show_error=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTrying alternative configuration...")
        interface.launch(
            share=False, 
            server_port=7860, 
            theme=gr.themes.Soft(),
            inbrowser=True
        )

