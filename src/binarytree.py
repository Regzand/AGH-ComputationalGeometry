from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


class Node:
    key: Any
    value: Any
    left: Optional['Node']
    right: Optional['Node']

    def find(self, key) -> Optional['Node']:
        if key == self.key:
            return self
        if key < self.key and self.left:
            return self.left.find(key)
        if self.right:
            return self.right.find(key)
        return None
