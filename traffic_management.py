from flask import Flask, render_template, jsonify, request
from api.interface import calculate_traffic_flow

app = Flask(__name__)

class TrafficLight:
    def __init__(self, light_type='single'):
        self.light_type = light_type
        self.status = 'red'

    def change_status(self, new_status):
        self.status = new_status
        return f'Changed to {new_status}'

class TrafficControl:
    def __init__(self):
        self.lights = {
            'left': {
                'red': TrafficLight(),
                'yellow': TrafficLight(),
                'green': TrafficLight()
            },
            'right': {
                'red': TrafficLight(),
                'yellow': TrafficLight(),
                'green': TrafficLight()
            },
            'straight': {
                'red': TrafficLight(),
                'yellow': TrafficLight(),
                'green': TrafficLight()
            }
        }
        self._setup_scheduler()

    def _setup_scheduler(self):
        import threading
        def switch_loop():
            import random
            import time
            time.sleep(random.randint(5,15))
            for direction in self.lights.values():
                for color_light in direction.values():
                    current = color_light.status
                    color_light.change_status('green' if current == 'red' else 'yellow' if current == 'green' else 'red')
            threading.Timer(0, switch_loop).start()
        switch_loop()

    def get_active_states(self):
        return {k: v.status for k, v in self.lights.items()}

@app.route('/')
def control_panel():
    return render_template('control_panel.html')

@app.route('/api/update_flow', methods=['POST'])
def handle_flow():
    flow_data = request.json.get('flow')
    recommended_type = calculate_traffic_flow({'flow': flow_data})
    
    # 根据灯型创建对应交通灯实例
    control = TrafficControl()
    # 根据推荐灯型选择对应方向
    direction = {
        'left-turn': 'left',
        'right-turn': 'right',
        'straight': 'straight'
    }.get(recommended_type, 'straight')
    control.lights[direction]['green'].change_status('green')
    
    return jsonify({
        'status': 'success',
        'recommended_type': recommended_type,
        'current_flow': flow_data
    })

if __name__ == '__main__':
    app.run(debug=True)