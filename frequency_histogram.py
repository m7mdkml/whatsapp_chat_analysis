# text_frequency.py by mohammed - to parse chat and analyze frequency of text sent over time

import pandas as pd
import re
import matplotlib.pyplot as plt


def parse_message(chat_file_path):
    """Parse the chat file and return a DataFrame of messages."""
    messages = []
    # Regex to capture date, time, sender, and message
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s(?:AM|PM))\s-\s(.*?):\s(.*)'
    current_message = None

    with open(chat_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                timestamp_str = f"{match.group(1)} {match.group(2)}"
                sender = match.group(3)
                message = match.group(4)

                timestamp = pd.to_datetime(
                    timestamp_str, format='%m/%d/%y %I:%M %p', errors='coerce'
                )

                if current_message:
                    messages.append(current_message)

                current_message = {'timestamp': timestamp, 'sender': sender, 'message': message}
            else:
                if current_message:
                    current_message['message'] += f" {line.strip()}"  # Append continuation lines

        if current_message:
            messages.append(current_message)

    return pd.DataFrame(messages)


def plot_message_histogram(chat_df):
    """Generate a histogram of message frequency over time."""
    if chat_df.empty:
        print("The chat DataFrame is empty. Please check the input file.")
        return

    # Group messages by date
    chat_df['date'] = chat_df['timestamp'].dt.date
    message_counts = chat_df.groupby(['date', 'sender']).size().unstack(fill_value=0)

    # Plot histogram
    ax = message_counts.plot(kind='bar', stacked=True, figsize=(12, 6), width=1)
    plt.title('Frequency of Messages Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.legend(title='Sender', loc='upper left', bbox_to_anchor=(1, 1))

    # Improve x-axis readability
    ax.set_xticks(range(0, len(message_counts), max(1, len(message_counts) // 10)))  # Limit ticks
    ax.set_xticklabels(
        [date.strftime('%m/%Y') for date in message_counts.index[::max(1, len(message_counts) // 10)]],
        rotation=45,
        ha='right'
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Replace with the actual path to your WhatsApp chat file
    chat_file_path = 'wedo_chat_2017_2024.txt'

    # Load chat data into a DataFrame
    chat_df = parse_message(chat_file_path)
    print(chat_df.head())  # Display the first few rows for verification

    # Plot histograms of message frequencies
    plot_message_histogram(chat_df)

