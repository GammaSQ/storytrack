import inspect
class interactable_base(object):

    def __init__(self, piggyback=None):
        if piggyback!=None:
            ref=piggyback
            try:
                pre=piggyback.__class__
                self=piggyback
            except AttributeError:
                self=piggyback()

        self.name=None
        self.state_dict={}
        self.classtree=[]
        self.lvl=0
        if getattr(self, 'reactions', None) == None:
            self.reactions={}
        if getattr(self, 'actions', None)==None:
            self.actions={}

    def state(self, *args, **kwargs):
        # Until better solution is found:
        if not hasattr(self, 'state_dict'):
            self.state_dict={}
        #################################

        # If too many arguments
        if len(args)>2:
            raise TypeError("state (self, key, value) takes at most 3 arguments, %i"%(len(args)+1))
        # If no arguments, return states as dict
        if len(args)==0:
            return self.state_dict

        # Find out key:
        if len(args)>0:
            key=args[0]
            if 'key' in kwargs:
                raise TypeError("Two definitions for 'key' submitted!")
        else:
            if 'key' not in kwargs:
                raise TypeError("key not specified")
            key = kwargs['key']

        # Is there value?
        if len(args)>1:
            value=args[1]
            if 'value' in kwargs:
                raise TypeError("Two definitions for 'value' submitted!")
            else:
                self.state_dict[key]=value
        elif 'value' in kwargs:
            value=kwargs['value']
        # If no value, return one or set to true
        else:
            if key in self.state_dict:
                return self.state_dict[key]
            else:
                self.state_dict[key]=True
                return None

        # Ther is value!
        if value==None:
            # If value set to None, simply delete
            if key in self.state_dict:
                del self.state_dict[key]
        # else, set key to whatever value
        else:
            self.state_dict[key]=value

    def read_state(self, key=None):
        if key:
            if key in self.state_dict:
                return self.state_dict[key]
            return None
        return self.state_dict

    def __setattr__(self, attr, ret):
        if attr not in getattr(self, 'no_action',[attr]):
            if attr.startswith("react_to_"):
                reg = attr.split("react_to_")[-1]
                self.reactions[reg]=ret
            else:
                if callable(ret):
                    self.actions[attr]=ret
        return super(interactable_base, self).__setattr__(attr, ret)

    def __getattr__(self, attr):
        if attr.startswith('__') or attr == 'no_action' or attr in getattr(self, 'no_action', [attr]):
            return self.__getattribute__(attr)
        elif attr in getattr(self, 'actions', []):
            return self.act(attr)
        elif attr.startswith('react_to_'):
            react=attr.split('react_to_')[-1]
            return self.react(react)

        return self.__getattribute__(attr)

    def act_on(self, action, **kwargs):
        call=hyper_call()(self.actions[action])
        meta=call(**kwargs)
        meta = meta or {}
        if 'target' in kwargs:
            try:
                kwargs['target'].react_to(action=action, actor=self, **meta)
            except AttributeError:
                pass
        return meta

class interactable(interactable_base):
    no_action = dict(inspect.getmembers(interactable_base, predicate=inspect.ismethod)).keys()

    def __init__(self, piggyback=None):#, name, actions={}, reactions={}):
        predic = dict(inspect.getmembers(self, predicate=inspect.ismethod))
        reactions={}
        actions={}
        for key, val in predic.items():
            act = getattr(val, 'act', None)
            if act:
                actions[key]=val
            elif act==None:
                continue
            else:
                reactions[key]=val
        self.actions=actions
        self.reactions=reactions
        
        return super(interactable, self).__init__(piggyback)

    def act_on(self, action, **kwargs):
        # Call the saved callback:
        call = self.actions[action]
        args=inspect.getargspec(call)[0]
        if ('target' in args and 'target' in kwargs) or ('target' not in args and 'target' not in kwargs):
            meta=call(**kwargs)
        else:
            try:
                target=kwargs.pop("target")
                meta=call(target, **kwargs)
            except KeyError:
                raise TypeError("'target' not specified!")
            finally:
                kwargs['target']=target
        # If we want to act on a specific target (e.g. OPEN the TREASURE),
        # it's reaction will be called. target has to be interactable.
        if not meta:
            meta={}
        if 'target' in kwargs:
            try:
                kwargs['target'].react_to(action=action, actor=self, **meta)
            except AttributeError:
                pass
        return meta

    def react_to(self, action, actor, **kwargs):
        call=self.reactions[action]
        args=inspect.getargspec(call)[0]
        if 'actor' in args:
            ret=call(actor=actor, **kwargs)
        else:
            ret = call(actor, **kwargs)
        if type(ret) == tuple and len(ret)>1:
            if len(ret)==2:
                reaction=ret[0]
                ret=ret[1]
            else:
                raise TypeError("Too many return-values of react_to_%s"%action)
            if reaction in self.actions:
                # If the action needs a target, ret has to have a "target" key!
                # WARNING!!! DANGER OF ENTERNAL LOOP!
                self.act_on(reaction, **ret)
        return ret

#####  -- -- not tested after this point! -- -- #####
#####################################################

    def register_action(self, action={}):
        for key in action.keys():
            if key in self.action:
                raise KeyError("Action %s does already exist!"%key)
        self.actions += action

    def replace_action(self, action, replacement):
        self.actions[action]=replacement

    def register_reaction(self, reaction={}):
        for key in reaction.keys():
            if key in self.reaction:
                raise KeyError("Reaction %s does already exist!"%key)
        self.action += reaction

    def replace_action(self, reaction, replacement):
        self.reactions[reaction]=replacement