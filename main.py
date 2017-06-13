from JsonToRawText import *
from ExtractEmotionEmoji import *
from MaxEntTrainData import *

def main():
    # Get raw sentiment text
    input_file = "./data/historical_tweet.json"
    output_file = "./data/historical_tweet.raw"
    # JsonToRawText(input_file, output_file).start()

    # Get text with emoji/emoticon
    input_file = output_file
    output_file = "./data/emoji_emoticon_only.raw"
    # ExtractEmotionEmoji(input_file, output_file).start()

    # Get train data set
    input_file = output_file
    output_file = "./data/maxent_train.input"
    MaxEntTrainData(input_file, output_file).start()

if __name__ == "__main__":
    main()
