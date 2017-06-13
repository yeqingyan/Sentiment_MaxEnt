import json
from Pipeline import Pipeline

"""
Json format:
{
    "user_id1": {
        "timestamp1": 0/-1/1,
        "timestamp2": 0/-1/1
    },
    "user_id2": {
        "timestamp1": 0/-1/1,
        "timestamp2": 0/-1/1
    }
}
"""
class SentimentToJson(Pipeline):
    def __init__(self, input_file, output_file, index_file):
        super().__init__(input_file, output_file)
        self.index_file = open(index_file, 'r')

    def process(self):
        error_count = 0
        json_file = {}
        # try:
        for key, value in zip(self.index_file.readlines(), self.input.readlines()):
            userid, timestamp = map(str, key.strip().split("\t"))
            value = value.strip()
            if userid in json_file:
                json_file[userid][timestamp] = str(value)
            else:
                json_file[userid] = { timestamp: str(value)}
        # except:
        #     print(len(self.index_file.readlines()))
        #     print(len(self.input.readlines()))
        #     exit()
        json.dump(json_file, self.output)

if __name__ == "__main__":
    import argparse

    PROGRAM_DESCRIPTION = "Combine sentiment into Json file"
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('input_file', help='Input sentiment file')
    parser.add_argument('output_file', help='output json file')
    parser.add_argument('index_file', help='index file')
    args = vars(parser.parse_args())

    SentimentToJson(args['input_file'], args['output_file'], args['index_file']).start()
