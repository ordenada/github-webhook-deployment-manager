from .log import logger
from .bot_client import send_report

def push_controller(data: dict):
    logger.info('receive a "push" event')

    sender_name: str = data['sender']['login']
    sender_avatar: str = data['sender']['avatar_url']
    commits: list[str] = [commit['message'] for commit in data['commits']]

    added_list: list[str] = data['head_commit']['added']
    removed_list: list[str] = data['head_commit']['removed']
    modified_list: list[str] = data['head_commit']['modified']

    report = '\n'.join(
        [f'📌 New Push by {sender_name}', '', 'Commits:']
        + [f'📌 {commit}' for commit in commits]
        + ['']
        + [f'🍏 {line}' for line in added_list]
        + [f'🍎 {line}' for line in removed_list]
        + [f'🍊 {line}' for line in modified_list]
    )

    send_report(report)
