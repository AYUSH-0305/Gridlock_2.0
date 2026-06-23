import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import forecast_router, feedback_router


def _load_graph_background(osm_service):
    """Download / load the OSM graph without blocking server startup."""
    try:
        graph = osm_service.load_graph()
        if graph is not None:
            print(f"[OSM] Graph ready — {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        else:
            print("[OSM] WARNING: graph unavailable, /forecast will return 500")
    except Exception as e:
        print(f"[OSM] ERROR loading graph: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    from backend.app.api.forecast import osm_service, model
    print(f"[Startup] ML model loaded: {model.pipeline is not None}")
    print("[Startup] OSM graph loading in background — /forecast ready once graph is loaded ...")
    threading.Thread(target=_load_graph_background, args=(osm_service,), daemon=True).start()
    yield


app = FastAPI(
    title="Gridlock Event Congestion API",
    description="Forecast impact, recommend manpower and diversions, and log feedback for event congestion.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast_router, prefix="/api")
app.include_router(feedback_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Gridlock Event Congestion backend is running."}
