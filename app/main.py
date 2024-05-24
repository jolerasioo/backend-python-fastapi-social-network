from fastapi import FastAPI, status

from . import models
from .database import engine
from .routers import post, user, auth, vote


#def main():
#    '''main function to run the app'''
#    # create the database tables
#    models.Base.metadata.create_all(bind=engine)
#
#    # create the FastAPI app with swagger ui parameters
#    app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
#
#    # include the routers
#    app.include_router(post.router)
#    app.include_router(user.router)
#    app.include_router(auth.router)
#
#    # root route    
#    @app.get("/", status_code=status.HTTP_200_OK)
#    def root() -> dict:
#        '''return the root route'''
#        return {"message": "Welcome to the FastAPI app"}
#
#    return app






# create the database tables
models.Base.metadata.create_all(bind=engine)

# create the FastAPI app with swagger ui parameters
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

# include the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# root route    
@app.get("/", status_code=status.HTTP_200_OK)
def root() -> dict:
    '''return the root route'''
    return {"message": "Welcome to the FastAPI app"}

# run the app
#if __name__ == "__main__":
#    app = main()
#    import uvicorn
#    uvicorn.run(app, host="localhost", port=8000)








