from jinja2 import Environment, FileSystemLoader, StrictUndefined


class JinjaRenderer():
    def __init__(self, facts):
        self.facts = facts

    def render(self, template_file) -> str:
        """Render a template file with Jinja2. Return the result."""
        return self.render_string(open(template_file).read())

    def render_string(self, template_string: str) -> str:
        """Render a template_string with Jinja2. Return the result."""
        jinja_env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined)
        template = jinja_env.from_string(template_string)
        return template.render(self.facts.to_dict())
