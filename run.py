from app import create_app
from app.config import DevelopmentConfig

import sqlalchemy as sa
from sqlalchemy import orm as so

from app.posts.models import Post

app = create_app(DevelopmentConfig)

@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so, "Post": Post}

if __name__ == "__main__":
    app.run(debug=True)
