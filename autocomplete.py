import numpy as np
class AutoComplete:
    def __init__(self) -> None:
        self.n_grams =  np.load('ngrams.npy', allow_pickle=True).tolist()
        self.vocabulary = np.load('vocabulary.npy', allow_pickle=True).tolist()
        self.k = 1.0
        
    def count_n_grams(data, n, start_token='<>', end_token = '<e>'):

        n_grams = {}
        for sentence in data:

            # prepend start token n times, and  append the end token one time
            sentence = [start_token] * n + sentence + [end_token]

            sentence = tuple(sentence)

            for i in range(len(sentence) - n + 1):

                # Get the n-gram from i to i+n
                n_gram = tuple(sentence[i:i+n])

                # check if the n-gram is in the dictionary
                if n_gram in n_grams:

                    # Increment the count for this n-gram
                    n_grams[n_gram] += 1
                else:
                    # Initialize this n-gram count to 1
                    n_grams[n_gram] = 1

        return n_grams


    def estimate_probability(self, word, previous_n_gram,
                         n_gram_counts, n_plus1_gram_counts, vocabulary_size):
        previous_n_gram = tuple(previous_n_gram)
        previous_n_gram_count = n_gram_counts.get(previous_n_gram, 0)

        denominator = previous_n_gram_count + self.k * vocabulary_size

        n_plus1_gram = previous_n_gram + (word,)

        n_plus1_gram_count = n_plus1_gram_counts.get(n_plus1_gram, 0)

        numerator = n_plus1_gram_count + self.k
        probability = numerator / denominator

        return probability


    def estimate_probabilities(self, previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary, end_token='<e>', unknown_token="<unk>"):

        previous_n_gram = tuple(previous_n_gram)

        vocabulary = vocabulary + [end_token, unknown_token]
        vocabulary_size = len(vocabulary)

        probabilities = {}
        for word in vocabulary:
            probability = self.estimate_probability(word, previous_n_gram,
                                            n_gram_counts, n_plus1_gram_counts,
                                            vocabulary_size)

            probabilities[word] = probability

        return probabilities


    def suggest_a_word(self, previous_tokens, n_gram_counts, n_plus1_gram_counts, vocabulary, end_token='<e>', unknown_token="<unk>", start_with=None):
        # length of previous words
        n = len(list(n_gram_counts.keys())[0])

        # append "start token" on "previous_tokens"
        previous_tokens = ['<s>'] * n + previous_tokens

        # From the words that the user already typed
        # get the most recent 'n' words as the previous n-gram
        previous_n_gram = previous_tokens[-n:]

        probabilities = self.estimate_probabilities(previous_n_gram,
                                            n_gram_counts, n_plus1_gram_counts,
                                            vocabulary)

        # Initialize suggested word to None
        # This will be set to the word with highest probability
        suggestion = None

        # Initialize the highest word probability to 0
        # this will be set to the highest probability
        # of all words to be suggested
        max_prob = 0


        # For each word and its probability in the probabilities dictionary:
        for word, prob in probabilities.items():  # complete this line

            # If the optional start_with string is set
            if start_with is not None:  # complete this line with the proper condition

                # Check if the beginning of the word does not match with the letters in 'start_with'
                if not word.startswith(start_with):  # complete this line with the proper condition

                    # if they don't match, skip this word (move onto the next word)
                    continue

            # Check if this word's probability
            # is greater than the current maximum probability
            if prob > max_prob:  # complete this line with the proper condition

                # If so, save this word as the best suggestion (so far)
                suggestion = word

                # Save the new maximum probability
                max_prob = prob


        return suggestion, max_prob

    def get_suggestions(self, previous_tokens, n_gram_counts_list, vocabulary, start_with=None):
        model_counts = len(n_gram_counts_list)
        suggestions = []
        for i in range(model_counts-1):
            n_gram_counts = n_gram_counts_list[i]
            n_plus1_gram_counts = n_gram_counts_list[i+1]

            suggestion = self.suggest_a_word(previous_tokens, n_gram_counts,
                                        n_plus1_gram_counts, vocabulary,
                                        start_with=start_with)
            suggestions.append(suggestion)
        return suggestions

print('Loading ngrams...')
