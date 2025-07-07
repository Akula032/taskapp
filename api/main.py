from fastapi import FastAPI
from modules.tasks import api as task_api
from modules.status import api as status_api
from modules.login import api as login_router
from modules.attendance import api as attendance_router
from fastapi.middleware.cors import CORSMiddleware
from modules.category import api as category_api
from modules.staff import api as staff_api
from modules.priority import api as priority_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(staff_api.router, prefix="/api", tags=["Staffs"])

app.include_router(priority_api.router, prefix="/api/priorities", tags=["Priority"])


app.include_router(task_api.router, tags=["Task"])
app.include_router(status_api.router)
app.include_router(login_router.router, prefix="/api")
app.include_router(attendance_router.router)
app.include_router(category_api.router)
# "http://15.168.156.20",
# "https://tsugawa.otani-shokai.org",
# "https://www.tsugawa.otani-shokai.org",
# "http://api.tsugawa.otani-shokai.org",
