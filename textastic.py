"""
File: textastic.py
Description: A reusable library for text analysis and comparison
"""

import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from string import punctuation
import pandas as pd
from sankey_nlp import make_sankey
import numpy as np
import plotly.graph_objects as go

punctuation_ls = set(punctuation)
class Textastic:
    def __init__(self):
        """ constructor """
        self.data = defaultdict(dict)
        self.stop_words = []

    @staticmethod
    def _default_parser(filename, stop_words):
        """ this should probably be a default text parser
        for processing simple unformatted text files. """

        with open(filename) as f:
            words = ''
            for line in f:
                split_line = line.strip()
                split_line = split_line.split(' ')
                for word in split_line:
                    word = word.lower()
                    for letter in word:
                        if letter in punctuation_ls:
                            word = word.replace(letter, '')
                    if word not in punctuation_ls:
                        if word != '':
                            if word not in stop_words:
                                words += word + ' '

        wc = Counter(words.split(' '))
        # print(wc)
        num = len(words)
        f.close()

        results = {
            'wordcount': wc,
            'numwords': num
        }

        print("Parsed: ", filename, ": ", results)

        return results

    def load_text(self, filename, stopfile, label=None, parser=None):
        self.load_stop_words(stopfile)
        if parser is None:
            results = Textastic._default_parser(filename, self.stop_words)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v



    def load_stop_words(self, stopfile):
        with open(stopfile) as f:
            for line in f:
                self.stop_words.append(line.strip())

    def wordcount_sankey(self, word_list=None, k=5):
        word_info = []
        # text name, word, wordcount
        if word_list is None:
            for text, info in self.data['wordcount'].items():
                word_list = info.most_common(k)   # [(word, wc), ...]
                for word, wc in word_list:
                    row = {'text': text, 'word': word, 'count': wc}
                    word_info.append(row)
        else:
            for word in word_list:
                for text, info in self.data['wordcount'].items():
                    for w, wc in info.items():
                        if w == word:
                            row = {'text': text, 'word': word, 'count': wc}
                            word_info.append(row)
        word_df = pd.DataFrame(word_info)
        # print(word_df)
        make_sankey(word_df,['text','word'], 'count')

    def word_length_hist(self, cols=3):
        """
        Generates histograms of word lengths for each text document.
        """
        # define number of rows
        n_rows = (len(self.data['wordcount']) + cols - 1) // cols

        # set plot
        fig, axs = plt.subplots(n_rows, cols, constrained_layout=True)

        # get word count for each text
        ax_index = 0
        for text_name in self.data['wordcount']:
            word_counts = self.data['wordcount'][text_name]

           # add the frequency of the unique word lengths
            word_lengths = []
            for word, count in word_counts.items():
                for _ in range(count):
                    word_lengths.append(len(word))

            # update subplots based on the ax_index and cols
            ax = axs[ax_index // cols, ax_index % cols]
            ax_index += 1

            # plot and titles
            ax.hist(word_lengths, bins=range(1, max(word_lengths)))
            ax.set_title(text_name)
            ax.set_xlabel('Word Length')
            ax.set_ylabel('Frequency')

        plt.show()

    def plot_custom_sentiment_scores(self):
        # Load positive and negative words from files
        with open('positive.txt', 'r') as file:
            positive_words = set(file.read().split())

        with open('negative.txt', 'r') as file:
            negative_words = set(file.read().split())

        sentiment_scores = []

        # Calculate sentiment score for each text file
        for text_name, word_counts in self.data['wordcount'].items():
            pos_count = sum(count for word, count in word_counts.items() if word in positive_words)
            neg_count = sum(count for word, count in word_counts.items() if word in negative_words)
            sentiment_score = pos_count - neg_count  # Simple heuristic
            sentiment_scores.append((text_name, sentiment_score))

        # Sort by sentiment score for better visualization
        sentiment_scores.sort(key=lambda x: x[1], reverse=True)

        # Unpack for plotting
        texts, sentiments = zip(*sentiment_scores)

        # Plot
        plt.figure(figsize=(12, 8))  # Adjust figure size as necessary
        colors = ['lightgreen' if score >= 0 else 'salmon' for score in sentiments]
        plt.bar(texts, sentiments, color=colors)
        plt.xlabel('Text')
        plt.ylabel('Sentiment Score')
        plt.title('Comparative Sentiment Analysis Across Texts')
        plt.xticks(rotation=45, ha="right")  # Ensure the text titles are used as x-axis labels
        plt.tight_layout()
        plt.show()


def main():
    stop_words_file = 'stopwords.txt'
    text1 = 'Off_Grid_Solar_Energy.txt'
    text2 = 'Predicting_Future_with_Digital_Twins.txt'
    text3 = 'Campaign_to_Electrify_Transport.txt'
    text4 = 'Pizza_Boxes_Out_of_Endangered_Trees?.txt'
    text5 = 'Sustainable_Architecture.txt'
    text6 = 'Helping_the_Climate_Through_Social_Media.txt'
    text7 = 'Harness_Abundant_Clean_Energy.txt'
    text8 = 'Sustainable_Home_Heaters.txt'
    text9 = 'Metaverse_Helps_Climate_Change.txt'

    text_class = Textastic()
    text_class.load_text(filename=text1, stopfile =stop_words_file)
    text_class.load_text(filename=text2, stopfile=stop_words_file)
    text_class.load_text(filename=text3, stopfile=stop_words_file)
    text_class.load_text(filename=text4, stopfile=stop_words_file)
    text_class.load_text(filename=text5, stopfile=stop_words_file)
    text_class.load_text(filename=text6, stopfile=stop_words_file)
    text_class.load_text(filename=text7, stopfile=stop_words_file)
    text_class.load_text(filename=text8, stopfile=stop_words_file)
    text_class.load_text(filename=text9, stopfile=stop_words_file)
    text_class.wordcount_sankey()
    text_class.word_length_hist()
    text_class.plot_custom_sentiment_scores()

if __name__ == '__main__':
    main()