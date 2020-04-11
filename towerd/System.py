import abc
import math


class System(abc.ABC):
    def __init__(self):
        self.entities = set()

    @abc.abstractmethod
    def update(self, dt, state, *args, **kwargs):
        raise NotImplementedError


class MovementSystem(System):
    def update(self, dt, state, movement_comps, loc_comps):
        for entity in self.entities:
            movement_comp = movement_comps[entity.e_id]
            speed = movement_comp.movement_speed
            from_node = movement_comp.from_node
            dest_node = movement_comp.dest_node

            m = state['map']
            from_node = m.nodes[from_node]
            dest_node = m.nodes[dest_node]
            loc_comp = loc_comps[entity.e_id]

            from_x, from_y = loc_comp.x, loc_comp.y
            dest_x, dest_y = dest_node.x, dest_node.y

            total_diff_x = dest_x - from_x
            total_diff_y = dest_y - from_y

            theta = math.atan2(total_diff_y, total_diff_x)
            dl = speed * dt

            dx = dl * math.cos(theta)
            dy = dl * math.sin(theta)

            if from_x < dest_x and (new_x := from_x + dx) < dest_x:
                loc_comp.x = new_x
            elif from_x > dest_x and (new_x := from_x - dx) > dest_x:
                loc_comp.x = new_x
            else:
                loc_comp.x = dest_x

            if from_y < dest_y and (new_y := from_y + dy) < dest_y:
                loc_comp.y = new_y
            elif from_y > dest_y and (new_y := from_y - dy) > dest_y:
                loc_comp.y = new_y
            else:
                loc_comp.y = dest_y


class SystemManager:
    def __init__(self):
        self.systems = {}
        self.system_bits = {}

    def register(self, T, bitset):
        self.systems[T.__name__] = T()
        self.system_bits[T.__name__] = bitset

    def get_system(self, T):
        return self.systems[T.__name__]

    def remove_system_entity(self, entity):
        for system in self.systems.values():
            system.entities.discard(entity)

    def update_system_entity(self, entity, entity_bitset):
        for system in self.systems.values():
            system_bits = self.system_bits[system.__class__.__name__]
            if system_bits & entity_bitset == system_bits:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)
