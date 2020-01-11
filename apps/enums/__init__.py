from dataclasses import dataclass


@dataclass(frozen=True)
class LoginType:
    GOOGLE = 'google'
    KAKAO = 'kakao'
    GITHUB = 'github'
