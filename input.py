import time

class Input():
    def __init__(self):
        self.key_code = {48:'0',49:'1',50:'2',51:'3',52:'4',53:'5',54:'6',55:'7',56:'8',57:'9',113:'q',119:'w',97:'a',115:'s',100:'d',304:'shift',32:'space',9:'tab'}
        self.key_held = {}
        self.key_clicked = {}
        self.active = {}
        for value in self.key_code.values():
            self.key_held[value] = False
            self.active[value] = True
            self.key_clicked[value] = False

    def update(self):
        for value in self.key_code.values():
            self.key_clicked[value] = False

    def update_held(self,event):
        #print(event.key)
        if event.key in self.key_code.keys():
            if self.key_held[self.key_code[event.key]] == False:
                self.key_clicked[self.key_code[event.key]] = True
            self.key_held[self.key_code[event.key]] = True

    def update_released(self,event):
        if event.key in self.key_code.keys():
            self.key_held[self.key_code[event.key]] = False
            self.key_clicked[self.key_code[event.key]] = False

    def deactivate_key(self,key):
        self.active[key] = False

    def activate_key(self,key):
        self.active[key] = True

input = Input()