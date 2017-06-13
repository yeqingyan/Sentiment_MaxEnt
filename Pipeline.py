class Pipeline:
    def __init__(self, input_file, output_file):
        self.input = open(input_file, 'r')
        self.output = open(output_file, 'w')

    def close(self):
        self.input.close()
        self.output.close()

    def process(self):
        assert False, "Overwrite process function!"

    def start(self):
        print(self.__class__.__name__ + " Start")
        self.process()
        self.close()
        print(self.__class__.__name__ + " Finish")
