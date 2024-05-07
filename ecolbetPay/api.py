from ninja import NinjaAPI
from appV1.views import router as payRouter
from ninja.security import HttpBearer

from appV1.utils import verify_token

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        t = verify_token(token=token)
        return t

app = NinjaAPI(
    title='Ecolbet Pay API',
    auth=GlobalAuth(),
)

app.add_router("/v1/", payRouter)