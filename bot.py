import requests

HOST = '127.0.0.1:8000'
USERS = [
    {
        'email': 'steve@mail.com',
        'first_name': 'Steve',
        'last_name': 'Smith',
        'password1': 'testing12345',
        'password2': 'testing12345'
    },
    {
        'email': 'johnn@mail.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'testing12345',
        'password2': 'testing12345'
    },
    {
        'email': 'sue@mail.com',
        'first_name': 'Sue',
        'last_name': 'Johnson',
        'password1': 'testing12345',
        'password2': 'testing12345'
    }
]


class ServerBot:
    def __init__(self, host):
        self.base_url = f"http://{host}/"
        self.posts = []
        self.likes = []

    def register_user(self, user: dict):
        url = self.base_url + 'api/register/'
        res = requests.post(url, json=user)

        if res.status_code == 201:
            access_token = res.json()['token']['access']
            return access_token

    def _login_user(self, email, password):
        url = self.base_url + 'api/token/'
        res = requests.post(url, json={'email': email,
                                       'password': password})
        if res.status_code == 200:
            headers = {'Authorization': f"Bearer {res.json()['access']}"}
            return headers

    def get_headers(self, user):
        return self._login_user(user['email'], user['password1'])

    def post_new_post(self, content, user):
        url = self.base_url + 'api/posts/'
        headers = self.get_headers(user)

        res = requests.post(url,
                            headers=headers,
                            json={'content': content})

        if res.status_code == 201:
            self.posts.append(res.json()['pk'])
            return res.json()

    def delete_post(self, pk, user):
        url = self.base_url + 'api/posts/' + str(pk) + '/'
        headers = self.get_headers(user)
        res = requests.delete(url, headers=headers)

        if res.status_code == 204:
            return True

    def like_post(self, pk, user):
        headers = self.get_headers(user)
        url = self.base_url + 'api/posts/' + str(pk) + '/likes/'
        res = requests.post(url, headers=headers)

        if res.status_code == 201:
            self.likes.append(res.json()['author'])
            return res.json()

    def unlike_post(self, pk, user):
        headers = self.get_headers(user)
        url = self.base_url + 'api/posts/' + str(pk) + '/likes/'
        res = requests.delete(url, headers=headers)

        if res.status_code == 204:
            return True

    def likes_analytics(self, user):
        url = self.base_url + 'api/posts/analytics/'
        headers = self.get_headers(user)
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            return res.json()

    def user_activity(self, user, pk):
        url = self.base_url + 'api/users/' + str(pk) + '/activity/'
        headers = self.get_headers(user)
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            return res.json()


class CreateData:
    def __init__(self, bot: ServerBot):
        self.bot = bot

    def create_users(self):
        for user in USERS:
            self.bot.register_user(user)

    def create_posts(self):
        for user in USERS:
            content = f"Post by {user['first_name']} {user['last_name']}"
            self.bot.post_new_post(content=content, user=user)

    def create_likes(self):
        for user in USERS:
            for post in self.bot.posts:
                bot.like_post(post, user)


if __name__ == '__main__':
    bot = ServerBot(HOST)
    data_manager = CreateData(bot)
    data_manager.create_users()
    data_manager.create_posts()
    data_manager.create_likes()
