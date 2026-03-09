import a2dl

GITHUB_LATEST = 'https://api.github.com/repos/{owner}/{repo}/releases/latest'


def get_github_latest_release(owner: str, repo: str | None = None):
    if repo is None:
        repo = owner
    data = a2dl.read_json(GITHUB_LATEST.format(owner=owner, repo=repo))
    return data
