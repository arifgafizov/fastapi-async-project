from fastapi import FastAPI

from api import users, sections, courses
from db.setup import engine, Base
from db.models import users as db_users
from db.models import courses as db_courses
from db.models import sections as db_sections

# db_users.Base.metadata.create_all(bind=engine)
# db_courses.Base.metadata.create_all(bind=engine)
# db_sections.Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        'name': 'users',
        'description': 'users api',
    },
    {
        'name': 'courses',
        'description': 'courses api',
    },
    {
        'name': 'sections',
        'description': 'sections api',
    }
]

app = FastAPI(
    title='Fast API LMS',
    description='LMS for managing students and courses.',
    version='0.0.1',
    license_info={'name': 'MIT'},
    openapi_tags=tags_metadata,
)


app.include_router(users.router)
app.include_router(sections.router)
app.include_router(courses.router)
