# text_frequency.py by mohammed - to parse chat and analyze frequency of text sent over time

import re # parsing library
from datetime import datetime # adding the from makes it so only the datetime class is imported
import pandas as pd
import matplotlib.pyplot as plt

# loads and process the chat into a dataframe
def load_chat(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file: # utf-8 is for odd characters
        for line in file:
            parsed = parse_message(line)
            if parsed:
               data.append(parsed)
    # creates a dataframe
    df = pd.DataFrame(data, columns=['timestamp', 'sender', 'message'])
    # convert timestamp into datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], format= "%m/%d/%y, %I:%M %p")
    return df


# To parse a single chat line
def parse_message(line):
    """
    Function to parse timestamps. r indicates raw string, each group is a pair of parenthesis and each group extracts matched text. 
    group 1 captures date format - \d is for matching digits 
    group 2 captures time format - spaces are matched literally, using ?: amends the AM|PM to the same group
    group 3 captures sender - *? will capture characters non-greedily i.e. it will capture everything before the :
    group 4 captures the message greedily
    """
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} (?:AM|PM)) - (.*?): (.*)"
    match = re.match(pattern, line) # checks if line matches parsed format
    if match:
        date, time, sender, message = match.groups() # if the groups match they will be stored into variables 
        timestamp = f"{date}, {time}" # combines date and time into a string
        return timestamp, sender, message
    return None
    
# plot message frequency over time
def plot_graph(df):
    # Group by sender and count daily messages
    df['date'] = df['timestamp'].dt.date
    message_counts = df.groupby(['sender', 'date']).size().unstack(fill_value=0)
    
    # plot histograms
    plt.figure(figsize=(10, 6))
    for sender in message_counts.index:
        message_counts.loc[sender].plot(kind='bar', alpha=0.5, label=sender)
    
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.title('Message Frequency Over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace with desired Whatsapp backup
    chat_file = "wedo_chat_2017_2024.txt"
    
    # load chat into DataFrame
    chat_df = load_chat(chat_file)
    
    plot_graph(chat_df)
    

