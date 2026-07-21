from app import app
from app.routes.ai import ai_router
from app.routes.file_upload import file_upload_router
from dependencies import initialize_middleware

# add middleware for handling cors requests and loading all properties
initialize_middleware(app)
#
# add the routers
app.include_router(ai_router)
#
app.include_router(file_upload_router)


#

@app.get("/")
@app.get("/Health-Check")
async def home_main():
    """
     Health Check endpoint.
    """
    return {"message": " Application Is Up And Running !!! "}
