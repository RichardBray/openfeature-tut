from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openfeature import api
from openfeature.contrib.provider.flagd import FlagdProvider
from openfeature.contrib.hook.opentelemetry import TracingHook

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

def setup_telemetry():
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces",
    )

    trace_provider = TracerProvider()
    processor = BatchSpanProcessor(otlp_exporter)
    trace_provider.add_span_processor(processor)
    trace.set_tracer_provider(trace_provider)

setup_telemetry()
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.set_provider(FlagdProvider())

client = api.get_client()
client.add_hooks([TracingHook()])

@app.get("/api/buy-now")
def root():
    show_new_item = client.get_boolean_value("new-item", True)

    if not show_new_item:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Feature not available"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Payment successful"}
    )
