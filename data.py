stack_size = {
    'wood': 99,
    'rock': 99,
    'branch': 99,
    'campfire': 101,
    'pickaxe':1
}

action = {
    'god': 'gather',
    'hand': 'gather',
    'wood': None,
    'rock': None,
    'branch': None,
    'campfire': 'place',
    'pickaxe': 'gather'
}

colors = {
    'purple': (142, 32, 167)
}

crafting = {
    'campfire': [('wood', 5), ('branch', 10)],
    'pickaxe': [('wood', 3), ('rock', 5)]
}

entity_data = {
    'pickaxe': {
        'name': 'pickaxe',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [0, 0],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'hand': 1},
        'yield': [('pickaxe', (1, 1), 100)],
        'is_barrier': False,
        'is_pickupable': True,
        'height': 0,
        'type': 'entity'
    },
    'campfire': {
        'name': 'campfire',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [0, 0],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'axe': 1, 'hand': 2},
        'yield': [('campfire', (1, 1), 100)],
        'is_barrier': True,
        'is_pickupable': True,
        'is_light_source': True,
        'height': 10,
        'type': 'entity'
    },
    'tree': {
        'name': 'tree',
        'size': [32, 32],
        'rect_size': [12, 12],
        'rect_offset': [10, 20],
        'world_offset': [5, 5],
        'gather_time': {'god': .1, 'axe': 1, 'hand': 2},
        'yield': [('wood', (8, 12), 20), ('wood', (4, 8), 100)],
        'is_barrier': True,
        'is_pickupable': True,
        'height': 10,
        'type': 'entity'
    },
    'branch': {
        'name': 'branch',
        'size': [16, 16],
        'rect_size': [14, 14],
        'rect_offset': [1, 1],
        'world_offset': [2, 2],
        'gather_time': {'god': .1, 'hand': 1},
        'yield': [('branch', (3, 4), 20), ('branch', (1, 2), 100)],
        'is_barrier': False,
        'is_pickupable': True,
        'height': 0,
        'type': 'entity'
    },
    'rock-1': {
        'name': 'rock',
        'size': [15, 5],
        'rect_size': [15, 5],
        'rect_offset': [0, 0],
        'world_offset': [0, 10],
        'gather_time': {'god': .1, 'pickaxe': 1},
        'yield': [('rock', (1, 1), 100)],
        'is_barrier': True,
        'is_pickupable': True,
        'height': 0,
        'type': 'entity'
    },
    'rock-2': {
        'name': 'rock',
        'size': [20, 10],
        'rect_size': [20, 10],
        'rect_offset': [0, 0],
        'world_offset': [0, 5],
        'gather_time': {'god': .1, 'pickaxe': 2},
        'yield': [('rock', (3, 4), 50), ('rock', (1, 2), 100)],
        'is_barrier': True,
        'is_pickupable': True,
        'height': 0,
        'type': 'entity'
    },
    'rock-3': {
        'name': 'rock',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [0, 0],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'pickaxe': 2},
        'yield': [('rock', (4, 5), 50), ('rock', (2, 3), 100)],
        'is_barrier': True,
        'is_pickupable': True,
        'height': 0,
        'type': 'entity'
    },
    'water': {
        'name': 'water',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [0, 0],
        'world_offset': [0, 0],
        'gather_time': {},
        'yield': [],
        'is_barrier': True,
        'is_pickupable': False,
        'height': 0,
        'type': 'tile'
    },
    'sand': {
        'name': 'sand',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [2, 2],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'hand': 2, 'shovel': 1},
        'yield': [('sand', (1, 1), 100)],
        'is_barrier': False,
        'is_pickupable': False,
        'height': 10,
        'type': 'tile'
    },
    'grass': {
        'name': 'grass',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [2, 2],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'hand': 2, 'shovel': 1},
        'yield': [('grass', (1, 1), 100)],
        'is_barrier': False,
        'is_pickupable': False,
        'height': 20,
        'type': 'tile'
    },
    'dirt': {
        'name': 'dirt',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [2, 2],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'hand': 2, 'shovel': 1},
        'yield': [('dirt', (1, 1), 100)],
        'is_barrier': False,
        'is_pickupable': False,
        'height': 30,
        'type': 'tile'
    },
    'stone': {
        'name': 'stone',
        'size': [16, 16],
        'rect_size': [16, 16],
        'rect_offset': [0, 0],
        'world_offset': [0, 0],
        'gather_time': {'god': .1, 'pickaxe': 2},
        'yield': [('stone', (1, 1), 100)],
        'is_barrier': False,
        'is_pickupable': False,
        'height': 25,
        'type': 'tile'
    },
}
