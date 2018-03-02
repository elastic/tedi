import shutil
from pathlib import Path
from .fileset import Fileset
from .jinja_renderer import JinjaRenderer


class Builder():
    def __init__(self, source_dir, target_dir, facts):
        self.files = Fileset(source_dir)
        self.target_dir = Path(target_dir)
        self.renderer = JinjaRenderer(facts)

    def __repr__(self):
        return "Builder(source_dir='%s', target_dir='%s', facts=%s)" % \
            (self.files.top_dir, self.target_dir, self.renderer.facts)

    def render(self):
        if self.target_dir.exists():
            shutil.rmtree(str(self.target_dir))
        self.target_dir.mkdir(parents=True)

        for source in self.files:
            target = self.target_dir / source.relative_to(self.files.top_dir)
            if source.is_dir():
                target.mkdir()
            elif source.suffix == '.j2':
                target = Path(target.with_suffix(''))  # Remove '.j2'
                with target.open('w') as f:
                    f.write(self.renderer.render(source))
            else:
                shutil.copy2(str(source), str(target))
