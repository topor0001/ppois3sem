class AccessControl:
    def __init__(self, control_id, user_role, resource_type, permissions, conditions):
        self.control_id = control_id
        self.user_role = user_role
        self.resource_type = resource_type
        self.permissions = permissions
        self.conditions = conditions
        self.assigned_users = []

    def check_permission(self, user_account, resource, action):
        if user_account.role != self.user_role:
            return False
        return action in self.permissions

    def assign_to_user(self, user_account):
        if user_account not in self.assigned_users:
            self.assigned_users.append(user_account)
            return True
        return False