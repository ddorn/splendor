# Splendor

This is a python version of the popular game [Splendor](https://www.spacecowboys.fr/splendor/)

### Install

With pip:
```shell script
git clone https://gitlab.com/ddorn/splendor.git
cd splendor
pip install . -U --user
```

With poetry:
```shell script
poetry add git+https://gitlab.com/ddorn/splendor.git
```

### Usage

Any AI should be a subclass of `BaseClient` and a game can be run with a script like this one:

```python
import random

from splendor import *
from splendor.data import *

class RandomAi(BaseClient):
    def play(self, state: BaseGame):
        r = random.random()
        visible_cards_ids = [c.id for stage in state.deck for c in stage]
        if r < 0.8:
            return TakeAction(random.choice([RED, GREEN, BLUE, BLACK, WHITE]))
        elif r < 0.9:
            return BuyAction(random.choice(visible_cards_ids))
        else:
            return ReserveAction(random.choice(visible_cards_ids + STAGES))

Runner(RandomAi(), TuiClient(), view_client=None)
```

This would start a game between the `RandomAi` and you, with a nice terminal interface.