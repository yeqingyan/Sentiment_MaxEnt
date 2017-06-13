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
class JsonToRawTextMaxEnt(Pipeline):
    def __init__(self, input_file, output_file, index_file):
        super().__init__(input_file, output_file)
        self.index_file = open(index_file, 'w')

    def process(self):
        error_count = 0
        json_file = json.load(self.input)
        for userid, tweets in json_file.items():
            for timestamp, text in tweets.items():
                try:
                    self.index_file.write(str(userid) + "\t" + str(timestamp) + "\n")
                    self.output.write(text.replace('\n', ' ').replace('\r', ' ')+ "\n")
                except:
                    error_count += 1
        print("Error {}".format(error_count))

    def close(self):
        super().close()
        self.index_file.close()

if __name__ == "__main__":
    import argparse

    PROGRAM_DESCRIPTION = "Extract text in Json file for MaxEnt"
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('input_file', help='Input json file')
    parser.add_argument('output_file', help='output file')
    parser.add_argument('index_file', help='index file')
    args = vars(parser.parse_args())

    JsonToRawTextMaxEnt(args['input_file'], args['output_file'], args['index_file']).start()
