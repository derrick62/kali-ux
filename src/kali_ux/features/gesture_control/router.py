"""Single in-process gesture arbitration contract; input provider remains opt-in."""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
@dataclass(frozen=True)
class Gesture:
    fingers:int; direction:str; phase:str='end'; distance:float=0.0
class GestureRouter:
    def __init__(self): self._handlers:dict[tuple[int,str],Callable[[Gesture],None]]={}; self.enabled=False
    def register(self,fingers:int,direction:str,handler:Callable[[Gesture],None])->None:
        key=(fingers,direction)
        if key in self._handlers: raise ValueError(f'Gesture already registered: {key}')
        self._handlers[key]=handler
    def dispatch(self,event:Gesture)->bool:
        if not self.enabled or event.phase not in ('end','cancel'): return False
        handler=self._handlers.get((event.fingers,event.direction))
        if not handler:return False
        handler(event);return True
