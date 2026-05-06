from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Category:
    id: int = 0
    name: str = "default"

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


@dataclass
class Tag:
    id: int = 0
    name: str = "default"

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


@dataclass
class Pet:
    name: str
    photo_urls: List[str]
    id: Optional[int] = None
    category: Optional[Category] = None
    tags: List[Tag] = field(default_factory=list)
    status: str = "available"

    def to_dict(self) -> dict:
        payload = {
            "name": self.name,
            "photoUrls": self.photo_urls,
            "status": self.status,
        }
        if self.id is not None:
            payload["id"] = self.id
        if self.category:
            payload["category"] = self.category.to_dict()
        if self.tags:
            payload["tags"] = [tag.to_dict() for tag in self.tags]
        return payload


class PetBuilder:
    """
    Builder pattern for constructing Pet payloads with fluent interface.
    Makes test data creation readable and flexible.
    """

    def __init__(self):
        self._id: Optional[int] = None
        self._name: str = "Buddy"
        self._photo_urls: List[str] = ["https://example.com/photo.jpg"]
        self._category: Optional[Category] = None
        self._tags: List[Tag] = []
        self._status: str = "available"

    def with_id(self, pet_id: int) -> "PetBuilder":
        self._id = pet_id
        return self

    def with_name(self, name: str) -> "PetBuilder":
        self._name = name
        return self

    def with_status(self, status: str) -> "PetBuilder":
        self._status = status
        return self

    def with_category(self, category_id: int, category_name: str) -> "PetBuilder":
        self._category = Category(id=category_id, name=category_name)
        return self

    def with_tag(self, tag_id: int, tag_name: str) -> "PetBuilder":
        self._tags.append(Tag(id=tag_id, name=tag_name))
        return self

    def with_photo_urls(self, urls: List[str]) -> "PetBuilder":
        self._photo_urls = urls
        return self

    def build(self) -> Pet:
        return Pet(
            id=self._id,
            name=self._name,
            photo_urls=self._photo_urls,
            category=self._category,
            tags=self._tags,
            status=self._status,
        )
