import inspect
from functools import wraps

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
    """
    @inject(Sim,"on_add")
    def _name_changer(original, self, *args, **kwargs):
        self.sim_info.first_name = "Hacked"
        return original(self, *args, **kwargs)
   """
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
