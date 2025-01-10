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


def plot_message_trend_line(chat_df, window_size=7):
    """Generate a trend line graph (moving average) of message frequency over time."""
    if chat_df.empty:
        print("The chat DataFrame is empty. Please check the input file.")
        return

    # Group messages by date
    chat_df['date'] = chat_df['timestamp'].dt.date
    daily_counts = chat_df.groupby(['date', 'sender']).size().unstack(fill_value=0)

    # Ensure all dates are included and resample for missing days
    daily_counts.index = pd.to_datetime(daily_counts.index)  # Convert to datetime
    daily_counts = daily_counts.resample('D').sum().fillna(0)

    # Calculate moving average for smoothing
    trend = daily_counts.rolling(window=window_size).mean()

    # Plot trend line graph
    ax = trend.plot(figsize=(12, 6), marker='', linewidth=2)
    plt.title(f'Trend of Messages Over Time (Window Size: {window_size} Days)')
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.legend(title='Sender', loc='upper left', bbox_to_anchor=(1, 1))

    # Adjust x-axis ticks and labels
    num_ticks = 10  # Adjust based on how crowded you want the x-axis
    ax.set_xticks(pd.date_range(start=daily_counts.index.min(), 
                                end=daily_counts.index.max(), 
                                periods=num_ticks))
    ax.set_xticklabels(
        [date.strftime('%b %Y') for date in pd.date_range(start=daily_counts.index.min(), 
                                                          end=daily_counts.index.max(), 
                                                          periods=num_ticks)],
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
    plot_message_trend_line(chat_df, window_size=7)

