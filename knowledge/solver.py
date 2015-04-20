import itertools

def solve(possibilities, players, projections, dialogue, goal):
  assert sorted(projections.keys()) == sorted(players)
  dialogue = dialogue.replace(goal, '<goal>')
  statements = parse(dialogue)

  def project(space, player):
    shards = {}
    for possibility in space:
      projection = projections[player](possibility)
      if projection not in shards: shards[projection] = set()
      shards[projection].add(possibility)
    return shards
  
  space = {}
  space[0] = possibilities[:]
  for i in range(len(statements)):
    (speaker, statement_parts) = statements[i]
    assert speaker in players
    space[i + 1] = space[i]
    for part in statement_parts:
      assert 0 <= part.time <= i
      shards = project(space[part.time], part.whose_information)
      func = lambda key : (len(shards[key]) == 1 if part.knowledge else len(shards[key]) > 1)
      if part.whose_information == speaker:
        ok_keys = [key for key in shards if func(key)]
      else:
        ok_keys_other = set(key for key in shards if func(key))
        shards = project(space[i], speaker)
        ok_keys = []
        for key in shards:
          if all(projections[part.whose_information](value) in ok_keys_other for value in shards[key]):
            ok_keys.append(key)
      new_space = []
      for key in ok_keys:
        new_space.extend(shards[key])
      space[i + 1] = [value for value in space[i + 1] if value in new_space]
    # print 'After statement', i, 'space of possibilities:', space[i + 1]
  return space[i + 1]


def parse(dialogue):
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
