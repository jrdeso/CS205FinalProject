import abc
import math


class System(abc.ABC):
    """
    A system consisting of the entities that it needs to update.

    :var entities: all the entities the system needs to update
    """
    def __init__(self):
        self.entities = set()

    @abc.abstractmethod
    def update(self, dt, state, *args, **kwargs):
        """
        Perform an update across all entities.

        :param dt: the amount of time passed since the last update
        :param state: the game state
        :param args: any number of arguments
        :param kwargs: any number of keyword arguments
        """
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
    """
    Manages all instances of registered systems

    :var systems: a dictionary mapping the system name to an instance of the
        system
    :var system_bits: a dictionary mapping the system name to a bitset
        representing required components
    :var max_entities: store of the max_entities parameter
    """
    def __init__(self):
        self.systems = {}
        self.system_bits = {}

    def register(self, T, bitset):
        """
        Register a System. Associates a bitset representing required components
        to the system.

        :param T: the System class
        :param bitset: a bitset representing required components
        """
        self.systems[T.__name__] = T()
        self.system_bits[T.__name__] = bitset

    def get_system(self, T):
        """
        Get the instance of the System.

        :param T: the System class
        """
        return self.systems[T.__name__]

    def remove_system_entity(self, T, entity):
        """
        Remove an entity from a registered System.

        :param T: the System class
        :param entity: the entity to remove
        """
        self.systems[T.__name__].entities.discard(entity)

    def remove_all_entity(self, entity):
        """
        Remove an entity from all systems.

        :param T: the System class
        :param entity: the entity to remove
        """
        for system in self.systems.values():
            system.entities.discard(entity)

    def update_system_entity(self, entity, entity_bitset):
        """
        Update an entity bitset. Remove enitity from systems where the entity
        bitset in part does not match the system bitset. Add them to systems
        where the entity_bitset does in part match the system bitset.

        :param entity: the entity
        :param entity_bitset: the new bitset for the entity
        """
        for system in self.systems.values():
            system_bits = self.system_bits[system.__class__.__name__]
            if system_bits & entity_bitset == system_bits:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)
