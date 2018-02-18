import flask_assistant as assist
from rocky import app, db

google = assist.Assistant(app, route='/assistants/google')

@google.action('nearest-cast')
def nearest_cast(location):
    """
    """
    print(location)
    # db.session.query(Cls).order_by(Cls.geom.distance_box('POINT(0 0)')).limit(10)
    return assist.tell('Testing')