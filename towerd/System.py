import abc
import math


class System(abc.ABC):
    def __init__(self):
        self.entities = set()

    @abc.abstractmethod
    def update(self, state, *args, **kwargs):
        raise NotImplementedError


class MovementSystem(System):
    def update(self, dt, state, movement_comps, loc_comps):
        for entity in self.entities:
            movement_comp = movement_comps[entity.id]
            speed = movement_comp.movement_speed
            from_node = movement_comp.from_node
            dest_node = movement_comp.dest_node

            m = state['map']
            from_node = m.node[from_node]
            dest_node = m.node[dest_node]
            loc_comp = loc_comps[entity.id]

            from_x, from_y = from_node.x, from_node.y
            dest_x, dest_y = dest_node.x, dest_node.y

            total_diff_x = dest_x - from_x
            total_diff_y = dest_y - from_y

            theta = math.atan(total_diff_y / total_diff_x)
            dl = speed * dt

            loc_comp.x += dl * math.cos(theta)
            loc_comp.y += dl * math.sin(theta)


class SystemManager:
    def __init__(self):
        self.systems = {}
        self.system_bits = {}

    def register(self, T, bitset):
        self.systems[T.__name__] = T()
        self.system_bits[T.__name__] = bitset

    def remove_system_entity(self, entity):
        for system in self.systems.values():
            system.entities.discard(entity)

    def update_system_entity(self, entity, entity_bitset):
        for system in self.systems.values():
            system_bits = self.system_bits[system.__class__.__name__]
            print(bin(system_bits), bin(entity_bitset))
            if system_bits & entity_bitset == system_bits:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)
