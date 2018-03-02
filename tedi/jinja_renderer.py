from jinja2 import Environment, FileSystemLoader, StrictUndefined


class JinjaRenderer():
    def __init__(self, facts):
        self.facts = facts

    def render(self, template_file) -> str:
        """Render a template file with Jinja2. Return the result."""
        jinja_env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined)
        template = jinja_env.get_template(str(template_file))
        return template.render(self.facts.to_dict())
