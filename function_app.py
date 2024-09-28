import logging
import azure.functions as func
import spotbot as sb
import cleanup

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="spotbot", methods=[func.HttpMethod.POST])
def spotbot(req: func.HttpRequest) -> func.HttpResponse:
    try:
        sb.run(req)
    except Exception as _excpt:
        logging.error(f"Exception occurred: {_excpt}")
        return func.HttpResponse(body=f"Exception occurred: {_excpt}", status_code=500)
    else:
        return func.HttpResponse(status_code=202)

@app.route(route="manual_cleanup", methods=[func.HttpMethod.POST])
def manual_cleanup(req: func.HttpRequest) -> func.HttpResponse:
    cleanup.cleanup()
    return func.HttpResponse(status_code=202)

@app.schedule(schedule="0 0 * * *",
              arg_name="timer_cleanup",
              run_on_startup=False)
def timer_cleanup(timer: func.TimerRequest) -> None:
    cleanup.cleanup()