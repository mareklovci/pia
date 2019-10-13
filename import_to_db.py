from accounting import db
from accounting.models import Post, User
import json


def main():
    input_file = open('data/posts.json', encoding='utf-8')
    json_array = json.load(input_file)

    for item in json_array:
        user = User.query.get(item['user_id'])
        post = Post(title=item['title'],
                    content=item['content'],
                    author=user)
        db.session.add(post)
    db.session.commit()


if __name__ == '__main__':
    main()
