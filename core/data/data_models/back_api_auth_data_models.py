from dataclasses import dataclass


@dataclass
class BackApiAuthPayload:
    token: str

    @classmethod
    def from_dict(cls, data: dict):
        token_value = data.get("token")

        return cls(
            token=token_value
        )

    def to_dict(self):
        token_value = self.token
        return token_value
