from flask import jsonify

def get_filtered_data(df, category, topics, time, level):
    status_message = "Here are elearning matching your interest & level" #default message
    # step 1: Initial filter by category if provided
    if category:
        filtered_df = df[df['Type'] == category]
    else:
        filtered_df = df
   
    # step 2 Further filter by topic if provided
    if topics:
        #if it is an array, filter by all topics
        filtered_df = filtered_df[filtered_df['Onderwerp'].isin(topics)]
    
    #step 3 Further filter by time if provided
    if time:
        filtered_df = filtered_df[filtered_df['Tijdsinvestering'] <= float(time)]
    
    #step 4 Further filter by level if provided
    if level:
        filtered_df = filtered_df[filtered_df['Niveau'] <= int(level)]

    #if no results found, return all elearnings for this level
    if filtered_df.empty:
        filtered_df = df[df['Niveau'] < int(level)]
        status_message = "No elearnings matching your criteria. Listing all learnings"

    filtered_df.reset_index(drop=True, inplace=True)

    result = jsonify({
        'status': status_message,
        'data': filtered_df.to_dict(orient='records')
    })
    return result