import nox

@nox.session(python='3.10')
def run(session):
    session.run('pip', 'install', '-r', 'requirements.txt', external=True)
    session.run('flask', 'run', '--host=localhost', '--port=8080', external=True)

@nox.session(python=['3.10'])
def tests(session):
    session.run('pip', 'install', '-r', 'requirements.txt')
    session.run('pytest')
