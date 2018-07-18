import sys
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2.exceptions import UndefinedError
from .logging import getLogger

logger = getLogger(__name__)


class JinjaRenderer():
    def __init__(self, facts):
        self.facts = facts

    def render(self, template_file) -> str:
        """Render a template file with Jinja2. Return the result."""
        return self.render_string(open(template_file).read())

    def render_string(self, template_string: str) -> str:
        """Render a template string with Jinja2. Return the result."""
        jinja_env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined)
        template = jinja_env.from_string(template_string)
        try:
            rendered = template.render(self.facts.to_dict())
        except UndefinedError as e:
            logger.critical('Template rendering failed.')
            logger.critical(f'The Jinja2 template engine said: "{e.message}".')
            logger.critical('Do you need to declare this as a fact in tedi.yml?')
            sys.exit(1)
        return rendered
