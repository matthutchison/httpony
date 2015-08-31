from httpie.cli import parser
from httpie.context import Environment
from httpie.output import streams
from requests.models import Request
from werkzeug.wrappers import Response
from werkzeug.wrappers import Request as WerkzeugRequest

from httpony import __version__


def make_app():
    """Make a WSGI app that has all the HTTPie pieces baked in."""
    env = Environment()
    args = parser.parse_args(args=['/'], env=env)
    args.output_options = 'HB'  # Output only requests.
    server = 'HTTPony/{0}'.format(__version__)

    def application(environ, start_response):
        wrequest = WerkzeugRequest(environ)
        request = Request(
            method=wrequest.method,
            url=wrequest.url,
            headers=wrequest.headers,
        )
        prepared = request.prepare()

        stream = streams.build_output_stream(args, env, prepared, response=None)
        streams.write(stream, env.stdout, env.stdout_isatty)

        # Make dreams come true.
        response = Response(headers={'Server': server})
        return response(environ, start_response)

    return application
