def index_words(text):
    """Return a list of indices where spaces occur in the text."""
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result


def index_words_iter(text):
    """Yield indices where spaces occur in the text, using a generator."""
    if text:
        yield 0  # Yield the index of the first word
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1  # Yield the index of each space


# Example usage of the list-returning function
text_input = "Hello world, this is a generator example."
indices_list = index_words(text_input)
print("Indices (list):", indices_list)  # Output: [0, 6, 12, 17, 20]

# Example usage of the generator function
indices_generator = index_words_iter(text_input)
print("Indices (generator):", list(indices_generator))  # Output: [0, 6, 12, 17, 20]
