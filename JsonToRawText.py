import json
from Pipeline import Pipeline

"""
Json format:
{
    "user_id1": {
        "timestamp1": "tweet_text1",
        "timestamp2": "tweet_text2"
    },
    "user_id2": {
        "timestamp1": "tweet_text1",
        "timestamp2": "tweet_text2"
    }
}
"""
class JsonToRawText(Pipeline):
    def process(self):
        error_count = 0
        json_file = json.load(self.input)
        for tweets in json_file.values():
            for text in tweets.values():
                try:
                    self.output.write(text.replace('\n', ' ').replace('\r', ' ')+"\n")
                except:
                    error_count += 1
        print("Error {}".format(error_count))

if __name__ == "__main__":
    import argparse

    PROGRAM_DESCRIPTION = "Extract text in Json file"
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('input_file', help='Input json file')
    parser.add_argument('output_file', help='output file')
    args = vars(parser.parse_args())

    JsonToRawText(args['input_file'], args['output_file']).start()
