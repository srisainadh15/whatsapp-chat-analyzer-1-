import re
import pandas as pd
from datetime import datetime
def preprocess(data):
    pattern1 = r"(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2})\s?(AM|PM)"

    def convert_to_24h(match):
        date_str = f"{match.group(1)}, {match.group(2)} {match.group(3)}"
        dt_obj = datetime.strptime(date_str, "%m/%d/%y, %I:%M %p")
        return dt_obj.strftime("%m/%d/%y, %H:%M")

    # Replace in the original text
    converted_data = re.sub(pattern1, convert_to_24h, data)

    print(converted_data)

    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{2}:\d{2}\s-\s'
    messages = re.split(pattern, converted_data)[1:]
    dates = re.findall(pattern, converted_data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean trailing ' -' and strip spaces
    df['message_date'] = df['message_date'].str.strip().str.replace(' -', '', regex=False)

    # Parse using correct format: MM/DD/YY
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M')

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df
