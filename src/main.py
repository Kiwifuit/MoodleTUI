from logging import Logger
from mtui import (
    loadConfig,
    decodePassword,
    encodePassword,
    getMultiFernet,
    login,
    logout,
    parseCourse,
    buildLogger,
    CredentialsDatabase,
    LogLevel,
)

from requests import Session
from bs4 import BeautifulSoup

from rich.progress import Progress
from rich.console import Console


CONFIG = loadConfig("res/config/config.ini")
PASSWORD_KEY = getMultiFernet(CONFIG, CONFIG.Auth.keys)
CREDENTIAL_DB = CredentialsDatabase(CONFIG.Path.credidentials)


def putCredentials(user: str, passwd: str):
    """
    Pushes credentials to the database

    Parameters
    ----------
    user : str
        Username
    passwd : str
        Password to associate with the username
    """
    passwd = encodePassword(PASSWORD_KEY, passwd)
    CREDENTIAL_DB.put(user, passwd)


def getCredentials(
    user: str = None,
) -> list[tuple[int, str, str]] | tuple[str, str, None]:
    """
    A function that retrieves credentials from the database

    Parameters
    ----------
    user : str, optional
        Grab the username and password of `user`, by default None

    Returns
    -------
    A list of tuples containing an `int` and two `str`s OR a tuple containing two `str`s and `None`
        Returns a list of tuples containing the following when `user` is falsy:

            - `int`: Index Number
            - `str`: Username
            - `str`: Password

        In the event that `user` is truthy, it returns a tuple with the username and
        password only
    """
    if not user:
        return list(
            map(
                lambda e: (e[0], e[1][0], e[1][1]),
                enumerate(
                    map(
                        lambda i: (i[0], decodePassword(PASSWORD_KEY, i[1])),
                        CREDENTIAL_DB.getAll(),
                    )
                ),
            )
        )

    u, p = CREDENTIAL_DB.get(user)
    return u, decodePassword(PASSWORD_KEY, p), None


def isDatabaseEmpty() -> bool:
    return not bool(tuple(CREDENTIAL_DB.getAll()))


def getStatusColor(stat: int) -> str:
    if 100 <= stat <= 199:
        return "blue"
    elif 200 <= stat <= 299:
        return "green"
    elif 300 <= stat <= 399:
        return "magenta"
    elif 400 <= stat <= 499:
        return "yellow"
    elif 500 <= stat <= 599:
        return "red"


def printDiagnostics(logger: Logger, data: dict):
    for function in data:
        functionData = data.get(function)
        code = functionData.get("responseCode")
        elapsed = round(functionData.get("elapsed").total_seconds(), 2)

        logger.info(f"{function!r} took {elapsed} seconds ({' '.join(map(str, code))!r})")


def selectUser(console: Console) -> tuple[str, str]:
    while True:
        if user := console.input(":person: Enter Username: ", emoji=True):
            return getCredentials(user)

        console.print("[bold]Registered Users[/bold]")
        for user in CREDENTIAL_DB.getUsers():
            console.print(f"\t- [underline cyan]{user}[/underline cyan]")


def getUserAndPassword(console: Console, logger: Logger) -> tuple[str, str]:
    username = console.input(":person: Enter Username: ", emoji=True)

    if username in CREDENTIAL_DB:
        password1 = console.input(f":lock: Enter Password for {username}: ")
        _, password2 = CREDENTIAL_DB.get(username)
    else:
        password1 = console.input(":lock: Enter Password: ", password=True, emoji=True)
        password2 = console.input(":lock: Confirm Password: ", password=True, emoji=True)

    if password1 == password2 and username not in CREDENTIAL_DB:
        putCredentials(username, password1)
        logger.info(f"Registered {username!r} to database!")
    else:
        logger.info("Logged in!")

    return username, password1


def main(console: Console, session: Session, logger: Logger):
    ...


def init():
    console = Console(record=True)
    session = Session()
    logger = buildLogger("info", console)
    user, passwd = getUserAndPassword(console, logger)

    session.headers = {"User-Agent": "Mozilla/5.0"}

    loginRes = login(session, user, passwd, CONFIG)
    printDiagnostics(logger, loginRes)
    logger.info(f"Logged in as {user!r}")

    try:
        main(console=console, session=session, logger=logger)
    finally:
        logoutRes = logout(session, CONFIG)

    printDiagnostics(logger, logoutRes)


if __name__ == "__main__":
    init()
    print(list(CREDENTIAL_DB.getAll()))
