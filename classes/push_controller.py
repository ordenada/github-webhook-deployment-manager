from .log import logger
from .bot_client import send_report

def push_controller(data: dict):
    logger.info('receive a "push" event')

    sender_name: str = data['sender']['login']
    sender_avatar: str = data['sender']['avatar_url']
    commits: list[str] = [commit['message'] for commit in data['commits']]
    repository = data['repository']['full_name']

    added_list: list[str] = data['head_commit']['added']
    removed_list: list[str] = data['head_commit']['removed']
    modified_list: list[str] = data['head_commit']['modified']

    report_list = [
        f'📌 New Push by {sender_name}: {repository}',
        '',
        'Commits:',
    ]
    report_list.extend([f'📌 {commit}' for commit in commits])
    report_list.extend(+ [''])
    report_list.extend([f'🍏 {line}' for line in added_list])
    report_list.extend([f'🍎 {line}' for line in removed_list])
    report_list.extend([f'🍊 {line}' for line in modified_list])

    report = '\n'.join(report_list)

    send_report(report)
