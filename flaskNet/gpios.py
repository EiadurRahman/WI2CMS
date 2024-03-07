import json

def get_data():
    with open('gpio_state.json','r') as file:
        data = json.load(file)
    return data


def dump(gpio,state):
    if state in [0,1]:
        data = get_data()
        data[gpio] = int(state)
        with open('gpio_state.json','w') as file :
            json.dump(data,file)
    else:
        print('not a valid state')

def parse_dump(string):
    try:
        string = string.replace(' ','')
        gpios = string.split(',')
        for gpio in gpios:
            gpio_index = gpio.split(':')[0]
            gpio_state = int(gpio.split(':')[1])
            dump(gpio_index,gpio_state)
        print(get_data())
    except Exception as err:
        print(err)

def update_gpio_state(new_state):
    with open('gpio_state.json', 'w') as file:
        json.dump(new_state, file)

