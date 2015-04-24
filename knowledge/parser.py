def parse(dialogue):
  '''Converts a "dialogue" (string of "Speaker: Statement" lines) into a sequence of (speaker, parts).

  Each "part" is a triple of the form: (whose knowledge, yes or no, at what time).
  For the Cheryl's birthday problem, it converts the dialogue into the equivalent of:
    (Albert, [Albert does not know at time 0, Bernard does not know at time 0])
    (Bernard, [Bernard does not know at time 0, Bernard knows at time 1])
    (Albert, [Albert knows at time 2])
  '''
  statements = [line.strip() for line in dialogue.strip().split('\n')]
  all_contents = []
  for i in range(len(statements)):
    speaker, full_statement = [part.strip() for part in statements[i].split(':', 1)]
    statement_parts = parts(full_statement)
    contents = [interpret(speaker, part, i) for part in statement_parts]
    all_contents.append((speaker, contents))
  return all_contents


def parts(statement):
  statements = [part.strip() for part in statement.split(', but')]
  statements = [statement.strip('.!') for statement in statements]
  statements = map(decruft, statements)
  return statements


def decruft(statement):
  for cruft in ['Now', 'Then', 'I know that']:
    if statement.startswith(cruft):
      statement = statement[len(cruft):].strip()
  for cruft in ['too', ' now']:
    if statement.endswith(cruft):
      statement = statement[:-len(cruft)].strip()
  statement = statement.replace(' also ', ' ')
  statement = statement.replace('know <goal>', 'know')
  assert statement.endswith('know')
  return statement


def interpret(speaker, statement, default_time):
  class Interpreted:
    time = default_time
    whose_information = None
    knowledge = False
    def __repr__(self):
      return self.whose_information + (' knows' if self.knowledge else ' does not know') + (' at time %d' % self.time)

  interpreted = Interpreted()
  if statement.startswith('At first'):
    interpreted.time = 0
    statement = statement[len('At first'):].strip()
  if statement.startswith('I know'):
    assert statement == 'I know', (statement, 'Not implemented')
    interpreted.whose_information = speaker
    interpreted.knowledge = True
    return interpreted
  if statement.startswith("I don't know"):
    assert statement == "I don't know"
    interpreted.whose_information = speaker
    interpreted.knowledge = False
    return interpreted
  other = statement.split()[0]
  assert statement == other + ' does not know', (statement, 'Not implemented')
  interpreted.whose_information = other
  interpreted.knowledge = False
  return interpreted
