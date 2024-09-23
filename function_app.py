import azure.functions as func
import spotbot as sb

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="spotbot", methods=[func.HttpMethod.POST])
def spotbot(req: func.HttpRequest) -> func.HttpResponse:
    sb.run(req)
    return func.HttpResponse(status_code=202)