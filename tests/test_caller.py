from helpers.caller import SpecifySession


def test_login():
    session = SpecifySession(
        username="sp7demofish",  # Public demo credentials, fine to have here
        password="sp7demofish",  # Public demo credentials, fine to have here
        instance_url="https://sp7demofish.specifycloud.org",
        collectionid="4",
    )
    session.login()
