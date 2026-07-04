from crm_bot.models import Request, Status


class RequestStorage:
    def __init__(self) -> None:
        self._requests: dict[int, Request] = {}
        self._counter: int = 0

    def add(self, user_id: int, username: str, text: str) -> Request:
        self._counter += 1
        req = Request(id=self._counter, user_id=user_id, username=username, text=text)
        self._requests[req.id] = req
        return req

    def get_all(self) -> list[Request]:
        return list(self._requests.values())

    def update_status(self, request_id: int, status: Status) -> Request | None:
        req = self._requests.get(request_id)
        if req is None:
            return None
        req.status = status
        return req