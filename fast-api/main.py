import logging
from .app.apis import sample_api
from ddtrace import config as ddtrace_config
from ddtrace.contrib.asgi import TraceMiddleware
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from util.config import config
from util.custom_exceptions import AuthException, CustomException, DatabaseException, \
    auth_exception_handler, custom_exception_handler, database_exception_handler
from util.database import build_postgres_url
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware


# CONFIGURE LOGGER
logging.basicConfig(
    level=logging.DEBUG, # logs all levels starting from DEBUG (Lowest level)
    handlers=[logging.StreamHandler] # logs to console
)

logger = logging.getLogger(__name__)
logger.info(f'Starting {config.APPLICATION_NAME} version {config.datadog.DD_VERSION}')

app = FastAPI(
    title=config.APPLICATION_NAME,
    description="Fast API Microservice Boilerplate", #TODO: Replace placeholder
    openapi_url="/openapi.json",
    docs_url="/",
    redoc_url="/redoc",
    swagger_ui_parameters={"defaultModelsExpandDepth": 0}  #schemas will be closed initially
)

# CONFIGURE DATADOG TELEMATICS

# HANDLES LISTED EXCEPTIONS USING THE PROVIDED HANDLERS
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(AuthException, auth_exception_handler)

# CONNECT TO THE PG DATABASE
logger.info("Connecting to postgres database")
engine = create_engine(build_postgres_url())

# ADD MIDDLEWARE
allow_origins = [
    "http://localhost:4000" #TODO: Replace placeholder
]

if config.ENVIRONMENT != 'TEST':
    app.add_middleware(TraceMiddleware, integration_config=ddtrace_config.asgi) #for Datadog application performance monitoring (APM)

app.add_middleware(ProxyHeadersMiddleware)  #for handling proxied requests
app.add_middleware(
    CORSMiddleware, #for handling requests from different domains
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_credentials=True,
)

# SET DATABASE CONNECT ON REQUEST AND CLOSE AFTER
@app.middleware('http')
async def db_connect(req: Request, call_next):
    req.state.conn = engine.connect()
    try:
        response = await call_next(req)
    finally:
        req.state.conn.close()
    return response

# CONFIGURE ROUTES
app.include_router(sample_api.router, tags=['Sample Endpoint'])
