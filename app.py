# pragma: no cover
from init import app  # pragma: no cover
import routes  # noqa: F401 # pragma: no cover
if __name__ == '__main__':  # pragma: no cover
    app.run(host="127.0.0.1", port=8080, debug=True)  # pragma: no cover
