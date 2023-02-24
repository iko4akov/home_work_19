from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_username(self, user_name):
        return self.session.query(User).filter(User.username == user_name).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_a):
        user = self.get_one(user_a.get("id"))
        user.username = user_a.get("username")
        user.password = user_a.get("password")
        user.role = user_a.get("role")

        self.session.add(user)
        self.session.commit()
