def generate_messages(similar_context, chat_history):
    """Generate the full list of messages for the model."""
    messages = [{"role": role, "content": content} for role, content in similar_context]
    messages += [{"role": role, "content": message} for role, message in chat_history]
    return messages
