system_message = {'role': 'system', 'content': 'You are a kind and engaging chatbot to talk to.'}

context = [system_message]

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break

    # Add user input to context
    context.append({'role': 'user', 'content': user_input})

    # Get Model response
    chat_bot_response = chat(
        messages=context,
        temperature=0.5,
        top_p=0.5
    )

    print(f"AI: {chat_bot_response[0]}")

    # Add model response to context
    context.append({'role': 'assistant', 'content': chat_bot_response[0]})

    # summarize context to limit it
    context.append({
        'role': 'user',
        'content': 'Summarize our conversation thus far in less than 100 words. '
                   'Make sure to keep track of pertinent details about the user & topics talked about.'
    })

    chat_bot_response = chat(
        messages=context,
        temperature=0.5,
        top_p=0.5
    )

    # update context to be system & summarization
    new_system_content = (
        f'You are a kind and engaging chatbot to talk to. For reference, here is what you have '
        f'discussed with the user thus far:\n\n{chat_bot_response[0]}'
    )

    context = [{'role': 'system', 'content': new_system_content}]

    print("-----------------------------------------")
    print(f"NEW CONTEXT: {new_system_content}")
