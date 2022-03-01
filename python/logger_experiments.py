from . import settings
from engora import CONFIG, ROOT, set_config_from_str, file, log, stats, thread
from pathlib import Path
from typing import Optional, Sequence
import os
import logging
import sys
import time
import xmod

SCRIPTS = ROOT / 'scripts'
CHANGE_GROUP_AND_PERMS = SCRIPTS / 'change-group-and-perms'


def get_rerun(rerun, work_dir):
    if rerun is None:
        return work_dir.exists()

    if not rerun and work_dir.exists() :
        raise ValueError(f'{work_dir = } exists')

    if rerun and not work_dir.exists():
        raise ValueError(f'{work_dir = } does not exist')

    return rerun


def update_settings(concurrency, batch_item_count):
    if concurrency:
        settings.AUTOTHROTTLE_TARGET_CONCURRENCY = concurrency
        settings.CONCURRENT_REQUESTS = concurrency
        settings.CONCURRENT_REQUESTS_PER_DOMAIN = concurrency
        settings.CONCURRENT_REQUESTS_PER_IP = concurrency

    settings.FEED_EXPORT_BATCH_ITEM_COUNT = batch_item_count


def get_initial_batch_id(name, work_dir):
    from engora.file.jl.find_journals import is_journal

    # Look for existing files
    files = work_dir.iterdir() if work_dir.exists() else []
    files = [f for f in files if is_journal(f, json_ok=False)]
    files = [f for f in files if f.stem.startswith(f'{name}-')]
    indexes = [int(f.stem.split('-')[-1]) for f in files]
    return 1 + max(indexes + [-1])


def command(
    name, batch_item_count, product_only, use_csv, work_dir, limited, JOBDIR
):
    initial_batch_id = get_initial_batch_id(name, work_dir)

    fmt = 'csv' if use_csv else 'jl'
    product_only = product_only or use_csv
    output_pattern = f'{work_dir}/{name}-%(batch_id)04d.{fmt}'

    return [
        'scrapy', 'crawl', name,
        '-o', output_pattern,
        '-a', f'{initial_batch_id=}',
        '-a', f'{limited=}',
        '-a', f'{product_only=}',
        '-a', f'{use_csv=}',
        '-a', f'{work_dir=!s}',
        '-s', f'{JOBDIR=!s}',
    ]


def assign(assignments):
    from scrapy.settings import default_settings

    for a in assignments:
        k, *v = a.split('=', maxsplit=1)
        if not (k and v):
            raise ValueError(f'Do not understand assignment {a}')

        if k.isupper():
            if not hasattr(default_settings, k):
                raise ValueError(f'Unknown scrapy setting {k}')

            yield from ('-s', a)

        elif k.islower():
            set_config_from_str(k, v[0])

        else:
            raise ValueError(f'Do not understand assignment {a}')


def log_specs(name, target, rerun, args, work_dir, limited, assignments):
    specs = {
        'name': name,
        'limited': limited,
        'target': target,
        'rerun': rerun,
        'work_dir': work_dir,
        'assignments': list(assignments),
        **stats.from_system()
    }

    log(file.dumps(specs, default=str))
    if CONFIG.dry_run:
        log('$', *args)


def fix_latest_symlink(work_dir):
    latest = work_dir.parent / 'latest'

    if latest.is_symlink():
        latest.unlink()

    if not latest.exists():
        latest.symlink_to(work_dir)


def edit_stats(stats_file):
    import editor

    def target():
        time.sleep(3)
        editor(filename=stats_file)

    thread(target=target, daemon=True).start()


def run_scrapy(args):
    from unittest.mock import patch

    with patch('sys.exit') as exit:
        from scrapy import cmdline
        try:
            cmdline.execute(args)
        finally:
            cmdline.garbage_collect()

    if error_code := exit.call_args_list and exit.call_args_list[0].args[0]:
        log.error('We got error code', error_code)
        time.sleep(1)
        sys.exit(*exit.call_args_list[0])


@xmod
def runner(
    name: str,
    assignments: Sequence[str] = None,
    batch_item_count: int = None,
    concurrency: int = 0,
    edit: bool = False,
    limited: bool = False,
    product_only: bool = False,
    rerun: Optional[bool] = None,
    target: Optional[str] = None,
    use_csv: bool = False,
):
    # Not 100% clear this is needed, but why not?
    os.chdir(ROOT)

    from engora.file import force_writable
    root = Path(CONFIG.root) / 'crawl' / name

    if CONFIG.production:
        class Stream:
            write = staticmethod(log)

        class Handler(logging.Handler):
            def emit(self, record):
                args = record.args
                if not args:
                    msg = record.msg
                elif isinstance(args, dict):
                    msg = record.msg.format(**args)
                else:
                    msg = record.msg.format(*args)

                logger = _LOGGERS.get(record.levelname, _LOGGERS['INFO'])
                logger(msg)

        # logging.basicConfig(stream=Stream())
        logging.basicConfig(handlers=[Handler()])

        if not CONFIG.verbose:
            logging.disable(logging.DEBUG)
        log.configure('production', f'crawl/{name}')

    if target:
        work_dir = root / target
        rerun = get_rerun(rerun, work_dir)
        force_writable.mkdir_writable(work_dir, use_logging=False)

    else:
        work_dir = force_writable.mkdir_timestamp(root, use_logging=False)
        if rerun:
            log.exit('--rerun is set but no target is given')

    if CONFIG.production:
        log.configure('production', work_dir)

    if batch_item_count is None:
        batch_item_count = settings.FEED_EXPORT_BATCH_ITEM_COUNT

    JOBDIR = work_dir / 'job'
    JOBDIR.mkdir(exist_ok=True)
    update_settings(concurrency, batch_item_count)

    args = command(
        name,
        batch_item_count,
        product_only,
        use_csv,
        work_dir,
        limited,
        JOBDIR,
    )

    args.extend(assign(assignments))

    log_specs(name, target, rerun, args, work_dir, limited, assignments)

    if not CONFIG.dry_run:
        fix_latest_symlink(work_dir)
        stats_file = stats.save_file(name, work_dir)
        if edit:
            edit_stats(stats_file)
        run_scrapy(args)


_LOGGERS = {
    'INFO': log._info3,
    'WARN': log._error3,
    'ERROR': log._error3,
    'DEBUG': log._debug3,
}
