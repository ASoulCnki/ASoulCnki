from werkzeug.exceptions import HTTPException
import traceback

from app import create_app
from app.lib.error import APIException
from app.lib.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    print(e)
    traceback.print_stack()
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式
        # log
        if not app.debug:
            print(e)
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
