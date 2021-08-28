# Lyrics generator

import random
import sys

def read_file(filename):
    """Reads a file and returns the text as a string"""
    with open(filename, 'r') as f:
        return f.read()

def make_chains(text):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    # Split the text into words
    words = text.split()

    # Create an empty dictionary to hold our markov chains
    chains = {}

    # Iterate through the words in the text
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    key = random.choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = random.choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return " ".join(words)

def main():
    args = sys.argv

    # Change this to read input_text from a file
    input_text = read_file(args[1])

    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)
    print random_text

if __name__ == "__main__":
    main()
