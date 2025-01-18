from ..log import logger
from ..bot_client import send_report
from ..update import update_repository

def push_controller(data: dict):
    logger.info('receive a "push" event')

    ref = data['ref']
    sender_name: str = data['sender']['login']
    sender_avatar: str = data['sender']['avatar_url']
    commits: list[str] = [commit['message'] for commit in data['commits']]
    repository = data['repository']['name']
    repository_full_name = data['repository']['full_name']

    added_list: list[str] = data['head_commit']['added']
    removed_list: list[str] = data['head_commit']['removed']
    modified_list: list[str] = data['head_commit']['modified']

    report_list = [
        f'📌 New Push by {sender_name}: {repository_full_name}',
        '',
        'Commits:',
    ]
    report_list.extend([f'📌 {commit}' for commit in commits])
    report_list.extend([''])
    report_list.extend([f'🍏 {line}' for line in added_list])
    report_list.extend([f'🍎 {line}' for line in removed_list])
    report_list.extend([f'🍊 {line}' for line in modified_list])

    should_update = False

    if ref == 'refs/heads/master' or ref == 'refs/heads/main':
        alert = True
        should_update = True
    else:
        alert = False

    report_list.extend(['', f'ref: {ref}'])

    report = '\n'.join(report_list)

    try:
        send_report(report, markdown=True, alert=alert)
    except:
        logger.warning('Cannot send the report with Markdown')
        try:
            send_report(report, alert=alert)
        except Exception as err:
            logger.error('Cannot send the report without Markdown')
            logger.error(err)

    # Update
    if should_update:
        logger.debug('updating... %s', repository)
        try:
            update_repository(repository=repository)
        except Exception as err:
            logger.error('Cannot update the repository: %s', repository)
            logger.error(err)
