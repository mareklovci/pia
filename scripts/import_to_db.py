from app import db, create_app
from app.models import Post, User
import json


def main():
    app = create_app()

    with app.app_context():
        input_file = open('../data/posts.json', encoding='utf-8')
        json_array = json.load(input_file)

        for item in json_array:
            user = User.query.get(item['user_id'])
            post = Post(title=item['title'],
                        content=item['content'],
                        post_author=user)
            db.session.add(post)
        db.session.commit()


if __name__ == '__main__':
    main()
