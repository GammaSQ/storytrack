class menue:
    def __init__(self, options, question):
        self.options=options
        self.question=question

    def __call__(self, option=None, **kwargs):
        if option==None:
            option=self.question()
        return self.options[option](**kwargs)

class cmd_menue(menue):
    def __init__(self, options, question=""):
        if question == "":
            if type(options) == list:
                question = ', '.join(range(len(options)))
            elif type(options) == dict:
                question = '"%s"'%'", "'.join(keys(options))
        super(cmd_menue, super).__init__(options, ret_string(question))

class ret_string:
    def __init__(self, response):
        self.response=response

    def __call__(self):
        return self.response
