# Client-Server Communication

The separation between client and server is meant to divide the task
of handling gameplay and rendering. It effectively allows for the
following:

- Potential for multiplayer over a network
- Client may render the game however it sees fit
- Allows for clients to be made in any framework or language
- Server does not have to be concerned with client resources

## Server

The initial connection with the server will yield the current map,
authorization code, and the role of the connected client. Following
communication will be state updates of the gameplay.

### server_init.json

```
{
    "auth_code": "",
    "role": ""
}
```

- `auth_code`: Authorization code for the client to keep.
- `role`: The role of the client. Values are `player` or `spectator`.

### map.json

The following data can either be sent in its entirety (preferred) or broken up
into separate packets for sending a map across the network.

```
{
    "map": {
        "0": {
            "type": "path_start",
            "coord": [0.0, 0.05],
            "edges": [
                ["1"]
            ]
        },
        "1": {
            "type": "path",
            "coord": [0.1, 0.15],
            "edges": [
                ["2"]
            ]
        },
        ...,

        "5": {
            "type": "path_end",
            "coord": [0.6, 0.2],
            "edges": []
        },
        "6": {
            "type": "tower",
            "coord": [0.0, 0.1],
            "edges": []
        }
    }
}
```

- `map`: Effectively an adjacency list with the key being the node number.
  - `type`: The supported types are
    - `path_start`: Start of the path where mobs may spawn
    - `path_end`: End of the path where the mobs deal damage to the player
    - `path`: Normal path node
    - `tower`: A slot for placing a tower
  - `coord`: An scaled x,y in the range [0, 1] from the upper left corner of the window.
  - `edges`: The adjacent nodes

### game_state.json

```
{
    "wave": 0,
    "defender": {
        "health": 100,
        "money": 100,
        "score": 0
    },
    "objects": [
        {
            "id": 0,
            "class": "tower",
            "attributes": {
                "type": "archer"
                "health": 100,
                "radius": 0.1,
                "damage": 3,
                "damage_x": 1,
                "attack_speed": 1,
                "attack_speed_x": 1
            },
            "state": {
                "node": "0",
                "target": 0
            }
        },
        {
            "id": 0,
            "class": "mob",
            "attributes": {
                "type": "orc",
                "health": 100,
                "damage": 3,
                "damage_x": 1,
                "attack_speed": 1,
                "attack_speed_x": 1,
                "movement_speed": 1,
                "movement_speed_x": 1,
                "coins": 10
            },
            "state": {
                "from_node": "0",
                "target_node": "1",
                "progress": 0.5
            }
        }
    ]
}
```

Most of this is self-explanatory. Map related units are also scaled relative to
the map (ie. `radius` of 0.5 is half the map). The notable information is the
mobs' current path:

- `from_node`: Node from where the mob came.
- `target_node`: Destination of the mob.
- `progress`: A percentage from [0, 1) of the distance traveled between
  `from_node` and `target_node`

The entire data is sent for initial connections if the game has already started.
Otherwise, the data can be broken up as needed.

#### progress.json

```
{
    "wave": 0,
    "defender": {
        "health": 100,
        "money": 100,
        "score": 0
    }
}
```

#### mob.json
```
{
    "id": 0,
    "class": "mob",
    "attributes": {
        "type": "orc",
        "health": 100,
        "damage": 3,
        "damage_x": 1,
        "attack_speed": 1,
        "attack_speed_x": 1,
        "movement_speed": 1,
        "movement_speed_x": 1,
        "coins": 10
    },
    "state": {
        "from_node": "0",
        "target_node": "1",
        "progress": 0.5
    }
}
```

#### tower.json
```
{
    "id": 0,
    "class": "tower",
    "attributes": {
        "type": "archer"
        "health": 100,
        "radius": 0.1,
        "damage": 3,
        "damage_x": 1,
        "attack_speed": 1,
        "attack_speed_x": 1
    },
    "state": {
        "node": "0",
        "target": 0
    }
}
```

## Client

The client should send packets periodically with an empty event in order to
request the new state of the game.

### client_interact.json

```
{
    "auth_code": "1234",
    "game_time": "0",
    "event": {
        "action_type": "upgrade",
        "action_parameter": ""
    }
}
```

- `auth_code`: The authorization code received from the server.
- `game_time`: Time at which the packet was sent
- `event`: The interaction of the client with the game. Does not proceed
  without proper authorization. Below are list of types and parameters.
  - `upgrade`: `<node>`
  - `destroy`: `<node>`
  - `build`: `<node>`
