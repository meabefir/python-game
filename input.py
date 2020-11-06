class Input():
    def __init__(self):
        self.key_code = {119:'w',97:'a',115:'s',100:'d',304:'shift',32:'space'}
        self.key_held = {}
        self.active = {}
        for value in self.key_code.values():
            self.key_held[value] = False
            self.active[value] = True

    def update_held(self,event):
        if event.key in self.key_code.keys():
            self.key_held[self.key_code[event.key]] = True

    def update_released(self,event):
        if event.key in self.key_code.keys():
            self.key_held[self.key_code[event.key]] = False

    def deactivate_key(self,key):
        self.active[key] = False

    def activate_key(self,key):
        self.active[key] = True

input = Input()