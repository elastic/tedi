import docker
import json
import logging
import os
import shutil
import yaml
from glob import glob
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path
from .paths import Paths
from .facts import Facts

logger = logging.getLogger('tedi.commands')
paths = Paths()


def die(message, exit_code=1):
    logger.error(message)
    raise SystemExit(exit_code)


def load_job_config(job):
    config_file = paths.template_path / job / 'tedi.yml'
    try:
        with config_file.open() as config:
            job_config = yaml.load(config)
    except FileNotFoundError:
        die('No config file "%s"' % config_file)
    if job_config is None:
        die('Empty YAML file "%s"' % config_file)
    if 'variants' not in job_config:
        die('Must specify a "variants" block in "%s"' % config_file)
    for variant, variant_config in job_config['variants'].items():
        if 'facts' not in variant_config or variant_config['facts'] is None:
            logger.warn('No facts specified for variant "%s" in "%s"' % (variant, config_file))
            variant_config['facts'] = {}
    return job_config


def render_template_file(src, dst, extra_facts={}):
    """Render a template from src Path to dst Path with Jinja2."""
    jinja_env = Environment(
        loader=FileSystemLoader('.'),
        undefined=StrictUndefined)
    template = jinja_env.get_template(str(src))
    facts = Facts().get_all()
    facts.update(extra_facts)
    with dst.open('w') as rendered_file:
        rendered_file.write(template.render(facts))


def render():
    """Render the templates to static files"""
    logger.info('Rendering...')
    jobs = [os.path.basename(j) for j in glob(str(paths.template_path / '*'))]
    task_matrix = []

    for job in jobs:
        job_config = load_job_config(job)
        variants = job_config['variants']

        logger.debug("Found %s variants for job %s: %s" % (len(variants), job, variants))
        for variant, config in variants.items():
            task = {
                'job': job,
                'variant': variant,
                'facts': config['facts']
            }
            task_matrix.append(task)

    for task in task_matrix:
        logger.debug('Running build task definition:')
        logger.debug(json.dumps(task, indent=4))
        for root, subdirs, files in os.walk(str(paths.template_path / task['job'])):
            new_dir = paths.make_render_path(Path(root), suffix=task['variant'])
            logger.debug("Creating render dir: %s" % new_dir)
            new_dir.mkdir(parents=True, exist_ok=True)

            for f in files:
                src = Path(root) / f
                dst = paths.make_render_path(Path(root) / f, suffix=task['variant'])
                logger.debug("Rendering: %s -> %s" % (src, dst))
                render_template_file(src, dst, extra_facts=task['facts'])


def clean():
    """Remove all rendered files"""
    if paths.render_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.render_path))
        shutil.rmtree(str(paths.render_path))


def build():
    """Build the images from the rendered files"""
    client = docker.from_env()
    jobs = glob(str(paths.render_path / '*'))
    for job in jobs:
        image = os.path.basename(job)
        logger.info('Building %s...' % image)
        client.images.build(
            path=str(job),
            tag=os.path.basename(image)
        )
