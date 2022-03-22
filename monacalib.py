import inspect
from functools import wraps

import interactions
import sims4
from interactions.context import InteractionContext
from interactions.priority import Priority
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim import Sim


def inject(target_object, target_function_name, safe=False):
    if safe and not hasattr(target_object, target_function_name):
        def _self_wrap(wrap_function):
            return wrap_function

        return _self_wrap

    def _wrap_original_function(original_function, new_function):
        @wraps(original_function)
        def _wrapped_function(*args, **kwargs):
            if type(original_function) is property:
                return new_function(original_function.fget, *args, **kwargs)
            else:
                return new_function(original_function, *args, **kwargs)

        if inspect.ismethod(original_function):
            return classmethod(_wrapped_function)
        elif type(original_function) is property:
            return property(_wrapped_function)
        else:
            return _wrapped_function

    def _injected(wrap_function):
        original_function = getattr(target_object, target_function_name)
        setattr(target_object, target_function_name, _wrap_original_function(original_function, wrap_function))

        return wrap_function

    return _injected

import services

all_sims = [0]
class monacalib:
    @inject(Sim,"on_add")
    def _name_changer(original, self, *args, **kwargs):
        self.sim_info.first_name = "Hacked"
        return original(self, *args, **kwargs)

    class sims:
        @staticmethod
        def getallsim():
            return all_sims
        @staticmethod
        def getfullname(selectedsim:Sim):
            sim_info = selectedsim.sim_info
            return sim_info.first_name + sim_info.last_name

        @staticmethod
        def getsimlastname(selectedsim:Sim):
            sim_info = selectedsim.sim_info
            return sim_info.last_name

        @staticmethod
        def getsimfirstname(selectedsim: Sim):
            sim_info = selectedsim.sim_info
            return sim_info.first_name

        @staticmethod
        def push_interaction(affordance, target, sim, priority=Priority.High):
            client = services.client_manager().get_first_client()
            manager = services.affordance_manager()
            resulta = affordance = manager.get(affordance)
            if sim is not None:
                    if not sim.queue.can_queue_visible_interaction():
                        return False
                    else:
                        context = InteractionContext(sim, InteractionContext.SOURCE_PIE_MENU, priority, client=client,
                                                     pick=None)
                        result = sim.push_super_affordance(affordance, target, context)
                        if not result:
                            return "Faild for other error"
                    return "Ok"
            if target is None:
                return "warn target is none"
                if sim is None:
                    return "error sim is none"
                    if resulta is None:
                        return "affrodance is not set"
                        if manager is None:
                            return "manager is not set"
                            if client is None:
                                return "client is not set"

    class game:
        @staticmethod
        def getactivesim():
            return services.get_active_sim()

        @staticmethod
        def getactivesiminfo():
            return services.active_sim_info()

        @staticmethod
        def getactivehousehold():
            return services.active_household()

        @staticmethod
        def getallsimfromhousehold(household):
            a = []
            for x in household.sim_info_gen():
                a.append(x)
            return a
    class utils:
        @staticmethod
        def reverse_fullname(first_name,last_name):
            return (last_name + first_name)
