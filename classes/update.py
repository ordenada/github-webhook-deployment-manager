import os
import pathlib
import subprocess

from .log import logger
from .bot_client import send_report, edit_report_message, delete_report_message


def update_repository(repository: str):
    GIT_BRANCH = os.environ['GIT_BRANCH']
    PM2_NAME = os.environ['PM2_NAME']

    home = pathlib.Path.home()
    workdir = home.joinpath('repositories')

    if not workdir.exists():
        logger.error('Folder "%s" does not exist', workdir)
        return
    
    current_folder = workdir.joinpath(repository)
    if not current_folder.exists():
        logger.error('Current folder "%s" does not exist', current_folder)
        return

    os.chdir(current_folder)
    logger.debug('cwd is %s', os.getcwd())

    message_id = send_report('🔄 _Updating..._', markdown=True)

    # remove non-committed changes
    logger.debug('git checkout -- .')
    git_checkout_result = subprocess.run(
        args=['git', 'checkout', '--', '.'],
        capture_output=True,
        text=True,
    )
    if git_checkout_result.stdout:
        logger.debug('git checkout results:', git_checkout_result.stdout)
    if git_checkout_result.returncode != 0 and git_checkout_result.stderr:
        logger.error('Error to git checkout: %s', repository)
        logger.error('Error of git checkout: %s', git_checkout_result.stderr)
        send_report(
            f'⚠️ Cannot git checkout {repository}: {git_checkout_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    # fetch the repository
    logger.debug('git fetch origin')
    git_fetch_result = subprocess.run(
        args=['git', 'fetch', 'origin'],
        capture_output=True,
        text=True,
    )
    if git_fetch_result.stdout:
        logger.debug('git fetch results: %s', git_fetch_result.stdout)
    if git_fetch_result.returncode != 0 and git_fetch_result.stderr:
        logger.error('Error to git fetch: %s', repository)
        logger.error('Error of git fetch: %s', git_fetch_result.stderr)
        send_report(
            f'⚠️ Cannot git fetch {repository}: {git_fetch_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    # pull the repository
    logger.debug('git pull origin %s', GIT_BRANCH)
    git_pull_result = subprocess.run(
        args=['git', 'pull', 'origin', GIT_BRANCH],
        capture_output=True,
        text=True,
    )
    if git_pull_result.stdout:
        logger.debug('git pull results: %s', git_pull_result.stdout)
    if git_pull_result.returncode != 0 and git_pull_result.stderr:
        logger.error('Error to git pull: %s', repository)
        logger.error('Error of git pull: %s', git_pull_result.stderr)
        send_report(
            f'⚠️ Cannot git pull {repository}: {git_pull_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    message_id = edit_report_message(
        message_id=message_id,
        report='📦 _Installing..._',
        markdown=True,
    )
    # install the repository
    logger.debug('bun install')
    install_result = subprocess.run(
        args=['bun', 'install'],
        capture_output=True,
    )
    if install_result.stdout:
        logger.debug('install results: %s', install_result.stdout)
    if install_result.returncode != 0 and install_result.stderr:
        logger.error('Error to install: %s', repository)
        logger.error('Error of install: %s', install_result.stderr)
        send_report(
            f'⚠️ Cannot install {repository}: {install_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    message_id = edit_report_message(
        message_id=message_id,
        report='💼 _Migrating..._',
        markdown=True,
    )

    # migrate the database
    logger.debug('bunx prisma db push')
    migrating_result = subprocess.run(
        args=['bunx', 'prisma', 'db', 'push'],
        capture_output=True,
        text=True,
    )
    if migrating_result.stdout:
        logger.debug('migrating results: %s', migrating_result.stdout)
    if migrating_result.returncode != 0 and migrating_result.stderr:
        logger.error('Error to migrate: %s', repository)
        logger.error('Error of migrate: %s', migrating_result.stderr)
        send_report(
            f'⚠️ Cannot migrate {repository}: {migrating_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    message_id = edit_report_message(
        message_id=message_id,
        report='🛠 _Building..._',
        markdown=True,
    )

    # build the repository
    logger.debug('bun run build')
    build_result = subprocess.run(
        args=['bun', 'run', 'build'],
        capture_output=True,
    )
    if build_result.stdout:
        logger.debug('build results: %s', build_result.stdout)
    if build_result.returncode != 0 and build_result.stderr:
        logger.error('Error to build: %s', repository)
        logger.error('Error of build: %s', build_result.stderr)
        send_report(
            f'⚠️ Cannot build {repository}: {build_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    message_id = edit_report_message(
        message_id=message_id,
        report='⏫ _Restart..._',
        markdown=True,
    )

    # restart the repository
    logger.debug('pm2 restart %s', PM2_NAME)
    restart_result = subprocess.run(
        args=['pm2', 'restart', PM2_NAME],
        capture_output=True,
        text=True,
    )
    if restart_result.stdout:
        logger.debug('restart results: %s', restart_result.stdout)
    if restart_result.returncode != 0 and restart_result.stderr:
        logger.error('Error to restart: %s', repository)
        logger.error('Error of restart: %s', restart_result.stderr)
        send_report(
            f'⚠️ Cannot restart {repository}: {restart_result.stderr}',
            alert=True,
        )
        delete_report_message(message_id)
        return

    # All right
    delete_report_message(message_id)
    send_report(
        f'✅ App updated {repository}',
        alert=True,
    )
    logger.info('App updated')
