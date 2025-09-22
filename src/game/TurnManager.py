from src.game.Color import Color


class TurnManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TurnManager, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'current_turn'):
            self.current_turn = Color.WHITE

    def reset(self):
        self.current_turn = Color.WHITE

    def get_current_turn(self):
        return self.current_turn

    def get_next_turn_color(self):
        if self.current_turn == Color.WHITE:
            return Color.BLACK
        return Color.WHITE

    def next_turn(self):
        if self.current_turn == Color.WHITE:
            self.current_turn = Color.BLACK
        else:
            self.current_turn = Color.WHITE
