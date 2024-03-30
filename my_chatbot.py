import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.response_selection import get_random_response
import collections.abc
collections.Hashable = collections.abc.Hashable

# Creating a ChatBot instance
chatbot = ChatBot(
    "ChatPot", # Name of the chatbot
    storage_adapter='chatterbot.storage.SQLStorageAdapter', # Using SQL storage adapter
    logic_adapters=[ # List of logic adapters
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.85,
            'response_selection_method': get_random_response
        },
    ],
    database_uri='sqlite:///database.sqlite3' # Database URI for storing data
)

# Training data for ListTrainer
with open('chats.txt', 'r') as file:
    training_data = file.read().splitlines()

training_data2 = {
    "Hi there!",
    "Hello!",
    "How are you doing today?",
    "I'm great, thanks for asking!",
    "What's up?",
    "Not much, just chatting with you!",
    "Tell me a joke.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "That's a good one! Do you know any more jokes?",
    "Sure! Why did the tomato turn red? Because it saw the salad dressing!",
    "Haha, that's hilarious!",
    "What's your favorite movie?",
    "I don't watch movies, but I've heard 'The Matrix' is popular.",
    "Do you have any pets?",
    "No, I'm just a virtual assistant!",
    "What's the meaning of life?",
    "That's a deep question! The meaning of life is subjective and varies for each individual.",
    "What do you like to do for fun?",
    "I enjoy learning new things and having interesting conversations!",
    "Can you help me with my homework?",
    "I can certainly try! What subject do you need help with?",
    "Mathematics.",
    "Okay, what specific math problem do you need assistance with?",
    "I'm struggling with algebraic equations.",
    "Sure, let's work through it together. Can you provide an example equation?",
    "x^2 + 4x - 5 = 0",
    "To solve this equation, we can use the quadratic formula: x = (-b ± √(b^2 - 4ac)) / (2a).",
    "Thank you, that's helpful!",
    "You're welcome!",
    "What's the weather like today?",
    "I'm not sure, you can check the weather forecast online!",
    "Okay, thanks.",
    "No problem!",
    "What's your favorite color?",
    "I don't have preferences like humans do, but I think blue is a nice color!",
    "I agree, blue is beautiful.",
    "It's a calming color, isn't it?",
    "Yes, it is!",
    "I have to go now, talk to you later!",
    "Sure, have a great day! Bye!",
    "Goodbye!",
    "Take care!"
}

training_data3 = {
    "Hi, can I help you",
    "Who are you?",
    "I am your virtual assistant. Ask me any questions...",
    "Where do you operate?",
    "We operate from Singapore",
    "What payment methods do you accept?",
    "We accept debit cards and major credit cards",
    "I would like to speak to your customer service agent",
    "Please call +38 3333 3333. Our operating hours are from 9am to 5pm, Monday to Friday"
}
with open('nfL6.json', 'r') as json_file:
    data = json.load(json_file)
train = []
for row in data[:100]:  # Limiting to 500 rows
    train.append(row['question'])
    train.append(row['answer'])

# Function to train the chatbot
def bot_trainer():
    # Initializing ListTrainer
    trainer = ListTrainer(chatbot)
    # Training the chatbot with multiple sets of training data
    trainer.train(training_data)
    trainer.train(training_data2)
    trainer.train(training_data3)
    trainer.train(train)

    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    corpus_trainer.train('chatterbot.corpus.english')
    trainer.train("chatterbot.corpus.english.conversations")


def chatbot_run():
    print("Starting chatbot... Welcome to the chatbot! Type ':q'/'quit'/'exit' to quit.")
    exit_conditions = (":q", "quit", "exit")
    with open("chat_history.txt", "a") as file:  # Open file for documentation
        while True:
            query = input("> ") # Prompting user for input
            if query.lower() in exit_conditions: # Checking for exit conditions
                break  # Exiting the loop if user wants to quit
            else:
                response = chatbot.get_response(query) # Getting response from the chatbot
                print(f"🪴 {response}")  # Printing chatbot's response
                # Writing user query and chatbot's response to file
                file.write(f"User: {query}\nChatbot: {response}\n")

# Main function
if __name__ == "__main__":
    bot_trainer()  # Training the chatbot
    chatbot_run()  # Running the chatbot

