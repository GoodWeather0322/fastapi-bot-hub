export $(grep -v '^#' .env | xargs)

if [ "$FASTAPI_RELOAD" = "true" ]; then
    RELOAD_OPTION="--reload"
else
    RELOAD_OPTION=""
fi

uvicorn app.main:app --host $FASTAPI_HOST --port $FASTAPI_PORT $RELOAD_OPTION