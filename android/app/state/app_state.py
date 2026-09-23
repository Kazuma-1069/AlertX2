class AppState:
    def __init__(self):
        self.auth_token = None
        self.user_id = None
        self.user_name = "User"
        self.is_authenticated = False
        self.contacts = []

app_state = AppState()
