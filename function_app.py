import azure.functions as func
import spotbot as sb
import cleanup
import logging

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

@app.function_name(name="tablecleanup")
@app.schedule(schedule="0 8 * * *",
              arg_name="tablecleanup",
              run_on_startup=False)
def table_cleanup(timer: func.TimerRequest) -> None:
    cleanup.cleanup()

@app.route(route="manualcleanup", methods=[func.HttpMethod.POST])
def manual_cleanup(req: func.HttpRequest) -> func.HttpResponse:
    cleanup.cleanup()