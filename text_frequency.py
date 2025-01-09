# text_frequency.py by mohammed - to parse chat and analyze frequency of text sent over time

import pandas as pd
import re
import matplotlib.pyplot as plt

def parse_message(chat_file_path):
    """
    Parse WhatsApp chat messages into a structured DataFrame.

    Args:
        chat_file_path (str): Path to the WhatsApp chat export file.

    Returns:
        pd.DataFrame: DataFrame with columns ['timestamp', 'sender', 'message'].
    """
    messages = []
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} (?:AM|PM)) - (.*?): (.*)'
    current_message = None

    with open(chat_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Check if line matches a new message
            match = re.match(pattern, line)
            if match:
                # Extract components
                timestamp_str = f"{match.group(1)} {match.group(2)}"
                sender = match.group(3)
                message = match.group(4)

                # Convert timestamp
                timestamp = pd.to_datetime(
                    timestamp_str, format='%m/%d/%y %I:%M %p', errors='coerce'
                )

                # Add previous message to the list if it exists
                if current_message:
                    messages.append(current_message)

                # Start a new message
                current_message = {'timestamp': timestamp, 'sender': sender, 'message': message}
            else:
                # Append to the current message if it's a continuation
                if current_message:
                    current_message['message'] += f" {line}"

        # Append the last message
        if current_message:
            messages.append(current_message)

    # Create a DataFrame
    return pd.DataFrame(messages)

def plot_message_histogram(chat_df):
    """
    Plot histograms of message frequencies over time per sender.

    Args:
        chat_df (pd.DataFrame): DataFrame containing chat data with 'timestamp' and 'sender' columns.
    """
    if chat_df.empty:
        print("The chat DataFrame is empty. Please check the input file.")
        return

    # Group messages by date and sender
    chat_df['date'] = chat_df['timestamp'].dt.date
    message_counts = chat_df.groupby(['date', 'sender']).size().reset_index(name='count')

    # Pivot for plotting
    pivot_df = message_counts.pivot(index='date', columns='sender', values='count').fillna(0)

    # Plot
    pivot_df.plot(kind='bar', stacked=True, figsize=(15, 7))
    plt.title("Message Frequency by Sender Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Messages")
    plt.legend(title="Sender")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace with the actual path to your WhatsApp chat file
    chat_file_path = chat_file_path = '/home/mohammed/Code/whatsapp_chat_analysis/wedo_chat_2017_2024.txt'

    # Load chat data into a DataFrame
    chat_df = parse_message(chat_file_path)

    # Debugging: Print the first few rows
    print(chat_df.head())

    # Plot histograms of message frequencies
    plot_message_histogram(chat_df)



