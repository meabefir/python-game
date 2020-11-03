class Input():
    def __init__(self):
        self.key_code = {119:'w',97:'a',115:'s',100:'d',304:'shift',32:'space'}
        self.key_held = {}
        for value in self.key_code.values():
            self.key_held[value] = False

    def update_held(self,event):
        self.key_held[self.key_code[event.key]] = True

    def update_released(self,event):
        self.key_held[self.key_code[event.key]] = False
